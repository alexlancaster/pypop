import subprocess
import hashlib
import pytest
import os.path
import tempfile
from base import run_popmeta_process, filecmp_list_of_files, abspath_test_data, xfail_windows, in_temp_dir

def test_Popmeta():

    exit_code = run_popmeta_process(['./tests/data/BIGDAWG_SynthControl_Data-out.xml', './tests/data/BIGDAWG_SynthControl_Data_dash-out.xml'], args=[])
    # check exit code
    assert exit_code == 0

    checked_filenames = ['1-locus-allele.dat', '1-locus-summary.dat', '3-locus-summary.dat', '3-locus-haplo.dat']
    
    # compare with output files list
    assert filecmp_list_of_files(checked_filenames, './tests/data/output/popmeta/')

    # make sure only expected generated files exist
    assert set(os.listdir()) ==  set(checked_filenames + ['meta.xml'])

