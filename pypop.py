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
from Arlequin import ArlequinExactHWTest
from Haplo import Emhaplofreq, HaploArlequin
from HardyWeinberg import HardyWeinberg, HardyWeinbergGuoThompson, HardyWeinbergGuoThompsonArlequin
from Homozygosity import Homozygosity, HomozygosityEWSlatkinExact
from ConfigParser import ConfigParser, NoOptionError
from Utils import XMLOutputStream, TextOutputStream
from getopt import getopt, GetoptError
from Filter import PassThroughFilter, AnthonyNolanFilter, AlleleCountAnthonyNolanFilter

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

# generate filename for logging filter output

defaultFilterLogFilename = uniquePrefix + "-filter.xml"

if debug:
  for section in config.sections():
    print section
    for option in config.options(section):
      print " ", option, "=", config.get(section, option)

# if 'frozen' look for VERSION info in current directory
if hasattr(sys, 'frozen'):
  versionpath = 'VERSION'
# otherwise look in installed datapath, by default
else:
  versionpath = os.path.join(datapath, 'VERSION')

# bein a development version trumps all..
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
xmlStream.opentag('dataanalysis xmlns:xi="http://www.w3.org/2001/XInclude"', date="%s-%s" % (datestr, timestr))
xmlStream.writeln()

# XInclude contents of filter.log
xmlStream.opentag('xi:include', href=defaultFilterLogFilename, parse="xml")
xmlStream.writeln()
xmlStream.emptytag('xi:fallback')
xmlStream.writeln()
xmlStream.closetag('xi:include')
xmlStream.writeln()

# more meta-data
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
  useAnthonyNolanFilter=config.getboolean("ParseFile", "useAnthonyNolanFilter")
except NoOptionError:
  useAnthonyNolanFilter=0

if useAnthonyNolanFilter:
  try:
    anthonynolanPath=config.get("ParseFile", "anthonynolanPath")
  except NoOptionError:
    anthonynolanPath=os.path.join(datapath, "anthonynolan", "HIG-seq-pep-text")
    if debug:
      print "Defaulting to system datapath %s for anthonynolanPath data" % anthonynolanPath

  # open log file for filter in append mode
  filterLogFile = XMLOutputStream(open(defaultFilterLogFilename, 'w'))

  # create a data cleaning filter to pass all data through

  filter = AnthonyNolanFilter(debug=debug,
                              directoryName=anthonynolanPath,
                              untypedAllele=untypedAllele,
                              filename=fileName,
                              logFile=filterLogFile)

  #filter = AlleleCountAnthonyNolanFilter(debug=debug,
  #                                       directoryName=anthonynolanPath,
  #                                       untypedAllele=untypedAllele,
  #                                       filename=fileName,
  #                                       logFile=filterLogFile,
  #                                       lumpThreshold=5)
  
else:
  # don't use filter, just create a "pass through filter"
  filter = PassThroughFilter()

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
                                      debug=debug)
    
    hwObject.dumpTable(locus, xmlStream)
    xmlStream.writeln()

  if config.has_section("HardyWeinbergGuoThompsonArlequin"):

    # default location for Arlequin executable
    arlequinExec = 'arlecore.exe'
        
    if config.has_section("Arlequin"):

      try:
        arlequinExec = config.get("Arlequin", "arlequinExec")
      except NoOptionError:
        print "Location to Arlequin executable file not given: assume `arlecore.exe' is in user's PATH"

    try:
      markovChainStepsHW = config.getint("HardyWeinbergGuoThompsonArlequin", \
                                         "markovChainStepsHW")
    except NoOptionError:
      samplingNum=100000
    except ValueError:
      sys.exit("require integer value")

    try:
      markovChainDememorisationStepsHW = config.getint("HardyWeinbergGuoThompsonArlequin", "markovChainDememorisationStepsHW")
    except NoOptionError:
      samplingNum=100000
    except ValueError:
      sys.exit("require integer value")


    hwArlequin=HardyWeinbergGuoThompsonArlequin(input.getIndividualsData(),
                                                locusName = locus,
                                                arlequinExec = arlequinExec,
                                                markovChainStepsHW = \
                                                markovChainStepsHW,
                                                markovChainDememorisationStepsHW=markovChainDememorisationStepsHW,
                                                untypedAllele=untypedAllele,
                                                debug=debug)
    hwArlequin.serializeTo(xmlStream)
    
    
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

  if config.has_section("HomozygosityEWSlatkinExact"):

    try:
      numReplicates=config.getint("HomozygosityEWSlatkinExact", \
                                  "numReplicates")
    except NoOptionError:
      numReplicates=10000

    hzExactObj = HomozygosityEWSlatkinExact(input.getAlleleCountAt(locus),
                                            numReplicates=numReplicates,
                                            debug=debug)

    hzExactObj.serializeHomozygosityTo(xmlStream)

  xmlStream.closetag('locus')
  xmlStream.writeln()

