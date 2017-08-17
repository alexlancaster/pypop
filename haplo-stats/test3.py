#!/usr/bin/env python
import numpy
import math
import itertools as it

# FIXME: these arrays have to be in same order
# this is fragile and probably needs changing in main code
haplos = numpy.array([['A1', 'B1'], ['A2', 'B1'], ['A1', 'B2'], ['A2', 'B2']],dtype='O')
freqs = numpy.array([0.3, 0.1, 0.1, 0.5]) 

uniq_alleles1 = ['A1','A2']
uniq_alleles2 = ['B1','B2']

freq1_dict = {'A1': 0.4, 'A2': 0.6}
freq2_dict = {'B1': 0.4, 'B2': 0.6}

# create an equivalent of a data frame with all haplotypes
# initially as a list
allhaplos = []
for row in list(it.product(uniq_alleles1, uniq_alleles2)):
    # get current alleles
    allele1, allele2 = row
    # loop through the haplotype frequency to get the haplotype frequency
    # if it exists for this allele1, allele2 pair
    i = 0
    hap_freq = 0.0
    for hap in haplos:
        if hap[0] == allele1 and hap[1] == allele2:
            hap_freq = freqs[i]
        i += 1
    
    # add the hap and allele frequencies
    newrow = (allele1, allele2, freq1_dict[allele1], freq2_dict[allele2], hap_freq)
    allhaplos.append(newrow)

# convert to numpy structured array
allhaplos = numpy.array(allhaplos, dtype=[('allele1', 'O'), ('allele2', 'O'), ('allele.freq1', float), ('allele.freq2', float), ('haplo.freq', float)])

# now we extract the columns we need for the computations
hap_prob = allhaplos['haplo.freq']
a_freq1 = allhaplos['allele.freq1']
a_freq2 = allhaplos['allele.freq2']
alleles1 = allhaplos['allele1']
alleles2 = allhaplos['allele2']

# get the maximum size of array
num_allpossible_haplos = len(allhaplos)

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
   F_2_1_prime = numpy.nan  
   ALD_2_1 = numpy.nan
else:
   F_2_1_prime = (F_2_1 - F_2)/(1 - F_2)
   ALD_2_1 = math.sqrt(F_2_1_prime)
if F_1 == 1:
   F_1_2_prime = numpy.nan
   ALD_1_2 = numpy.nan
else:
   F_1_2_prime = (F_1_2 - F_1)/(1 - F_1)
   ALD_1_2 = math.sqrt(F_1_2_prime)
print "ALD_1_2:", ALD_1_2
print "ALD_2_1:", ALD_2_1

## compute Wn & Dprime
zero = numpy.array([0.0])
dprime_den = zero.repeat(num_allpossible_haplos)
d_ij = hap_prob - a_freq1 * a_freq2
den_lt0 = numpy.minimum( a_freq1*a_freq2, (1-a_freq1)*(1-a_freq2) )
den_ge0 = numpy.minimum( (1-a_freq1)*a_freq2, a_freq1*(1-a_freq2) )
dprime_den[d_ij < 0] = den_lt0[d_ij < 0]
dprime_den[d_ij >=0] = den_ge0[d_ij >=0]
dprime_ij = d_ij/dprime_den
print "dprime_den:", dprime_den

print "i a_freq1 a_freq2 d_ij dprime hap_prob haplo"
for i in range(num_allpossible_haplos):
    print i, a_freq1[i], a_freq2[i], d_ij[i], dprime_ij[i], hap_prob[i], "%s:%s" % (alleles1[i], alleles2[i])

print "  alleles1:", alleles1 , 
print "  alleles2:", alleles2
print "  length(alleles1):", numpy.unique(alleles1).size*1.0 , 
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
