#!/usr/bin/env python

import os
import os.path
import sys
import shutil
import unittest
import pytest
import filecmp
from pytest_pipeline import PipelineRun, mark, utils

class AlleleColon(PipelineRun):

    # before_run-marked functions will be run before the pipeline is executed
    @mark.before_run
    def test_prep_executable(self):

        DIR = os.path.dirname(os.path.realpath(__file__))
        currpath = os.path.join(DIR, '..')
        print currpath
        # copy the executable to the run directory
        shutil.copy2(os.path.join(currpath, "bin/pypop.py"), ".")
        shutil.copy2(os.path.join(currpath, "data/ihiws2017/Test_Allele_Colon_HardyWeinberg.ini"), ".")
        shutil.copy2(os.path.join(currpath, "data/ihiws2017/Test_Allele_Colon_HardyWeinberg.pop"), ".")
        # ensure that the file is executable
        assert os.access("pypop.py", os.X_OK)

# a pipeline run is treated as a test fixture
run = AlleleColon.class_fixture(cmd="./pypop.py -c Test_Allele_Colon_HardyWeinberg.ini Test_Allele_Colon_HardyWeinberg.pop", stdout="run.stdout")

# the fixture is bound to a unittest.TestCase using the usefixtures mark
@pytest.mark.usefixtures("run")
# tests per-pipeline run are grouped in one unittest.TestCase instance
class TestAlleleColon(unittest.TestCase):

    def test_exit_code(self):
        # the run fixture is stored as the `run_fixture` attribute
        assert self.run_fixture.exit_code == 0

    def test_result_md5(self):
        # compare with md5sum of output file
        assert utils.file_md5sum('Test_Allele_Colon_HardyWeinberg-out.txt') == '3c4e98c7dd6d1d5876d9d077b762b9f0'

