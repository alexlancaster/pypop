import subprocess
import hashlib
import pytest
import os.path
from base import run_pypop_process, filecmp_ignore_newlines, abspath_test_data

@pytest.mark.skip(reason="not yet implemented")
def test_GenerateTSV():
    exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_EM.ini', './tests/data/BIGDAWG_SynthControl_Data.pop', args=['--generate-tsv'])
    # check exit code
    assert exit_code == 0

    # compare with output files
    for out_filename in ['1-locus-allele.dat', '1-locus-pairwise-fnd.dat', '3-locus-summary.dat', '1-locus-genotype.dat', '1-locus-summary.dat', '4-locus-haplo.dat', '1-locus-hardyweinberg.dat', '3-locus-haplo.dat', '4-locus-summary.dat', 'BIGDAWG_SynthControl_Data-out.txt']:
        gold_out_filename = abspath_test_data(os.path.join('./tests/data/output', out_filename))
        assert filecmp_ignore_newlines(out_filename, gold_out_filename)
