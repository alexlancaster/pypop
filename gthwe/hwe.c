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
  int a[LENGTH], n[MAX_ALLELE];
   
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
  if (read_data(a, &no_allele, &total, &sample, &infile, &title))
    exit(2);
  
  /* "de"-construct or "flatten" struct to pass to function, so
    function can be called from outside program without internal
    knowledge of this typedef */
  step = sample.step;
  group = sample.group;
  size = sample.size;

  /* pass the parsed variables to do the main processing */
  run_data(a, n, no_allele, total, step, group, size, title, outfile);
  
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
 * run_data(): does the main processing, given the data in variables,
 * this can be called by external programs or be made into an
 * extension function in languages like Python using SWIG.
 */
/* int run_data(int a[LENGTH], int n[MAX_ALLELE], int no_allele, int total, 
	     int thestep, int thegroup, int thesize,
	     char *title, FILE *outfile) */

int run_data(int *a, int *n, int no_allele, int total, 
	     int thestep, int thegroup, int thesize,
	     char *title, FILE *outfile)
{
  int actual_switch, counter;
  Index index;
  double ln_p_observed, ln_p_simulated, p_mean, p_square; 
  double constant, p_simulated, total_step;
  struct randomization sample;
  struct outcome result;
  register int i, j;
  long t1;

  /* int *a = (int *)calloc(genotypes, sizeof(int)); */

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
  print_data(a, no_allele, sample, &outfile, title);
#endif

  /* calculate number of alleles of each gamete */
  cal_n(no_allele, a, n);

#if DEBUG
  printf("no_allele=%d, total=%d, thestep=%d, thegroup=%d, thesize=%d, title=%s, t1=%ld\n",no_allele, total, sample.step, sample.group, sample.size, title, t1);
  for (i=0; i < no_allele; i++) 
    for (j=0; j <= i; j++)
      printf("a[%d, %d] = %d\n", i, j, a[LL(i,j)]);

  for (i=0; i < no_allele; i++) 
    printf("n[%d] = %d\n", i, n[i]);

  printf("after looping through a, n!\n");

  fflush(stdout);

#endif

  constant = cal_const(no_allele, n, total);
  
  ln_p_observed = ln_p_value(a, no_allele, constant);  
  
  ln_p_simulated = ln_p_observed; 
  
  p_mean = p_square = (double) 0.0;
  
  result.p_value = result.se = (double) 0.0;	/* initialization */
  
  result.swch_count[0] = result.swch_count[1] = result.swch_count[2] = 0;
  
  for (i = 0; i < sample.step; ++i)
    {        
      /* de-memorization for given steps */
      
      select_index(&index, no_allele);

      ln_p_simulated = cal_prob(a, index, ln_p_simulated, &actual_switch);
      ++result.swch_count[actual_switch];
    }
  
  for (i = 0; i < sample.group; ++i)
    {
      counter = 0;
      
      for (j = 0; j < sample.size; ++j)
	{
	  select_index(&index, no_allele);
	  ln_p_simulated = cal_prob(a, index, ln_p_simulated, &actual_switch);
	  
	  if (ln_p_simulated <= ln_p_observed)  
	    ++counter;
	  ++result.swch_count[actual_switch];
	  
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

#ifdef PERMU_TEST
  /* calculate number of alleles of each gamete */
  cal_n(no_allele, a, n);

  /* reinitialize constant after n has been calculated using cal_n above: 
     don't know why this isn't done in original code? */
  constant = cal_const(no_allele, n, total);

  /* check original array */
  for (i=0; i < no_allele; i++) 
    printf("n[%d] = %d\n", i, n[i]);

  /* don't reinitialize observed value */
  /* ln_p_observed = ln_p_value(a, no_allele, constant);  */

  printf("Constant: %e, Observed: %e\n", constant, ln_p_observed);

  /* calculate the number of gametes */
  int total_gametes = 0;
  for (i=0; i < no_allele; i++) 
    total_gametes += n[i];

  printf("n = [");
  for (i=0; i < no_allele; i++) 
    printf("%d,", n[i]);
  printf("]\n");

  printf("total gametes: %d\n", total_gametes);

  int *s = (int *)calloc(total_gametes, sizeof(int));
  int gamete = 0;

  /* create index of gametes */
  for (i=0; i < no_allele; i++) 
    for (j=0; j < n[i]; j++) {
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
  int *g = (int *)calloc(total, sizeof(int));

  /* start permuting index of gametes */
  int permu = 0, l = 0;
  int K = 0;
  int N = 17000;
  double ln_p_perm;
  for (permu=0; permu < N; permu++) {
    gsl_ran_shuffle(r, s, total_gametes, sizeof(int));

    /*
    printf("after permutation: %d\n", permu);
    printf("s = [");
    for (i=0; i < total_gametes; i++) {
      printf("%d,", s[i]);
    }
    printf("]\n");

    printf("pairs: ");
    */
    for (i=0; i < total_gametes/2; i++) {
      /* printf("(%d,%d)", s[i*2], s[i*2+1]); */
      l = LL(s[i*2],s[i*2+1]);
      g[l]++;
    }
    /* printf("\n"); 

    printf("g = [");
    for (i=0; i < total; i++) 
      printf("%d,", g[i]);
    printf("]\n");
    */

    ln_p_perm = ln_p_value(g, no_allele, constant);

    printf("obs. log[Pr(f)] = %e, sim. log[Pr(g)] = %e\n", ln_p_observed, ln_p_perm);

    if (ln_p_perm <= ln_p_observed)
      K++;
    /* printf("K = %d\n", K); */

    /* reset genotype array, g */
    for (i=0; i < total; i++)
      g[i] = 0;
  }

  printf("finished permutations!\n");
  printf("K = %d, N = %d\n", K, N);
  double p_value = (double)K/N;
  printf("pvalue = %g\n", p_value);

#endif

  return (0);

}

