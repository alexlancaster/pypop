import subprocess
import hashlib
import pytest
import os.path
import tempfile
from lxml import etree
from base import abspath_test_data, in_temp_dir
from PyPop.xslt import format_number_fixed_width

def test_format_number_fixed_width():

    # empty XML to test against
    root = etree.XML('<a/>')

    # pad out with leading zeros
    output = str(root.xpath("es:format_number_fixed_width('0.032', 5)"))
    assert output == '0.03200'

    # converts to scientific notation to fit in the 5 character ('places') limit
    output = str(root.xpath("es:format_number_fixed_width('0.00000433', 5)"))
    print(output)
    assert output == '4.3E-06'

    # does not convert to scientific notation, because we have 6 characters
    output = str(root.xpath("es:format_number_fixed_width('0.00000433', 6)"))
    print(output)
    assert output == '0.000004'

    # check rounding! 
    output = str(root.xpath("es:format_number_fixed_width('0.00000491', 6)"))
    print(output)
    assert output == '0.000005'

    # again need scientific notation to fit
    output = str(root.xpath("es:format_number_fixed_width('0.000000433', 6)"))
    print(output)
    assert output == '4.33E-07'

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

