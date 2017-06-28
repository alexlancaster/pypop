/* This file is part of PyPop

  Copyright (C) 2017. 

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
USA.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF
ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION
TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS. */

/* interface definition file for SWIG */

%module Haplostats

%include "typemap.i"

%{
extern void haplo_em_pin(
   int    [], /* *S_n_loci,             number of loci                                 */
   int    [], /* *n_subject,            number of subjects                             */
   double  [], /*weight,               weight per subject                             */
   int    [], /*geno_vec,             vector of genotypes,  col-major from           */
                                  /* n_subject x 2*n_loci matrix                    */
   int    [], /*n_alleles,            vector of number alleles per locus,            */
				  /* length=n_loci                                  */
   int    [], /*max_haps,             number of maximum haplotypes over all subjects */
				  /*  - CRITICAL for memory alloc                   */
   int    [], /*max_iter,             max num. iters for each EM loop                */
   int    [], /*loci_insert_order,    vector for order of insert of loci for         */
                                  /* progressive insertion; length = n_loci         */
   double  [], /*min_prior,            trim haplo's with prior < min_prior            */
   double  [], /*min_posterior,        trim subject's pair of haplos if               */
				  /* post < min_posterior                           */
   double  [], /*tol,                  convergence tolerance for change in lnlike in  */ 
				  /*  EM loop                                       */
   int    [], /*insert_batch_size,    number of loci to insert in a batch before     */
                                  /*  each EM loop; order of inserted               */
                                  /* loci determined by loci_insert_order           */
   int    [], /*converge,             convergence indicator for EM                   */
   double  [], /*S_lnlike,             lnlike from final EM                           */
   int    [], /*S_n_u_hap,            number of unique haplotypes                    */
   int    [], /*n_hap_pairs,          total number of pairs of haplotypes over all   */
                                  /* subjects                                       */
   int    [], /*random_start,         indicator of random posteriors should be       */
				  /* generated at the start of each EM loop.        */
                                  /* 1 = Yes, 0 = No                                */
   int    [], /*iseed1,               seeds for AS183 random unif                    */
   int    [], /*iseed2,	 */
   int    [], /* iseed3, */
   int    [] /*verbose)              indicator if verbose pringing during  run,     */
                                  /* for debugging. verbose=0 means no printing     */
                                  /* verbose=1 means lots of printing to screen     */
			 );


%}

extern void haplo_em_pin(
   int    [], /* *S_n_loci,             number of loci                                 */
   int    [], /* *n_subject,            number of subjects                             */
   double  [], /*weight,               weight per subject                             */
   int    [], /*geno_vec,             vector of genotypes,  col-major from           */
                                  /* n_subject x 2*n_loci matrix                    */
   int    [], /*n_alleles,            vector of number alleles per locus,            */
				  /* length=n_loci                                  */
   int    [], /*max_haps,             number of maximum haplotypes over all subjects */
				  /*  - CRITICAL for memory alloc                   */
   int    [], /*max_iter,             max num. iters for each EM loop                */
   int    [], /*loci_insert_order,    vector for order of insert of loci for         */
                                  /* progressive insertion; length = n_loci         */
   double  [], /*min_prior,            trim haplo's with prior < min_prior            */
   double  [], /*min_posterior,        trim subject's pair of haplos if               */
				  /* post < min_posterior                           */
   double  [], /*tol,                  convergence tolerance for change in lnlike in  */ 
				  /*  EM loop                                       */
   int    [], /*insert_batch_size,    number of loci to insert in a batch before     */
                                  /*  each EM loop; order of inserted               */
                                  /* loci determined by loci_insert_order           */
   int    [], /*converge,             convergence indicator for EM                   */
   double  [], /*S_lnlike,             lnlike from final EM                           */
   int    [], /*S_n_u_hap,            number of unique haplotypes                    */
   int    [], /*n_hap_pairs,          total number of pairs of haplotypes over all   */
                                  /* subjects                                       */
   int    [], /*random_start,         indicator of random posteriors should be       */
				  /* generated at the start of each EM loop.        */
                                  /* 1 = Yes, 0 = No                                */
   int    [], /*iseed1,               seeds for AS183 random unif                    */
   int    [], /*iseed2,	 */
   int    [], /* iseed3, */
   int    [] /*verbose)              indicator if verbose pringing during  run,     */
                                  /* for debugging. verbose=0 means no printing     */
                                  /* verbose=1 means lots of printing to screen     */
			 );


/*
 * Local variables:
 * mode: c
 * End:
 */
