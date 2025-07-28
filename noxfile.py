import json
import re
import subprocess
from datetime import date
from pathlib import Path

import nox

nox.options.sessions = ["precommit"]  # default session


@nox.session
def precommit(session):
    """
    Run all pre-commit hooks (code formatting, spell check, linting).
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
    """Run tests using pytest."""
    session.install(".[test]")  # assumes [test] includes pytest, etc.
    session.run("pytest", *session.posargs)


@nox.session
def docs(session):
    """Build HTML documentation with Sphinx."""
    output_dir = session.posargs[0] if len(session.posargs) == 1 else "_htmlbuild"
    print("generate HTML docs in:", output_dir)
    session.run(
        "python", "src/script_build/generate_metadata.py", "src/PyPop/_metadata.py"
    )  # needed because we aren't installing pypop
    session.run("rm", "-rf", output_dir, external=True)
    session.install("-r", "website/requirements-docs.txt")
    session.run("sphinx-build", "website", output_dir)


@nox.session
def docs_pdf(session):
    """Build PDF documentation with Sphinx. Requires LaTeX to already be installed"""
    output_dir = session.posargs[0] if len(session.posargs) == 1 else "_latexbuild"
    print("generate PDF docs in:", output_dir)
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
    """Update NEWS.md from latest GitHub *draft* release notes (if not already present)."""

    session.run("gh", "--version", external=True)

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

    section = match.group(1).strip().replace("YYYY-MM-DD", date.today().isoformat())

    # Step 4: Check for duplication
    news_path = Path("NEWS.md")
    news_contents = news_path.read_text(encoding="utf-8")
    if section in news_contents:
        session.log("Section already present in NEWS.md; skipping.")
        return

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

    today = date.today().isoformat()

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
        payload = json.dumps({"body": updated_body})

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
def publish_release(session):
    """Preview and prepare publishing the latest draft release. (Dry-run only)"""

    # Confirm branch
    current_branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if current_branch != "main":
        session.warn(
            f"Warning: You are on branch '{current_branch}', not 'main'. Proceeding in dry-run mode for testing."
        )

    session.log("Running update_news to sync NEWS.md from draft release...")
    update_news(session)

    session.log("Showing changes to NEWS.md:")
    session.run("git", "diff", "NEWS.md")

    proceed = input("Continue and commit NEWS.md update? [y/N]: ").lower()
    if proceed != "y":
        session.error("Aborted.")

    session.log("Simulating commit (dry-run, not actually committing)...")
    session.log(
        "Command: git commit NEWS.md -m 'Update NEWS.md from latest draft release'"
    )
    session.log("Command: pre-commit run --all-files")

    # Push the commit (dry-run only, not actually pushing)
    session.log("Simulating git push (dry-run only)...")
    session.log("Command: git push")

    # bump github release date
    tag_name = bump_release_date(session)

    session.log("Dry-run only — simulating publish.")
    session.log(f"Command: gh release edit {tag_name} --draft=false")

    session.log("Waiting for GitHub Actions to finish...")
    session.log("Command: git pull")

    session.log("Release flow completed in dry-run mode.")
