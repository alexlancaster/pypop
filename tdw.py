#!/usr/bin/env python

"""Test driving wrapper.
"""

usageMessage = """Usage: tdw.py INPUTFILE
Process and run population genetics statistics on an INPUTFILE.
Expects to find a file called 'config.ini' in the current directory.

  INPUTFILE   input text file"""

import sys, os, string, time

from ParseFile import ParseGenotypeFile
from HardyWeinberg import HardyWeinberg, HardyWeinbergGuoThompson
from Homozygosity import Homozygosity
from ConfigParser import ConfigParser, NoOptionError
from Utils import XMLOutputStream, TextOutputStream

if len(sys.argv) != 2:
  sys.exit(usageMessage)

# parse out the parts of the filename

fileName = sys.argv[1]
baseFileName = os.path.basename(fileName)
prefixFileName = string.split(baseFileName, ".")[0]

config = ConfigParser()

if os.path.isfile("config.ini"):
  config.read("config.ini")
else:
  sys.exit("Could not find config.ini" + os.linesep + usageMessage)
				
if len(config.sections()) == 0:
	sys.exit("No output defined!  Exiting...")

# generate data and file prefix information

now = time.time()
datestr = time.strftime("%Y-%m-%d", time.localtime(now))
timestr = time.strftime("%H-%M-%S", time.localtime(now))
uniquePrefix = "%s-%s-%s" % (prefixFileName, datestr, timestr)

# Parse "General" section

try:
  debug = config.getboolean("General", "debug")
except NoOptionError:
  debug=0
except ValueError:
  sys.exit("require a 0 or 1 as debug flag")

# generate filenames for both text and XML files

defaultTxtOutFilename = uniquePrefix + "-out.txt"
try:
  txtOutFilename = config.get("General", "txtOutFilename")
  if txtOutFilename == '':
    txtOutFilename = defaultTxtOutFilename
except NoOptionError:
  txtOutFilename = defaultTxtOutFilename

defaultXmlOutFilename = uniquePrefix + "-out.xml"
try:
  xmlOutFilename = config.get("General", "xmlOutFilename")
  if xmlOutFilename == '':
    xmlOutFilename = defaultXmlOutFilename
except NoOptionError:
  xmlOutFilename = defaultXmlOutFilename

if debug:
  for section in config.sections():
    print section
    for option in config.options(section):
      print " ", option, "=", config.get(section, option)

# create streams

txtStream = TextOutputStream(open(txtOutFilename, 'w'))
xmlStream = XMLOutputStream(open(xmlOutFilename, 'w'))

# opening tag
xmlStream.opentag('dataanalysis', 'date', "%s-%s" % (datestr, timestr))
xmlStream.writeln()
xmlStream.tagContents('filename', baseFileName)
xmlStream.writeln()

# Parse "ParseFile" section
try:
	alleleDesignator = config.get("ParseFile", "alleleDesignator")
except NoOptionError:
	alleleDesignator = '*'

try:
	untypedAllele = config.get("ParseFile", "untypedAllele")
except NoOptionError:
	untypedAllele = '****'

# Generate the parse file object
input = ParseGenotypeFile(fileName, 
			  alleleDesignator=alleleDesignator, 
			  untypedAllele=untypedAllele,
			  debug=debug)

# serialize summary info into text
input.serializeMetadataTo(txtStream)

# serialize summary info for population in XML
input.serializeMetadataTo(xmlStream)

loci = input.getLocusList()
loci.sort()
for locus in loci:
  txtStream.write("\nLocus: %s\n======\n" % locus)
  xmlStream.opentag('locus', 'name', locus)
  xmlStream.writeln()
  
  input.serializeAlleleCountDataAt(txtStream, locus)
  input.serializeAlleleCountDataAt(xmlStream, locus)
  
  # Parse "HardyWeinberg" section
  
  if config.has_section("HardyWeinberg") and \
     len(config.options("HardyWeinberg")) > 0:
    
    try:
      lumpBelow =  config.getint("HardyWeinberg", "lumpBelow")
    except NoOptionError:
      lumpBelow=5
    except ValueError:
      sys.exit("require integer value")

    hwObject = HardyWeinberg(input.getLocusDataAt(locus), 
                             input.getAlleleCountAt(locus), 
                             lumpBelow=lumpBelow,
                             debug=debug)

    # serialize HardyWeinberg
    hwObject.serializeTo(txtStream)
    hwObject.serializeTo(xmlStream)

