*************************
Interpreting PyPop output
*************************

As mentioned in :ref:`guide-usage-intro-run-details`, The XML file
is the primary output created by PyPop and contains the complete set of
results. The text output, generated from the XML file via XSLT, contains
a human-readable summary of the XML results. Below we discuss the output
contained in this text file.

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

   Counts ordered by frequency   | Counts ordered by name        
   Name      Frequency (Count)   | Name      Frequency (Count)   
   0201      0.21111   19        | 0101      0.13333   12        
   0301      0.15556   14        | 0201      0.21111   19        
   0101      0.13333   12        | 0210      0.10000   9         
   2501      0.12222   11        | 0218      0.10000   9         
   0210      0.10000   9         | 0301      0.15556   14        
   0218      0.10000   9         | 2501      0.12222   11        
   3204      0.08889   8         | 3204      0.08889   8         
   6901      0.04444   4         | 6814      0.03333   3         
   6814      0.03333   3         | 6901      0.04444   4         
   7403      0.01111   1         | 7403      0.01111   1         
   Total     1.00000   90        | Total     1.00000   90        

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

   0201 8/5.1
   0301 4/4.0 1/0.8
   0401 3/6.9 1/2.7 6/2.3
   0501 8/9.9 5/3.8 5/6.7 6/4.8
         0201  0301  0401  0501
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
                 0201          15       20.78        1.61        0.2050      
                 0301          10       10.47        0.02        0.8850      
                 0401           9       16.31        3.28        0.0703      
                 0501          18       20.43        0.29        0.5915      

   ------------------------------------------------------------------------------
   Common genotypes                                                      
            0201:0201           8        5.11        1.63        0.2014      
            0201:0401           3        6.93        2.23        0.1358      
            0201:0501           8        9.89        0.36        0.5472      
            0401:0501           5        6.70        0.43        0.5109      
                Total          24       28.63
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

If enabled in the configuration file, the exact test for deviations from
HWP will be output. The exact test uses the method of [Guo:Thompson:1992]_.
The :math:`p`-value provided describes how probable the observed set of
genotypes is, with respect to a large sample of other genotypic
configurations (conditioned on the same allele frequencies and :math:`2n`).
:math:`p`-values lower than 0.05 can be interpreted as evidence that the
sample does not fit HWP. In addition, those individual genotypes
deviating significantly (:math:`p< 0.05`) from expected HWP as
computed with the Chen and "diff" measures are reported.

There are two implementations for this test, the first using the gthwe
implementation originally due to Guo & Thompson, but modified by John
Chen, the second being Arlequin's [Schneider:etal:2000]_ implementation.

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
neutrality ([Ewens:1972]_; [Watterson:1978]_). We use the term *observed
homozygosity* to denote the homozygosity statistic (:math:`F`), computed as
the sum of the squared allele frequencies. This value is compared to the
*expected homozygosity* which is computed by simulation under
neutrality/equilibrium expectations, for the same sample size (:math:`2n`)
and number of unique alleles (:math:`k`). Note that the homozygosity ``F``
statistic, , is often referred to as the *expected homozygosity* (with
*expectation* referring to HWP) to distinguish it from the observed
proportion of homozygotes. We avoid referring to the observed :math:`F`
statistic as the "*observed expected homozygosity*" (to simplify and
hopefully avoid confusion) since the homozygosity test of neutrality is
concerned with comparisons of observed results to expectations under
neutrality. Both the *observed* statistic (based on the actual data) and
*expected* statistic (based on simulations under neutrality) used in
this test are computed as the sum of the squared allele frequencies.

The *normalized deviate of the homozygosity* (:math:`F_{nd}`) is the
difference between the *observed homozygosity* and *expected
homozygosity*, divided by the square root of the variance of the
expected homozygosity (also obtained by simulations; [Salamon:etal:1999]_).
Significant negative normalized deviates imply *observed homozygosity*
values lower than *expected homozygosity*, in the direction of balancing
selection. Significant positive values are in the direction of
directional selection.

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
implementation of the exact test written by Slatkin ([Slatkin:1994]_;
[Slatkin:1996]_). A Markov-chain Monte Carlo method is used to obtain the
null distribution of the homozygosity statistic under neutrality. The
reported :math:`p`-values are one-tailed (against the alternative of
balancing selection), but can be interpreted for a two-tailed test by
considering either extreme of the distribution (< 0.025 or > 0.975) at
the 0.05 level.

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
Expectation-Maximization (EM) algorithm ([Dempster:1977]_;
[Excoffier:Slatkin:1995]_). Multiple starting conditions are used to
minimize the possibility of local maxima being reached by the EM
iterations. The haplotype frequencies reported are those that correspond
to the highest logarithm of the sample likelihood found over the
different starting conditions and are labeled as the maximum likelihood
estimates (MLE).

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
pair of loci.

