#!/usr/bin/env python

"""Test driving wrapper

"""

import sys

import ParseFile, HardyWeinberg

input = ParseFile.ParseGenotypeFile(sys.argv[1],
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
  hwObject = HardyWeinberg.HardyWeinberg(input.getLocusData(locus), input.getAlleleCountAt(locus), debug=1)


