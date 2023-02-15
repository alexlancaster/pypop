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

/************************************************************************
  program name: read_data.c

  funtion to read data

  status: modified from g-t program

  date: 12/15/99

*************************************************************************/
#include "hwe.h"

int read_data(int **genotypes, int **allele_array, int *no_allele, 
	      int *total, struct randomization *sample, FILE **infile, 
	      char *title)
{
  register int i, j, l, err = 1;

  *total = 0;
  
  if (fscanf(*infile, "%s", title) != 1)
    {
      fprintf(stderr, "Please supply title\n");
      printf("title %s", title);
      return (err);
    }
  
  if (fscanf(*infile, "%d", no_allele) != 1)
    {
      fprintf(stderr, "Please supply number of alleles\n");
      return (err);
    }
  
  if (*no_allele < 2)
    {
      fprintf(stderr, "***Error! Number of alleles less than 2. \n");
      return (err);
    }
  
  /* now we know how big genotype array is calloc memory for it */
  *genotypes = calloc((*no_allele * (*no_allele + 1) / 2), sizeof(int));
  
  /* likewise for allele_array */
  *allele_array = calloc(*no_allele, sizeof(int));

  for (i = 0; i < *no_allele; ++i)
    {
      for (j = 0; j <= i; ++j)
	{
	  int *temp = *genotypes;
	  l = LL(i, j);
	  fscanf(*infile, "%d ", &temp[l]);
	  *total += temp[l];
#if DEBUG
	  printf("in file: genotypes[%d]: %d, total=%d\n", l, temp[l], *total);
#endif
	}
    }
  
  if (fscanf(*infile, "%d %d %d \n", &sample->step,
	     &sample->group, &sample->size) != 3)
    {
      fprintf(stderr, " Please supply parameters.\n");
      return (err);
    }
  else if (sample->step < 1 || sample->group <= 1)
    {
      fprintf(stderr, "***Error in parameter specification.\n");
      return (err);
    }
  
  return (0);

}

