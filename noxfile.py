"""nox commands."""

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

import nox
from zoneinfo import ZoneInfo

nox.options.sessions = ["precommit"]  # default session

# Eastern Time (handles DST automatically)
ET = ZoneInfo("America/New_York")

## helper functions


def run_git_command(session, *args):
    """Run git command with arguments."""
    session.run("git", *args, external=True)


def file_was_modified(filename):
    """Returns True if file has unstaged changes."""
    result = subprocess.run(
        ["git", "diff", "--name-only"], stdout=subprocess.PIPE, text=True, check=True
    )
    return filename in result.stdout.splitlines()


def commit_with_retry(session, filename, message):
    """Use git to commit to repo, and retry."""
    committed = True  # whether a commit was done
    try:
        run_git_command(session, "commit", filename, "-m", message)
    except nox.command.CommandFailed:
        session.warn(
            f"Commit failed, checking if {filename} was modified by pre-commit..."
        )

        # if file_was_modified(filename):
        try:
            session.log(f"{filename} modified. Re-staging and retrying commit.")
            run_git_command(session, "commit", filename, "-m", message)
        except nox.command.CommandFailed:
            session.warn(
                "Still failed. Skipping commit — possibly no changes to commit."
            )
            committed = False

    return committed


@nox.session
def precommit(session):
    """Run all pre-commit hooks (code formatting, spell check, linting).

    This mirrors checks applied in CI and on pull requests.
    """
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session
def build(session):
    """Build the package (including binary extensions)."""
    session.install("build")
    session.run("python", "-m", "build")


@nox.session
def tests(session):
    """Run unit tests and doctests using pytest."""
    session.install(".[test]")  # now install assumes [test] includes pytest, etc.
    session.run(
        "pytest", "--pyargs", "PyPop", "website/docs", "tests", *session.posargs
    )  # do docstring tests then unit tests


@nox.session
def docs(session):
    """Build HTML documentation with Sphinx."""
    output_dir = session.posargs[0] if len(session.posargs) == 1 else "_htmlbuild"
    print("generate HTML docs in:", output_dir)
    session.install("tomli")
    session.run(
        "python", "src/script_build/generate_metadata.py", "src/PyPop/_metadata.py"
    )  # needed because we aren't installing pypop
    session.run("rm", "-rf", output_dir, external=True)
    session.install("-r", "website/requirements-docs.txt")
    session.run("sphinx-build", "website", output_dir)


@nox.session
def docs_pdf(session):
    """Build PDF documentation with Sphinx. Requires LaTeX to already be installed."""
    output_dir = session.posargs[0] if len(session.posargs) == 1 else "_latexbuild"
    print("generate PDF docs in:", output_dir)
    session.install("tomli")
    session.run(
        "python", "src/script_build/generate_metadata.py", "src/PyPop/_metadata.py"
    )  # needed because we aren't installing pypop
    session.run("rm", "-rf", output_dir, external=True)
    session.install("-r", "website/requirements-docs.txt")
    session.run("sphinx-build", "-b", "latex", "website", output_dir)
    session.run("make", "-C", output_dir)


@nox.session
def clean(session):
    # FIXME: very basic, needs work
    """Clean build artifacts."""
    session.run(
        "rm", "-rf", "build", "dist", "src/pypop_genomics.egg-info", external=True
    )


@nox.session
def sdist_test(session):
    """Build sdist, install with test extras, and run tests."""
    session.install("build")

    # imports need to be after the installation to ensure they're only
    # required in the virtual env

    import build as pybuild  # noqa: PLC0415

    # build the sdist programmatically
    builder = pybuild.ProjectBuilder(".")
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)

    sdist_file = builder.build("sdist", str(dist_dir))

    session.log(f"built sdist: {sdist_file}")

    # Install the sdist with test extras
    session.install(sdist_file + "[test]")

    # Run the tests
    session.run("pytest", *session.posargs)


@nox.session
def update_news(session):
    """Update NEWS.md in local checkout from latest GitHub *draft* release notes (if not already present)."""
    session.log("Running update NEWS.md from latest release draft...")
    # session.run("gh", "--version", external=True)

    # Step 1: Use gh api to list all releases
    result = subprocess.run(
        ["gh", "api", "/repos/:owner/:repo/releases"],
        capture_output=True,
        text=True,
        check=True,
    )
    releases = json.loads(result.stdout)

    # Step 2: Find the most recently created draft release
    drafts = [r for r in releases if r.get("draft")]
    if not drafts:
        session.error("No draft releases found.")

    latest_draft = sorted(drafts, key=lambda r: r["created_at"], reverse=True)[0]
    tag_name = latest_draft["tag_name"]
    body = latest_draft.get("body", "")
    session.log(f"Found draft release: {tag_name}")

    if not body:
        session.error(f"Draft release '{tag_name}' has no body content.")

    # Step 3: Extract between markers
    match = re.search(
        r"<!-- START cut-and-paste to NEWS\.md -->\s*(.*?)\s*<!-- END cut-and-paste to NEWS\.md -->",
        body,
        re.DOTALL,
    )
    if not match:
        session.error("Could not find cut-and-paste section in draft release notes.")

    section = (
        match.group(1)
        .strip()
        .replace("YYYY-MM-DD", datetime.now(tz=ET).date().isoformat())
    )

    # Step 4: Check for duplication
    news_path = Path("NEWS.md")
    news_contents = news_path.read_text(encoding="utf-8")
    if section in news_contents:
        session.log("Section already present in NEWS.md; skipping.")
        return None

    # Step 5: Insert above latest version header
    release_header_pattern = re.compile(r"^## \[\d+\.\d+\.\d+\]", re.MULTILINE)
    match = release_header_pattern.search(news_contents)
    if not match:
        session.error("Could not find a release header in NEWS.md")

    insert_at = match.start()
    new_contents = (
        news_contents[:insert_at] + section + "\n\n" + news_contents[insert_at:]
    )
    news_path.write_text(new_contents, encoding="utf-8")

    session.log(f"Inserted release notes from draft '{tag_name}' into NEWS.md.")

    return "NEWS.md"


