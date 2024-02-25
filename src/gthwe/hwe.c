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

/***********************************************************************

  program name: hwe.c
  
  main program


  Status: modified from g-t program

  Date: 12/14/99

************************************************************************/

#include <time.h>
#include <stdio.h>
#include "hwe.h"
#include "func.h"
#include <math.h>

unsigned long tausval, congrval;

/* correct execution of this program: gthwe infile outfile */
int main(int argc, char *argv[])
{
  int *genotypes, *allele_array;
   
  int no_allele, total;
  struct randomization sample;
  int step, group, size;

  FILE *infile, *outfile;
  
  char title[80];

  /* sanity check for existence of files */
  if (check_file(argc, argv, &infile, &outfile))
		exit(1);
  
  printf("Just a second. \n");

  /* random number init stuff was moved to init_rand() and is called
     from run_data() */

  /* get the parameters and data from the file and read into variables */
  if (read_data(&genotypes, &allele_array, &no_allele, &total, &sample, &infile, &title))
    exit(2);
  
  /* "de"-construct or "flatten" struct to pass to function, so
    function can be called from outside program without internal
    knowledge of this typedef */
  step = sample.step;
  group = sample.group;
  size = sample.size;

  /* pass the parsed variables to do the main processing */
  run_data(genotypes, allele_array, no_allele, total, step, group, size, title, outfile, 1, 0);

  free(genotypes);
  free(allele_array);
  return (0);
}

/* 
 * init_rand(): initializes random number generator 
 */
long init_rand(int testing) 
{
  register int i, j;
  unsigned long xxx[12];
  
  unsigned long  conorig=0;
  unsigned long  tauorig=0;
  long t1;
  extern unsigned long congrval, tausval;

  if (!testing) 
    {
      srand(time(NULL)); 
    }
  else {
    /* if invoked in testing mode, fix random number seed so output is deterministic */
    srand(1234);  
  }

  /* seeds selection for Splus type random number generator. */	
  for (i = 0; i < 12; i++) {
    
    xxx[i] = (unsigned long) (floor((64.0 * rand())/(RAND_MAX))) ; 
    if (xxx[i] == 64)
      { 
	xxx[i] = 63;
      }
    
  }
  
  for (j = 0; j < 6; ++j) {
    tauorig =  (((tauorig + (xxx[j + 6] * (pow(2, (6 * j))))))) ;
    conorig =  (((conorig + (xxx[j] * (pow(2, (6 * j)))))));
  }		
  while (conorig > 4294967295. )
    conorig -= 4294967295.;
  congrval = (unsigned long) conorig ;
  while (tauorig > 4294967295. )
    tauorig -= 4294967295.;
  tausval = (unsigned long) tauorig;
  time(&t1); 

  return (t1);
}


/* 
 * run_data(): does the main processing, given the data in variables,
 * this can be called by external programs or be made into an
 * extension function in languages like Python using SWIG.
 */
