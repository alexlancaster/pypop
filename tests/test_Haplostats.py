import base
import unittest
from PyPop import _Haplostats
from pytest import approx
from numpy import array
from numpy.testing import assert_array_almost_equal
from operator import add
from PyPop.Haplo import _compute_LD

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

    sum_hap_codes = list(map(add, hap1_code, hap2_code))
#   print ("sum_hap_codes: ", sum_hap_codes)

    assert status2 == 0
    assert hap_prob == [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    assert u_hap == [1, 2, 1, 7, 2, 1, 2, 3, 3, 6, 3, 7, 4, 1, 4, 3, 5, 4, 5, 5, 6, 4, 6, 5, 6, 6, 6, 7, 7, 2, 7, 7]
    assert u_hap_code == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    assert subj_id == [0, 0, 1, 1, 2, 2, 3, 4, 4]
    assert post == [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5]
#NB: assert sum_hap_codes for comparison with R output
#    due to diff elementwise listing from R (probably from factor coersion)
#   assert hap1_code == [5, 4, 2, 3, 0, 1, 6, 8, 9]
#   assert hap2_code == [12, 13, 7, 6, 15, 14, 7, 11, 10]
    assert sum_hap_codes == [17, 17, 9, 9, 15, 15, 13, 19, 19] 

def test_Haplostats_Simple3():
    n_loci = 3
    n_subject = 50
    weight = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    n_alleles = [12, 10, 20]
    max_haps = 320
    max_iter = 5000
    loci_insert_order =[0, 1, 2]
    min_prior = 0.0
    min_posterior = 0.000000001
    tol = 0.00001
    insert_batch_size = 3
    random_start = 0
    iseed1 = 18717; iseed2= 16090; iseed3=14502
    verbose = 0
    geno_vec = [2,1,2,1,2,1,10,9,10,6,2,10,11,10,6,6,2,10,10,2,2,1,6,5,12,6,11,12,2,2,2,11,6,1,2,11,6,11,2,11,10,1,1,3,2,1,1,6,10,8,3,10,11,2,5,1,12,2,11,6,3,3,11,3,11,10,11,2,5,12,7,1,1,5,3,12,2,10,1,10,4,3,10,10,2,3,10,2,2,1,10,4,1,10,3,10,1,1,1,2,4,2,1,5,6,3,2,9,2,1,4,2,9,2,1,1,5,2,2,4,2,3,1,4,2,1,8,2,3,2,5,4,1,3,8,4,2,4,4,3,2,5,3,2,4,2,3,1,2,4,8,5,9,5,8,5,9,8,2,1,4,4,9,4,9,9,9,10,6,9,4,3,3,6,4,9,9,9,8,8,10,9,2,6,8,9,7,9,4,9,2,5,3,4,6,5,3,3,3,10,18,1,5,1,12,2,1,9,1,5,9,13,9,1,12,12,13,1,1,16,9,2,2,6,12,1,18,14,2,1,1,8,4,2,6,16,1,9,9,9,1,3,2,9,18,9,2,2,2,9,17,9,18,9,13,9,19,9,6,6,16,5,18,16,1,6,17,19,4,17,5,9,16,16,1,6,7,6,5,11,15,16,6,6,7,13,7,9,9,20,9,14,2,10,16,4,2,15,4,13]

    ret_val = call_Haplostats(n_loci, n_subject, weight, n_alleles,
                              max_haps, max_iter, loci_insert_order,
                              min_prior, min_posterior, tol, insert_batch_size,
                              random_start, iseed1, iseed2, iseed3, verbose, geno_vec)
    status1, converge, S_lnlike, S_n_u_hap, n_hap_pairs, status2, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code = ret_val

#   import numpy
#   print ("u_hap: " u_hap)
#   print ("hap_prob  u_hap_code u_hap(needs to be split for printing)")
#   print (numpy.c_[hap_prob,u_hap_code])
#   print ("subj_id  hap1_code  hap2_code")
#   print (numpy.c_[subj_id,hap1_code,hap2_code])

    sum_hap_codes = list(map(add, hap1_code, hap2_code))
#   print ("sum_hap_codes: ", sum_hap_codes)
    assert status1 == 0
    assert converge == 1
    assert S_lnlike == -337.8527372502544
    assert S_n_u_hap == 68
    assert n_hap_pairs == 57

    assert status2 == 0
    assert_array_almost_equal(hap_prob,[0.11,0.01,0.009999999,0.005,0.04,0.005,0.01,0.06,0.02,0.02,0.01,0.0025,0.0025,0.01,0.01,0.01,0.02,0.01,0.0025,0.0025,0.01,0.01,0.01,0.01,0.01,0.05,0.01,0.005,0.005,0.01,0.005,0.005,8.567844e-11,0.01,0.005,0.0025,0.0025,0.005,0.0025,0.0025,0.01,0.04,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.09,0.03,0.01,0.01,0.02,0.01,0.01,0.01,0.01,0.01,0.03,0.02,0.03,1.326529e-09,0.01,0.01,0.01,0.01,0.01])
    assert u_hap == [1,3,2,1,3,9,1,3,20,1,5,3,1,5,9,1,5,14,2,1,5,2,4,9,2,4,17,2,5,1,2,5,17,2,6,12,2,6,13,2,6,18,2,8,5,2,8,6,2,8,7,2,8,11,2,8,12,2,8,13,2,9,9,2,10,19,3,4,10,3,4,12,3,4,13,3,4,16,3,8,18,4,5,3,4,5,14,4,10,15,5,4,6,5,4,16,5,6,1,5,6,4,5,6,6,5,6,12,5,6,13,5,6,16,5,8,12,5,8,13,6,1,5,6,1,6,6,1,12,6,1,15,6,1,16,6,7,7,7,2,5,8,10,13,9,8,9,10,2,1,10,2,4,10,2,5,10,2,6,10,2,9,10,6,6,10,9,12,11,2,6,11,9,1,11,9,8,11,9,9,11,9,13,11,9,18,11,9,20,12,2,1,12,9,1,12,9,14,12,9,16,12,9,19]
    assert u_hap_code == [7,11,14,17,19,20,27,37,40,42,46,47,48,50,53,54,55,57,58,59,64,73,85,86,87,88,94,99,100,103,106,107,108,109,110,111,112,113,114,115,119,120,121,122,123,132,136,143,144,149,151,152,153,155,177,184,194,205,208,209,211,214,215,218,227,229,230,232]
    assert subj_id == [0,1,2,3,4,4,4,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,18,19,20,21,22,23,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,39,40,41,41,42,43,44,45,46,47,48,49]
    assert_array_almost_equal(post, [1.0,1.0,1.0,1.0,0.25,0.25,0.25,0.25,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,8.567844e-09,1.0,1.0,1.0,1.0,0.5,0.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.9999999,1.326529e-07,1.0,0.5,0.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])
    assert sum_hap_codes == [134, 168, 241, 61, 162, 170, 162, 170, 26, 381, 208, 343, 239, 125, 239, 423, 237, 326, 304, 257, 222, 258, 259, 270, 173, 18, 130, 219, 217, 304, 347, 269, 382, 60, 206, 145, 296, 271, 184, 109, 299, 281, 246, 74, 223, 226, 304, 117, 119, 14, 240, 138, 170, 14, 129, 158, 180]

def test_Haplostats_UchiTelleClassI():
    n_loci = 3
    n_subject = 45
    weight = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    n_alleles = [10, 14, 12]
    max_haps = 236
    max_iter = 5000
    loci_insert_order =[0, 1, 2]
    min_prior = 0.0
    min_posterior = 0.000000001
    tol = 0.00001
    insert_batch_size = 3
    random_start = 0
    iseed1 = 18717; iseed2= 16090; iseed3=14502
    verbose = 0
    geno_vec = [1,3,1,5,3,6,5,8,2,7,9,3,1,1,3,1,1,5,2,6,4,2,7,4,6,1,1,3,1,7,2,2,1,3,6,4,1,10,5,2,6,7,2,6,9,2,6,4,2,7,7,7,2,2,1,3,6,4,2,6,4,4,2,2,5,8,2,5,4,6,5,3,6,5,8,2,7,9,3,9,5,5,2,6,2,6,5,2,6,4,2,7,8,11,12,11,2,1,9,2,1,9,2,1,11,2,1,9,2,1,2,10,2,1,6,6,9,2,1,6,2,7,13,6,14,6,5,6,7,3,2,6,2,1,1,6,1,9,2,1,6,2,7,13,6,1,9,2,1,2,7,1,11,2,1,2,2,1,2,2,6,11,2,1,9,2,1,1,1,6,6,4,2,14,2,6,9,2,1,2,2,3,8,10,12,10,2,1,4,2,1,4,2,1,10,2,1,4,9,3,5,2,1,4,9,9,4,2,1,9,2,3,7,9,11,9,11,9,3,5,2,9,2,1,1,9,1,4,2,1,9,2,3,7,6,1,4,2,1,2,3,1,10,2,1,2,2,1,2,2,9,10,2,1,4,2,2,3,8,10,2,6,2,5,2,9,4,2,1,2]

    ret_val = call_Haplostats(n_loci, n_subject, weight, n_alleles,
                              max_haps, max_iter, loci_insert_order,
                              min_prior, min_posterior, tol, insert_batch_size,
                              random_start, iseed1, iseed2, iseed3, verbose, geno_vec)
    status1, converge, S_lnlike, S_n_u_hap, n_hap_pairs, status2, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code = ret_val

    sum_hap_codes = list(map(add, hap1_code, hap2_code))
#   print ("sum_hap_codes: ", sum_hap_codes)
    assert status1 == 0
    assert converge == 1
    assert S_lnlike == -311.6829460557762
    assert S_n_u_hap == 70
    assert n_hap_pairs == 54

    assert status2 == 0


def test_Haplostats_PyPopStringMatrix():
    """
    This is the same numerical example as test_Haplostats_Simple()
    except we are setting up via PyPop StringMatrix, and letting the class
    handle all the translation into the low-level variables for the wrapper
    """

    from PyPop.Utils import StringMatrix
    from PyPop.Haplo import Haplostats
    import numpy
    import numpy.testing

    control = {'max_iter': 5000,
               'min_posterior': 0.000000001,
               'tol': 0.00001,
               'insert_batch_size': 2,
               'random_start': 0,
               'verbose': 0,
               'max_haps_limit': 10000 }

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

    haplo = Haplostats(geno)
    converge, lnlike, n_u_hap, n_hap_pairs, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code, haplotype, dprime, Wn, ALD_1_2, ALD_2_1 = \
              haplo.estHaplotypes(weight=None, control=control, numInitCond=1, testMode=True)

    assert converge == 1
    assert lnlike == -20.42316124449607
    assert n_u_hap == 16
    assert n_hap_pairs == 9

    assert hap_prob == [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    assert u_hap == [1, 2, 1, 7, 2, 1, 2, 3, 3, 6, 3, 7, 4, 1, 4, 3, 5, 4, 5, 5, 6, 4, 6, 5, 6, 6, 6, 7, 7, 2, 7, 7]
    assert u_hap_code == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    assert subj_id == [1, 1, 2, 2, 3, 3, 4, 5, 5]
    assert post == [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5]
    # FIXME: disabled for the moment, apparently platform-dependent (see #28)
    # assert hap1_code == [6, 5, 3, 4, 1, 2, 7, 9, 10]
    # assert hap2_code == [13, 14, 8, 7, 16, 15, 8, 12, 11]
    numpy.testing.assert_array_equal(haplotype, numpy.array([['1','27'], ['1','62'], ['2','7'], ['2','44'], ['4','61'], ['4','62'], ['7','7'], ['7','44'], ['8','51'], ['8','55'], ['11','51'], ['11','55'], ['11','61'], ['11','62'], ['13','27'], ['13','62']]))

    # FIXME: check!
    assert dprime == approx(0.791865079365)
    assert Wn == approx(0.586301969978)
    assert ALD_1_2 == approx(0.624695047554)
    assert ALD_2_1 == approx(0.587569651393)

    # try again with same input data, but running with more iterations, to test whether the loop is behaving deterministically
    # this gives a different loglikelihood and completely different set of haplotypes
    converge, lnlike, n_u_hap, n_hap_pairs, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code, haplotype, dprime, Wn, ALD_1_2, ALD_2_1 = \
              haplo.estHaplotypes(weight=None, control=control, numInitCond=10, testMode=True)

    assert converge == 1
    assert lnlike == -18.173826527916734
    assert n_u_hap == 10
    assert n_hap_pairs == 6
    assert_array_almost_equal(hap_prob, [0.1, 5.862016163766863e-07, 0.09999941379838362, 0.1, 0.19999941379838362, 0.10000058620161638, 0.1, 0.1, 0.1, 0.1])
    assert u_hap == [1, 2, 2, 1, 2, 3, 3, 6, 4, 1, 4, 3, 5, 5, 6, 4, 6, 7, 7, 7]
    assert u_hap_code == [1, 3, 4, 5, 7, 8, 10, 11, 14, 16]
    assert subj_id == [1, 2, 2, 3, 4, 5]
    assert_array_almost_equal(post, [1.0, 5.862016163766862e-06, 0.9999941379838362, 1.0, 1.0, 1.0])
    numpy.testing.assert_array_equal(haplotype, numpy.array([['1','27'], ['2','7'], ['2','44'], ['4','61'], ['7','7'], ['7','44'], ['8','55'], ['11','51'], ['11','62'], ['13','62']]))

    # FIXME: check!
    assert dprime == approx(0.932142124391)
    assert Wn == approx(0.874006628251)
    assert ALD_1_2 == approx(0.86953788372)
    assert ALD_2_1 == approx(0.849835490713)
        
def test_Haplostats_compute_LD_sym():
    """
    Test LD computations in a standalone mode
    FIXME: if used standalone from Haplostats, move to another test module
    """
    haplos = array([['A1', 'B1'], ['A2', 'B1'], ['A1', 'B2'], ['A2', 'B2']],dtype='O')
    freqs = array([0.3, 0.1, 0.1, 0.5]) 
    dprime, wn, ALD_1_2, ALD_2_1 = _compute_LD(haplos, freqs, compute_ALD=True)

    assert dprime == approx(0.58333333333333326)
    assert wn == approx(0.583333333333)
    assert ALD_1_2 == approx(0.583333333333)
    assert ALD_2_1 == approx(0.583333333333)

def test_Haplostats_compute_LD_assym():
    """
    Test LD computations in a standalone mode.
    Note that in this example standard Dprime doesn't match the ALD values
    """
    haplos = array([['A1', 'B1'], ['A2', 'B1'], ['A1', 'B2'], ['A2', 'B2'], ['A1', 'B3'], ['A2', 'B3']],dtype='O')
    freqs = array([0.3, 0.0, 0.0, 0.5, 0.0, 0.2]) 

    dprime, wn, ALD_1_2, ALD_2_1 = _compute_LD(haplos, freqs, compute_ALD=True)

    assert dprime == approx(1.0)
    assert wn == approx(1.0)
    assert ALD_1_2 == approx(1.0)
    assert ALD_2_1 == approx(0.734282307367)
