/* This file is part of PyPop

  Copyright (C) 2003-2008. The Regents of the University of California
  (Regents) All Rights Reserved.

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

/* a translation from Richard Single's awk programme */ 

#define NAME_LEN    22       /* 10 chars for allele name, plus colon and null */ 
#define LINE_LEN    132      /* RS changed from 120 to 132=6*2*(10+1) */ 
#define MAX_ROWS    5000     /* increased from 1023                   */ 
#define MAX_ALLELES 200      /* increased from 80 for a large dataset */
#define MAX_LOCI    20 
#define MAX_COLS    MAX_LOCI * 2 
                             /* max genotypes:  2^max_loci*max_rows */ 
#define MAX_GENOS   40000    /* RS changed from 64*MAX_ROWS and then 20000 */
#define MAX_HAPLOS  30000    /* RS added and changed declaration in main_proc */
 
#define CRITERION   0.000001 
#define MAX_ITER    400      /* RS changed from 200 */
 
#define FALSE 0 
#define TRUE  1 
 
#define MAX_INIT 50 

#define MAX_GENOS_PER_PHENO 64 /* 2^(max_loci - 1) */

#define MAX_PERMU 1001
#define MAX_INIT_FOR_PERMU 5 

#ifdef EXTERNAL_MODE
#define FP_ITER fp_out
#define FP_PERMU fp_out
#else
#define FP_ITER NULL
#define FP_PERMU NULL
#endif

#ifdef __SWIG__
#define xmlfprintf fprintf
#else
#define xmlfprintf fprintf
#endif

/* include re-implemented drand48() on Windows */
#if defined(_WIN32) || defined(__WIN32__) || defined(_WIN64) || defined(__WIN64__)
#include "drand48.c"
#define drand48(x) drand48_windows(x)
#define srand48(x) srand48_windows(x)
#endif

/* 
 * macros to initialize elements of a given static array to `zero'
 * make sure that functions are `re-entrant' (i.e. don't carry bogus
 * data over from previous invocations) and are therefore idempotent
 * (behave identically from function-call to function-call) when used
 * in a shared library context.
 */

#define INIT_STATIC_DIM1(type,id,size1) \
memset(id, '\0', size1*sizeof(type))

#define INIT_STATIC_DIM2(type,id,size1,size2) \
memset(id, '\0', size1*size2*sizeof(type))

#define INIT_STATIC_DIM3(type,id,size1,size2,size3) \
memset(id, '\0', size1*size2*size3*sizeof(type))

/*
 * macros to allocate memory for automatic variables in a function to
 * zero via `calloc' for different dimensional arrays.  a
 * corresponding `free' must always be used at the end of the function
 */

#define CALLOC_ARRAY_DIM1(type,name,size1) \
type *name = (type *)calloc(size1, sizeof(type))

#define CALLOC_ARRAY_DIM2(type,name,size1,size2) \
type (*name)[size2] = (type (*)[size2])calloc(size1*size2, sizeof(type))

#define CALLOC_ARRAY_DIM3(type,name,size1,size2,size3) \
type (*name)[size2][size3] = (type (*)[size2][size3])calloc(size1*size2*size3, sizeof(type))
