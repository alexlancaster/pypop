*************************
Interpreting PyPop output
*************************

As mentioned in :ref:`guide-usage-intro-run-details`, The XML file
is the primary output created by PyPop and contains the complete set of
results. The text output, generated from the XML file via XSLT, contains
a human-readable summary of the XML results. Below we discuss the output
contained in this text file.

.. warning::

   The text output we discuss below is strictly intended for
   consumption by an end-user, or incorporation into a paper. You
   should never extract information from this text file output to
   perform any downstream analyses (e.g. don't take the values in the
   output and paste them into another program).  This is because the
   results are rounded for space, and you may lose a lot of precision
   if you use any floating-point output in further analyses.

   You should use the :ref:`TSV outputs <guide-usage-popmeta>` for
   maximum precision (which, in turn, are derived from the raw XML
   output) for such analyses.


.. _instructions-pop-summary:

Population summary
==================

A ``Population Summary`` is generated for each dataset analyzed. This
summary provides basic demographic information and summarizes
information about the sample size.

Sample output:

.. code-block:: text

   Population Summary
   ==================
   Population Name: UchiTelle
          Lab code: USAFEL
     Typing method: 12th Workshop SSOP
         Ethnicity: Telle
         Continent: NW Asia
   Collection site: Targen Village
          Latitude: 41 deg 12 min N
         Longitude: 94 deg 7 min E

   Population Totals
   _________________
   Sample Size (n): 47
   Allele Count (2n): 94
   Total Loci in file: 9
   Total Loci with data: 8

.. _instructions-locus-info:

Single locus analyses
=====================

.. _instructions-allelecounts:

Basic allele count information
------------------------------

Information relevant to individual loci is reported. Sample size and
allele counts will differ among loci if not all individuals were typed
at each locus. Untyped individuals are those for which one or two
alleles were not reported. The alleles are listed in descending
frequency (and count) in the left hand column, and are sorted
numerically in the right column. The number of distinct alleles ``k`` is
reported.

.. code-block:: text

   I. Single Locus Analyses
   ========================

   1. Locus: A
   ___________

   1.1. Allele Counts [A]
   ----------------------
   Untyped individuals: 2
   Sample Size (n): 45
   Allele Count (2n): 90
   Distinct alleles (k): 10

   Counts ordered by frequency    | Counts ordered by name        
   Name      Frequency (Count)    | Name      Frequency (Count)   
   02:01      0.21111   19        | 01:01      0.13333   12        
   03:01      0.15556   14        | 02:01      0.21111   19        
   01:01      0.13333   12        | 02:10      0.10000   9         
   25:01      0.12222   11        | 02:18      0.10000   9         
   02:10      0.10000   9         | 03:01      0.15556   14        
   02:18      0.10000   9         | 25:01      0.12222   11        
   32:04      0.08889   8         | 32:04      0.08889   8         
   69:01      0.04444   4         | 68:14      0.03333   3         
   68:14      0.03333   3         | 69:01      0.04444   4         
   74:03      0.01111   1         | 74:03      0.01111   1         
   Total     1.00000   90         | Total     1.00000   90        

In the cases where there is no information for a locus, a message is
displayed indicating lack of data.

Sample output:

.. code-block:: text

   4. Locus: DRA
   _____________
    No data for this locus!

.. _instructions-hardyweinberg:

Chi-square test for deviation from Hardy-Weinberg proportions (HWP).
--------------------------------------------------------------------

For each locus, the observed genotype counts are compared to those
expected under Hardy Weinberg proportions (HWP). A triangular matrix
reports observed and expected genotype counts. If the matrix is more
than 80 characters, the output is split into different sections. Each
cell contains the observed and expected number for a given genotype in
the format ``observed/expected``.

.. code-block:: text

   6.2. HardyWeinberg [DQA1]
   -------------------------
   Table of genotypes, format of each cell is: observed/expected.

   02:01 8/5.1
   03:01 4/4.0  1/0.8
   04:01 3/6.9  1/2.7  6/2.3
   05:01 8/9.9  5/3.8  5/6.7  6/4.8
         02:01  03:01  04:01  05:01
                                [Cols: 1 to 4]
        

The values in this matrix are used to test hypotheses of deviation from
HWP. The output also includes the chi-square statistic, the number of
degrees of freedom and associated :math:`p`-value for a number of classes of
genotypes and is summarized in the following table:

