import subprocess
import hashlib
import pytest
import os.path
from base import run_pypop_process, filecmp_ignore_newlines, filecmp_list_of_files, abspath_test_data, xfail_windows, in_temp_dir

common_filenames = ['1-locus-allele.dat', '1-locus-summary.dat']

# FIXME: not quite sure why 2 locus fails on Windows, but 3, 4 locus pass
@xfail_windows
def test_GenerateTSV_2_locus():
    exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_EM_2_locus.ini', './tests/data/BIGDAWG_SynthControl_Data.pop', args=['--enable-tsv', '--enable-ihwg'])
    # check exit code
    assert exit_code == 0

    assert filecmp_list_of_files(common_filenames + ['2-locus-summary.dat', '2-locus-haplo.dat'], './tests/data/output/generate_tsv_2_locus')
        
def test_GenerateTSV_3_locus():
    exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_EM.ini', './tests/data/BIGDAWG_SynthControl_Data.pop', args=['--enable-tsv', '--enable-ihwg'])
    # check exit code
    assert exit_code == 0

    # compare with output files
    assert filecmp_list_of_files(common_filenames + ['3-locus-haplo.dat','3-locus-summary.dat'], './tests/data/output/generate_tsv_3_locus')

def test_GenerateTSV_4_locus():
    exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_EM_4_locus.ini', './tests/data/BIGDAWG_SynthControl_Data.pop', args=['--enable-tsv', '--enable-ihwg'])
    # check exit code
    assert exit_code == 0

    # compare with output files
    assert filecmp_list_of_files(common_filenames + ['4-locus-haplo.dat','4-locus-summary.dat'], './tests/data/output/generate_tsv_4_locus')
