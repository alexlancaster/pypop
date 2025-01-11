from base import (
    in_temp_dir,  # noqa: F401
    run_pypop_process,
)


def test_DataMinimalNoHeaderNoIDs():
    exit_code = run_pypop_process(
        "./tests/data/doc-examples/config-minimal-example.ini",
        "./tests/data/doc-examples/data-minimal-noheader-noids.pop",
    )
    # check exit code
    assert exit_code == 0


def test_DataMinimalNoHeader():
    exit_code = run_pypop_process(
        "./tests/data/doc-examples/config-minimal-example.ini",
        "./tests/data/doc-examples/data-minimal-noheader.pop",
    )
    # check exit code
    assert exit_code == 0
