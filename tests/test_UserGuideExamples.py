from base import (
    in_temp_dir,  # noqa: F401
    run_pypop_process,
    skip_musllinux_x86_64,
)


@skip_musllinux_x86_64
def test_DataMinimalNoHeaderNoIDs():
    exit_code = run_pypop_process(
        "./tests/data/doc-examples/config-minimal-example.ini",
        "./tests/data/doc-examples/data-minimal-noheader-noids.pop",
    )
    # check exit code
    assert exit_code == 0


@skip_musllinux_x86_64
def test_DataMinimalNoHeader():
    exit_code = run_pypop_process(
        "./tests/data/doc-examples/config-minimal-example.ini",
        "./tests/data/doc-examples/data-minimal-noheader.pop",
    )
    # check exit code
    assert exit_code == 0