.. code-block:: text

                         Observed    Expected  Chi-square   DoF   p-value   
   ------------------------------------------------------------------------------
               Common         N/A         N/A        4.65     1  0.0310*   
   ------------------------------------------------------------------------------
     Lumped genotypes         N/A         N/A        1.17     1  0.2797  
   ------------------------------------------------------------------------------
      Common + lumped         N/A         N/A        5.82     1  0.0158* 
   ------------------------------------------------------------------------------
      All homozygotes          21       13.01        4.91     1  0.0268* 
   ------------------------------------------------------------------------------
    All heterozygotes          26       33.99        1.88     1  0.1706  
   ------------------------------------------------------------------------------
   Common heterozygotes by allele                                        
                 02:01         15       20.78        1.61        0.2050      
                 03:01         10       10.47        0.02        0.8850      
                 04:01          9       16.31        3.28        0.0703      
                 05:01         18       20.43        0.29        0.5915      

   ------------------------------------------------------------------------------
   Common genotypes                                                      
            02:01+02:01         8        5.11        1.63        0.2014      
            02:01+04:01         3        6.93        2.23        0.1358      
            02:01+05:01         8        9.89        0.36        0.5472      
            04:01+05:01         5        6.70        0.43        0.5109      
                  Total        24       28.63
   ------------------------------------------------------------------------------
        

-  **Common.**

   The result for goodness of fit to HWP using only the genotypes with
   at least ``lumpBelow`` expected counts (the common genotypes) (in the
   output shown throughout this example ``lumpBelow`` is equal to 5).

   If the dataset contains no genotypes with expected counts equal or
   greater than ``lumpBelow``, then there are no common genotypes and
   the following message is reported:

   .. code-block:: text

         No common genotypes; chi-square cannot be calculated
         

   The analysis of common genotypes may lead to a situtation where there
   are fewer classes (genotypes) than allele frequencies to estimate.
   This means that the analysis cannot be performed (degrees of freedom
   < 1). In such a case the following message is reported, explaining
   why the analysis could not be performed:

   .. code-block:: text

         Too many parameters for chi-square test.
         

   To obviate this as much as possible, only alleles which occur in
   common genotypes are used in the calculation of degrees of freedom.

-  **Lumped genotypes.**

   The result for goodness of fit to HWP for the pooled set of genotypes
   that individually have less than ``lumpBelow`` expected counts.

   The pooling procedure is designed to avoid carrying out the
   chi-square goodness of fit test in cases where there are low expected
   counts, which could lead to spurious rejection of HWP. However, in
   certain cases it may not be possible to carry out this pooling
   approach. The interpretation of results based on lumped genotypes
   will depend on the particular genotypes that are combined in this
   class.

   If the sum of expected counts in the lumped class does not add up to
   ``lumpBelow``, then the test for the lumped genotypes cannot be
   calculated and the following message is reported:

   .. code-block:: text

         The total number of expected genotypes is less than 5
           

   This may by remedied by combining rare alleles and recalculating
   overall chi-square value and degrees of freedom. (This would require
   appropriate manipulation of the data set by hand and is not a feature
   of PyPop).

-  **Common + lumped.**

   The result for goodness of fit to HWP for both the common and the
   lumped genotypes.

-  **All homozygotes.**

   The result for goodness of fit to HWP for the pooled set of
   homozygous genotypes.

-  **All heterozygotes.**

   The result for goodness of fit to HWP for the pooled set of
   heterozygous genotypes.

-  **Common heterozygotes.**

   The common heterozygotes by allele section summarizes the observed
   and expected number of counts of all heterozygotes carrying a
   specific allele with expected value GE ``lumpBelow``.

-  **Common genotypes.**

   The common genotypes by genotype section lists observed, expected,
   chi-square and :math:`p`-values for all observed genotypes with expected
   values GE ``lumpBelow``.

.. _instructions-hardyweinberg-exact:

Exact test for deviation from HWP
---------------------------------

If enabled in the configuration file, the exact test for deviations
from HWP will be output. The exact test uses the method of
:cite:t:`guo_performing_1992`. The :math:`p`-value provided describes
how probable the observed set of genotypes is, with respect to a large
sample of other genotypic configurations (conditioned on the same
allele frequencies and :math:`2n`).  :math:`p`-values lower than 0.05
can be interpreted as evidence that the sample does not fit HWP. In
addition, those individual genotypes deviating significantly
(:math:`p< 0.05`) from expected HWP as computed with the Chen and
"diff" measures are reported.

