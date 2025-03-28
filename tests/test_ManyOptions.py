from pathlib import Path

import pytest
from base import (
    in_temp_dir,  # noqa: F401
    run_pypop_process,
    skip_musllinux_x86_64,
)


@pytest.mark.slow
@skip_musllinux_x86_64
def test_ManyOptions():
    generated_filenames = [
        "BIGDAWG_SynthControl_Data_with_metadata-" + suffix
        for suffix in [
            "filter-A-randomized.tsv",
            "filter-DRB1-randomized.tsv",
            "filtered.pop",
            "filter.xml",
            "out.txt",
            "out.xml",
        ]
    ]
    print(generated_filenames)

    exit_code = run_pypop_process(
        "./tests/data/custom-binning-examples/many_options_config.ini",
        "./tests/data/BIGDAWG_SynthControl_Data_with_metadata.pop",
    )
    # check exit code
    assert exit_code == 0

    # FIXME: currently just checks presence of files, don't check contents
    assert {p.name for p in Path().iterdir()} == set(generated_filenames)
