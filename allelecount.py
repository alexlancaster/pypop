#!/usr/bin/env python

"""Python population genetics statistics -- parse a literature (allele
   and count data file).  """

import sys
from ParseFile import ParseAlleleCountFile
from Homozygosity import Homozygosity
from ConfigParser import ConfigParser, NoOptionError

from Utils import XMLOutputStream

config = ConfigParser()

config.read('allelecount.ini')
  
try:
  debug = config.getboolean("General", "debug")
except NoOptionError:
  debug=0
except ValueError:
  sys.exit("require a 0 or 1 as debug flag")

try:
  validPopFields = config.get("ParseAlleleCountFile", "validPopFields")
except NoOptionError:
  sys.exit("No valid population fields defined")

try:
  validSampleFields = config.get("ParseAlleleCountFile", "validSampleFields")
except NoOptionError:
  sys.exit("No valid sample fields defined")


xmlStream = XMLOutputStream(open('parseallelecount.xml', 'w'))

input = ParseAlleleCountFile(sys.argv[1],
                             validPopFields=validPopFields,
                             validSampleFields=validSampleFields,
                             separator='\t',
                             debug=debug)

xmlStream.opentag('dataanalysis')

input.serializeMetadataTo(xmlStream)

try:
  rootPath=config.get("Homozygosity", "rootPath")
except NoOptionError:
  rootPath='/net/share/PyPop/homozygosity'
  print "Defaulting to system datapath %s for homozygosity tables" % rootPath

hzObject = Homozygosity(input.getAlleleCount(),
                        rootPath=rootPath,
                        debug=debug)

hzObject.serializeHomozygosityTo(xmlStream)

xmlStream.closetag('dataanalysis')

xmlStream.close()