There are two implementations for this test, the first using the gthwe
implementation originally due to Guo & Thompson, but modified by John
Chen, the second being Arlequin's
:cite:p:`schneider_arlequin_2000,excoffier_arlequin_2010`
implementation.

.. code-block:: text

   6.3. Guo and Thompson HardyWeinberg output [DQA1]
   -------------------------------------------------
   Total steps in MCMC: 1000000
   Dememorization steps: 2000
   Number of Markov chain samples: 1000
   Markov chain sample size: 1000
   Std. error: 0.0009431 
   p-value (overall): 0.0537

.. code-block:: text

   6.4. Guo and Thompson HardyWeinberg output(Arlequin's implementation) [DQA1]
   ----------------------------------------------------------------------------- 
   Observed heterozygosity: 0.553190
   Expected heterozygosity: 0.763900
   Std. deviation: 0.000630
   Dememorization steps: 100172
   p-value: 0.0518

Note that in the Arlequin implementation, the output is slightly
different, and the only directly comparable value between the two
implementation is the :math:`p`-value. These :math:`p`-values may be slightly
different, but should agree to within one significant figure.

.. _instructions-homozygosity:

The Ewens-Watterson homozygosity test of neutrality
---------------------------------------------------

For each locus, we implement the Ewens-Watterson homozygosity test of
neutrality :cite:p:`ewens_sampling_1972,watterson_homozygosity_1978`. We use the term
*observed homozygosity* to denote the homozygosity statistic
(:math:`F`), computed as the sum of the squared allele
frequencies. This value is compared to the *expected homozygosity*
which is computed by simulation under neutrality/equilibrium
expectations, for the same sample size (:math:`2n`) and number of
unique alleles (:math:`k`). Note that the homozygosity ``F``
statistic, :math:`F=\sum_{i=1}^{k}p_{i}^{2}`, is often referred to as
the *expected homozygosity* (with *expectation* referring to HWP) to
distinguish it from the observed proportion of homozygotes. We avoid
referring to the observed :math:`F` statistic as the "*observed
expected homozygosity*" (to simplify and hopefully avoid confusion)
since the homozygosity test of neutrality is concerned with
comparisons of observed results to expectations under neutrality. Both
the *observed* statistic (based on the actual data) and *expected*
statistic (based on simulations under neutrality) used in this test
are computed as the sum of the squared allele frequencies.

The *normalized deviate of the homozygosity* (:math:`F_{nd}`) is the
difference between the *observed homozygosity* and *expected
homozygosity*, divided by the square root of the variance of the
expected homozygosity (also obtained by simulations;
:cite:p:`salamon_evolution_1999`).  Significant negative normalized
deviates imply *observed homozygosity* values lower than *expected
homozygosity*, in the direction of balancing selection. Significant
positive values are in the direction of directional selection.

The :math:`p`-value in the last row of the output is the probability of
obtaining a homozygosity :math:`F` statistic under neutral evolution that is
less than or equal to the observed :math:`F` statistic. It is computed based
on the null distribution of homozygosity :math:`F` values simulated under
neutrality/equilibrium conditions for the same sample size (:math:`2n`) and
number of unique alleles (:math:`k`). For a one-tailed test of the null
hypothesis of neutrality against the alternative of balancing selection,
:math:`p`-values less than 0.05 are considered significant at the 0.05
level. For a two-tailed test against the alternative of either balancing
or directional selection, :math:`p`-values less than 0.025 or greater than
0.975 can be considered significant at the 0.05 level.

The standard implementation of the test uses a Monte-Carlo
implementation of the exact test written by Slatkin
:cite:yearpar:`slatkin_exact_1994,slatkin_correction_1996`. A Markov-chain
Monte Carlo method is used to obtain the null distribution of the
homozygosity statistic under neutrality. The reported :math:`p`-values
are one-tailed (against the alternative of balancing selection), but
can be interpreted for a two-tailed test by considering either extreme
of the distribution (< 0.025 or > 0.975) at the 0.05 level.

.. code-block:: text

   1.6. Slatkin's implementation of EW homozygosity test of neutrality [A]
   -----------------------------------------------------------------------
   Observed F: 0.1326, Expected F: 0.2654, Variance in F: 0.0083
   Normalized deviate of F (Fnd): -1.4603, p-value of F: 0.0029**

.. warning::

   The version of this test based on tables of simulated percentiles of
   the Ewens-Watterson statistics is now disabled by default and its use
   is deprecated in preference to the Slatkin exact test described
   above, however some older PyPop runs may include output, so it is
   documented here for completeness. This version differs from the
   Monte-Carlo Markov Chain version described above in that the data is
   simulated under neutrality to obtain the required statistics.

   .. code-block:: text

      1.4. Ewens-Watterson homozygosity test of neutrality [A]
      --------------------------------------------------------
      Observed F: 0.1326, Expected F: 0.2651, Normalized deviate (Fnd): -1.4506
      p-value range: 0.0000 < p <= 0.0100 *

.. _instructions-haplo:

Multi-locus analyses
====================

Haplotype frequencies are estimated using the iterative
Expectation-Maximization (EM) algorithm
:cite:p:`dempster_maximum_1977,excoffier_maximum-likelihood_1995`. Multiple
starting conditions are used to minimize the possibility of local
maxima being reached by the EM iterations. The haplotype frequencies
reported are those that correspond to the highest logarithm of the
sample likelihood found over the different starting conditions and are
labeled as the maximum likelihood estimates (MLE).

The output provides the names of loci for which haplotype frequencies
were estimated, the number of individual genotypes in the dataset
(``before-filtering``), the number of genotypes that have data for all
loci for which haplotype estimation will be performed
(``after-filtering``), the number of unique phenotypes (unphased
genotypes), the number of unique phased genotypes, the total number of
possible haplotypes that are compatible with the genotypic data (many of
these will have an estimated frequency of zero), and the log-likelihood
of the observed genotypes under the assumption of linkage equilibrium.

.. _instructions-pairwise-ld:

All pairwise LD
---------------

A series of linkage disequilibrium (LD) measures are provided for each
pair of loci, as shown in the sample output below.

.. code-block:: text

   II. Multi-locus Analyses
   ========================

   Haplotype/ linkage disequlibrium (LD) statistics
   ________________________________________________

   Pairwise LD estimates
   ---------------------
   Locus pair        D      D'      Wn  ln(L_1) ln(L_0)      S  ALD_1_2  ALD_2_1
   A:C         0.01465 0.49229 0.39472  -289.09 -326.81  75.44  0.41435  0.37525
   A:B         0.01491 0.50895 0.40145  -293.47 -330.84  74.73  0.40726  0.39512
   A:DRB1      0.01299 0.42896 0.38416  -282.00 -309.16  54.32  0.32934  0.38370
   A:DQA1      0.01219 0.33413 0.36466  -269.57 -286.08  33.02  0.25803  0.34897
   A:DQB1      0.01356 0.39266 0.37495  -275.58 -297.62  44.07  0.29931  0.37489
   A:DPA1      0.01681 0.32397 0.36666  -219.78 -226.97  14.38  0.19446  0.35360
   A:DPB1      0.01362 0.42240 0.40404  -237.85 -262.06  48.42  0.33848  0.41739
   C:B         0.04125 0.88739 0.85752  -210.37 -342.68 264.63  0.84781  0.86104
   C:DRB1      0.01698 0.48046 0.47513  -280.34 -317.66  74.62  0.32308  0.47691
   C:DQA1      0.02072 0.47797 0.49368  -263.23 -293.74  61.01  0.31386  0.50338
   C:DQB1      0.01766 0.45793 0.49879  -269.55 -305.28  71.46  0.30479  0.50122
   C:DPA1      0.02039 0.41030 0.46438  -224.72 -236.52  23.61  0.21172  0.46433
   C:DPB1      0.01898 0.46453 0.37002  -242.45 -268.46  52.01  0.33462  0.45327
   B:DRB1      0.01723 0.50254 0.41712  -286.79 -320.50  67.42  0.32654  0.43913
   B:DQA1      0.01845 0.44225 0.43582  -271.36 -296.59  50.45  0.28877  0.44993
   B:DQB1      0.01958 0.49040 0.43654  -277.30 -308.13  61.65  0.31328  0.45679
   B:DPA1      0.01875 0.37441 0.40117  -229.76 -239.16  18.80  0.20689  0.40443
   B:DPB1      0.01898 0.46082 0.38001  -247.84 -272.77  49.86  0.32227  0.45680
   DRB1:DQA1   0.06138 0.92556 0.92465  -164.06 -271.56 214.99  0.82051  0.93006
   DRB1:DQB1   0.06058 1.00000 1.00000  -147.74 -283.10 270.72  0.93302  1.00000

   ...

For each locus pair, we report three measures of overall linkage
disequilibrium. :math:`D'`  :cite:p:`hedrick_gametic_1987` weights the contribution to
LD of specific allele pairs by the product of their allele frequencies
(``D'`` in the output); :math:`W_n`  :cite:p:`cramer_mathematical_1946` is a re-expression
of the chi-square statistic for deviations between observed and
expected haplotype frequencies (``W_n`` in the
output)). :math:`W_{A/B}` and :math:`W_{B/A}` (``ALD_1_2`` and
``ALD_2_1``, respectively in the output) are extensions of :math:`W_n`
that account for asymmetry when the number of alleles differs at two
loci :cite:p:`thomson_conditional_2014`. Below we describe the measures, each of
which is normalized to lie between zero and one.

:math:`D'` 
   Overall LD, summing contributions (:math:`D'_{ij}=D_{ij} /D_{max}`) of all the haplotypes in a
   multi-allelic two-locus system, can be measured using Hedrick's
   :math:`D'` statistic, using the products of allele frequencies at the
   loci, :math:`p_i` and :math:`q_j`, as weights.

.. math::
   
   {D}' = \sum_{i=1}^{I} {\sum_{j=1}^{J} {p_i } } q_j \left|{{D}'_{ij} } \right|

