#!/usr/bin/env python

"""Test driving wrapper

"""

import sys

import ParseFile, HardyWeinberg
from Homozygosity import Homozygosity

fileName = sys.argv[1]
homozyPath = sys.argv[2]

input = ParseFile.ParseGenotypeFile(fileName,
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
  hwObject = HardyWeinberg.HardyWeinberg(input.getLocusDataAt(locus),
                                         input.getAlleleCountAt(locus),
                                         debug=0)
  hwObject.getChisq()

  hzObject = Homozygosity(input.getAlleleCountAt(locus),
			  rootPath=homozyPath,
			  debug=1)

  print "Fo = ", hzObject.getObservedHomozygosity()

  if hzObject.canGenerateExpectedStats():
	  print "count = ", hzObject.getCount()
	  print "mean of Fe = ", hzObject.getMean()
	  print "var of Fe = ", hzObject.getVar()
	  print "sem of Fe =", hzObject.getSem()
	  print "%f < pval < %f" % hzObject.getPValueRange()
  else:
	  print "Can't generate expected stats"


