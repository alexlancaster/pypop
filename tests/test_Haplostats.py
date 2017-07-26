import base
import unittest
import _Haplostats

def call_Haplostats(n_loci, n_subject, weight, n_alleles,
                    max_haps, max_iter, loci_insert_order,
                    min_prior, min_posterior, tol, insert_batch_size,
                    random_start, iseed1, iseed2, iseed3, verbose, geno_vec):

    ret_val = _Haplostats.haplo_em_pin_wrap(n_loci, n_subject, weight, n_alleles,
                                            max_haps, max_iter, loci_insert_order,
                                            min_prior, min_posterior, tol, insert_batch_size,
                                            random_start, iseed1, iseed2, iseed3, verbose, geno_vec)

    # values returned from haplo_em_pin
    status1, converge, S_lnlike, S_n_u_hap, n_hap_pairs = ret_val

    ret_val = _Haplostats.haplo_em_ret_info_wrap(\
        # input parameters
        S_n_u_hap, n_loci, n_hap_pairs,
        # output parameters: declaring array sizes for ret_val
        S_n_u_hap,          # hap_prob
        S_n_u_hap * n_loci, # u_hap
        S_n_u_hap,          # u_hap_code
        n_hap_pairs,        # subj_id
        n_hap_pairs,        # post
        n_hap_pairs,        # hap1_code
        n_hap_pairs,        # hap2_code
        )

    # values returned from haplo_em_ret_info
    status2, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code = ret_val
    _Haplostats.haplo_free_memory()

    return status1, converge, S_lnlike, S_n_u_hap, n_hap_pairs, status2, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code

def test_Haplostats_Simple():
    n_loci = 2
    n_subject = 5
    weight = [1.0, 1.0, 1.0, 1.0, 1.0]
    n_alleles = [7, 7]
    max_haps = 18
    max_iter = 5000
    loci_insert_order =[0, 1]
    min_prior = 0.0
    min_posterior = 0.000000001
    tol = 0.00001
    insert_batch_size = 2
    random_start = 0
    iseed1 = 18717; iseed2= 16090; iseed3=14502
    verbose = 0
    geno_vec = [3, 2, 1, 4, 5, 6, 4, 7, 4, 6, 7, 1, 2, 1, 4, 6, 3, 7, 3, 5 ]

    ret_val = call_Haplostats(n_loci, n_subject, weight, n_alleles,
                              max_haps, max_iter, loci_insert_order,
                              min_prior, min_posterior, tol, insert_batch_size,
                              random_start, iseed1, iseed2, iseed3, verbose, geno_vec)
    status1, converge, S_lnlike, S_n_u_hap, n_hap_pairs, status2, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code = ret_val

    assert status1 == 0
    assert converge == 1
    assert S_lnlike == -20.42316124449607
    assert S_n_u_hap == 16
    assert n_hap_pairs == 9

    assert status2 == 0
    assert hap_prob == [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    assert u_hap == [1, 2, 1, 7, 2, 1, 2, 3, 3, 6, 3, 7, 4, 1, 4, 3, 5, 4, 5, 5, 6, 4, 6, 5, 6, 6, 6, 7, 7, 2, 7, 7]
    assert u_hap_code == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    assert subj_id == [0, 0, 1, 1, 2, 2, 3, 4, 4]
    assert post == [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5]
    assert hap1_code == [5, 4, 2, 3, 0, 1, 6, 8, 9]
    assert hap2_code == [12, 13, 7, 6, 15, 14, 7, 11, 10]

