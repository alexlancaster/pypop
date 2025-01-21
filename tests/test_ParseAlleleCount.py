from base import (
    DEFAULT_GOLD_OUTPUT_DIR,
    abspath_test_data,
    filecmp_ignore_newlines,
    in_temp_dir,  # noqa: F401
    run_pypop_process,
)


def test_ParseAlleleCount_Semityped():
    exit_code = run_pypop_process(
        "./tests/data/allelecount.ini",
        "./tests/data/allelecount-semityped.pop",
    )
    # check exit code
    assert exit_code == 0

    out_filename = "allelecount-semityped-out.txt"
    gold_out_filename = abspath_test_data(
        DEFAULT_GOLD_OUTPUT_DIR / "ParseAlleleCount_Semityped" / out_filename
    )

    assert filecmp_ignore_newlines(out_filename, gold_out_filename)
