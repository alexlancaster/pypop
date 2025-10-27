from pathlib import Path
from unittest import mock

import pytest
from base import (
    DEFAULT_GOLD_OUTPUT_DIR,
    abspath_test_data,
    filecmp_ignore_newlines,
    filecmp_list_of_files,
    in_temp_dir,  # noqa: F401
    run_pypop_process,
    skip_musllinux_x86_64,
)


def test_USAFEL_with_pval(benchmark):
    exit_code = benchmark(
        run_pypop_process,
        "./tests/data/minimal-no-emhaplofreq-no-guothompson-no-slatkin.ini",
        "./tests/data/USAFEL-UchiTelle-small.pop",
    )
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(
        DEFAULT_GOLD_OUTPUT_DIR
        / "USAFEL-UchiTelle-small-out-no-emhaplofreq-noguothompson-no-slatkin.txt"
    )

    assert filecmp_ignore_newlines(out_filename, gold_out_filename)


@pytest.mark.pval_benchmarking
def test_USAFEL_with_scipy(benchmark):
    with mock.patch("PyPop.hardyweinberg.use_scipy", True):
        exit_code = benchmark(
            run_pypop_process,
            "./tests/data/minimal-no-emhaplofreq-no-guothompson-no-slatkin.ini",
            "./tests/data/USAFEL-UchiTelle-small.pop",
        )
        # check exit code
        assert exit_code == 0

        out_filename = "USAFEL-UchiTelle-small-out.txt"
        gold_out_filename = abspath_test_data(
            DEFAULT_GOLD_OUTPUT_DIR
            / "USAFEL-UchiTelle-small-out-no-emhaplofreq-noguothompson-no-slatkin.txt"
        )

        assert filecmp_ignore_newlines(out_filename, gold_out_filename)


def test_USAFEL_slatkin():
    exit_code = run_pypop_process(
        "./tests/data/minimal-no-emhaplofreq-no-guothompson.ini",
        "./tests/data/USAFEL-UchiTelle-small.pop",
    )
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(
        DEFAULT_GOLD_OUTPUT_DIR
        / "USAFEL-UchiTelle-small-out-no-emhaplofreq-noguothompson.txt"
    )

    assert filecmp_ignore_newlines(out_filename, gold_out_filename)


def test_USAFEL_slatkin_guothompson():
    exit_code = run_pypop_process(
        "./tests/data/minimal-no-emhaplofreq.ini",
        "./tests/data/USAFEL-UchiTelle-small.pop",
    )
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(
        DEFAULT_GOLD_OUTPUT_DIR / "USAFEL-UchiTelle-small-out-no-emhaplofreq.txt"
    )
    assert filecmp_ignore_newlines(out_filename, gold_out_filename)


@skip_musllinux_x86_64
def test_USAFEL_slatkin_guothompson_emhaplofreq():
    exit_code = run_pypop_process(
        "./tests/data/minimal.ini", "./tests/data/USAFEL-UchiTelle-small.pop"
    )
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(DEFAULT_GOLD_OUTPUT_DIR / out_filename)
    assert filecmp_ignore_newlines(out_filename, gold_out_filename)


@skip_musllinux_x86_64
def test_USAFEL_slatkin_guothompson_emhaplofreq_with_permu_tsv():
    exit_code = run_pypop_process(
        "./tests/data/minimal-with-permu.ini",
        "./tests/data/USAFEL-UchiTelle-small.pop",
        args=["--enable-tsv"],
    )
    # check exit code
    assert exit_code == 0

    gold_subdir = "USAFEL-UchiTelle_with_permu_tsv"

    # check text outputs
    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(
        DEFAULT_GOLD_OUTPUT_DIR / gold_subdir / "USAFEL-UchiTelle-small-out.txt"
    )
    assert filecmp_ignore_newlines(out_filename, gold_out_filename)

    # check TSV outputs
    checked_filenames = [
        "1-locus-allele.tsv",
        "1-locus-summary.tsv",
        "1-locus-genotype.tsv",
        "1-locus-hardyweinberg.tsv",
        "2-locus-summary.tsv",
        "2-locus-haplo.tsv",
        "3-locus-summary.tsv",
        "3-locus-haplo.tsv",
    ]

    # files to be checked for presence (not content), "USAFEL-UchiTelle-small-out.txt" already checked
    generated_filenames = [
        "USAFEL-UchiTelle-small-out.xml",
        "USAFEL-UchiTelle-small-out.txt",
        "meta.xml",
    ]

    # compare specific TSV files
    assert filecmp_list_of_files(
        checked_filenames, DEFAULT_GOLD_OUTPUT_DIR / gold_subdir
    )

    # make sure only expected generated and expected files exist
    assert {p.name for p in Path().iterdir()} == set(
        checked_filenames + generated_filenames
    )
