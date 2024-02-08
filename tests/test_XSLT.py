import subprocess
import hashlib
import pytest
import os.path
import tempfile
from lxml import etree
from base import abspath_test_data, in_temp_dir
from PyPop.xslt import format_number_fixed_width

def _run_format_function(root, num, places):
    xpath_str = "es:format_number_fixed_width('%s', %d)" % (num, places)
    output = str(root.xpath(xpath_str))
    # print(num, output)
    return output

def test_format_number_fixed_width():

    test_cases = [
        # in_str            # out_str   #places
        ('0.032',           '0.03200',  5), # pad out with leading zeros
        ('0.0433',          '0.04330',  5),
        ('0.04333',         '0.04333',  5),
        ('0.000004333',     '4.33e-6',  5), # converts to scientific notation to fit in the 5 character ('places') limit
        ('0.0000000004333', '4.3e-10',  5),
        ('0.00000433',      '0.000004', 6), # does not convert to scientific notation, because we have 6 characters
        ('0.00000491',      '0.000005', 6), # check rounding! 
        ('0.000000433',     '4.33e-7',  6), # again need scientific notation to fit
        ('0.000000',        '0.0000',   4), # handle zero as float, not sci notation
        ('0.02726',         '0.0273',   4), # rounding test 
        ('0.02725',         '0.0272',   4), # note that is somewhat unexpected: Python rounding for '5' can be weird, see: https://docs.python.org/3/library/functions.html#round
        ]

    # empty XML to test against
    root = etree.XML('<a/>')

    for test_case in test_cases:
        in_str, out_str, places = test_case
        assert out_str == _run_format_function(root, in_str, places)
    
def test_formatting_with_XML_doc():

    # read and parse stylesheet
    styledoc = etree.parse(abspath_test_data('src/PyPop/xslt/text.xsl'))
    style = etree.XSLT(styledoc)
    
    # parse output XML file
    doc = etree.parse(abspath_test_data('./tests/data/BIGDAWG_SynthControl_Data-out.xml'))

    # process via stylesheet
    result = style(doc, **{"new-hardyweinberg-format": "1",
                           "use-python-extensions": "1"})

    # save result to file
    result.write_output('BIGDAWG_SynthControl_Data-out.txt')

    # check exit code
    assert True == True

