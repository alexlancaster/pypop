#! /usr/bin/env python
import sys
from ParseFile import ParseGenotypeFile
from Utils import XMLOutputStream, TextOutputStream

# read in IHWG and parse data file from first argument to created
# object, print usage if number of arguments is incorrect

if len(sys.argv) != 2:
    sys.exit("Usage: summary.py <datafile>")

parsefile = ParseGenotypeFile (sys.argv[1],
                               alleleDesignator='*',
                               untypedAllele='****',
                               debug=0)

# serialize summary info for population

"""the argument to the serialize* methods should be a
{Text,XML}OutputStream, which is created from a file object.
Currently this is simply stdout, so to serialize the output to a file,
you need to create a file handle to pass to the
{Text,XML}OutputStream, e.g.:

xmlOutStream = XMLOutputStream(open('output.xml', 'w'))
parsefile.serializeMetadataTo(xmlOutStream)
parsefile.serializeAlleleCountTo(xmlOutStream)
xmlOutStream.close()

Remember not to close() the stream output until the entire data you
want to dump to the file has been written.

"""
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
