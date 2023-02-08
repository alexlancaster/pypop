/* This file is part of PyPop
  
  Copyright (C) 1992. Sun-Wei Guo.
  Modifications Copyright (C) 1999, 2003, 2004. 
  The Regents of the University of California (Regents) All Rights Reserved.

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

/***************************************************************************
  program name: hwe.h

  header file for hwe.c

  status: modified from g-t program

  date: 12/14/99

***************************************************************************/

#include  <stdio.h>
#include  <stdlib.h> 
#include  <math.h>

#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_sys.h>

#define  EPSILON     1e-6
#define  GREATER_OR_EQUAL(a,b) (gsl_fcmp(a,b,EPSILON)>=0)
#define  LESS_OR_EQUAL(a,b)    (gsl_fcmp(a,b,EPSILON)<=0)

#define  STR_END       '\0'
#define  MAXRAND       RAND_MAX

#define  MIN(x, y)     ((x) < (y)) ? (x) : (y)
#define  RATIO(u, v)   ( (double) (u) ) / ( 1.0 + (double) (v) ) 
#define  TRANS(x)     (MIN(1.0, x))/2.0  /* transition probability */

#define  LL(a, b)      a * ( a + 1 ) / 2  + b
#define  L(a, b)       ( a < b ) ? b*(b + 1)/2 + a : a*(a+1)/2 + b

#define  EXPECT(a,b,c) ((double) a) / ((double) c) * ((double) b) / 2.0

#ifdef __SWIG__
int pyfprintf(FILE *fp, const char *format, ...);
#define xmlfprintf fprintf
#else
#define xmlfprintf fprintf
#endif

typedef struct _Index
{
  int i1;
  int i2;
  int j1;
  int j2;
  int type;
  double cst;
} Index;

struct outcome 
{
  double p_value;  /* mean p-value */
  double se;       /* standard error of the p-value */
  int swch_count[3];  /* switch counts for partial and full switch */
};

struct randomization 
{
  int group; /* total number of chunks */
  int size;  /* size of a chunk */
  int step;  /* number of steps to de-memerization */
};


