#!/usr/bin/env python
import os.path, sys

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '..'))

import _Haplostats

def haplo_em_fitter(n_loci,
                    n_subject,
                    weight,
                    geno_vec,
                    n_alleles,
                    max_haps,
                    max_iter,
                    loci_insert_order,
                    min_posterior,
                    tol,
                    insert_batch_size,
                    random_start,
                    iseed1,
                    iseed2,
                    iseed3,
                    verbose):


    converge = 0
    min_prior = 0.0
    n_unique = 0
    lnlike = 0.0
    n_u_hap = 0
    n_hap_pairs = 0

    tmp1 = _Haplostats.haplo_em_pin_wrap(n_loci, n_subject, weight, n_alleles,
                                            max_haps, max_iter, loci_insert_order,
                                            min_prior, min_posterior, tol, insert_batch_size,
                                            random_start, iseed1, iseed2, iseed3, verbose, geno_vec)

    # values returned from haplo_em_pin
    status1, converge, lnlike, n_u_hap, n_hap_pairs = tmp1

    tmp2 = _Haplostats.haplo_em_ret_info_wrap(\
        # input parameters
        n_u_hap, n_loci, n_hap_pairs,
        # output parameters: declaring array sizes for ret_val
        n_u_hap,          # hap_prob
        n_u_hap * n_loci, # u_hap
        n_u_hap,          # u_hap_code
        n_hap_pairs,        # subj_id
        n_hap_pairs,        # post
        n_hap_pairs,        # hap1_code
        n_hap_pairs,        # hap2_code
        )

    # values returned from haplo_em_ret_info
    status2, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code = tmp2

    _Haplostats.haplo_free_memory()

    return converge, lnlike, n_u_hap, n_hap_pairs, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code

n_loci = 2
n_subject = 5
weight = [1.0, 1.0, 1.0, 1.0, 1.0]
n_alleles = [7, 7]
max_haps = 18
max_iter = 5000
loci_insert_order =[0, 1]
min_posterior = 0.000000001
tol = 0.00001
insert_batch_size = 2
random_start = 0
iseed1 = 18717; iseed2= 16090; iseed3=14502
verbose = 0
geno_vec = [3, 2, 1, 4, 5, 6, 4, 7, 4, 6, 7, 1, 2, 1, 4, 6, 3, 7, 3, 5 ]

converge, lnlike, n_u_hap, n_hap_pairs, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code = \
          ret_val = haplo_em_fitter(n_loci,
                                    n_subject,
                                    weight,
                                    geno_vec,
                                    n_alleles,
                                    max_haps,
                                    max_iter,
                                    loci_insert_order,
                                    min_posterior,
                                    tol,
                                    insert_batch_size,
                                    random_start,
                                    iseed1,
                                    iseed2,
                                    iseed3,
                                    verbose)

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


