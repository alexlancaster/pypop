#!/usr/bin/env python

"""Python population genetics statistics -- parse a literature (allele
   and count data file).  """

usage_message = """Usage: allelecount.py [OPTION] INPUTFILE
Process and run population genetics statistics on an INPUTFILE,
which consists only of allelecount data (not multilocus genotypes).
Note: config file name MUST be given.

  -h, --help           show this message
  -c, --config=FILE    select config file

  INPUTFILE  input text file"""

import sys, os, string
from getopt import getopt, GetoptError
from ConfigParser import ConfigParser, NoOptionError

from ParseFile import ParseAlleleCountFile
from Homozygosity import Homozygosity, HomozygosityEWSlatkinExact
from Utils import XMLOutputStream

try:
  opts, args =getopt(sys.argv[1:],"c:h", ["config=", "help"])
except GetoptError:
  sys.exit(usage_message)

# parse options
for o, v in opts:
  if o in ("-c", "--config"):
    configFilename = v
  elif o in ("-h", "--help"):
    sys.exit(usage_message)

# check number of arguments
if len(args) != 1:
  sys.exit(usage_message)

# parse arguments
fileName = args[0]


# generate basename
baseFileName = os.path.basename(fileName)

# parse out the parts of the filename
prefixFileName = string.split(baseFileName, ".")[0]
xmlOutFileName = prefixFileName + '.xml'
txtOutFileName = prefixFileName + '.txt'

config = ConfigParser()
config.read(configFilename)
  
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



xmlStream = XMLOutputStream(open(xmlOutFileName, 'w'))

input = ParseAlleleCountFile(fileName,
                             validPopFields=validPopFields,
                             validSampleFields=validSampleFields,
                             separator='\t',
                             debug=debug)

xmlStream.opentag('dataanalysis', role='allele-count-data')
xmlStream.writeln()


xmlStream.tagContents('filename', baseFileName)
xmlStream.writeln()

input.serializeMetadataTo(xmlStream)

# get the locus name
locus = input.getLocusName()

# wrap the output in a locus tag with the name of the locus, thus the
# output XML has the same hierarchy as the ParseGenotypeFile output.

xmlStream.opentag('locus', name=locus)
xmlStream.writeln()

# generate the allele count statistics
input.serializeAlleleCountDataAt(xmlStream, locus)

# Homozygosity

try:
  rootPath=config.get("Homozygosity", "rootPath")
except NoOptionError:
  rootPath='/net/share/PyPop/homozygosity'
  print "Defaulting to system datapath %s for homozygosity tables" % rootPath

hzObject = Homozygosity(input.getAlleleCount(),
                        rootPath=rootPath,
                        debug=debug)

hzObject.serializeHomozygosityTo(xmlStream)

# HomozygosityEWSlatkinExact

try:
  numReplicates = config.getint("HomozygosityEWSlatkinExact", "numReplicates")

except NoOptionError:
  numReplicates = 10000

hzExactObj = HomozygosityEWSlatkinExact(input.getAlleleCount(), 
                                        numReplicates=numReplicates, 
                                        debug=debug)

hzExactObj.serializeHomozygosityTo(xmlStream)

xmlStream.closetag('locus')
xmlStream.writeln()
xmlStream.closetag('dataanalysis')
xmlStream.close()

import libxml2
import libxslt

# parse XSL stylesheet
styledoc = libxml2.parseFile("/net/share/PyPop/text.xsl")
style = libxslt.parseStylesheetDoc(styledoc)

# parse XML file
doc = libxml2.parseFile(xmlOutFileName)

# apply XSL transform to it
result = style.applyStylesheet(doc, None)

# save result to text file
style.saveResultToFilename(txtOutFileName, result, 0)
style.freeStylesheet()
doc.freeDoc()
result.freeDoc()
