#!/usr/bin/env python
import numpy

# two locus haplotypes array
haplotype = numpy.array([['A1', 'B1'], ['A2', 'B1'], ['A1', 'B2']], dtype='O')

# get "shape" of array, in this case, 2d, so rows and cols as a "tuple"
rows, cols = haplotype.shape

for j in range(0, cols):
    for i in range(0, rows):
        print i, j, haplotype[i, j]

