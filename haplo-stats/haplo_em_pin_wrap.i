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
extern int main_proc(int xn_loci, 
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

/*
 * Local variables:
 * mode: c
 * End:
 */
