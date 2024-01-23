import sys
import subprocess
import hashlib
import pytest
import os.path
from base import abspath_test_data, run_pypop_process, filecmp_ignore_newlines, in_temp_dir, DEFAULT_GOLD_OUTPUT_DIR

def test_Filters_DigitBinning_USAFEL():
    exit_code = run_pypop_process('./tests/data/Filters_DigitBinning_USAFEL.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-Filters_DigitBinning-out.txt"
    gold_out_filename = abspath_test_data(os.path.join(DEFAULT_GOLD_OUTPUT_DIR, out_filename))

    assert filecmp_ignore_newlines(out_filename, gold_out_filename)

def test_Filters_CustomBinning_USAFEL():
    exit_code = run_pypop_process('./tests/data/Filters_CustomBinning_USAFEL.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-Filters_CustomBinning-out.txt"
    gold_out_filename = abspath_test_data(os.path.join(DEFAULT_GOLD_OUTPUT_DIR, out_filename))

    assert filecmp_ignore_newlines(out_filename, gold_out_filename)

def test_Filters_CustomBinning_HLANomen2010():
    exit_code = run_pypop_process('./tests/data/HLANomen2010_hap.ini', './tests/data/HLANomen2010_Filter-test.pop')
    # check exit code
    assert exit_code == 0

    # check filter log output as well
    for out_filename in ["HLANomen2010_Filter-test-out.txt", "HLANomen2010_Filter-test-filter.xml"]: 
        gold_out_filename = abspath_test_data(os.path.join(DEFAULT_GOLD_OUTPUT_DIR, out_filename))
        assert filecmp_ignore_newlines(out_filename, gold_out_filename)
    
def test_Filters_CustomBinning_G_Filter():
    exit_code = run_pypop_process('./tests/data/custom-binning-examples/G-Filter_config.ini', './tests/data/BIGDAWG_SynthControl_Data.pop')
    # check exit code
    assert exit_code == 0

    # check filter log output as well
    for out_filename in ["BIGDAWG_SynthControl_Data-filter.xml", "BIGDAWG_SynthControl_Data-out.txt"]:
        gold_out_filename = abspath_test_data(os.path.join(DEFAULT_GOLD_OUTPUT_DIR, "custom-binning-G-Filter", out_filename))
        assert filecmp_ignore_newlines(out_filename, gold_out_filename)

def test_Filters_CustomBinning_P_Filter():
    exit_code = run_pypop_process('./tests/data/custom-binning-examples/P-Filter_config.ini', './tests/data/BIGDAWG_SynthControl_Data.pop')
    # check exit code
    assert exit_code == 0

    # check filter log output as well
    for out_filename in ["BIGDAWG_SynthControl_Data-filter.xml", "BIGDAWG_SynthControl_Data-out.txt"]:
        gold_out_filename = abspath_test_data(os.path.join(DEFAULT_GOLD_OUTPUT_DIR, "custom-binning-P-Filter", out_filename))
        assert filecmp_ignore_newlines(out_filename, gold_out_filename)
        