:math:`W_n`
   Also known as Cramer's V Statistic :cite:p:`cramer_mathematical_1946`, :math:`W_n`, is a
   second overall measure of LD between two loci. It is a re-expression
   of the Chi-square statistic, :math:`X^2_{LD}`, normalized
   to be between zero and one. When there are only two alleles per
   locus, :math:`W_n` is equivalent to the correlation coefficient
   between the two loci, defined as:

.. math::

   W_n = \left[ {\frac{\sum_{i=1}^{I} {\sum_{j=1}^{J}{D_{ij}^2 / p_i } q_j } }{\min (I - 1,J - 1)}} \right]^{\frac{1}{2}} = \left[ {\frac{X_{LD}^2 / 2N}{\min (I - 1,J - 1)}}\right]^{\frac{1}{2}}


two alleles case
   When there are only two alleles per locus, :math:`W_n` is equivalent
   to the correlation coefficient between the two loci, defined as
   :math:`r =\sqrt {D_{11} / p_1 p_2 q_1 q_2 }`.

:math:`W_{A/B}` and :math:`W_{B/A}`
   When there are different numbers of alleles at the two loci,
   the direct correlation property for the :math:`r` correlation 
   measure is not retained by :math:`W_n`, its multi-allelic extension. 
   The complementary pair of conditional asymmetric LD (ALD) measures, 
   :math:`W_{A/B}` and :math:`W_{B/A}`, were developed to extend the :math:`W_n` measure. 
   :math:`W_{A/B}` is (inversely) related to the 
   degree of variation of A locus alleles on haplotypes conditioned 
   on B locus alleles. If there is no variation of A locus alleles 
   on haplotypes conditioned on B locus alleles, then :math:`W_{A/B} = 1`
   :math:`W_{A/B} = W_{B/A} = W_n` when there is symmetry in the data and 
   thus for bi-allelic SNPs.

