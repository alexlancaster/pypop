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

    from pathlib import Path  # noqa: PLC0415

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