# don't parse the config.ini output options, just yet

##     try:
##       if config.getboolean("HardyWeinberg", "outputChisq"):
##         hwObject.getChisq()
##     except NoOptionError:
##       pass
##     except ValueError:
##       sys.exit("require a 0 or 1 as a flag")

  # Parse "HardyWeinbergGuoThompson"
  
  if config.has_section("HardyWeinbergGuoThompson") and \
     len(config.options("HardyWeinbergGuoThompson")) > 0:
    
    try:
      dememorizationSteps = config.getint("HardyWeinbergGuoThompson",
                                          "dememorizationSteps")
    except NoOptionError:
      dememorizationSteps=2000
    except ValueError:
      sys.exit("require integer value")

    try:
      samplingNum = config.getint("HardyWeinbergGuoThompson", "samplingNum")
    except NoOptionError:
      samplingNum=1000
    except ValueError:
      sys.exit("require integer value")

    try:
      samplingSize = config.getint("HardyWeinbergGuoThompson", "samplingSize")
    except NoOptionError:
      samplingSize=1000
    except ValueError:
      sys.exit("require integer value")

    # guo & thompson implementation
    hwObject=HardyWeinbergGuoThompson(input.getLocusDataAt(locus), 
                                      input.getAlleleCountAt(locus),
                                      dememorizationSteps=dememorizationSteps,
                                      samplingNum=samplingNum,
                                      samplingSize=samplingSize,
                                      lumpBelow=lumpBelow,
                                      debug=debug)
    
    # output to text only (XML serialization to be completed)
    txtStream.writeln("Guo & Thompson Hardy-Weinberg statistics:")
    txtStream.writeln("=========================================")
    hwObject.dumpTable(locus, txtStream)
    txtStream.writeln()
    
  # Parse "Homozygosity" section
	
  if config.has_section("Homozygosity") and \
     len(config.options("Homozygosity")) > 0:
          
    try:
      rootPath=config.get("Homozygosity", "rootPath")
    except NoOptionError:
      sys.exit("If homozygosity statistics are run, path to the simulated data sets must be provided")


    hzObject = Homozygosity(input.getAlleleCountAt(locus),
                                    rootPath=rootPath,
                                    debug=debug)

    hzObject.serializeHomozygosityTo(txtStream)
    hzObject.serializeHomozygosityTo(xmlStream)

# don't parse the config.ini output options, just yet

##     try:
##       if config.getboolean("Homozygosity", "outputObservedHomozygosity"):
##         print "Fo = ", hzObject.getObservedHomozygosity()
##     except NoOptionError:
##       pass
##     except ValueError:
##       sys.exit("require a 0 or 1 as a flag")
          
##     if hzObject.canGenerateExpectedStats():
##       try:
##         if config.getboolean("Homozygosity", "outputCount"):
##           print "count = ", hzObject.getCount()
##       except NoOptionError:
##         pass
##       except ValueError:
##         sys.exit("require a 0 or 1 as a flag")
                  
##       try:
##         if config.getboolean("Homozygosity", "outputMean"):
##           print "mean of Fe = ", hzObject.getMean()
##       except NoOptionError:
##         pass
##       except ValueError:
##         sys.exit("require a 0 or 1 as a flag")
                                                
##       try:
##         if config.getboolean("Homozygosity", "outputVar"):
##           print "var of Fe = ", hzObject.getVar()
##       except NoOptionError:
##         pass
##       except ValueError:
##         sys.exit("require a 0 or 1 as a flag")

##       try:
##         if config.getboolean("Homozygosity", "outputSem"):
##           print "sem of Fe = ", hzObject.getSem()
##       except NoOptionError:
##         pass
##       except ValueError:
##         sys.exit("require a 0 or 1 as a flag")

##       try:
##         if config.getboolean("Homozygosity", "outputPValueRange"):
##           print "%f < pval < %f" % hzObject.getPValueRange()
##       except NoOptionError:
##         pass
##       except ValueError:
##         sys.exit("require a 0 or 1 as a flag")

##       else:
##          print "Can't generate expected stats"

  xmlStream.closetag('locus')
  xmlStream.writeln()

# closing tag
xmlStream.closetag('dataanalysis')

# close streams
txtStream.close()
xmlStream.close()
