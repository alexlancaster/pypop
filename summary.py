#! /usr/bin/env python
import sys
from ParseTSV import ParseTSV
from AlleleFreq import AlleleFreq

# create object
parsefile = ParseTSV (debug=0)

# read in IHWG data file from first argument
parsefile.sample_file_read(sys.argv[1])

# parse the population metadata header
parsefile.map_pop_headers()

# parse the sample metadata header
parsefile.map_sample_headers()

# print out summary info for population
pop_data = parsefile.get_pop_data()
for summary in pop_data.keys():
    print "%20s: %s" % (summary, pop_data[summary])

# using the locus map and lines of individuals, generate the
# allele counts
allelefreq = AlleleFreq(parsefile.get_allele_map(), parsefile.get_file_data(),
                        debug=0)
allelefreq.generate_allelecount()

# print out allele frequency data
allelefreq.print_allelefreq()


# read in the file that contains the desired output fields
#output_sample = parsefile.db_fields_read('ihwg-output-fields.dat')

# write it
#parsefile.gen_sample_output(output_sample)
