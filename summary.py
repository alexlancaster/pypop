#! /usr/bin/env python
import sys
from ParseTSV import ParseTSV

# create object
parsefile = ParseTSV ()

# read in IHWG data file from first argument
parsefile.sample_file_read(sys.argv[1])

# print the parsed header info
parsefile.map_headers()

