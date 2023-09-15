import subprocess
import hashlib
import pytest
import os.path
from base import run_pypop_process, filecmp_ignore_newlines, abspath_test_data, xfail_windows, run_in_temp_dir

# FIXME: should eventually only include the files relevant for the number of loci
filenames = ['1-locus-allele.dat',
             '1-locus-summary.dat']

# FIXME: not quite sure why 2 locus fails on Windows, but 3, 4 locus pass
@xfail_windows
def test_GenerateTSV_2_locus():
    with run_in_temp_dir():

        exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_EM_2_locus.ini', './tests/data/BIGDAWG_SynthControl_Data.pop', args=['--enable-tsv', '--enable-ihwg'])
        # check exit code
        assert exit_code == 0

        # compare with output files
        for out_filename in filenames + ['2-locus-summary.dat', '2-locus-haplo.dat']:  # add 2 locus files
            gold_out_filename = abspath_test_data(os.path.join('./tests/data/output/generate_tsv_2_locus', out_filename))
            assert filecmp_ignore_newlines(out_filename, gold_out_filename)
        
def test_GenerateTSV_3_locus():
    with run_in_temp_dir():
        
        exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_EM.ini', './tests/data/BIGDAWG_SynthControl_Data.pop', args=['--enable-tsv', '--enable-ihwg'])
        # check exit code
        assert exit_code == 0

        # compare with output files
        for out_filename in filenames + ['3-locus-haplo.dat','3-locus-summary.dat']:
            gold_out_filename = abspath_test_data(os.path.join('./tests/data/output/generate_tsv_3_locus', out_filename))
            assert filecmp_ignore_newlines(out_filename, gold_out_filename)

def test_GenerateTSV_4_locus():
    with run_in_temp_dir():
    
        exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_EM_4_locus.ini', './tests/data/BIGDAWG_SynthControl_Data.pop', args=['--enable-tsv', '--enable-ihwg'])
        # check exit code
        assert exit_code == 0

        # compare with output files
        for out_filename in filenames + ['4-locus-haplo.dat','4-locus-summary.dat']:
            gold_out_filename = abspath_test_data(os.path.join('./tests/data/output/generate_tsv_4_locus', out_filename))
            assert filecmp_ignore_newlines(out_filename, gold_out_filename)
