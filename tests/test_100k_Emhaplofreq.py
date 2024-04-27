import subprocess
import hashlib
import pytest
# FIXME: psutil currently not used, unit test disabled
# import psutil
from base import run_pypop_process

memory_in_gb = 2  # memory needed for this test in GB
memory_in_bytes = memory_in_gb * (1024 * 1024 * 1024)

@pytest.mark.skip(reason="module deprecated")
##@pytest.mark.skipif(psutil.virtual_memory().available <= memory_in_bytes, reason="test can only be run if there is sufficient memory on the machine")
def test_100k_Emhaplofreq():
    exit_code = run_pypop_process('./tests/data/Test_100k_20loci_Dataset.ini', './tests/data/Test_100k_20loci_Dataset.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    # FIXME: disable for the moment
    # with open("Test_100k_20loci_Dataset-out.txt", 'rb') as out_handle:
    #    assert hashlib.md5(out_handle.read()).hexdigest() == 'd899396e90d99ad9eb2002506e699091'

