import sys
import subprocess
import hashlib
import pytest
import os.path
from base import abspath_test_data, run_pypop_process, filecmp_ignore_newlines, in_temp_dir, DEFAULT_GOLD_OUTPUT_DIR

@pytest.mark.slow
def test_ManyOptions():

    generated_filenames = ['BIGDAWG_SynthControl_Data_with_metadata-' + suffix \
                           for suffix in ['filter-A-randomized.tsv', 'filter-DRB1-randomized.tsv', 'filtered.pop', 'filter.xml', 'out.txt', 'out.xml']]
    print(generated_filenames)
    
    exit_code = run_pypop_process('./tests/data/custom-binning-examples/many_options_config.ini', './tests/data/BIGDAWG_SynthControl_Data_with_metadata.pop')
    # check exit code
    assert exit_code == 0

    # FIXME: currently just checks presence of files, don't check contents
    assert set(os.listdir()) ==  set(generated_filenames)
        
