import sys
import subprocess
import hashlib
import pytest
import os.path
from base import abspath_test_data, run_pypop_process, filecmp_ignore_newlines, filecmp_list_of_files, in_temp_dir, DEFAULT_GOLD_OUTPUT_DIR, xfail_windows

def test_USAFEL():
    exit_code = run_pypop_process('./tests/data/minimal-no-emhaplofreq-no-guothompson-no-slatkin.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(os.path.join(DEFAULT_GOLD_OUTPUT_DIR, "USAFEL-UchiTelle-small-out-no-emhaplofreq-noguothompson-no-slatkin.txt"))

    assert filecmp_ignore_newlines(out_filename, gold_out_filename)

def test_USAFEL_slatkin():
    exit_code = run_pypop_process('./tests/data/minimal-no-emhaplofreq-no-guothompson.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(os.path.join(DEFAULT_GOLD_OUTPUT_DIR, "USAFEL-UchiTelle-small-out-no-emhaplofreq-noguothompson.txt"))

    assert filecmp_ignore_newlines(out_filename, gold_out_filename)

def test_USAFEL_slatkin_guothompson():
    exit_code = run_pypop_process('./tests/data/minimal-no-emhaplofreq.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(os.path.join(DEFAULT_GOLD_OUTPUT_DIR, "USAFEL-UchiTelle-small-out-no-emhaplofreq.txt"))
    assert filecmp_ignore_newlines(out_filename, gold_out_filename)

def test_USAFEL_slatkin_guothompson_emhaplofreq():
    exit_code = run_pypop_process('./tests/data/minimal.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(os.path.join(DEFAULT_GOLD_OUTPUT_DIR, out_filename))
    assert filecmp_ignore_newlines(out_filename, gold_out_filename)

# FIXME: error in one-line of 2-locus-haplo.tsv on Windows
# ld.d is 0.01563 rather than 0.01562
@xfail_windows    
def test_USAFEL_slatkin_guothompson_emhaplofreq_with_permu_tsv():
    exit_code = run_pypop_process('./tests/data/minimal-with-permu.ini', './tests/data/USAFEL-UchiTelle-small.pop', args=['--enable-tsv'])
    # check exit code
    assert exit_code == 0

    gold_subdir = 'USAFEL-UchiTelle_with_permu_tsv'

    # check text outputs
    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(os.path.join(DEFAULT_GOLD_OUTPUT_DIR, gold_subdir, "USAFEL-UchiTelle-small-out.txt"))
    assert filecmp_ignore_newlines(out_filename, gold_out_filename)

    # check TSV outputs
    checked_filenames = ['1-locus-allele.tsv', '1-locus-summary.tsv', '1-locus-genotype.tsv', '1-locus-hardyweinberg.tsv', '2-locus-summary.tsv', '2-locus-haplo.tsv', '3-locus-summary.tsv', '3-locus-haplo.tsv']

    # files to be checked for presence (not content), "USAFEL-UchiTelle-small-out.txt" already checked
    generated_filenames = ['USAFEL-UchiTelle-small-out.xml', 'USAFEL-UchiTelle-small-out.txt', 'meta.xml']
    
    # compare specific TSV files
    assert filecmp_list_of_files(checked_filenames, os.path.join(DEFAULT_GOLD_OUTPUT_DIR, gold_subdir))

    # make sure only expected generated and expected files exist
    assert set(os.listdir()) ==  set(checked_filenames + generated_filenames)
                         
    
