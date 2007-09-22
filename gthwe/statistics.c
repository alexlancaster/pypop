/* This file is part of PyPop
  
  Copyright (C) 2004, 2005. 
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

#include "hwe.h"
#include "func.h"
double diff_statistic(int i, int j, int total_gametes, 
		      int *allele_array, int *genotypes)
{
  double p_i, p_j, expected;
  double cur_observed = (double)genotypes[L(i,j)];

  p_i = (double)allele_array[i]/(double)total_gametes;

  if (i != j) {
    p_j = (double)allele_array[j]/(double)total_gametes;
    /* heterozygote case */
    expected = 2*p_i*p_j*total_gametes/2;
  }
  else {
    /* homozygote case */
    expected = p_i*p_i*total_gametes/2;
  }

  /* printf("cur_observed = %g, expected = %g\n", cur_observed, expected); */

  double diff_stat = fabs(cur_observed - expected);

  return (diff_stat); 
}

/*
  THIS FUNCTION IS CURRENTLY **BROKEN**, A PLACEHOLDER FOR TESTING
  PURPOSES ONLY, PLEASE DO NOT RELY ON ITS OUTPUT.

  heterozygote test statistic, Z_ij from Biometrics 55:1269-1272

  Z_ij = abs(d_ij) / sqrt(var(d_ij))

  where:

  d_ij = p_i*p_j - 1/2 * p_ij

  var(d_ij) = 1/2*n * {p_i*p_j*[(1-p_i)(1-p_j) + p_i*p_j]
                       + p_i^2*(p_jj - p_j^2) + p_j^2*(p_ii -p_i^2) }

  
  homozygote test statistic, Z_ii from Chen et al. 2004 

  Z_ij = abs(d_ii) / sqrt(var(d_ii))

  where:
  
  d_ii = p_i^2 - p_ii

  var(d_ii) = 1/n * (p_i^4 - 2*p_i^3 + p_i^2)

*/
double chen_statistic (int i, int j, int total_gametes, 
		      int *allele_array, int *genotypes)
{
  double p_i, p_j, p_ij, p_ii, p_jj;
  double d, var, norm_dev;
  int total_indivs = total_gametes/2;

  /* printf("allele_array[%d]=%d, allele_array[%d]=%d, N=%d, obs_count=%d\n", 
     i, allele_array[i], j, allele_array[j], total_indivs, obs_count); */
  p_i = (double)allele_array[i]/(double)total_gametes;
  p_ii = (double)genotypes[L(i,i)]/(double)total_indivs;
  
  if (i != j) {
    /* heterozygote case */
    p_j = (double)allele_array[j]/(double)total_gametes;

    p_ij = (double)genotypes[L(i,j)]/(double)total_indivs;
    p_jj = (double)genotypes[L(j,j)]/(double)total_indivs;

    d = p_i*p_j - (0.5)*p_ij;
    var = (1.0/(double)total_gametes)*(p_i*p_j*((1-p_i)*(1-p_j) + p_i*p_j)
			     + p_i*p_i*(p_jj - p_j*p_j) 
			     + p_j*p_j*(p_ii - p_i*p_i));
  }
  else {
    /* homozygote case */
    d = p_i*p_i - p_ii;
    var = (1.0/(double)total_indivs)*(pow(p_i, 4.0)-(2*pow(p_i,3.0))+(p_i*p_i));
  }

  norm_dev = fabs(d)/sqrt(var);

  /* printf("i=%d, j=%d, p_i=%g, p_j=%g, p_ii=%g, p_ij=%g, p_jj=%g, d=%g, d'=%g, var=%g, ", i, j, p_i, p_j, p_ii, p_ij, p_jj, d, p_i*p_j - (0.5)*p_ij, var);   */
  return(norm_dev);

}

void init_stats(char *statistic_type, 
		double (*statistic_func) (int, int, int, int *, int *),
		double *obs_normdev, int no_allele, int total_individuals,
		int *allele_array, int *genotypes,  FILE *outfile)
{
  register int i, j;

  for (i=0; i < no_allele; i++) 
    for (j=0; j <= i; j++) {
      obs_normdev[L(i,j)] = statistic_func(i, j, (total_individuals * 2), 
					   allele_array, genotypes);
#ifdef LOGGING
#ifndef XML_OUTPUT
      fprintf(outfile, "obs. teststat %s (%d,%d)[%d] = %f\n", statistic_type, i, j, genotypes[L(i,j)], obs_normdev[L(i,j)]);
#else
      xmlfprintf(outfile, "<genotypeObservedStatistic statistic=\"%s\" row=\"%d\" col=\"%d\" id=\"%d\">%g</genotypeObservedStatistic>\n", statistic_type, i, j, L(i,j), obs_normdev[L(i,j)]);
#endif
#endif
      fflush(stdout);
    }
}

void store_stats(char *statistic_type, double (*statistic_func) (int, int, int, int *, int *),
		 double *obs_normdev, int *normdev_count, 
		 int no_allele, int total_individuals,
		 int *allele_array, int *genotypes, FILE *outfile)
{
  register int k, l;

  /* go through genotype list at this step of the chain */
  for (k=0; k < no_allele; k++) 
    for (l=0; l <= k; l++) {
      /* increase count in genotype if test statistic > test statistic[0] */
      /* printf("genotypes[%d,%d]=%d, ", k, l, genotypes[L(k,l)]); */
      
      double sim_normdev = statistic_func(k, l, (total_individuals * 2), 
					  allele_array, genotypes);
      int comparison=0;
      if (GREATER_OR_EQUAL (sim_normdev, obs_normdev[L(k,l)])) {
	normdev_count[L(k,l)]++;
	comparison=1;
	/* printf("obs = %g\n", obs_normdev[L(k,l)]); */
      }

#ifdef LOGGING
#ifdef XML_OUTPUT
      xmlfprintf(outfile, "<genotypeSimulatedStatistic statistic=\"%s\" row=\"%d\" col=\"%d\" id=\"%d\">%g</genotypeSimulatedStatistic>\n", statistic_type, k, l, L(k,l), sim_normdev);
#else
      fprintf(outfile, "sim. test-stat %s (%d,%d) [%d]= %g (%g) [%s]\n", statistic_type, k, l, genotypes[L(k,l)], sim_normdev, obs_normdev[L(k,l)], comparison ? "YES": "NO"); 
#endif
#endif
    }
}

void print_stats(char *statistic_type, int *normdev_count, 
		 int no_allele, double steps, FILE *outfile)
{
  register int k, l;
  for (k=0; k < no_allele; k++) 
    for (l=0; l <= k; l++) {
#ifndef XML_OUTPUT      
      fprintf(outfile, 
	      "test-stat %s count (%d,%d) = %d, p-value = %g\n", 
	      statistic_type, k, l, normdev_count[L(k,l)], 
	      normdev_count[L(k,l)]/steps);
#else
      xmlfprintf(outfile, "<pvalue type=\"genotype\" statistic=\"%s\" row=\"%d\" col=\"%d\">%g</pvalue>\n", statistic_type, k, l, normdev_count[L(k,l)]/steps);
#endif
    }
}
