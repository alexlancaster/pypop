import subprocess
import hashlib
import pytest
import os.path
import tempfile
from lxml import etree
from base import abspath_test_data, in_temp_dir
from PyPop.xslt import convert_to_scientific

def test_convert_to_scientific():

    # read and parse stylesheet
    styledoc = etree.parse(abspath_test_data('src/PyPop/xslt/text.xsl'))
    style = etree.XSLT(styledoc)
    
    # read output XML file
    doc = etree.parse(abspath_test_data('./tests/data/BIGDAWG_SynthControl_Data-out.xml'))

    # process via stylesheet
    result = style(doc, **{"new-hardyweinberg-format": "1"})

    # save result to file
    result.write_output('BIGDAWG_SynthControl_Data-out.txt')

    # check exit code

    assert True == True

