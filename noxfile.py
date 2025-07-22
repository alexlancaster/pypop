import nox


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
    session.run("pytest")


@nox.session
def docs(session):
    """Build documentation with Sphinx."""
    session.run(
        "python", "src/script_build/generate_metadata.py", "src/PyPop/_metadata.py"
    )  # needed because we aren't installing pypop
    session.run("rm", "-rf", "_htmlbuild", external=True)
    session.install("-r", "website/requirements-docs.txt")
    session.run("sphinx-build", "website", "_htmlbuild")


@nox.session
def clean(session):
    # FIXME: very basic, needs work
    """Clean build artifacts."""
    session.run(
        "rm", "-rf", "build", "dist", "src/pypop_genomics.egg-info", external=True
    )
