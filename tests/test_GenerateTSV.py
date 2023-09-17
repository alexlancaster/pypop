import subprocess
import hashlib
import pytest
import os.path
from base import run_pypop_process, filecmp_ignore_newlines, filecmp_list_of_files, abspath_test_data, xfail_windows, in_temp_dir

checked_filenames_common = ['1-locus-allele.tsv', '1-locus-summary.tsv']
generated_filenames_common = ['BIGDAWG_SynthControl_Data-out.txt', 'BIGDAWG_SynthControl_Data-out.xml', 'meta.xml']
args_common = ['--enable-tsv', '--enable-ihwg']

# FIXME: not quite sure why 2 locus fails on Windows, but 3, 4 locus pass
@xfail_windows
def test_GenerateTSV_2_locus():
    exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_EM_2_locus.ini', './tests/data/BIGDAWG_SynthControl_Data.pop', args=args_common)
    # check exit code
    assert exit_code == 0

    checked_filenames = checked_filenames_common + ['2-locus-summary.tsv', '2-locus-haplo.tsv']

    # compare specific files
    assert filecmp_list_of_files(checked_filenames, './tests/data/output/generate_tsv_2_locus')

    # make sure only expected generated files exist
    assert set(os.listdir()) ==  set(checked_filenames + generated_filenames_common)

        
def test_GenerateTSV_3_locus():
    exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_EM.ini', './tests/data/BIGDAWG_SynthControl_Data.pop', args=args_common)
    # check exit code
    assert exit_code == 0

    checked_filenames = checked_filenames_common + ['3-locus-haplo.tsv','3-locus-summary.tsv']
    
    # compare with output files
    assert filecmp_list_of_files(checked_filenames, './tests/data/output/generate_tsv_3_locus')

    # make sure only expected generated files exist
    assert set(os.listdir()) ==  set(checked_filenames + generated_filenames_common)


def test_GenerateTSV_4_locus():
    exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_EM_4_locus.ini', './tests/data/BIGDAWG_SynthControl_Data.pop', args=args_common)
    # check exit code
    assert exit_code == 0

    checked_filenames = checked_filenames_common + ['4-locus-haplo.tsv','4-locus-summary.tsv']
    
    # compare with output files
    assert filecmp_list_of_files(checked_filenames, './tests/data/output/generate_tsv_4_locus')

    # make sure only expected generated files exist
    assert set(os.listdir()) ==  set(checked_filenames + generated_filenames_common)

def test_GenerateTSV_3_and_4_locus():
    exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_EM_3_and_4_locus.ini', './tests/data/BIGDAWG_SynthControl_Data.pop', args=args_common)
    # check exit code
    assert exit_code == 0

    checked_filenames = checked_filenames_common + ['3-locus-haplo.tsv','3-locus-summary.tsv', '4-locus-haplo.tsv','4-locus-summary.tsv']
    
    # compare with output files
    assert filecmp_list_of_files(checked_filenames, './tests/data/output/generate_tsv_3_and_4_locus')

    # make sure only expected generated files exist
    assert set(os.listdir()) ==  set(checked_filenames + generated_filenames_common)
    
# FIXME: not quite sure why 5 locus also fails on Windows (slightly different numbers)
@xfail_windows
def test_GenerateTSV_5_locus():
    exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_EM_5_locus.ini', './tests/data/BIGDAWG_SynthControl_Data.pop', args=args_common)
    # check exit code
    assert exit_code == 0

    checked_filenames = checked_filenames_common + ['5-locus-haplo.tsv','5-locus-summary.tsv']
    
    # compare with output files
    assert filecmp_list_of_files(checked_filenames, './tests/data/output/generate_tsv_5_locus')

    # make sure only expected generated files exist
    assert set(os.listdir()) ==  set(checked_filenames + generated_filenames_common)
    
