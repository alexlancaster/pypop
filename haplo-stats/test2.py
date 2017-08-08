#!/usr/bin/env python
import os.path
import sys
import string
import numpy

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '..'))

from PyPop.Utils import StringMatrix
from PyPop.Haplo import Haplostats

# matching USAFEL-UchiTelle.pop example

geno = StringMatrix(45, ['A', 'C', 'B'])
geno[ 0, 'A'] = ( '101', '201')
geno[ 1, 'A'] = ( '210', '3012')
geno[ 2, 'A'] = ( '101', '218')
geno[ 3, 'A'] = ( '2501', '201')
geno[ 4, 'A'] = ( '210', '3204')
geno[ 5, 'A'] = ( '3012', '3204')
geno[ 6, 'A'] = ( '2501', '3204')
geno[ 7, 'A'] = ( '6814', '201')
geno[ 8, 'A'] = ( '201', '201')
geno[ 9, 'A'] = ( '3204', '101')
geno[10, 'A'] = ( '6901', '210')
geno[11, 'A'] = ( '210', '3012')
geno[12, 'A'] = ( '101', '218')
geno[13, 'A'] = ( '101', '201')
geno[14, 'A'] = ( '210', '3012')
geno[15, 'A'] = ( '101', '218')
geno[16, 'A'] = ( '101', '218')
geno[17, 'A'] = ( '2501', '201')
geno[18, 'A'] = ( '201', '201')
geno[19, 'A'] = ( '3012', '2501')
geno[20, 'A'] = ( '218', '6814')
geno[21, 'A'] = ( '201', '201')
geno[22, 'A'] = ( '3204', '2501')
geno[23, 'A'] = ( '218', '218')
geno[24, 'A'] = ( '3012', '3012')
geno[25, 'A'] = ( '101', '2501')
geno[26, 'A'] = ( '101', '210')
geno[27, 'A'] = ( '210', '3012')
geno[28, 'A'] = ( '101', '2501')
geno[29, 'A'] = ( '3204', '6814')
geno[30, 'A'] = ( '201', '201')
geno[31, 'A'] = ( '201', '3204')
geno[32, 'A'] = ( '101', '6901')
geno[33, 'A'] = ( '210', '210')
geno[34, 'A'] = ( '3012', '6901')
geno[35, 'A'] = ( '218', '2501')
geno[36, 'A'] = ( '101', '2501')
geno[37, 'A'] = ( '7403', '201')
geno[38, 'A'] = ( '2501', '3012')
geno[39, 'A'] = ( '201', '201')
geno[40, 'A'] = ( '3012', '3012')
geno[41, 'A'] = ( '3204', '2501')
geno[42, 'A'] = ( '201', '201')
geno[43, 'A'] = ( '3012', '3012')
geno[44, 'A'] = ( '6901', '218')
geno[ 0, 'C'] = ( '307', '605')
geno[ 1, 'C'] = ( '712', '102')
geno[ 2, 'C'] = ( '804', '1202')
geno[ 3, 'C'] = ( '1507', '307')
geno[ 4, 'C'] = ( '1801', '102')
geno[ 5, 'C'] = ( '1507', '605')
geno[ 6, 'C'] = ( '307', '307')
geno[ 7, 'C'] = ( '102', '712')
geno[ 8, 'C'] = ( '1202', '2025')
geno[ 9, 'C'] = ( '307', '605')
geno[10, 'C'] = ( '102', '102')
geno[11, 'C'] = ( '1202', '1202')
geno[12, 'C'] = ( '307', '307')
geno[13, 'C'] = ( '102', '102')
geno[14, 'C'] = ( '1507', '307')
geno[15, 'C'] = ( '307', '712')
geno[16, 'C'] = ( '102', '102')
geno[17, 'C'] = ( '1202', '1507')
geno[18, 'C'] = ( '307', '307')
geno[19, 'C'] = ( '102', '102')
geno[20, 'C'] = ( '307', '307')
geno[21, 'C'] = ( '1208', '307')
geno[22, 'C'] = ( '307', '102')
geno[23, 'C'] = ( '102', '307')
geno[24, 'C'] = ( '605', '307')
geno[25, 'C'] = ( '605', '605')
geno[26, 'C'] = ( '1202', '1507')
geno[27, 'C'] = ( '307', '307')
geno[28, 'C'] = ( '102', '102')
geno[29, 'C'] = ( '605', '1202')
geno[30, 'C'] = ( '307', '307')
geno[31, 'C'] = ( '712', '102')
geno[32, 'C'] = ( '2025', '102')
geno[33, 'C'] = ( '605', '102')
geno[34, 'C'] = ( '3021', '605')
geno[35, 'C'] = ( '605', '605')
geno[36, 'C'] = ( '501', '408')
geno[37, 'C'] = ( '605', '307')
geno[38, 'C'] = ( '712', '3021')
geno[39, 'C'] = ( '403', '307')
geno[40, 'C'] = ( '307', '605')
geno[41, 'C'] = ( '605', '1202')
geno[42, 'C'] = ( '307', '307')
geno[43, 'C'] = ( '102', '102')
geno[44, 'C'] = ( '102', '307')
geno[ 0, 'B'] = ( '307', '605')
geno[ 1, 'B'] = ( '712', '102')
geno[ 2, 'B'] = ( '804', '1202')
geno[ 3, 'B'] = ( '1507', '307')
geno[ 4, 'B'] = ( '1801', '102')
geno[ 5, 'B'] = ( '1507', '605')
geno[ 6, 'B'] = ( '307', '307')
geno[ 7, 'B'] = ( '102', '712')
geno[ 8, 'B'] = ( '1202', '2025')
geno[ 9, 'B'] = ( '307', '605')
geno[10, 'B'] = ( '102', '102')
geno[11, 'B'] = ( '1202', '1202')
geno[12, 'B'] = ( '307', '307')
geno[13, 'B'] = ( '102', '102')
geno[14, 'B'] = ( '1507', '307')
geno[15, 'B'] = ( '307', '712')
geno[16, 'B'] = ( '102', '102')
geno[17, 'B'] = ( '1202', '1507')
geno[18, 'B'] = ( '307', '307')
geno[19, 'B'] = ( '102', '102')
geno[20, 'B'] = ( '307', '307')
geno[21, 'B'] = ( '1208', '307')
geno[22, 'B'] = ( '307', '102')
geno[23, 'B'] = ( '102', '307')
geno[24, 'B'] = ( '605', '307')
geno[25, 'B'] = ( '605', '605')
geno[26, 'B'] = ( '1202', '1507')
geno[27, 'B'] = ( '307', '307')
geno[28, 'B'] = ( '102', '102')
geno[29, 'B'] = ( '605', '1202')
geno[30, 'B'] = ( '307', '307')
geno[31, 'B'] = ( '712', '102')
geno[32, 'B'] = ( '2025', '102')
geno[33, 'B'] = ( '605', '102')
geno[34, 'B'] = ( '3021', '605')
geno[35, 'B'] = ( '605', '605')
geno[36, 'B'] = ( '501', '408')
geno[37, 'B'] = ( '605', '307')
geno[38, 'B'] = ( '712', '3021')
geno[39, 'B'] = ( '403', '307')
geno[40, 'B'] = ( '307', '605')
geno[41, 'B'] = ( '605', '1202')
geno[42, 'B'] = ( '307', '307')
geno[43, 'B'] = ( '102', '102')
geno[44, 'B'] = ( '102', '307')

