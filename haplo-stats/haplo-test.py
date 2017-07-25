#!/usr/bin/env python
import os.path, sys

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '..'))

import _Haplostats

n_loci = 2

ret_val = _Haplostats.haplo_em_pin_wrap(n_loci, 5, [1.0, 1.0, 1.0, 1.0, 1.0], [7, 7], 18, 5000, [0, 1], 0.0, 0.000000001, 0.00001, 2, 0, 18717, 16090, 14502, 0, [3, 2, 1, 4, 5, 6, 4, 7, 4, 6, 7, 1, 2, 1, 4, 6, 3, 7, 3, 5 ])

status, converge, S_lnlike, S_n_u_hap, n_hap_pairs = ret_val

print "status:", status
print "converge:", converge
print "S_lnlike:", S_lnlike
print "S_n_u_hap:", S_n_u_hap
print "n_hap_pairs:", n_hap_pairs

#ret_val = _Haplostats.haplo_em_ret_info_wrap(S_n_u_hap, n_loci, n_hap_pairs)
ret_val = _Haplostats.haplo_em_ret_info_wrap(S_n_u_hap, n_loci, n_hap_pairs,
                                             S_n_u_hap,  # length of hap_prob
                                             n_hap_pairs # length of xpost
                                             )

status, hap_prob, post = ret_val

print "status:", status
print "hap_prob:", hap_prob
print "post:", post

_Haplostats.haplo_free_memory()
