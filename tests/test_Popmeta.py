import subprocess
import hashlib
import pytest
import os.path
import tempfile
from base import run_popmeta_process, filecmp_list_of_files, abspath_test_data, in_temp_dir, DEFAULT_GOLD_OUTPUT_DIR

def test_Popmeta():
    exit_code = run_popmeta_process(['./tests/data/BIGDAWG_SynthControl_Data-out.xml', './tests/data/BIGDAWG_SynthControl_Data_dash-out.xml'], args=[])
    # check exit code
    assert exit_code == 0

    checked_filenames = ['1-locus-allele.tsv', '1-locus-summary.tsv', '3-locus-summary.tsv', '3-locus-haplo.tsv']
    # compare with output files list
    assert filecmp_list_of_files(checked_filenames, os.path.join(DEFAULT_GOLD_OUTPUT_DIR, 'popmeta/'))

    # make sure only expected generated files exist
    assert set(os.listdir()) ==  set(checked_filenames + ['meta.xml'])

def test_Popmeta_Prefix():
    exit_code = run_popmeta_process(['./tests/data/BIGDAWG_SynthControl_Data-out.xml', './tests/data/BIGDAWG_SynthControl_Data_dash-out.xml'], args=['--prefix-tsv', 'prefix'])
    # check exit code
    assert exit_code == 0

    checked_filenames = ['prefix-1-locus-allele.tsv', 'prefix-1-locus-summary.tsv', 'prefix-3-locus-summary.tsv', 'prefix-3-locus-haplo.tsv']
    # compare with output files list
    assert filecmp_list_of_files(checked_filenames, os.path.join(DEFAULT_GOLD_OUTPUT_DIR, 'popmeta_prefix/'))

    # make sure only expected generated files exist
    assert set(os.listdir()) ==  set(checked_filenames + ['meta.xml'])
    
