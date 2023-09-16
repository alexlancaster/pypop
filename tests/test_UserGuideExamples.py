import subprocess
import hashlib
import pytest
import os.path
from base import run_pypop_process, abspath_test_data, in_temp_dir

def test_DataMinimalNoHeaderNoIDs():
    exit_code = run_pypop_process('./tests/data/doc-examples/config-minimal-example.ini', './tests/data/doc-examples/data-minimal-noheader-noids.pop')
    # check exit code
    assert exit_code == 0

def test_DataMinimalNoHeader():
    exit_code = run_pypop_process('./tests/data/doc-examples/config-minimal-example.ini', './tests/data/doc-examples/data-minimal-noheader.pop')
    # check exit code
    assert exit_code == 0
    
