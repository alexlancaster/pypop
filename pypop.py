#!/usr/bin/env python

"""Python population genetics statistics.
"""

import sys, os, string, time

datapath = os.path.join(sys.prefix, 'share', 'PyPop')
altpath = os.path.join(datapath, 'config.ini')

usage_message = """Usage: pypop [OPTION] INPUTFILE
Process and run population genetics statistics on an INPUTFILE.
Expects to find a configuration file called 'config.ini' in the
current directory or in %s.

  -l, --use-libxslt    filter XML via XSLT using libxslt (default)
  -s, --use-4suite     filter XML via XSLT using 4Suite
  -h, --help           show this message
  -c, --config=FILE    select alternative config file
  -d, --debug          enable debugging output (overrides config file setting)

  INPUTFILE   input text file""" % altpath

from ParseFile import ParseGenotypeFile
from Haplo import Emhaplofreq
from HardyWeinberg import HardyWeinberg, HardyWeinbergGuoThompson
from Homozygosity import Homozygosity
from ConfigParser import ConfigParser, NoOptionError
from Utils import XMLOutputStream, TextOutputStream
from getopt import getopt, GetoptError
from Filter import AnthonyNolanFilter

try:
  opts, args =getopt(sys.argv[1:],"lsc:hd", ["use-libxslt", "use-4suite", "experimental", "config=", "help", "debug"])
except GetoptError:
  sys.exit(usage_message)

# default options
use_libxsltmod = 0
use_FourSuite = 0
configFilename = 'config.ini'
specifiedConfigFile = 0
debugFlag = 0

# parse options
for o, v in opts:
  if o in ("-l", "--use-libxslt"):
    use_libxsltmod = 1
  elif o in ("-s", "--use-4suite"):
    use_FourSuite = 1
  elif o in ("-c", "--config"):
    configFilename = v
    specifiedConfigFile = 1
  elif o in ("-d", "--debug"):
    debugFlag = 1
  elif o in ("-h", "--help"):
    sys.exit(usage_message)

# if neither option is set explicitly, use libxslt python wrappers
if not (use_libxsltmod or use_FourSuite):
  use_libxsltmod = 1

# check number of arguments
if len(args) != 1:
  sys.exit(usage_message)

# parse arguments
fileName = args[0]

# parse out the parts of the filename
baseFileName = os.path.basename(fileName)
prefixFileName = string.split(baseFileName, ".")[0]

config = ConfigParser()

if os.path.isfile(configFilename):
  config.read(configFilename)
else:
  if specifiedConfigFile:
    sys.exit("Could not find config file: `%s' " % configFilename)
  else:
    if os.path.isfile(altpath):
      config.read(altpath)
    else:
      sys.exit("Could not find config file either in current directory or " +
               altpath + os.linesep + usage_message)
				
if len(config.sections()) == 0:
	sys.exit("No output defined!  Exiting...")

# generate date and time

now = time.time()
datestr = time.strftime("%Y-%m-%d", time.localtime(now))
timestr = time.strftime("%H-%M-%S", time.localtime(now))

# Parse "General" section

try:
  debug = config.getboolean("General", "debug")
except NoOptionError:
  debug=0
except ValueError:
  sys.exit("require a 0 or 1 as debug flag")

# if "-d" command line option used, then respect that, overriding
# config file setting

if debugFlag == 1:
  debug = 1

# generate file prefix
try:
  outFilePrefixType = config.get("General", "outFilePrefixType")
  if outFilePrefixType == 'filename':
    uniquePrefix = prefixFileName
  else:
    sys.exit("outFilePrefixType: %s must be 'filename'" % outFilePrefixType)
except NoOptionError:
  uniquePrefix = "%s-%s-%s" % (prefixFileName, datestr, timestr)  


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

# get version
versionpath = os.path.join(datapath, 'VERSION')
if os.path.isfile('DEVEL_VERSION'):
  version = 'DEVEL_VERSION'
elif os.path.isfile(versionpath):
  f = open(versionpath)
  version = string.strip(f.readline())
else:
  sys.exit("Could not find a version!  Exiting...")

