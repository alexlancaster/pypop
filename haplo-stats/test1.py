#!/usr/bin/env python
import os.path
import sys
import string
import numpy

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '..'))

from PyPop.Utils import StringMatrix
from PyPop.Haplo import Haplostats

# here we try to match this haplo.stats example

# control = haplo.em.control(n.try=1)
# data(hla.demo)
# attach(hla.demo)
# geno = hla.demo[1:5,c(21:24)]
# label <-c("DRB","B")
# save.em <- haplo.em(geno=geno, locus.label=label, control=control)

# R geno matrix looks like this:

# DRB.a1 DRB.a2 B.a1 B.a2
#       4     11   62   61
#       2      7    7   44
#       1     13   27   62
#       7      7    7   44
#       8     11   51   55

# so we set StringMatrix to be:

geno = StringMatrix(5, ["DRB", "B"])
geno[0, 'DRB'] = ('4', '11')
geno[1, 'DRB'] = ('2', '7')
geno[2, 'DRB'] = ('1', '13')
geno[3, 'DRB'] = ('7', '7')
geno[4, 'DRB'] = ('8', '11')
geno[0, 'B'] = ('62', '61')
geno[1, 'B'] = ('7', '44')
geno[2, 'B'] = ('27', '62')
geno[3, 'B'] = ('7', '44')
geno[4, 'B'] = ('51', '55')

# set all the control parameters
# possibly move this into the .ini file eventually?
control = {'max_iter': 5000,
           'min_posterior': 0.000000001,
           'tol': 0.00001,
           'insert_batch_size': 2,
           'random_start': 0,
           'verbose': 0,
           'max_haps_limit': 10000 }

# FIXME: currently this assumes that geno StringMatrix contains only the loci required
# need to make sure that this works with subMatrices

import io
from PyPop.Utils import XMLOutputStream

xmlOutput = XMLOutputStream(io.StringIO())

haplo = Haplostats(geno, stream=xmlOutput)
converge, lnlike, n_u_hap, n_hap_pairs, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code, haplotype, dprime, Wn, ALD_1_2, ALD_2_1 = \
          haplo.estHaplotypes(weight=None, control=control, numInitCond=1)

print(" converge:", converge)
print(" lnlike:", lnlike)
print(" n_u_hap:", n_u_hap)
print(" n_hap_pairs:", n_hap_pairs)
print(" hap_prob:", hap_prob)
print(" u_hap:", u_hap)
print(" u_hap_code:", u_hap_code)
print(" subj_id:", subj_id)
print(" post:", post)
print(" hap1_code:", hap1_code)
print(" hap2_code:", hap2_code)

# Print columns side-by-side for easier checking
# NB: u_hap is trickier since it has n.loci entries per haplo
print('hap_prob  u_hap_code u_hap(needs to be split for printing)')
print(numpy.c_[hap_prob,u_hap_code])
print('subj_id  hap1_code  hap2_code')
print(numpy.c_[subj_id,hap1_code,hap2_code])
#   for x1,x2,x3 in zip(hap_prob,u_hap,u_hap_code):
#       print x1 + '\t\t' + x2 + '\t\t' + x3


print("sample XML output")
print(xmlOutput.f.getvalue())