@nox.session
def push_news(session):
    """Commit and push local changes to NEWS.md back to repo."""
    news_filename = "NEWS.md"
    message = f"Update {news_filename} from latest draft release"

    session.log(f"Showing changes to {news_filename}:")
    run_git_command(session, "diff", f"{news_filename}")

    proceed = input(
        f"Continue and commit and push {news_filename} update? [y/N]: "
    ).lower()
    if proceed != "y":
        session.log("Simulating commit (dry-run, not actually committing)...")
        session.log(f"Command: git commit {news_filename} -m '{message}'")

        session.log("Simulating git push (dry-run only)...")
        session.log("Command: git push")
    else:
        commit_occurred = commit_with_retry(session, news_filename, message)
        if commit_occurred:
            run_git_command(session, "push")
        else:
            session.warn("no changes were committed, skipping git push...")


@nox.session
def bump_release_date(session):
    """Bump release date in draft release to today."""
    session.log("Fetching draft releases...")
    result = subprocess.run(
        ["gh", "api", "/repos/:owner/:repo/releases"],
        capture_output=True,
        text=True,
        check=True,
    )
    releases = json.loads(result.stdout)
    drafts = [r for r in releases if r.get("draft")]
    if not drafts:
        session.error("No draft releases found.")

    latest_draft = sorted(drafts, key=lambda r: r["created_at"], reverse=True)[0]
    release_id = latest_draft["id"]
    tag_name = latest_draft["tag_name"]
    original_body = latest_draft.get("body", "")

    if not original_body:
        session.error(f"Draft release '{tag_name}' has no body content.")

    session.log(f"Preparing ISO date substitution for release '{tag_name}'...")

    # Regex to match both the placeholder and already substituted dates
    # Matches "## [1.2.2] - YYYY-MM-DD" or "## [1.2.2] - 2023-03-10"

    today = datetime.now(tz=ET).date().isoformat()

    updated_body = re.sub(
        r"(## \[\d+\.\d+\.\d+\] - )(?:\d{4}-\d{2}-\d{2}|YYYY-MM-DD)",
        lambda m: m.group(1) + today,
        original_body,
    )

    # Log the updated body (for preview)
    session.log(f"Updated release body:\n{updated_body}")

    proceed2 = input("Continue to bump release date? [y/N]: ").lower()
    if proceed2 == "y":
        session.log("Update the date in the release.")

        # PATCH the body in-memory
        payload = json.dumps(
            {
                "body": updated_body,
                "tag_name": tag_name,  # preserve the original tag
            }
        )

        subprocess.run(
            [
                "gh",
                "api",
                "--method",
                "PATCH",
                f"/repos/:owner/:repo/releases/{release_id}",
                "--input",
                "-",  # <- this tells gh to read from stdin
            ],
            input=payload.encode("utf-8"),
            capture_output=True,
            check=True,
        )
    else:
        session.log("Skipping bumping release date")

    return tag_name


@nox.session
def prepare_release(session):
    """Prepare latest release draft with correct tag, target, and NEWS.md update."""
    # Confirm branch
    current_branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    ).stdout.strip()

    session.log(f"Current branch: {current_branch}")

    # Determine if we should override the release target
    use_custom_target = current_branch != "main"

    # update the NEWS.md file
    update_news(session)

    # push it back to the repo, if changed
    push_news(session)

    # bump github release date, returns the current tag_name
    tag_name = bump_release_date(session)

    if use_custom_target:
        session.warn(
            f"Branch is '{current_branch}', so release target will be set to that instead of 'main'."
        )
        edit_command = [
            "gh",
            "release",
            "edit",
            f"{tag_name}",
            "--target",
            current_branch,
        ]
    else:
        edit_command = [
            "gh",
            "release",
            "edit",
            f"{tag_name}",
            "--target",
            "main",
        ]
    proceed2 = input("Continue and update release? [y/N]: ").lower()
    if proceed2 != "y":
        session.log("Dry-run only — simulating publish.")
        session.log(f"Command: {' '.join(edit_command)}")
    else:
        session.run(*edit_command, external=True)

    return tag_name


@nox.session
def publish_release(session):
    """Finalize publishing the release after preparing it."""
    tag_name = prepare_release(session)

    proceed = input("Continue and publish release on GitHub? [y/N]: ").lower()
    if proceed != "y":
        session.log(
            "Dry-run only — you can publish the release manually via GitHub UI."
        )
        session.log(
            f"To publish manually: https://github.com/<your-org>/<your-repo>/releases/tag/{tag_name}"
        )
    else:
        session.run(
            "gh", "release", "edit", f"{tag_name}", "--draft=false", external=True
        )
        session.log(f"Release: {tag_name} published.")