altpath = os.path.join(datapath, 'config.ini')
# create XML stream
xmlStream = XMLOutputStream(open(xmlOutFilename, 'w'))

# opening tag
xmlStream.opentag('dataanalysis', date="%s-%s" % (datestr, timestr))
xmlStream.writeln()
xmlStream.tagContents('filename', baseFileName)
xmlStream.writeln()
xmlStream.tagContents('pypop-version', version)
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

try:
  fieldPairDesignator = config.get("ParseFile", "fieldPairDesignator")
except NoOptionError:
  fieldPairDesignator = '(2)'

try:
  validPopFields = config.get("ParseFile", "validPopFields")
except NoOptionError:
  sys.exit("No valid population fields defined")

try:
  popNameDesignator = config.get("ParseFile", "popNameDesignator")
except NoOptionError:
  popNameDesignator = "+"

try:
  validSampleFields = config.get("ParseFile", "validSampleFields")
except NoOptionError:
  sys.exit("No valid sample fields defined")

try:
  anthonynolanPath=config.get("ParseFile", "anthonynolanPath")
except NoOptionError:
  anthonynolanPath=os.path.join(datapath, "anthonynolan", "HIG-seq-pep-text")
  if debug:
    print "Defaulting to system datapath %s for anthonynolanPath data" % anthonynolanPath

# open log file for filter in append mode
filterLogFile = TextOutputStream(open('filter.log', 'a'))

# create a data cleaning filter to pass all data through

filter = AnthonyNolanFilter(debug=debug,
                            directoryName=anthonynolanPath,
                            untypedAllele=untypedAllele,
                            filename=fileName,
                            logFile=filterLogFile)

# Generate the parse file object
input = ParseGenotypeFile(fileName,
                          validPopFields=validPopFields,
                          validSampleFields=validSampleFields,
			  alleleDesignator=alleleDesignator, 
			  untypedAllele=untypedAllele,
                          popNameDesignator=popNameDesignator,
                          fieldPairDesignator=fieldPairDesignator,
                          filter=filter,
			  debug=debug)

# serialize summary info for population in XML
input.serializeMetadataTo(xmlStream)

loci = input.getLocusList()

for locus in loci:
  xmlStream.opentag('locus', name=locus)
  xmlStream.writeln()
  
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
    hwObject.serializeTo(xmlStream)

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

    try:
      maxMatrixSize = config.getint("HardyWeinbergGuoThompson", "maxMatrixSize")
    except NoOptionError:
      maxMatrixSize=250
    except ValueError:
      sys.exit("require integer value")

    # guo & thompson implementation
    hwObject=HardyWeinbergGuoThompson(input.getLocusDataAt(locus), 
                                      input.getAlleleCountAt(locus),
                                      dememorizationSteps=dememorizationSteps,
                                      samplingNum=samplingNum,
                                      samplingSize=samplingSize,
                                      maxMatrixSize=maxMatrixSize,
                                      lumpBelow=lumpBelow,
                                      debug=debug)
    
    hwObject.dumpTable(locus, xmlStream)
    xmlStream.writeln()
    
  # Parse "Homozygosity" section
	
  if config.has_section("Homozygosity"):
          
    try:
      rootPath=config.get("Homozygosity", "rootPath")
    except NoOptionError:
      rootPath=os.path.join(datapath, "homozygosity")
      if debug:
        print "Defaulting to system datapath %s for homozygosity tables" % rootPath
        

    hzObject = Homozygosity(input.getAlleleCountAt(locus),
                                    rootPath=rootPath,
                                    debug=debug)

    hzObject.serializeHomozygosityTo(xmlStream)

  xmlStream.closetag('locus')
  xmlStream.writeln()

# estimate haplotypes

