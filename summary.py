#! /usr/bin/env python
import sys, time
from ParseFile import ParseGenotypeFile
from Homozygosity import Homozygosity
from HardyWeinberg import HardyWeinberg, HardyWeinbergGuoThompson
from Utils import XMLOutputStream, TextOutputStream

# read in IHWG and parse data file from first argument to created
# object, print usage if number of arguments is incorrect

if len(sys.argv) != 2:
    sys.exit("Usage: summary.py <datafile>")

input = ParseGenotypeFile (sys.argv[1],
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
input.serializeMetadataTo(xmlOutStream)
input.serializeAlleleCountTo(xmlOutStream)
xmlOutStream.close()

Remember not to close() the stream output until the entire data you
want to dump to the file has been written.

"""

txtStream = TextOutputStream(open('out.txt', 'w'))
xmlStream = XMLOutputStream(open('out.xml', 'w'))

now = time.time()
timestr = time.strftime("%Y-%m-%d", time.localtime(now))

# opening tag
xmlStream.opentag('dataanalysis', 'date', timestr)
xmlStream.writeln()
xmlStream.tagContents('filename', sys.argv[1])
xmlStream.writeln()

input.serializeMetadataTo(txtStream)

# serialize summary info for population in XML
input.serializeMetadataTo(xmlStream)

# serialize the allele count in text form to stdout
#input.serializeAlleleCountDataTo(txtStream)

# serialize the allele count in XML form to stdout
#input.serializeAlleleCountDataTo(xmlStream)

loci = input.getLocusList()
loci.sort()
for locus in loci:

    txtStream.write("\nLocus: %s\n======\n" % locus)
    xmlStream.opentag('locus', 'name', locus)
    xmlStream.writeln()
    
    input.serializeAlleleCountDataAt(txtStream, locus)
    input.serializeAlleleCountDataAt(xmlStream, locus)
    
    hzObject = Homozygosity(input.getAlleleCountAt(locus),
                            rootPath='/home/alex/src/homozygosity',
                            debug=0)

    hzObject.serializeHomozygosityTo(txtStream)
    hzObject.serializeHomozygosityTo(xmlStream)

    hwObject = HardyWeinbergGuoThompson(input.getLocusDataAt(locus), 
                                        input.getAlleleCountAt(locus), 
                                        lumpBelow=5,
                                        debug=0)

    hwObject.serializeTo(txtStream)
    hwObject.serializeTo(xmlStream)

    hwObject.dumpTable(locus, xmlStream)

    xmlStream.closetag('locus')
    xmlStream.writeln()

# closing tag
xmlStream.closetag('dataanalysis')