int run_data(int *genotypes, int *allele_array, int no_allele, 
	     int total_individuals, int thestep, int thegroup, int thesize,
	     char *title,
#ifdef XML_OUTPUT
	     char *outfilename,
#else
	     FILE *outfile,
#endif
	     int header, int testing)
{
  int actual_switch, counter;
  Index index;
  double ln_p_observed, ln_p_simulated, p_mean, p_square; 
  double constant, p_simulated, total_step;
  struct randomization sample;
  struct outcome result;
  register int i, j;
  long t1;
  int num_genotypes = no_allele * (no_allele + 1) / 2;

#ifdef XML_OUTPUT
  FILE *outfile;
  outfile = fopen(outfilename, "w");
#endif
  
  /* int *genotypes = (int *)calloc(genotypes, sizeof(int)); */

  /* do random number initialization */
  t1 = init_rand(testing); 

  /* reassemble struct */
  sample.step = thestep;
  sample.group = thegroup;
  sample.size = thesize;

#ifdef XML_OUTPUT
  if (header)
    xmlfprintf(outfile, "<hardyweinbergGuoThompson>\n");
  xmlfprintf(outfile, "<dememorizationSteps>%d</dememorizationSteps>\n", 
	  sample.step);
  xmlfprintf(outfile, "<samplingNum>%d</samplingNum>\n", sample.group);
  xmlfprintf(outfile, "<samplingSize>%d</samplingSize>\n", sample.size);
#endif

#ifndef SUPPRESS_ALLELE_TABLE
  print_data(genotypes, no_allele, sample, &outfile, title);
#endif

  /* calculate number of alleles of each gamete */
  cal_n(no_allele, genotypes, allele_array);

#if DEBUG
  printf("no_allele=%d, total_individuals=%d, thestep=%d, thegroup=%d, thesize=%d, title=%s, t1=%ld\n",no_allele, total_individuals, sample.step, sample.group, sample.size, title, t1);
  for (i=0; i < no_allele; i++) 
    for (j=0; j <= i; j++)
      printf("genotypes[%d, %d] = %d\n", i, j, genotypes[LL(i,j)]);

  for (i=0; i < num_genotypes; i++) 
    printf("genotypes[%d] = %d\n", i, genotypes[i]);

  for (i=0; i < no_allele; i++) 
    printf("allele_array[%d] = %d\n", i, allele_array[i]);

  printf("after looping through a, n!\n");

  fflush(stdout);
#endif


#ifdef INDIVID_GENOTYPES
  double *obs_chen_statistic = (double *)calloc(num_genotypes, sizeof(double));
  double *obs_diff_statistic = (double *)calloc(num_genotypes, sizeof(double));

  init_stats("chen_statistic", chen_statistic, obs_chen_statistic, 
	     no_allele, total_individuals, 
	     allele_array, genotypes, outfile);
  init_stats("diff_statistic", diff_statistic, obs_diff_statistic, 
	     no_allele, total_individuals, 
	     allele_array, genotypes, outfile);

  int *chen_statistic_count = (int *)calloc(num_genotypes, sizeof(int));
  int *diff_statistic_count = (int *)calloc(num_genotypes, sizeof(int));
#endif

  constant = cal_const(no_allele, allele_array, total_individuals);
  
  ln_p_observed = ln_p_value(genotypes, no_allele, constant);  
  
  ln_p_simulated = ln_p_observed; 
  
  p_mean = p_square = (double) 0.0;
  
  result.p_value = result.se = (double) 0.0;	/* initialization */
  
  result.swch_count[0] = result.swch_count[1] = result.swch_count[2] = 0;

  for (i = 0; i < sample.step; ++i)
    {        
      /* de-memorization for given steps */
      
      select_index(&index, no_allele);

      ln_p_simulated = cal_prob(genotypes, index, ln_p_simulated, &actual_switch);
      ++result.swch_count[actual_switch];
    }
  
  for (i = 0; i < sample.group; ++i)
    {
      counter = 0;
      
      for (j = 0; j < sample.size; ++j)
	{
	  select_index(&index, no_allele);
	  ln_p_simulated = cal_prob(genotypes, index, 
				    ln_p_simulated, &actual_switch);
	  
	  if (LESS_OR_EQUAL(ln_p_simulated, ln_p_observed))  
	    ++counter;
	  ++result.swch_count[actual_switch];

#ifdef INDIVID_GENOTYPES	  
	  store_stats("chen_statistic", chen_statistic, obs_chen_statistic, 
		      chen_statistic_count, no_allele, total_individuals, 
		      allele_array, genotypes, outfile);
	  store_stats("diff_statistic", diff_statistic, obs_diff_statistic, 
		      diff_statistic_count, no_allele, total_individuals, 
		      allele_array, genotypes, outfile);
#endif
	}
      p_simulated = (double) counter / sample.size;
      p_mean += p_simulated;
      p_square += p_simulated * p_simulated;
      
    }
  p_mean /= sample.group;
  result.p_value = p_mean;
  result.se = p_square / ((double) sample.group) / (sample.group - 1.0)
    - p_mean / (sample.group - 1.0) * p_mean;
  result.se = sqrt(result.se);
   
  total_step = sample.step + sample.group * sample.size;
  
#ifndef XML_OUTPUT
  fprintf(outfile, "Randomization test P-value: %7.4g  (%7.4g) \n",
	  result.p_value, result.se);
  fprintf(outfile, "Percentage of partial switches: %6.2f \n",
	  result.swch_count[1] / total_step * 100);
  fprintf(outfile, "Percentage of full switches: %6.2f \n",
	  result.swch_count[2] / total_step * 100);
  fprintf(outfile, "Percentage of all switches: %6.2f \n",
	  (result.swch_count[1] + result.swch_count[2]) / total_step * 100);
#else
  xmlfprintf(outfile, "<pvalue type=\"overall\">%7.4g</pvalue><stderr>%7.4g</stderr>\n",
	  result.p_value, result.se);
  xmlfprintf(outfile, "<switches>\n");
  xmlfprintf(outfile, "<percent-partial>%6.2f</percent-partial>\n",
	  result.swch_count[1] / total_step * 100);
  xmlfprintf(outfile, "<percent-full>%6.2f</percent-full>\n",
	  result.swch_count[2] / total_step * 100);
  xmlfprintf(outfile, "<percent-all>%6.2f</percent-all>\n",
	  (result.swch_count[1] + result.swch_count[2]) / total_step * 100);
  xmlfprintf(outfile, "</switches>\n");
#endif
  
  stamp_time(t1, &outfile);
  
#ifdef INDIVID_GENOTYPES
  /* print pvalues for each genotype */
  /* correct for number of dememorisation steps? */
  print_stats("chen_statistic", chen_statistic_count, no_allele, 
	      total_step - sample.step, outfile);
  print_stats("diff_statistic", diff_statistic_count, no_allele, 
	      total_step - sample.step, outfile);

  /* free dynamically-allocated memory  */
  free(obs_chen_statistic);
  free(chen_statistic_count);

  free(obs_diff_statistic);
  free(diff_statistic_count);
#endif

#ifdef XML_OUTPUT
  fclose(outfile);
  if (header)
    xmlfprintf(outfile, "</hardyweinbergGuoThompson>");
#endif
  return (0);
}

