#! /usr/bin/env python
import sys
from ParseTSV import ParseTSV

# create object
parsefile = ParseTSV ()

# read in IHWG data file from first argument
parsefile.sample_file_read(sys.argv[1])

# print the parsed header info
parsefile.map_headers()

# read in the file that contains the desired output fields
output_sample = parsefile.db_fields_read('ihwg-output-fields.dat')

# write it
parsefile.gen_sample_output(output_sample)
