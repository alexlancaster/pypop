#! /usr/bin/env python
import sys
from ParseFile import ParseFile
from AlleleFreq import AlleleFreq

# create object
parsefile = ParseFile (debug=0)

# read in IHWG and parse data file from first argument
parsefile.parseFile(sys.argv[1])

# print out summary info for population
popData = parsefile.getPopData()
for summary in popData.keys():
    print "%20s: %s" % (summary, popData[summary])

# using the locus map and lines of individuals, generate the
# allele counts
allelefreq = AlleleFreq(parsefile.getAlleleMap(), parsefile.getFileData(),
                        debug=0)
allelefreq.generateAllelecount()

# print out allele frequency data
allelefreq.printAllelefreq()


# read in the file that contains the desired output fields
#outputSample = parsefile.dbFieldsRead('ihwg-output-fields.dat')

# write it
#parsefile.genSampleOutput(outputSample)
