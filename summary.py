#! /usr/bin/env python
import sys
from ParseFile import ParseGenotypeFile
from Utils import XMLOutputStream, TextOutputStream

# read in IHWG and parse data file from first argument to created
# object

parsefile = ParseGenotypeFile (sys.argv[1],
                               alleleDesignator='*',
                               untypedAllele='****',
                               debug=0)

# serialize summary info for population
parsefile.serializeMetadataTo(TextOutputStream(sys.stdout))

# serialize the allele count in text form to stdout
parsefile.serializeAlleleCountTo(TextOutputStream(sys.stdout))

# serialize summary info for population in XML
parsefile.serializeMetadataTo(XMLOutputStream(sys.stdout))

# serialize the allele count in XML form to stdout
parsefile.serializeAlleleCountTo(XMLOutputStream(sys.stdout))

# retrieve the allele frequency data
#freqcount = parsefile.getAlleleCount()

#for locus in parsefile.getLocusList():
#    print
#     print "Locus: ", locus
#     print
#     print parsefile.getLocusDataAt(locus)
#     print
#     print "Allele Counts for: ", locus
#     print
#     print parsefile.getAlleleCountAt(locus)
