#!/usr/bin/env python
import os.path, sys

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '..'))

from PyPop.Utils import StringMatrix
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

def haplo_em(geno,
             locus_label=None,
             weight=None, 
             control=None):

    # FIXME: geno data structure needs to be generated from PyPop's StringMatrix class

    # FIXME: hardcode, should be taken from geno
    ncols = 4
    nrows = 5
    
    n_loci = ncols / 2
    n_subject = nrows
    subj_id = range(1, n_subject + 1)
    
    if n_loci < 2:
        print "Must have at least 2 loci for haplotype estimation!"
        exit(-1)

    # set up weight
    if not weight:
        weight = [1.0]*n_subject

    if len(weight) != n_subject:
        print "Length of weight != number of subjects (nrow of geno)"
        exit(-1)

    # Create locus label if not included
    if not locus_label:
        locus_label = ["loc-%d" % i for i in range(n_loci+1)]
    
    if len(locus_label)!= n_loci:
        print "length of locus.label != n_loci"
        exit(-1)

    # FIXME: we hardcode not yet translated, need to use PyPop's StringMatrix here
    # temp.geno <- setupGeno(geno, miss.val=miss.val, locus.label=locus.label)

    # Compute the max number of pairs of haplotypes over all subjects
    # FIXME: hardcode again, not yet translated, again need to use/modify StringMatrix
    # max_pairs = geno.count.pairs(temp_geno)
    # max_haps = 2*sum(max_pairs)
    max_haps = 18

    # FIXME: do we need this?
    if max_haps > control['max_haps_limit']:
        max_haps = control['max_haps_limit']

    # FIXME: hardcode
    geno_vec = [3, 2, 1, 4, 5, 6, 4, 7, 4, 6, 7, 1, 2, 1, 4, 6, 3, 7, 3, 5]

    # FIXME: need to add a method to PyPop's StringMatrix
    # allele.labels <- attr(temp.geno, "unique.alleles")

    # FIXME: hardcode for the time being
    n_alleles = [7, 7]

    # FIXME: not (yet) using a.freq, so don't calculate
    # also too complicated to translate right now
    # for(i in 1:n_loci){
    #  n.alleles[i] <- length(allele.labels[[i]])
    #  j <- (i-1)*2 + 1
    #  p <- table(temp.geno[,c(j, (j+1))], exclude=NA)
    #  p <- p/sum(p)
    #  a.freq[[i]] <- list(p=p)
    # }

    loci_insert_order = range(0, n_loci)

    # FIXME: hardcode
    iseed1 = 18717; iseed2= 16090; iseed3=14502

    converge, lnlike, n_u_hap, n_hap_pairs, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code = \
              haplo_em_fitter(n_loci,
                              n_subject,
                              weight,
                              geno_vec,
                              n_alleles,
                              max_haps,
                              control['max_iter'],
                              loci_insert_order,
                              control['min_posterior'],
                              control['tol'],
                              control['insert_batch_size'],
                              control['random_start'],
                              iseed1,
                              iseed2,
                              iseed3,
                              control['verbose'])

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

#Print columns side-by-side for easier checking
#NB: u_hap is trickier since it has n.loci entries per haplo
    import numpy
    print 'hap_prob  u_hap_code u_hap(needs to be split for printing)'
    print numpy.c_[hap_prob,u_hap_code]
    print 'subj_id  hap1_code  hap2_code'
    print numpy.c_[subj_id,hap1_code,hap2_code]
#   for x1,x2,x3 in zip(hap_prob,u_hap,u_hap_code):
#       print x1 + '\t\t' + x2 + '\t\t' + x3


    # FIXME: add loop here


geno = None
control = {'max_iter': 5000,
           'min_posterior': 0.000000001,
           'tol': 0.00001,
           'insert_batch_size': 2,
           'random_start': 0,
           'verbose': 0,
           'max_haps_limit': 10000 }

# match this haplo.stats example
#
# control = haplo.em.control(n.try=1)
# data(hla.demo)
# attach(hla.demo)
# geno = hla.demo[1:5,c(17,18,21:24)]
# label <-c("DQB","DRB","B")
# keep <- !apply(is.na(geno) | geno==0, 1, any)
# save.em.keep <- haplo.em(geno=geno[keep,], locus.label=label, control=control)

# R geno matrix looks like this:
#
#  DQB.a1 DQB.a2 DRB.a1 DRB.a2 B.a1 B.a2
# 1     31     32      4     11   62   61
# 2     21     62      2      7    7   44
# 3     31     63      1     13   27   62
# 4     21     31      7      7    7   44
# 5     31     42      8     11   51   55

# translating this into a PyPop StringMatrix looks like this:

matrix = StringMatrix(5, ["DQB", "DRB", "B"])
matrix[0, 'DQB'] = ('31', '32')
matrix[1, 'DQB'] = ('21', '62')
matrix[2, 'DQB'] = ('31', '63')
matrix[3, 'DQB'] = ('21', '31')
matrix[4, 'DQB'] = ('31', '42')
matrix[0, 'DRB'] = ('4', '11')
matrix[1, 'DRB'] = ('2', '7')
matrix[2, 'DRB'] = ('1', '13')
matrix[3, 'DRB'] = ('7', '7')
matrix[4, 'DRB'] = ('8', '11')
matrix[0, 'B'] = ('62', '61')
matrix[1, 'B'] = ('7', '44')
matrix[2, 'B'] = ('27', '62')
matrix[3, 'B'] = ('7', '44')
matrix[4, 'B'] = ('51', '55')


# FIXME: goal will be to transform the above data structure into the geno_vec used in haplo_em
# I think the best way to do this is to add a method to the StringMatrix class
# that transforms a StringMatrix into the geno_vec and so with other functionality
# currently in the R haplo.stats

# for example I have added a method to get all the unique alleles
print matrix.getUniqueAlleles("B")

print matrix.convertToInts()["B"]

#haplo_em(geno, locus_label=["B"], weight=None, control=control)
