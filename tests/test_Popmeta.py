import os.path

from base import (
    DEFAULT_GOLD_OUTPUT_DIR,
    filecmp_list_of_files,
    in_temp_dir,  # noqa: F401
    run_popmeta_process,
)


def test_Popmeta():
    exit_code = run_popmeta_process(
        [
            "./tests/data/BIGDAWG_SynthControl_Data-out.xml",
            "./tests/data/BIGDAWG_SynthControl_Data_dash-out.xml",
        ],
        args=[],
    )
    # check exit code
    assert exit_code == 0

    checked_filenames = [
        "1-locus-allele.tsv",
        "1-locus-summary.tsv",
        "3-locus-summary.tsv",
        "3-locus-haplo.tsv",
    ]
    # compare with output files list
    assert filecmp_list_of_files(
        checked_filenames, DEFAULT_GOLD_OUTPUT_DIR / "popmeta/"
    )

    # make sure only expected generated files exist
    assert set(os.listdir()) == {*checked_filenames, "meta.xml"}


def test_Popmeta_Prefix():
    exit_code = run_popmeta_process(
        [
            "./tests/data/BIGDAWG_SynthControl_Data-out.xml",
            "./tests/data/BIGDAWG_SynthControl_Data_dash-out.xml",
        ],
        args=["--prefix-tsv", "prefix"],
    )
    # check exit code
    assert exit_code == 0

    checked_filenames = [
        "prefix-1-locus-allele.tsv",
        "prefix-1-locus-summary.tsv",
        "prefix-3-locus-summary.tsv",
        "prefix-3-locus-haplo.tsv",
    ]
    # compare with output files list
    assert filecmp_list_of_files(
        checked_filenames, DEFAULT_GOLD_OUTPUT_DIR / "popmeta_prefix/"
    )

    # make sure only expected generated files exist
    assert set(os.listdir()) == {*checked_filenames, "meta.xml"}