if config.has_section("Emhaplofreq"):

  # create object to generate haplotype and LD statistics
  # a wrapper around the emhaplofreq module
  haplo = Emhaplofreq(input.getIndividualsData(), debug=debug)
  
  try:
    locusKeys=config.get("Emhaplofreq", "lociToEstHaplo")

    if locusKeys == '*':
      print "wildcard '*' given for lociToEstHaplo, assume entire data set"
      locusKeys=string.join(input.getIndividualsData().colList,':')

    # estimate haplotype frequencies for the specified loci
    haplo.estHaplotypes(locusKeys)

  except NoOptionError:
    print "no loci provided for which to estimate haplotype frequencies"

  try:
    locusKeysLD=config.get("Emhaplofreq", "lociToEstLD")

    if locusKeysLD == '*':
      print "wildcard '*' given for lociToEstLD, assume entire data set"
      locusKeysLD=string.join(input.getIndividualsData().colList,':')

    # estimate LD for the specified loci
    haplo.estLinkageDisequilibrium(locusKeysLD)

  except NoOptionError:
    print "no loci provided for which to estimate LD"


  # do all pairwise LD
  try:
    estAllPairwiseLD = config.getboolean("Emhaplofreq", "estAllPairwiseLD")
  except NoOptionError:
    estAllPairwiseLD=0
  except ValueError:
    sys.exit("require a 0 or 1 as a flag")

  if estAllPairwiseLD:
    print "estimating all pairwise LD..."
    haplo.estAllPairwiseLD()

  # do all pairwise haplotypes
  try:
    estAllPairwiseHaplo = config.getboolean("Emhaplofreq",
                                            "estAllPairwiseHaplo")
  except NoOptionError:
    estAllPairwiseHaplo=0
  except ValueError:
    sys.exit("require a 0 or 1 as a flag")

  if estAllPairwiseHaplo:
    print "estimating all pairwise haplotypes..."
    haplo.estAllPairwiseHaplo()

  # do all pairwise LD *and* haplotypes
  try:
    estAllPairwiseLDHaplo = config.getboolean("Emhaplofreq",
                                              "estAllPairwiseLDHaplo")
  except NoOptionError:
    estAllPairwiseLDHaplo=0
  except ValueError:
    sys.exit("require a 0 or 1 as a flag")

  if estAllPairwiseLDHaplo:
    print "estimating all pairwise LD and haplotypes..."
    haplo.estAllPairwiseLDHaplo()

  # serialize to XML
  haplo.serializeTo(xmlStream)
  
# closing tag
xmlStream.closetag('dataanalysis')

# close XML stream
xmlStream.close()

# create default XSL stylesheet location
xslFilenameDefault = os.path.join(datapath, 'text.xsl')

# check config options, and use that location, if provided
try:
  xslFilename = config.get("General", "xslFilename")
except NoOptionError:
  xslFilename=xslFilenameDefault

# check to see if file exists, otherwise fail with an error
if os.path.isfile(xslFilename):
  pass
else:
  sys.exit("Could not find xsl file: `%s' " % xslFilename)

if use_libxsltmod:

## obsolete libxslt bindings
  
##   import libxsltmod
##   output = libxsltmod.translate_to_string('f', xslFilename,
##                                           'f', xmlOutFilename)
  
##   # open new txt output
##   newOut = TextOutputStream(open(txtOutFilename, 'w'))
##   newOut.write(output)
##   newOut.close()

  # now use bindings that are part of libxml2/libxslt 
  import libxml2
  import libxslt

  styledoc = libxml2.parseFile(xslFilename)
  style = libxslt.parseStylesheetDoc(styledoc)
  doc = libxml2.parseFile(xmlOutFilename)
  result = style.applyStylesheet(doc, None)
  style.saveResultToFilename(txtOutFilename, result, 0)
  style.freeStylesheet()
  doc.freeDoc()
  result.freeDoc()

if use_FourSuite:

  from xml.xslt.Processor import Processor

  # open XSLT stylesheet
  styleSheet = open(xslFilename, 'r')
  
  # re-open text stream
  xmlStream = open(xmlOutFilename, 'r')

  # open new txt output
  newOut = TextOutputStream(open(txtOutFilename, 'w'))
  
  # create xsl process
  p = Processor()
  
  # attach the stylesheet
  p.appendStylesheetStream(styleSheet)
  
  # run the stylesheet on the XML output
  p.runStream(xmlStream, outputStream=newOut)
  
  # close streams
  newOut.close()
  styleSheet.close()