int run_randomization(int *genotypes, int *allele_array, int no_allele, 
		      int total_individuals, int iterations,
#ifdef XML_OUTPUT
		      char *outfilename,
#else
		      FILE *outfile,
#endif
		      int header, int testing)
{
  double ln_p_observed; 
  double constant;
  register int i, j, l;
  int num_genotypes = no_allele * (no_allele + 1) / 2;

#ifdef XML_OUTPUT
  FILE *outfile;
  outfile = fopen(outfilename, "w");
#endif
  
  /* calculate number of alleles of each gamete */
  cal_n(no_allele, genotypes, allele_array); 

  /* reinitialize constant after n has been calculated using cal_n above */
  constant = cal_const(no_allele, allele_array, total_individuals); 

  /* calculate ln(probability) in observed data */
  ln_p_observed = ln_p_value(genotypes, no_allele, constant);   

#ifdef XML_OUTPUT
  if (outfile == NULL) {
    printf("problem with opening file!\n");
  }
  if (header)
    xmlfprintf(outfile, 
	    "\n<hardyweinbergGuoThompson type=\"monte-carlo\">\n");

#else
  fprintf(outfile, "Constant: %e, Observed: %e\n", constant, ln_p_observed);
#endif

#ifdef INDIVID_GENOTYPES	  
  /* allocate memory for per-genotype statistics */
  double *obs_chen_statistic = (double *)calloc(num_genotypes, sizeof(double));
  double *obs_diff_statistic = (double *)calloc(num_genotypes, sizeof(double));

  init_stats("chen_statistic", chen_statistic, obs_chen_statistic, 
	     no_allele, total_individuals, 
	     allele_array, genotypes, outfile);
  init_stats("diff_statistic", diff_statistic, obs_diff_statistic, 
	     no_allele, total_individuals, 
	     allele_array, genotypes, outfile);

  /* allocate memory for per-genotype counts */
  int *chen_statistic_count = (int *)calloc(num_genotypes, sizeof(int));
  int *diff_statistic_count = (int *)calloc(num_genotypes, sizeof(int));

#endif

  /* calculate the number of gametes */
  int total_gametes = 0;
  for (i=0; i < no_allele; i++) 
    total_gametes += allele_array[i];

#ifdef PERMU_DEBUG
  printf("n = [");
  for (i=0; i < no_allele; i++) 
    printf("%d,", allele_array[i]);
  printf("]\n");
  printf("total gametes: %d\n", total_gametes);
#endif

  int *s = (int *)calloc(total_gametes, sizeof(int));
  int gamete = 0;

  /* create index of gametes */
  for (i=0; i < no_allele; i++) 
    for (j=0; j < allele_array[i]; j++) {
      s[gamete] = i;
      gamete++;
    }

#ifdef PERMU_DEBUG
  printf("before permutation");
  printf("s = [");
  for (i=0; i < total_gametes; i++) {
    printf("%d,", s[i]);
  }
  printf("]\n");
#endif

  const gsl_rng_type * T;
  gsl_rng * r;
  
  gsl_rng_env_setup();
  T = gsl_rng_default;
  r = gsl_rng_alloc (T);

  /* create empty genotype array */
  int *g = (int *)calloc(num_genotypes, sizeof(int));

  /* start permuting index of gametes */
  int permu = 0;
  int K = 0;

  double ln_p_perm;
  for (permu=0; permu < iterations; permu++) {
    gsl_ran_shuffle(r, s, total_gametes, sizeof(int));

#ifdef PERMU_DEBUG
    printf("after permutation: %d\n", permu);
    printf("s = [");
    for (i=0; i < total_gametes; i++) {
      printf("%d,", s[i]);
    }
    printf("]\n");
    printf("pairs: ");
#endif

    for (i=0; i < total_gametes/2; i++) {
      l = L(s[i*2],s[i*2+1]);
#ifdef PERMU_DEBUG
      printf("(%d,%d)->%d, ", s[i*2], s[i*2+1], l); 
#endif
      g[l]++;
    }

#ifdef PERMU_DEBUG
    printf("\n");  

    printf("g = [");
    for (i=0; i < num_genotypes; i++) 
      printf("%d,", g[i]);
    printf("]\n");

    printf("check that allele_array[] has not changed\n");
    for (i=0; i < no_allele; i++) 
      printf("allele_array[%d] = %d\n", i, allele_array[i]);
#endif

    ln_p_perm = ln_p_value(g, no_allele, constant);

#ifdef PERMU_DEBUG
    printf("obs. log[Pr(f)] = %e, sim. log[Pr(g)] = %e\n", ln_p_observed, ln_p_perm);
#endif

    if (LESS_OR_EQUAL(ln_p_perm, ln_p_observed))
      K++;

#ifdef INDIVID_GENOTYPES	  
    /* store the individual genotype stats */
    store_stats("chen_statistic", chen_statistic, obs_chen_statistic, 
		chen_statistic_count, no_allele, 
		total_individuals, allele_array, g, outfile);

    store_stats("diff_statistic", diff_statistic, obs_diff_statistic, 
		diff_statistic_count, no_allele, 
		total_individuals, allele_array, g, outfile);
#endif

    /* go through genotype list, reset genotype array, g  */
    for (i=0; i < num_genotypes; i++) 
      g[i] = 0;
  }

  double p_value = (double)K/iterations;

#ifdef XML_OUTPUT
  xmlfprintf(outfile, "<steps>%d</steps>\n", iterations);
  xmlfprintf(outfile, "<pvalue type=\"overall\">%g</pvalue>\n", p_value);
#else
  fprintf(outfile, "K = %d, N = %d\n", K, iterations);
  fprintf(outfile, "pvalue = %g\n", p_value);
#endif

#ifdef INDIVID_GENOTYPES
  /* print pvalues for each genotype */
  print_stats("chen_statistic", chen_statistic_count, 
	      no_allele, iterations, outfile);
  print_stats("diff_statistic", diff_statistic_count, 
	      no_allele, iterations, outfile);

  /* free dynamically-allocated memory for stats  */
  free(obs_chen_statistic);
  free(chen_statistic_count);

  free(obs_diff_statistic);
  free(diff_statistic_count);
#endif


  /* free dynamically-allocated memory  */
  free(g);
  free(s);

#ifdef XML_OUTPUT
  fclose(outfile);
  if (header)
    xmlfprintf(outfile, "</hardyweinbergGuoThompson>\n");
#endif
  return (0);
}
