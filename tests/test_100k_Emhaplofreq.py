import base
import subprocess
import hashlib
import pytest

def test_100k_Emhaplofreq():
    process=subprocess.Popen(
	['./bin/pypop.py', '-m', '-c', './tests/data/Test_100k_20loci_Dataset.ini', './tests/data/Test_100k_20loci_Dataset.pop'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )
    process.communicate()
    exit_code = process.wait()  # wait until script completed

    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("Test_100k_20loci_Dataset-out.txt", 'rb').read()).hexdigest() == '66eec16da1ac9efaa45b4f2750cc2ca6'

