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

/* prototype for internal inclusion */
%{
extern int haplo_em_pin_wrap(int, int, double [], int [], int, int, int [], double, double, double, int, int, int, int, int, int, int [], int *, double *, int *, int *);
extern int haplo_em_ret_info_wrap(double, int, int, int, double *, int, int *, int, int *, int, int *, int, double *, int, int *, int, int *);
extern void haplo_free_memory();
%}

/* to generate SWIG wrapper */
extern int haplo_em_pin_wrap(int xn_loci,
                             int xn_subject,
                             double xweight[],
                             int xn_alleles[],
                             int xmax_haps,
                             int xmax_iter,
                             int xloci_insert_order[],
                             double xmin_prior,
                             double xmin_posterior,
                             double xtol,
                             int xinsert_batch_size,
                             int xrandom_start,
                             int xiseed1,
                             int xiseed2,
                             int xiseed3,
                             int xverbose,
                             int xgeno_vec[],

                             int *OutValue,
                             double *OutValue,
                             int *OutValue,
                             int *OutValue);

extern int haplo_em_ret_info_wrap(
          double xS_n_u_hap,   // number of unique hapoltypes
          int xn_loci,         // number of loci
          int xn_hap_pairs,     // number of pairs of loci over all subjects

          int len, double *OutList, // hap_prob: probabilities for unique haplotypes, length= n_u_hap
          int len, int *OutList,    // u_hap: unique haplotype, length=n_u_hap * n_loci
          int len, int *OutList,    // u_hap_code: code for unique haplotypes, length=n_u_hap
          int len, int *OutList,    // subj_id: subject id = index of subject, length=
          int len, double *OutList, // post: posterior probability of pair of haplotypes
          int len, int *OutList,    // hap1_code: code for haplotype-1 of a pair, length=n_pairs
          int len, int *OutList     // hap2_code: code for haplotype-2 of a pair, length=n_pairs
          );

extern void haplo_free_memory();


/*
 * Local variables:
 * mode: c
 * End:
 */
