#!/usr/bin/env python

"""Test driving wrapper.

Usage:  tdw.py <filename>

Expects to find a file called 'config.ini' in the current directory.

"""

import sys

from ParseFile import ParseGenotypeFile
from HardyWeinberg import HardyWeinberg
from Homozygosity import Homozygosity
from ConfigParser import ConfigParser, NoOptionError

fileName = sys.argv[1]

config = ConfigParser()

config.read("config.ini")

for section in config.sections():
  print section
  for option in config.options(section):
          print " ", option, "=", config.get(section, option)
				
if len(config.sections()) == 0:
	sys.exit("No output defined!  Exiting...")

# Parse "General" section

try:
	debug = config.getboolean("General", "debug")
except NoOptionError:
	debug=0
except ValueError:
	sys.exit("require a 0 or 1 as debug flag")

# Parse "ParseFile" section
try:
	alleleDesignator = config.get("ParseFile", "alleleDesignator")
except NoOptionError:
	alleleDesignator = '*'

try:
	untypedAllele = config.get("ParseFile", "alleleDesignator")
except NoOptionError:
	untypedAllele = '****'



input = ParseGenotypeFile(fileName, 
			  alleleDesignator='*', 
			  untypedAllele='****',
			  debug=0)


popData = input.getPopData()
for summary in popData.keys():
 	print "%20s: %s" % (summary, popData[summary])

loci = input.getLocusList()
loci.sort()
for locus in loci:
  print "\nLocus:", locus
  print "======\n"
  
  
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
          
    try:
      if config.getboolean("HardyWeinberg", "outputChisq"):
        hwObject.getChisq()
    except NoOptionError:
      pass
    except ValueError:
      sys.exit("require a 0 or 1 as a flag")

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
            
    try:
      if config.getboolean("Homozygosity", "outputObservedHomozygosity"):
        print "Fo = ", hzObject.getObservedHomozygosity()
    except NoOptionError:
      pass
    except ValueError:
      sys.exit("require a 0 or 1 as a flag")
          
    if hzObject.canGenerateExpectedStats():
      try:
        if config.getboolean("Homozygosity", "outputCount"):
          print "count = ", hzObject.getCount()
      except NoOptionError:
        pass
      except ValueError:
        sys.exit("require a 0 or 1 as a flag")
                  
      try:
        if config.getboolean("Homozygosity", "outputMean"):
          print "mean of Fe = ", hzObject.getMean()
      except NoOptionError:
        pass
      except ValueError:
        sys.exit("require a 0 or 1 as a flag")
                                                
      try:
        if config.getboolean("Homozygosity", "outputVar"):
          print "var of Fe = ", hzObject.getVar()
      except NoOptionError:
        pass
      except ValueError:
        sys.exit("require a 0 or 1 as a flag")

      try:
        if config.getboolean("Homozygosity", "outputSem"):
          print "sem of Fe = ", hzObject.getSem()
      except NoOptionError:
        pass
      except ValueError:
        sys.exit("require a 0 or 1 as a flag")

      try:
        if config.getboolean("Homozygosity", "outputPValueRange"):
          print "%f < pval < %f" % hzObject.getPValueRange()
      except NoOptionError:
        pass
      except ValueError:
        sys.exit("require a 0 or 1 as a flag")

    else:
      print "Can't generate expected stats"

