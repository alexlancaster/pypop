/***********************************************************************

  program name: hwe.c
  
  main program


  Status: modified from g-t program

  Date: 12/14/99

************************************************************************/

#include <time.h>
#include "hwe.h"
#include "func.h"
#include <math.h>

#include <gsl/gsl_rng.h>

int main(int argc, char *argv[])
/* correct execution of this program: gthwe infile outfile */
{
  int genotypes[LENGTH], allele_array[MAX_ALLELE];
   
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
  if (read_data(genotypes, &no_allele, &total, &sample, &infile, &title))
    exit(2);
  
  /* "de"-construct or "flatten" struct to pass to function, so
    function can be called from outside program without internal
    knowledge of this typedef */
  step = sample.step;
  group = sample.group;
  size = sample.size;

  /* pass the parsed variables to do the main processing */
  run_data(genotypes, allele_array, no_allele, total, step, group, size, title, outfile);
  
  return (0);
}

/* 
 * init_rand(): initializes random number generator 
 */
long init_rand(void) {

  register int i, j;
  unsigned long xxx[12];
  
  unsigned long  conorig=0;
  unsigned long  tauorig=0;
  long t1;
  extern unsigned long congrval, tausval;

  /* srand(time(NULL));  */
  
  /* for testing purposes only */
  srand(1234);  

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
  THIS FUNCTION IS CURRENTLY **BROKEN**, A PLACEHOLDER FOR TESTING
  PURPOSES ONLY, PLEASE DO NOT RELY ON ITS OUTPUT.

  var(2p_ip_j) = 4 var(p_i) * var(p_j)
               = 4 * 1/2N p_i*(1-p_i) * 1/2N p_j*(1-p_j)
               = 1/N^2 * p_i*(1-p_i) * p_j*(1-p_j)

  var(p_i^2) = var(p_i) * var(p_i)
             = (1/4N^2)* p_i^2 * (1-p_i)^2
*/
double norm_dev(int i, int j, int obs_count, int total_gametes, int *allele_array)
{
  double p_i = 0.0, p_j = 0.0;
  double obs_freq, exp_freq, var, norm_dev;
  int total_indivs = total_gametes/2;

  /* printf("allele_array[%d]=%d, allele_array[%d]=%d, N=%d, obs_count=%d\n", 
     i, allele_array[i], j, allele_array[j], total_indivs, obs_count); */
  p_i = (double)allele_array[i]/(double)total_gametes;

  if (i != j) {
    p_j = (double)allele_array[i]/(double)total_gametes;
    exp_freq = 2*p_i*p_j;
    var = (p_i*(1-p_i) * p_j*(1-p_j))/(double)(total_indivs*total_indivs);
  }
  else {
    exp_freq = p_i*p_i;
    var = (p_i*p_i *(1-p_j)*(1-p_j))/(4.0*total_indivs*total_indivs);
  }

  obs_freq = (double)obs_count*2/(double)total_gametes;

  /* printf("p_i=%g, p_j=%g, exp_freq=%g, obs_freq=%g, var=%g, ", 
     p_i, p_j, exp_freq, obs_freq, var);  */
  norm_dev = fabs(exp_freq - obs_freq)/sqrt(var);
  /* printf("norm_dev = %g\n", norm_dev);  */
  return(norm_dev);

}


/* 
 * run_data(): does the main processing, given the data in variables,
 * this can be called by external programs or be made into an
 * extension function in languages like Python using SWIG.
 */
/* int run_data(int genotypes[LENGTH], int allele_array[MAX_ALLELE], int no_allele, int total_individuals, 
	     int thestep, int thegroup, int thesize,
	     char *title, FILE *outfile) */

int run_data(int *genotypes, int *allele_array, int no_allele, 
	     int total_individuals, int thestep, int thegroup, int thesize,
	     char *title, FILE *outfile)
{
  int actual_switch, counter;
  Index index;
  double ln_p_observed, ln_p_simulated, p_mean, p_square; 
  double constant, p_simulated, total_step;
  struct randomization sample;
  struct outcome result;
  register int i, j, k, l;
  long t1;
  int num_genotypes = no_allele * (no_allele + 1) / 2;

  /* int *genotypes = (int *)calloc(genotypes, sizeof(int)); */

  /* do random number initialization */
  t1 = init_rand(); 

  /* reassemble struct */
  sample.step = thestep;
  sample.group = thegroup;
  sample.size = thesize;

#ifdef XML_OUTPUT
  fprintf(outfile, "<hardyweinbergGuoThompson>\n");
  fprintf(outfile, "<dememorizationSteps>%d</dememorizationSteps>\n", 
	  sample.step);
  fprintf(outfile, "<samplingNum>%d</samplingNum>\n", sample.group);
  fprintf(outfile, "<samplingSize>%d</samplingSize>\n", sample.size);
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

  double *obs_normdev = (double *)calloc(num_genotypes, sizeof(double));

  for (i=0; i < no_allele; i++) 
    for (j=0; j <= i; j++) {
      obs_normdev[L(i,j)] = norm_dev(i, j, genotypes[L(i,j)], (total_individuals * 2), allele_array);
      printf("obs_normdev[%d, %d] = %f\n", i, j, obs_normdev[L(i,j)]);
      fflush(stdout);
    }
  int *normdev_count = (int *)calloc(num_genotypes, sizeof(int));

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
	  ln_p_simulated = cal_prob(genotypes, index, ln_p_simulated, &actual_switch);
	  
	  if (ln_p_simulated <= ln_p_observed)  
	    ++counter;
	  ++result.swch_count[actual_switch];

#ifdef INDIVID_GENOTYPES	  
	  /* go through genotype list at this step of the chain */
	  for (k=0; k < no_allele; k++) 
	    for (l=0; l <= k; l++) {
	      /* increase count in genotype if norm_dev > norm_dev[0] */
	      /* printf("genotypes[%d,%d]=%d, ", k, l, genotypes[L(k,l)]); */

	      double sim_normdev = 
		norm_dev(k, l, genotypes[L(k,l)], 
			 (total_individuals * 2), allele_array);
	      /* printf("norm dev: sim = %g, ", sim_normdev); */

	      if (sim_normdev > obs_normdev[L(k,l)]) {
		normdev_count[L(k,l)]++;
		/* printf("obs = %g\n", obs_normdev[L(k,l)]); */
	      }
	    }
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
  fprintf(outfile, "<pvalue>%7.4g</pvalue><stderr>%7.4g</stderr>\n",
	  result.p_value, result.se);
  fprintf(outfile, "<switches>\n");
  fprintf(outfile, "<percent-partial>%6.2f</percent-partial>\n",
	  result.swch_count[1] / total_step * 100);
  fprintf(outfile, "<percent-full>%6.2f</percent-full>\n",
	  result.swch_count[2] / total_step * 100);
  fprintf(outfile, "<percent-all>%6.2f</percent-all>\n",
	  (result.swch_count[1] + result.swch_count[2]) / total_step * 100);
  fprintf(outfile, "</switches>\n");
#endif
  
  stamp_time(t1, &outfile);
  
#ifdef XML_OUTPUT
  fprintf(outfile, "</hardyweinbergGuoThompson>");
#endif

#ifdef INDIVID_GENOTYPES

  /* print pvalues for each genotype */
  for (i=0; i < num_genotypes; i++) {
    /* THIS P-VALUE IS *BROKEN*, THIS IS PLACEHOLDER CODE ONLY! */
    printf("normdev_count[%d] = %d, p-value = %g\n", 
	   i, normdev_count[i], normdev_count[i]/total_step);
  }

  /* free dynamically-allocated memory  */
  free(obs_normdev);
  free(normdev_count);

#endif

  return (0);
}

int run_randomization(int *genotypes, int *allele_array, int no_allele, 
		      int total_individuals, int iterations)

{

  double ln_p_observed; 
  double constant;
  register int i, j, k, l;
  int num_genotypes = no_allele * (no_allele + 1) / 2;


  /* calculate number of alleles of each gamete */
  cal_n(no_allele, genotypes, allele_array); 

  /* reinitialize constant after n has been calculated using cal_n above: 
     don't know why this isn't done in original code? */
  constant = cal_const(no_allele, allele_array, total_individuals); 

  /* check original array */
  /* for (i=0; i < no_allele; i++) 
    for (j=0; j <= i; j++)
      printf("a_copy[%d, %d] = %d\n", i, j, a_copy[LL(i,j)]);
  */

  ln_p_observed = ln_p_value(genotypes, no_allele, constant);   

  /* printf("after recalculating observed value\n"); */

  /* store histograms of each genotype

   create a two dimensional array of size:
   max. number of genotypes * max. number of individuals in pop
      = k * (k + 1) / 2 * N = num_genotypes * total

  */

  int **histograms = (int **)calloc(num_genotypes, sizeof(int *));
  for (i = 0; i < num_genotypes; i++)
    histograms[i] = calloc(total_individuals, sizeof(int));
  
  printf("Constant: %e, Observed: %e\n", constant, ln_p_observed);

  /* calculate the number of gametes */
  int total_gametes = 0;
  for (i=0; i < no_allele; i++) 
    total_gametes += allele_array[i];

  printf("n = [");
  for (i=0; i < no_allele; i++) 
    printf("%d,", allele_array[i]);
  printf("]\n");

  printf("total gametes: %d\n", total_gametes);

  int *s = (int *)calloc(total_gametes, sizeof(int));
  int gamete = 0;

  /* create index of gametes */
  for (i=0; i < no_allele; i++) 
    for (j=0; j < allele_array[i]; j++) {
      s[gamete] = i;
      gamete++;
    }

  printf("before permutation");
  printf("s = [");
  for (i=0; i < total_gametes; i++) {
    printf("%d,", s[i]);
  }
  printf("]\n");

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

    cal_n(no_allele, g, allele_array);

    printf("check that allele_array[] has not changed\n");
    for (i=0; i < no_allele; i++) 
      printf("allele_array[%d] = %d\n", i, allele_array[i]);
#endif

    ln_p_perm = ln_p_value(g, no_allele, constant);

    printf("obs. log[Pr(f)] = %e, sim. log[Pr(g)] = %e\n", ln_p_observed, ln_p_perm);

    if (ln_p_perm <= ln_p_observed)
      K++;
    /* printf("K = %d\n", K); */

    /* go through genotype list */
    for (i=0; i < num_genotypes; i++) {
      /* increase the count g[i]-th place in the i-th histogram by one */
      histograms[i][g[i]]++;

      /* once done, reset genotype array, g */
      g[i] = 0;
    }
  }

  printf("finished permutations!\n");
  printf("K = %d, N = %d\n", K, iterations);
  double p_value = (double)K/iterations;
  printf("pvalue = %g\n", p_value);

  /* print histograms */
  for (i=0; i < num_genotypes; i++) {
    printf("histogram[%d]: {", i);
    for (j=0; j < total_individuals; j++) {
      printf("%d, ", histograms[i][j]);
    }
    printf("} observed: FIXME, need to copy original genotypes[] array\n");
  }


  /* free dynamically-allocated memory  */
  for(i = 0; i < num_genotypes; i++)
    free(histograms[i]);
  free(histograms);

  free(g);
  free(s);

  return (0);


}
