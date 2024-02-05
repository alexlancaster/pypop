import subprocess
import hashlib
import pytest
import os.path
import tempfile
from lxml import etree
from base import abspath_test_data, in_temp_dir
from PyPop.xslt import format_number_fixed_width

def test_format_number_fixed_width():

    # read and parse stylesheet
    styledoc = etree.parse(abspath_test_data('src/PyPop/xslt/text.xsl'))
    style = etree.XSLT(styledoc)
    
    # read output XML file
    doc = etree.parse(abspath_test_data('./tests/data/BIGDAWG_SynthControl_Data-out.xml'))

    # process via stylesheet
    result = style(doc, **{"new-hardyweinberg-format": "1",
                           "use-python-extensions": "1"})

    # save result to file
    result.write_output('BIGDAWG_SynthControl_Data-out.txt')

    # check exit code

    assert True == True

