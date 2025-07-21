import nox


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


# @nox.session
# def docs(session):
#     """Build documentation with Sphinx."""
#     session.install("sphinx")
#     session.run("sphinx-build", "docs", "build/docs")


@nox.session
def clean(session):
    """Clean build artifacts."""
    session.run(
        "rm", "-rf", "build", "dist", "src/pypop_genomics.egg-info", external=True
    )
