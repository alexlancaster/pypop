#! /usr/bin/env python
import sys
from ParseFile import ParseGenotypeFile

# read in IHWG and parse data file from first argument to created
# object

parsefile = ParseGenotypeFile (sys.argv[1],
                               alleleDesignator='*',
                               untypedAllele='****',
                               debug=0)

# print out summary info for population
popData = parsefile.getPopData()
for summary in popData.keys():
    print "%20s: %s" % (summary, popData[summary])

# retrieve the allele frequency data
freqcount = parsefile.getAlleleCount()

# quick & dirty print output of the allele frequency table for each
# locus, with totals of allele and total counts in parentheses.
for locus in freqcount.keys():
    print
    print "Locus:", locus
    print "======"
    print
    alleleTable, total = freqcount[locus]
    totalFreq = 0
    alleles = alleleTable.keys()
    alleles.sort()
    for allele in alleles:
        freq = float(alleleTable[allele])/float(total)
        totalFreq += freq
        print "%s :%0.5f (%d)" % (allele, freq, alleleTable[allele])
    print "Total freq: %0.5f (%d)" % (totalFreq, total)

for locus in parsefile.getLocusList():
    print "Locus: ", locus
    print
    print parsefile.getLocusData(locus)
    print

# read in the file that contains the desired output fields
#outputSample = parsefile.dbFieldsRead('ihwg-output-fields.dat')

# write it
#parsefile.genSampleOutput(outputSample)
