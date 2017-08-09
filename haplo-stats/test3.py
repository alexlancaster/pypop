#!/usr/bin/env python
import numpy

# NB: haplotype[i, j] contains allele for ith haplo at jth locus 
# two locus haplotypes array
haplotype = numpy.array([['A1', 'B1'], ['A2', 'B1'], ['A1', 'B2'], ['A2', 'B2']],dtype='O')

# get "shape" of array, in this case, 2d, so rows and cols as a "tuple"
rows, cols = haplotype.shape

for j in range(0, cols):
    for i in range(0, rows):
        print i, j, haplotype[i, j]

# print haplo table with 1 row per haplo
print "NB: haplotype[i, j] contains allele for ith haplo at jth locus"
print "i haplo"
for i in range(0, rows):
    print i,  
    for j in range(0, cols):
        print haplotype[i, j],
    print

alleles1 = numpy.array(['A1','A2'])
alleles2 = numpy.array(['B1','B2'])
hap_prob = numpy.array([0.3, 0.1, 0.1, 0.5])
a_freq1 = numpy.array([0.4, 0.6, 0.4, 0.6])  #FIXME: HARD CODED, WILL NEED TO COMPUTE FROM hap_prob
a_freq2 = numpy.array([0.4, 0.4, 0.6, 0.6])

zero = numpy.array([0.0])
dprime_den = zero.repeat(rows)
d_ij = hap_prob - a_freq1 * a_freq2
den_lt0 = numpy.minimum( a_freq1*a_freq2, (1-a_freq1)*(1-a_freq2) )
den_ge0 = numpy.minimum( (1-a_freq1)*a_freq2, a_freq1*(1-a_freq2) )
dprime_den[d_ij < 0] = den_lt0[d_ij < 0]
dprime_den[d_ij >=0] = den_ge0[d_ij >=0]
dprime_ij = d_ij/dprime_den
print "dprime_den:", dprime_den

print "i a_freq1 a_freq2 d_ij dprime hap_prob haplo"
for i in range(0, rows):
    print i, a_freq1[i], a_freq2[i], d_ij[i], dprime_ij[i], hap_prob[i], 
    for j in range(0, cols):
        print haplotype[i, j],
    print

print "  alleles1:", alleles1 , "CURRENTLY HARD CODED"
print "  alleles2:", alleles2
print "  length(alleles1):", numpy.unique(alleles1).size*1.0 , "MAY BE A BETTER WAY TO GET"
print "  length(alleles2):", numpy.unique(alleles2).size*1.0

dp_temp = abs(dprime_ij)*a_freq1*a_freq2
dprime = dp_temp.sum()
print "Dprime: ", dprime

w_ij = (d_ij*d_ij) / (a_freq1*a_freq2)
w = w_ij.sum()
#FIXME: NOT SURE THIS SYNTAX FOR 'min' IS CORRECT (OR GOOD)
#WANT:  wn <- sqrt( w / (min( length(unique(alleles1)), length(unique(alleles2)) ) - 1.0) )
w_den = numpy.minimum(numpy.unique(alleles1).size*1.0, numpy.unique(alleles2).size*1.0) - 1.0
wn = numpy.sqrt( w / w_den )
print "Wn: ", wn

print
print "NOTE: OVERALL D' & Wn ARE ONLY CORRECT IF ALL COMBOS OF ALLELES ARE LISTED (EVEN IF ZERO HF)"


