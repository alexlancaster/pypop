#!/usr/bin/env python

"""Python population genetics statistics.
"""

import sys
from ParseFile import ParseAlleleCountFile
from Homozygosity import Homozygosity

from Utils import XMLOutputStream

xmlStream = XMLOutputStream(open('parseallelecount.xml', 'w'))

input = ParseAlleleCountFile(sys.argv[1],
                             validPopFields="""populat
method
ethnic
country
latit
longit""",
                             
                             validSampleFields="""DQA1
count""",
                             separator='\t',
                             debug=1)

xmlStream.opentag('dataanalysis')

input.serializeMetadataTo(xmlStream)

hzObject = Homozygosity(input.getAlleleCount(),
                        rootPath='/net/share/PyPop/homozygosity',
                        debug=1)

hzObject.serializeHomozygosityTo(xmlStream)

xmlStream.closetag('dataanalysis')

xmlStream.close()