# estimate haplotypes

if config.has_section("Emhaplofreq"):

  # create object to generate haplotype and LD statistics
  # a wrapper around the emhaplofreq module
  haplo = Emhaplofreq(input.getIndividualsData(),
                      debug=debug,
                      untypedAllele=untypedAllele)
  
  try:
    allPairwiseLD = config.getboolean("Emhaplofreq", "allPairwiseLD")
  except NoOptionError:
    allPairwiseLD=0
  except ValueError:
    sys.exit("require a 0 or 1 as a flag")

  try:
    allPairwiseLDWithPermu = config.getboolean("Emhaplofreq",
                                               "allPairwiseLDWithPermu")
  except NoOptionError:
    allPairwiseLDWithPermu=0
  except ValueError:
    sys.exit("require a 0 or 1 as a flag")

  if allPairwiseLD:
    print "estimating all pairwise LD:",
    if allPairwiseLDWithPermu:
      print "with permutation test"
    else:
      print "with no permutation test"


  # first set the list of 2-locus haplotypes to show to empty
  twoLocusHaplosToShow = []

  try:
    locusKeys=config.get("Emhaplofreq", "lociToEstHaplo")

    if locusKeys == '*':
      print "wildcard '*' given for lociToEstHaplo, assume entire data set"
      locusKeys=string.join(input.getIndividualsData().colList,':')

    # if we will be running allPairwise*, then exclude any two-locus
    # haplotypes, since we will estimate them as part of 'all pairwise'
    if allPairwiseLD:

      modLocusKeys = []
      for group in string.split(locusKeys, ','):

        # if a two-locus haplo, add it to the list that allPairwise
        # will use
        if len(string.split(group, ':')) == 2:
          twoLocusHaplosToShow.append(string.upper(group))

        # otherwise add it to the regular output
        else:
          modLocusKeys.append(group)

      locusKeys = string.join(modLocusKeys, ',')

    # estimate haplotypes on set of locusKeys *only* if there are
    # locus groups that remain after excluding two locus haplotypes
    if locusKeys:
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

  # do all pairwise LD, w/ or w/o permutation test
  if allPairwiseLD:
    haplo.allPairwise(permutationFlag=allPairwiseLDWithPermu,
                      haploSuppressFlag=0,
                      haplosToShow=twoLocusHaplosToShow)
  
  # serialize to XML
  haplo.serializeTo(xmlStream)

# this is pre-alpha prototype code!!
# do not use
## if config.has_section("Arlequin"):

##   try:
##     arlequinExec = config.get("Arlequin", "arlequinExec")
##   except NoOptionError:
##     arlequinExec = 'arlecore.exe'
##     print "Location to Arlequin executable file not given: assume `arlecore.exe' is in user's PATH"

##   arlequin = ArlequinExactHWTest(matrix = input.getIndividualsData(),
##                                  lociList = input.getIndividualsData().colList,
##                                  arlequinExec = arlequinExec,
##                                  untypedAllele = untypedAllele)
##   print arlequin.getHWExactTest()
##   arlequin.cleanup()
#  
##   haploArlequin = HaploArlequin('arl_run.arp',
##                                 0,
##                                 2,
##                                 0,
##                                 2,
##                                 mapOrder = None,
##                                 untypedAllele = '****',
##                                 arlequinPrefix = "arl_run",
##                                 debug=debug)

##   fileData = open(fileName, 'r').readlines()
##   haploArlequin.outputArlequin(fileData[3:])
##   haploArlequin.runArlequin()

  
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

  # read and parse stylesheet
  styledoc = libxml2.parseFile(xslFilename)
  style = libxslt.parseStylesheetDoc(styledoc)

  # read output XML file
  doc = libxml2.parseFile(xmlOutFilename)

  # resolve and perform any XIncludes the document may have
  doc.xincludeProcess()

  # process via stylesheet
  result = style.applyStylesheet(doc, None)

  # save result to file
  style.saveResultToFilename(txtOutFilename, result, 0)

  # cleanup
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