# set all the control parameters
# possibly move this into the .ini file eventually?
control = {'max_iter': 5000,
           'min_posterior': 0.000000001,
           'tol': 0.00001,
           'insert_batch_size': 3,
           'random_start': 0,
           'verbose': 0,
           'max_haps_limit': 2000000 }

# FIXME: currently this assumes that geno StringMatrix contains only the loci required
# need to make sure that this works with subMatrices

import StringIO
from PyPop.Utils import XMLOutputStream

xmlOutput = XMLOutputStream(StringIO.StringIO())

haplo = Haplostats(geno, stream=xmlOutput)
converge, lnlike, n_u_hap, n_hap_pairs, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code, haplotype = \
          haplo.estHaplotypes(weight=None, control=control, numInitCond=1)

print " converge:", converge
print " lnlike:", lnlike
print " n_u_hap:", n_u_hap
print " n_hap_pairs:", n_hap_pairs
print " hap_prob:", hap_prob
print " u_hap:", u_hap
print " u_hap_code:", u_hap_code
print " subj_id:", subj_id
print " post:", post
print " hap1_code:", hap1_code
print " hap2_code:", hap2_code

# Print columns side-by-side for easier checking
# NB: u_hap is trickier since it has n.loci entries per haplo
print 'hap_prob  u_hap_code u_hap(needs to be split for printing)'
print numpy.c_[hap_prob,u_hap_code]
print 'subj_id  hap1_code  hap2_code'
print numpy.c_[subj_id,hap1_code,hap2_code]
#   for x1,x2,x3 in zip(hap_prob,u_hap,u_hap_code):
#       print x1 + '\t\t' + x2 + '\t\t' + x3


print "sample XML output"
print xmlOutput.f.getvalue()

