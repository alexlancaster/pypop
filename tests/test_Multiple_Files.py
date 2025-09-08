import tempfile
from pathlib import Path

from base import (
    abspath_test_data,
    in_temp_dir,  # noqa: F401
    run_pypop_process,
)

generated_filenames_common = {
    "Test_Allele_Colon_Emhaplofreq-out.txt",
    "Test_Allele_Colon_Emhaplofreq-out.xml",
    "Test_Allele_Colon_HardyWeinberg-out.txt",
    "Test_Allele_Colon_HardyWeinberg-out.xml",
}


def test_Multiple_Files():
    exit_code = run_pypop_process(
        "./tests/data/Test_Allele_Colon_HardyWeinberg.ini",
        poplistfile="./tests/data/Test_Allele_Filelist.txt",
    )

    # check exit code
    assert exit_code == 0

    # check that correct files are generated (don't check contents)
    assert {
        p.name for p in Path().iterdir() if p.is_file()
    } == generated_filenames_common


def test_Multiple_Files_Absolute():
    # locate the test data files via abspath_test_data
    test_files = [
        abspath_test_data("tests/data/Test_Allele_Colon_Emhaplofreq.pop"),
        abspath_test_data("tests/data/Test_Allele_Colon_HardyWeinberg.pop"),
    ]

    # create a temporary filelist in the current working directory
    # can't use context manager because we need to manually delete
    tf = tempfile.NamedTemporaryFile("w", dir=".", suffix=".txt", delete=False)  # noqa: SIM115
    try:
        for f in test_files:
            tf.write(str(f) + "\n")
        tf.flush()  # ensure content is written

        # run pypop process with the absolute path filelist
        exit_code = run_pypop_process(
            abspath_test_data("tests/data/Test_Allele_Colon_HardyWeinberg.ini"),
            poplistfile=tf.name,
        )
        assert exit_code == 0

    finally:
        Path(tf.name).unlink(missing_ok=True)  # clean up temp file

    # check the generated files
    assert {
        p.name for p in Path().iterdir() if p.is_file()
    } == generated_filenames_common
