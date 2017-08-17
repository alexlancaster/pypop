#!/usr/bin/env python
import numpy, math

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

alleles1 = numpy.array(['A1','A2','A1','A2'])
alleles2 = numpy.array(['B1','B1','B2','B2'])
hap_prob = numpy.array([0.3, 0.1, 0.1, 0.5])
a_freq1 = numpy.array([0.4, 0.6, 0.4, 0.6])  #FIXME: HARD CODED, WILL NEED TO COMPUTE FROM hap_prob
a_freq2 = numpy.array([0.4, 0.4, 0.6, 0.6])

## compute ALD
F_1 = 0.0
F_2_1 = 0.0
F_2 = 0.0
F_1_2 = 0.0
for i in numpy.unique(alleles1):
   af_1 = numpy.unique(a_freq1[alleles1==i])
   F_1 = F_1 + af_1**2
   F_2_1 = F_2_1 + ((hap_prob[alleles1==i]**2)/af_1).sum()
for i in numpy.unique(alleles2):
   af_2 = numpy.unique(a_freq2[alleles2==i])
   F_2 = F_2 + af_2**2
   F_1_2 = F_1_2 + ((hap_prob[alleles2==i]**2)/af_2).sum()
if F_2 == 1.0:
   F_2_1_prime = nan  
   ALD_2_1 = nan
else:
   F_2_1_prime = (F_2_1 - F_2)/(1 - F_2)
   ALD_2_1 = math.sqrt(F_2_1_prime)
if F_1 == 1:
   F_1_2_prime =nan
   ALD_1_2 = nan
else:
   F_1_2_prime = (F_1_2 - F_1)/(1 - F_1)
   ALD_1_2 = math.sqrt(F_1_2_prime)
print "ALD_1_2:", ALD_1_2
print "ALD_2_1:", ALD_2_1
print "FIXME: NOT SURE YOU CAN ASSIGN nan IN ABOVE if()"

## compute Wn & Dprime
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
print "  length(unique(alleles1)):", numpy.unique(alleles1).size*1.0 , "MAY BE A BETTER WAY TO GET"
print "  length(unique(alleles2)):", numpy.unique(alleles2).size*1.0

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

# R VERSION OF ADDING ZERO FREQ FOR MISSING HAPLOS
#   # add zero frequency haplotypes
#   a1.list <- sort(unique(as.character(dat$allele1)))
#   a2.list <- sort(unique(as.character(dat$allele2)))
#   tmp <- expand.grid(a1.list,a2.list) #create all possible combos of allele1 & allele2
#   names(tmp)[1] <- "allele1"
#   names(tmp)[2] <- "allele2"
#   dat1 <- unique( dat[dat$allele1 %in% unique(dat$allele1),c("allele1","allele.freq1")] )
#   dat2 <- unique( dat[dat$allele2 %in% unique(dat$allele2),c("allele2","allele.freq2")] )
#   tmp1 <- merge(tmp, dat1, by="allele1", all.x=T, all.y=T)
#   tmp  <- merge(tmp1, dat2, by="allele2", all.x=T, all.y=T)
#   dat$allele.freq1 <- NULL
#   dat$allele.freq2 <- NULL
#   tmp1 <- merge(tmp, dat, by=c("allele1","allele2"), all.x=T, all.y=T)
#   tmp1$haplo.freq[is.na(tmp1$haplo.freq)] <- 0

#EMULATE R's expand.grid()
#https://gist.github.com/trcook/a60ef43d44dc7ef197601b9ff72dd9d8
import itertools as it
#[i for i in it.product(["a","b","c"],[1,2,3])]
for i in it.product(["a","b","c"],[1,2,3]):
  print i

# FIXME: below not yet working
import numpy.lib.recfunctions as rfn

dat1 = numpy.array([('A1', 0.4), ('A2', 0.6)], dtype=[('allele1', 'O'), ('freq', float)])
print dat1
print dat1.dtype.names

dat2 = numpy.array([('B1', 0.3), ('B2', 0.7)], dtype=[('allele2', 'O'), ('freq', float)])
print dat2
print dat2.dtype.names

grid = list(it.product(alleles1,alleles2))
print grid

tmp = numpy.array(grid, dtype=[('allele1', 'O'), ('allele2', 'O')])
print tmp
print tmp.dtype.names

tmp1 = rfn.join_by('allele1', tmp, dat1, jointype='inner', usemask=False)
print tmp1
print tmp1.dtype.names

tmp =  rfn.join_by('allele2', tmp1, dat2, jointype='inner', usemask=False)
print tmp
print tmp.dtype.names



##############################
#NB: rpy IS NOT PRESENT
#import rpy
#from rpy import *
#r("expand.grid(alleles1,alleles2)")