.. math::

   W_{A/B} = \left[ {\frac{\sum_{i=1}^{I} {\sum_{j=1}^{J}{D_{ij}^2 / q_j } } }{ 1 - F_A }} \right]^{\frac{1}{2}} 

.. math::

   W_{B/A} = \left[ {\frac{\sum_{i=1}^{I} {\sum_{j=1}^{J}{D_{ij}^2 / p_i } } }{ 1 - F_B }} \right]^{\frac{1}{2}} 
   
In addition to the LD measures described above, for each locus pair,
we describe three additional measures related to the log-likelihood
that are displayed in the output above:

:math:`\ln(L_1)`
   the log-likelihood of obtaining the observed data given the inferred
   haplotype frequencies (``ln(L_1)`` in the output)

:math:`\ln(L_0)`   
   the log-likelihood of the data under the null hypothesis of linkage
   equilibrium (``ln(L_0)`` in the output)

:math:`S`
   the statistic (``S`` in the output) is defined as twice the
   difference between these likelihoods. :math:`S` has an asymptotic
   chi-square distribution, but the null distribution of :math:`S` is
   better approximated using a randomization procedure. If a
   permutation test is requested (by setting the option
   ``allPairwiseLDWithPermu`` to a a number greater than zero in the
   :ref:`.ini file <config-allPairwiseLDWithPermu>`), the empirical
   distribution of :math:`S` is generated by shuffling genotypes among
   individuals, separately for each locus, thus creating linkage
   equilibrium. The additional column ``# permu`` that will be
   generated (not shown in the example output above) will indicate how
   many permutations were carried out. The :math:`p`-value (also not
   shown) will be the fraction of permutations that results in values of
   `S` greater or equal to that observed. A :math:`p < 0.05` is
   indicative of overall significant LD.