.. code-block:: text

   II. Multi-locus Analyses
   ========================

   Haplotype/ linkage disequlibrium (LD) statistics
   ________________________________________________

   Pairwise LD estimates
   ---------------------
   Locus pair        D'        Wn   ln(L_1)   ln(L_0)         S # permu p-value  
   A:C          0.49229   0.39472   -289.09   -326.81     75.44    1000 0.8510   
   A:B          0.50895   0.40145   -293.47   -330.83     74.73    1000 0.8730   
   A:DRB1       0.44304   0.37671   -282.00   -309.16     54.32    1000 0.7540   
   A:DQA1       0.29361   0.34239   -257.94   -269.88     23.88    1000 0.9020   
   A:DQB1       0.39266   0.37495   -275.58   -297.61     44.07    1000 0.8140   
   A:DPA1       0.31210   0.37987   -203.89   -206.99      6.21    1000 0.8840   
   A:DPB1       0.42241   0.40404   -237.84   -262.05     48.42    1000 0.5930   
   C:B          0.88739   0.85752   -210.36   -342.68    264.63    1000 0.0000***
   C:DRB1       0.48046   0.47513   -280.34   -317.65     74.62    1000 0.2140   
   C:DQA1       0.42257   0.49869   -250.36   -276.72     52.73    1000 0.0370*  
   C:DQB1       0.45793   0.49879   -269.54   -305.27     71.46    1000 0.0580   
   C:DPA1       0.37214   0.46870   -208.99   -215.36     12.74    1000 0.7450   
   C:DPB1       0.46436   0.36984   -242.45   -268.45     52.01    1000 0.6290   
   B:DRB1       0.50255   0.41712   -286.79   -320.50     67.42    1000 0.4140   
   B:DQA1       0.41441   0.42844   -259.86   -279.56     39.40    1000 0.3880   
   B:DQB1       0.49040   0.43654   -277.29   -308.12     61.65    1000 0.2870   
   B:DPA1       0.29272   0.38831   -213.43   -218.01      9.14    1000 0.8780   
   B:DPB1       0.46082   0.38001   -247.83   -272.77     49.86    1000 0.7320   
   DRB1:DQA1    0.91847   0.91468   -164.06   -254.54    180.96    1000 0.0000***
   DRB1:DQB1    1.00000   1.00000   -147.73   -283.09    270.72    1000 0.0000***

   ...

We report two measures of overall linkage disequilibrium. :math:`D'`
[Hedrick:1987]_ weights the contribution to LD of specific allele pairs by
the product of their allele frequencies; :math:`W_n` [Cramer:1946]_ is
a re-expression of the chi-square statistic for deviations between
observed and expected haplotype frequencies. Both measures are
normalized to lie between zero and one.

:math:`D'`
   Overall LD, summing contributions (:math:`D'_{ij}=D_{ij} /D_{max}`) of all the haplotypes in a
   multi-allelic two-locus system, can be measured using Hedrick's
   :math:`D'` statistic, using the products of allele frequencies at the
   loci, :math:`p_i` and :math:`q_j`, as weights.

.. math::
   
   {D}' = \sum_{i=1}^{I} {\sum_{j=1}^{J} {p_i } } q_j \left|{{D}'_{ij} } \right|

:math:`W_n`
   Also known as Cramer's V Statistic [Cramer:1946]_, :math:`W_n`, is a
   second overall measure of LD between two loci. It is a re-expression
   of the Chi-square statistic, ``X``\ :sub:`LD`\ :sup:`2`, normalized
   to be between zero and one. When there are only two alleles per
   locus, ``W``\ :sub:`n` is equivalent to the correlation coefficient
   between the two loci, defined as:

.. math::

   W_n = \left[ {\frac{\sum_{i=1}^{I} {\sum_{j=1}^{J}{D_{ij}^2 / p_i } q_j } }{\min (I - 1,J - 1)}} \right]^{\frac{1}{2}} = \left[ {\frac{X_{LD}^2 / 2N}{\min (I - 1,J - 1)}}\right]^{\frac{1}{2}}


When there are only two alleles per locus, :math:`W_n` is equivalent
to the correlation coefficient between the two loci, defined as
:math:`r =\sqrt {D_{11} / p_1 p_2 q_1 q_2 }`.

   
For each locus pair the log-likelihood of obtaining the observed data
given the inferred haplotype frequencies [``ln(L_1)``], and the
likelihood of the data under the null hypothesis of linkage
equilibrium [``ln(L_0)``] are given. The statistic :math:`S` (``S`` in
the output) is defined as twice the difference between these
likelihoods. :math:`S` has an asymptotic chi-square distribution, but the
null distribution of :math:`S` is better approximated using a
randomization procedure. The empirical distribution of :math:`S` is
generated by shuffling genotypes among individuals, separately for
each locus, thus creating linkage equilibrium. ( ``# permu`` indicates
how many permutations were carried out). The :math:`p`-value is the
fraction of permutations that results in values of `S` greater or
equal to that observed. A :math:`p < 0.05` is indicative of overall
significant LD.

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
   0101:1301:0402:   0.02222   2.0       | 0201:1401:0402:   0.03335   3.0       
   0101:1301:1101:   0.01111   1.0       | 3204:1401:0802:   0.03333   3.0       
   0101:1401:0901:   0.01111   1.0       | 0301:1401:0407:   0.03333   3.0       
   0101:1520:0802:   0.01111   1.0       | 0301:1301:0402:   0.03333   3.0       
   0101:1801:0407:   0.01111   1.0       | 0201:1401:1101:   0.03332   3.0       
   0101:3902:0404:   0.01111   1.0       | 0301:1520:0802:   0.02222   2.0       
   0101:3902:1602:   0.01111   1.0       | 0101:4005:0802:   0.02222   2.0       
   0101:4005:0802:   0.02222   2.0       | 0301:3902:0402:   0.02222   2.0       
   0101:8101:0802:   0.01111   1.0       | 0201:1301:1602:   0.02222   2.0       
   0101:8101:1602:   0.01111   1.0       | 0218:1401:0404:   0.02222   2.0       
   0201:1301:1602:   0.02222   2.0       | 0210:5101:1602:   0.02222   2.0       
   0201:1401:0402:   0.03335   3.0       | 0218:1401:1602:   0.02222   2.0       
   0201:1401:0404:   0.01111   1.0       | 0101:1301:0402:   0.02222   2.0       
   0201:1401:0407:   0.02222   2.0       | 2501:4005:0802:   0.02222   2.0       
   0201:1401:0802:   0.01111   1.0       | 2501:1301:0802:   0.02222   2.0       

   ...