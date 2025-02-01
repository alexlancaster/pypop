from base import (
    DEFAULT_GOLD_OUTPUT_DIR,
    abspath_test_data,
    filecmp_ignore_newlines,
    filecmp_list_of_files,
    in_temp_dir,  # noqa: F401
    run_pypop_process,
)


def test_Filters_DigitBinning_USAFEL():
    exit_code = run_pypop_process(
        "./tests/data/Filters_DigitBinning_USAFEL.ini",
        "./tests/data/USAFEL-UchiTelle-small.pop",
    )
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-Filters_DigitBinning-out.txt"
    gold_out_filename = abspath_test_data(DEFAULT_GOLD_OUTPUT_DIR / out_filename)

    assert filecmp_ignore_newlines(out_filename, gold_out_filename)


def test_Filters_CustomBinning_USAFEL():
    exit_code = run_pypop_process(
        "./tests/data/Filters_CustomBinning_USAFEL.ini",
        "./tests/data/USAFEL-UchiTelle-small.pop",
    )
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-Filters_CustomBinning-out.txt"
    gold_out_filename = abspath_test_data(DEFAULT_GOLD_OUTPUT_DIR / out_filename)

    assert filecmp_ignore_newlines(out_filename, gold_out_filename)


def test_Filters_CustomBinning_HLANomen2010():
    exit_code = run_pypop_process(
        "./tests/data/HLANomen2010_hap.ini", "./tests/data/HLANomen2010_Filter-test.pop"
    )
    # check exit code
    assert exit_code == 0

    # check filter log output as well
    for out_filename in [
        "HLANomen2010_Filter-test-out.txt",
        "HLANomen2010_Filter-test-filter.xml",
    ]:
        gold_out_filename = abspath_test_data(DEFAULT_GOLD_OUTPUT_DIR / out_filename)
        assert filecmp_ignore_newlines(out_filename, gold_out_filename)


def test_Filters_CustomBinning_G_Filter():
    exit_code = run_pypop_process(
        "./tests/data/custom-binning-examples/G-Filter_config.ini",
        "./tests/data/BIGDAWG_SynthControl_Data.pop",
    )
    # check exit code
    assert exit_code == 0

    # check filter log output as well
    for out_filename in [
        "BIGDAWG_SynthControl_Data-filter.xml",
        "BIGDAWG_SynthControl_Data-out.txt",
    ]:
        gold_out_filename = abspath_test_data(
            DEFAULT_GOLD_OUTPUT_DIR / "custom-binning-G-Filter" / out_filename
        )
        assert filecmp_ignore_newlines(out_filename, gold_out_filename)


def test_Filters_CustomBinning_P_Filter():
    exit_code = run_pypop_process(
        "./tests/data/custom-binning-examples/P-Filter_config.ini",
        "./tests/data/BIGDAWG_SynthControl_Data.pop",
    )
    # check exit code
    assert exit_code == 0

    # check filter log output as well
    for out_filename in [
        "BIGDAWG_SynthControl_Data-filter.xml",
        "BIGDAWG_SynthControl_Data-out.txt",
    ]:
        gold_out_filename = abspath_test_data(
            DEFAULT_GOLD_OUTPUT_DIR / "custom-binning-P-Filter" / out_filename
        )
        assert filecmp_ignore_newlines(out_filename, gold_out_filename)


def test_Filters_Sequence_OldNomenclature():
    exit_code = run_pypop_process(
        "./tests/data/sequence-nopoptests.ini",
        "./tests/data/USAFEL-UchiTelle.pop",
    )
    # check exit code
    assert exit_code == 0

    # compare output
    assert filecmp_list_of_files(
        ["USAFEL-UchiTelle-filter.xml", "USAFEL-UchiTelle-out.txt"],
        DEFAULT_GOLD_OUTPUT_DIR / "Filters_Sequence_OldNomenclature",
    )


def test_Filters_Sequence_NewNomenclature():
    exit_code = run_pypop_process(
        "./tests/data/sequence-nopoptests-msf-3.59.0-alpha.ini",
        "./tests/data/USAFEL-UchiTelle-small.pop",
    )
    # check exit code
    assert exit_code == 0

    # compare output
    assert filecmp_list_of_files(
        ["USAFEL-UchiTelle-small-filter.xml", "USAFEL-UchiTelle-small-out.txt"],
        DEFAULT_GOLD_OUTPUT_DIR / "Filters_Sequence_NewNomenclature",
    )


def test_Filters_Sequence_DumpFiltered():
    exit_code = run_pypop_process(
        "./tests/data/sequence-nopoptests-dump-filtered.ini",
        "./tests/data/USAFEL-UchiTelle.pop",
    )
    # check exit code
    assert exit_code == 0

    # compare output
    assert filecmp_list_of_files(
        ["USAFEL-UchiTelle-filtered.pop"],
        DEFAULT_GOLD_OUTPUT_DIR / "Filters_Sequence_DumpFiltered",
    )


def test_Filters_AnthonyNolan_Sequence_DumpFiltered():
    exit_code = run_pypop_process(
        "./tests/data/anthonynolan-sequence-nopoptests-dump-filtered.ini",
        "./tests/data/USAFEL-UchiTelle.pop",
    )
    # check exit code
    assert exit_code == 0

    # compare output
    assert filecmp_list_of_files(
        [
            "USAFEL-UchiTelle-filter.xml",
            "USAFEL-UchiTelle-out.txt",
            "USAFEL-UchiTelle-filtered.pop",
        ],
        DEFAULT_GOLD_OUTPUT_DIR / "Filters_AnthonyNolan_Sequence_DumpFiltered",
    )
