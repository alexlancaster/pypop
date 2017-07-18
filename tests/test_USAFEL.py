import base
import subprocess
import hashlib
import pytest

def test_USAFEL():
    exit_code = base.run_pypop_process('./tests/data/minimal.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("USAFEL-UchiTelle-small-out.txt", 'rb').read()).hexdigest() == '97f06318478f8faa6b4a17397ca0edfe'
