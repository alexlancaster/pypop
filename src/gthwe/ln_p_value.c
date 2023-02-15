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

/*************************************************************************

  program name: ln_p_value.c

  function to compute the log p value for given genotype frequencies

  status: modified from g-t program 

  date: 12/14/99

*************************************************************************/
#include "hwe.h"

double ln_p_value(int *a, int no_allele, double constant)

{
  int i=0, j=0, l=0, temp=0;
  double ln_prob = 0.0;
  double log_factorial();

#ifdef PERMU_DEBUG  
  printf("const=%e, ", constant);
#endif
  ln_prob = constant;
  temp = 0;
  
  for (i = 0; i < no_allele; ++i)
    {
      for (j = 0; j < i; ++j)
	{
	  l = LL(i, j);
	  temp += a[l];
	  ln_prob = ln_prob - log_factorial(a[l]);
	}
      l = LL(i, i);
      ln_prob = ln_prob - log_factorial(a[l]); 
    }

  ln_prob = ln_prob + (temp * log(2.0));

#ifdef PERMU_DEBUG
  printf("no_allele=%d, temp=%d, ln_prob=%e\n", no_allele, temp, ln_prob);
#endif
  return (ln_prob);
}