Individual LD coefficients, :math:`D_{ij}`, are stored in the XML
output file, but are not printed in the default text output. They can
be accessed in the summary text files created by the ``popmeta``
script (see :ref:`guide-usage-intro-run-details`).

.. _instructions-haplotype-freqs:

Haplotype frequency estimation
------------------------------

.. code-block:: text

   Haplotype frequency est. for loci: A:B:DRB1
   -------------------------------------------
   Number of individuals: 47 (before-filtering)
   Number of individuals: 45 (after-filtering)
   Unique phenotypes: 45
   Unique genotypes: 113
   Number of haplotypes: 188
   Loglikelihood under linkage equilibrium [ln(L_0)]: -472.700542
   Loglikelihood obtained via the EM algorithm [ln(L_1)]: -340.676530
   Number of iterations before convergence: 67

The estimated haplotype frequencies are sorted alphanumerically by
haplotype name (left side), or in decreasing frequency (right side).
Only haplotypes estimated at a frequency of 0.00001 or larger are
reported. The first column gives the allele names in each of the three
loci, the second column provides the maximum likelihood estimate for
their frequencies, (``frequency``), and the third column gives the
corresponding approximate number of haplotypes (``# copies``).

.. code-block:: text

   Haplotypes sorted by name             | Haplotypes sorted by frequency     
   haplotype         frequency # copies  | haplotype         frequency # copies  
   01:01~13:01~04:02   0.02222   2.0     | 02:01~14:01~04:02   0.03335   3.0       
   01:01~13:01~11:01   0.01111   1.0     | 32:04~14:01~08:02   0.03333   3.0       
   01:01~14:01~09:01   0.01111   1.0     | 03:01~14:01~04:07   0.03333   3.0       
   01:01~15:20~08:02   0.01111   1.0     | 03:01~13:01~04:02   0.03333   3.0       
   01:01~18:01~04:07   0.01111   1.0     | 02:01~14:01~11:01   0.03332   3.0       
   01:01~39:02~04:04   0.01111   1.0     | 03:01~15:20~08:02   0.02222   2.0       
   01:01~39:02~16:02   0.01111   1.0     | 01:01~40:05~08:02   0.02222   2.0       
   01:01~40:05~08:02   0.02222   2.0     | 03:01~39:02~04:02   0.02222   2.0       
   01:01~81:01~08:02   0.01111   1.0     | 02:01~13:01~16:02   0.02222   2.0       
   01:01~81:01~16:02   0.01111   1.0     | 02:18~14:01~04:04   0.02222   2.0       
   02:01~13:01~16:02   0.02222   2.0     | 02:10~51:01~16:02   0.02222   2.0       
   02:01~14:01~04:02   0.03335   3.0     | 02:18~14:01~16:02   0.02222   2.0       
   02:01~14:01~04:04   0.01111   1.0     | 01:01~13:01~04:02   0.02222   2.0       
   02:01~14:01~04:07   0.02222   2.0     | 25:01~40:05~08:02   0.02222   2.0       
   02:01~14:01~08:02   0.01111   1.0     | 25:01~13:01~08:02   0.02222   2.0       

   ...
