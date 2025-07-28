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
