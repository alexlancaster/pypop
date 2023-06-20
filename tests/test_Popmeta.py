import subprocess
import hashlib
import pytest
import os.path
from base import run_popmeta_process, filecmp_ignore_newlines, abspath_test_data, xfail_windows

def test_Popmeta():
    exit_code = run_popmeta_process(['./tests/data/BIGDAWG_SynthControl_Data-out.xml', './tests/data/BIGDAWG_SynthControl_Data_dash-out.xml'], args=[])
    # check exit code
    assert exit_code == 0

    # compare with output files
    for out_filename in ['1-locus-allele.dat', '1-locus-hardyweinberg.dat', '1-locus-summary.dat',
                         '1-locus-pairwise-fnd.dat','1-locus-genotype.dat',
                         '2-locus-summary.dat', '2-locus-haplo.dat',
                         '3-locus-summary.dat', '3-locus-haplo.dat',
                         '4-locus-summary.dat', '4-locus-haplo.dat']:
        gold_out_filename = abspath_test_data(os.path.join('./tests/data/output/popmeta/', out_filename))
        assert filecmp_ignore_newlines(out_filename, gold_out_filename)
