#!/usr/bin/env python

"""Test driving wrapper for homozygosity module.

Very incomplete!

"""

import sys

from ParseFile import ParseGenotypeFile
from Homozygosity import Homozygosity

fileName = sys.argv[1]
homozyPath = sys.argv[2]

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
  hzObject = Homozygosity(input.getAlleleCountAt(locus),
			  rootPath=homozyPath,
			  debug=0)
  if hzObject._parseFile():
	  print "Fo = ", hzObject.getObservedHomozygosity()
	  print "count = ", hzObject.getCount()
	  print "mean of Fe = ", hzObject.getMean()
	  print "var of Fe = ", hzObject.getVar()
	  print "sem of Fe =", hzObject.getSem()
	  print "pval =", hzObject.getPValue()


