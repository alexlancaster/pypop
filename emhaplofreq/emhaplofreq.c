#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <float.h>  /* needed for DBL_EPSILON */

#include "emhaplofreq.h"

/***************** begin: function prototypes ***************************/

void print_usage(void);

FILE *parse_args(int, char **, int *);
/* argc, argv */
/* returns open filehandle of input file */

int read_infile(FILE *, char (*)[], char (*)[][], int *);
/* open filehandle for data, ref array, data array, number of records */
/* returns number of loci */

int main_proc(FILE *, char (*)[][], int, int, int);
/* data array, number of loci, number of records */
/* main procedure that handles memory allocation and creation of arrays, 
  * spawns the rest of the data preparation and processing functions, 
  * performs the EM calculation, and prints out the results. 
  * we only return from it to exit. 
*/

int count_unique_haplos(char (*)[][], char (*)[], int (*)[], char (*)[][], int *, int, int, int (*)[], int *);
/* geno, haplo, haplocus, unique_allele, n_unique_allele, n_unique_geno, n_loci, xgeno, xhaplo */
/* returns number of haplotypes */
/* 
  * creates array of possible haplotypes from array of possibly observed genotypes 
  * create haplocus[i][j]: a 2-dim array of allele# at jth locus of ith haplotype
*/

void id_unique_alleles(char (*)[][], char (*)[][], int *, double (*)[], int, int);
/* data array, unique_allele array, no. of unique alleles array, allele_freq, no. of loci, no. of records */
/* 
  * creates array of alleles unique to each locus 
  * Creates allele_freq[i][j]:  freq for jth allele at the ith locus 
*/

double min(double, double);
/*
  * return minimum argument
*/

void linkage_diseq(FILE *, double *, int (*)[], double (*)[], char (*)[][], int *, 
       int, int, int); 
/* mle, haplocus, allele_freq, unique_allele, n_unique_allele, n_loci, n_haplo, n_recs */
/*
  * compute LD coefficients
*/

void sort2arrays(char (*)[], double *, int);
/* haplo array, mle array, no. of haplotypes */
/*
  * insertion sort in ascending order for 1st array also applied to 2nd array
*/

void emcalc(int (*)[], int *, int *, double *, double *, int, int, int, int, 
       int *, int (*)[], int *, int *, double *);
/* genopheno, numgeno, obspheno, freq_zero, mle, n_haplo, n_unique_geno, 
   n_unique_pheno, n_recs, xhaplo, xgeno, error_flag, iter_count, loglike */
/*
  * perform EM iterations with results in the mle array
*/

void haplo_freqs_no_ld(double *, double (*)[], int (*)[], int *, int, int);
/* freqs, allele_freq, haplocus, n_unique_allele, n_loci, n_haplo */
/*
  * compute haplotype frequencies under no LD as products of allele frequencies 
*/

double loglikelihood(int (*)[], double *, int *, int, int, int, int *, int (*)[]);
/* genopheno, hap_freq, n_haplo, n_unique_geno, n_unique_pheno, xhaplo, xgeno */
/*
  * compute log likelihood for a given set of haplotype frequencies
*/

void srand48(long int seedval);

double drand48(void);

void permute_alleles(char (*)[][], int, int);
/* data array, number of loci, number of records */
/* 
  * permutes the alleles at all but the last locus
*/

/******************* end: function prototypes ****************************/

int main(int argc, char **argv)
{
  FILE *if_handle, *fp_out;
  char ref[MAX_ROWS][NAME_LEN];
  char data[MAX_ROWS][MAX_COLS][NAME_LEN];
  int num_loci, num_recs;
  int ret_val;
  int permu_flag;

  if_handle = parse_args(argc, argv, &permu_flag);

/***
  if ((fp_out = fopen("main.out", "w")) == NULL)
  {
    fprintf(stderr, "\nUnable to open main.out for writing.\n\n");
    exit(EXIT_FAILURE);
  }
***/
  fp_out = stdout;

  num_loci = read_infile(if_handle, ref, data, &num_recs);
  fprintf(fp_out, "num_loci: %d\n", num_loci);
  if (num_loci > MAX_LOCI) 
  {
    fprintf(stderr, "Error: number of loci: %d, exceeds maximum of: %d\n",
      num_loci, MAX_LOCI);
    exit(EXIT_FAILURE);
  }

  ret_val = main_proc(fp_out, data, num_loci, num_recs, permu_flag);

  return (ret_val);
}

/************************************************************************/

void print_usage(void)
{
  fprintf(stderr, "Usage: emhaplofreq [-] INPUTFILENAME.\n\n");
  fprintf(stderr, "If  `-' is provided use standard input rather than INPUTFILENAME.\n");
  fprintf(stderr, "If `-p' is provided a permutation test for overall LD is done.\n");
}

/************************************************************************/

FILE *parse_args(int arg_count, char *arg_buff[], int *permu_flag)
{
  FILE *fh;
  int use_stdin = 0;

  if (arg_count < 2)
  {
    print_usage();
    exit(EXIT_FAILURE);
  }

  for (; arg_count > 1 && arg_buff[1][0] == '-'; arg_count--, arg_buff++)
  {
    switch (arg_buff[1][1])
    {
      case NULL:
	use_stdin = 1;
        *permu_flag = 0;
	break;
      case 'p':                  
        *permu_flag = 1; 
        break;
      default:
        print_usage();
        exit(EXIT_FAILURE);
        break;      /* not reached */
    }
  }

  if (use_stdin)
  {
    fh = stdin;
  }
  else 
  {

    /* what's left at argv[1] should be the name of the data file */

    if ((fh = fopen(arg_buff[1], "r")) == NULL)
    {
      perror("Unable to open file");
      fprintf(stderr, "\tOffending filename: %s\n\n", arg_buff[1]);
      exit(EXIT_FAILURE);
    }
    /* skip this until we're through testing */
    /* 
    else 
    { 
      fprintf(stdout, "\nOpened file %s\n", arg_buff[1]); 
      fprintf(stdout, "\nN.B. The first line is expected to contain comments, "); 
      fprintf(stdout, "and will not be parsed.\n\n"); 
    } 
    */
  }

  return (fh);
}

/************************************************************************/

int read_infile(FILE * in_file, char (*reference_ar)[NAME_LEN],
    char (*data_ar)[MAX_COLS][NAME_LEN], int *records)
{
  /* first line is ignored--should be labels or comments */
  /* subsequent lines contain an identifying label of up to 10 characters */
  /* followed by columns of locus_1*allele_1 locus_1*allele2....          */

  /* we'd like to return the number of loci and the number of lines */

  int i, j, num_cols;
  char buff[LINE_LEN];
  char *buff_ptr;

  fgets(buff, LINE_LEN, in_file);  /* eat the first line */

  /* read the second line and store it, ascertaining the number of loci */
  num_cols = i = 0;

  fgets(buff, LINE_LEN, in_file);

  buff_ptr = strtok(buff, "\t \n");
  strcpy(reference_ar[i], buff_ptr);

  while ((buff_ptr = strtok(NULL, "\t \n")) != NULL)
  {
    strcpy(data_ar[i][num_cols], buff_ptr);
    strcat(data_ar[i][num_cols++], ":");
  }

  /* now read the rest */
  while ((fgets(buff, LINE_LEN, in_file)) != NULL)
  {
    if (strlen(buff) < 2)
      continue;      /* quietly bypass empty lines */

    buff_ptr = strtok(buff, "\t \n");
    strcpy(reference_ar[++i], buff_ptr);

    for (j = 0; j < num_cols; j++)
    {
      buff_ptr = strtok(NULL, "\t \n");
      strcpy(data_ar[i][j], buff_ptr);
      strcat(data_ar[i][j], ":");
    }
  }
  *records = i + 1;

  fclose(in_file);
  return (num_cols / 2);  /* this being the number of loci */
}

/************************************************************************/

int main_proc(FILE * fp_out, char (*data_ar)[MAX_COLS][NAME_LEN], int n_loci, 
      int n_recs, int permu_flag)
{

  
  /******************* begin: declarations ****************************/
  int i, j, obs, locus, col_0, col_1;
  int unique_pheno_flag, unique_geno_flag;
  char buff[NAME_LEN];

  int n_hetero, n_hetero_prev;  /* heterozygous sites through current and previous locus loop */
  int n_geno, n_geno_prev;  /* distinct genotypes through current and previous locus loop */
  int unique_pheno_count, n_unique_pheno, unique_geno_count, n_unique_geno;

  /* needed for checking */
  int count;      
  double temp;

  /* these should be malloced, but the stack will experience meltdown: */
  static char pheno[MAX_ROWS][LINE_LEN], geno[MAX_GENOS][2][LINE_LEN / 2];
  static char temp_geno[MAX_GENOS_PER_PHENO][2][LINE_LEN / 2];
  static int numgeno[MAX_ROWS], obspheno[MAX_ROWS], genopheno[MAX_GENOS][MAX_ROWS];

  char temp_pheno[LINE_LEN];

  /* needed for the count_unique_haplotypes function */
  int n_haplo;
  static char haplo[MAX_HAPLOS][LINE_LEN / 2];  /* RS changed to MAX_HAPLOS from 2*MAX_ROWS */

  /* needed for the count_unique_haplotypes and allele_frequencies functions */
  static int haplocus[MAX_HAPLOS][MAX_LOCI];
  int xhaplo[MAX_HAPLOS], xgeno[MAX_GENOS][2];

  /* needed for the id_unique_alleles function */
  static char unique_allele[MAX_LOCI][MAX_ALLELES][NAME_LEN];
  static int n_unique_allele[MAX_LOCI];
  static double allele_freq[MAX_LOCI][MAX_ALLELES];

  /* nothing needed for sort2arrays function */

  /* needed for the emcalc function */
  double mle[MAX_HAPLOS], freq_zero[MAX_HAPLOS];

  /* needed to store loglikelihood under no LD */
  double loglike0;

  /* needed for multiple starting conditions */
  int error_flag, error_flag_best, init_cond, iter_count, iter_count_best;
  double freq_sum, loglike, loglike_best;
  double mle_best[MAX_HAPLOS];

  /* needed for permutations */
  int permu, max_permutations, max_init_cond;
  double like_ratio[MAX_PERMU], pvalue;
  FILE *fp_permu, *fp_iter;

  /******************* end: declarations ****************************/

  srand48(1234567);

  if ((fp_iter = fopen("summary_iter.out", "w")) == NULL)
  {
    fprintf(stderr, "\nUnable to open summary_iter.out for writing.\n\n");
    exit(EXIT_FAILURE);
  }

  if (permu_flag == 1)
  {
    max_permutations = MAX_PERMU;
    if ((fp_permu = fopen("summary_permu.out", "w")) == NULL)
    {
      fprintf(stderr, "\nUnable to open summary_permu.out for writing.\n\n");
      exit(EXIT_FAILURE);
    }
  }
  else
    max_permutations = 1;

  max_init_cond = MAX_INIT;  

  for (permu = 0; permu < max_permutations; permu++)
  {
  /*** begin: pre-processing for permutations ***/
  if (permu > 0) 
  {
    max_init_cond = MAX_INIT_FOR_PERMU; 

    if (permu == 1) fprintf(fp_out, "\nComputing LD permutations...\n");

    permute_alleles(data_ar, n_loci, n_recs); 

    /* initialize values for first obs from last permu */
    /* values for subsequent obs do not need inititialization */
    strcpy(pheno[0], "\0"); 
    for (i = 0; i < (int)pow(2, n_loci - 1); i++) 
    {
      strcpy(geno[i][0], "\0");
      strcpy(geno[i][1], "\0");
    }

    /* initialize genopheno from last permu */
    for (i = 0; i < MAX_GENOS; i++)
    {
      for (j = 0; j < n_recs; j++) genopheno[i][j] = 0;
    }

    /* initialize allele freqs from last permu */
    for (j = 0; j < n_loci; j++)
    {
      for (i = 0; i < MAX_ALLELES; i++) allele_freq[j][i] = 0;
    }
  }
  /*** end: pre-processing for permutations ***/

  /********* begin: arranging unique phenotypes and genotypes ************/
  n_hetero = n_hetero_prev = 0;
  n_geno = n_geno_prev = 1;
  /* begin by counting the unique phenotypes and genotypes */

  for (locus = 0; locus < n_loci; locus++)
  {
    col_0 = locus * 2;
    col_1 = col_0 + 1;

    if (strcmp(data_ar[0][col_0], data_ar[0][col_1]))
    {
      n_hetero++;
      if (strcmp(data_ar[0][col_0], data_ar[0][col_1]) > 0)
      {
        strcpy(buff, data_ar[0][col_0]);
        strcpy(data_ar[0][col_0], data_ar[0][col_1]);
        strcpy(data_ar[0][col_1], buff);
      }
    }
    strcat(pheno[0], data_ar[0][col_0]);
    strcat(pheno[0], data_ar[0][col_1]);

    /* update num distinct genotypes current locus loop */
    n_geno_prev = n_geno;
    if (n_hetero > 0)
      n_geno = (int)pow(2, n_hetero - 1);
    else
      n_geno = 1;

    if ((n_geno > 1) && (n_hetero - n_hetero_prev == 1))
    {
      /* copy current geno sequence to create multiple genos for this pheno */
      for (i = n_geno_prev; i < 2 * n_geno_prev; i++)
      {
        strcat(geno[i][0], geno[i - n_geno_prev][0]);
        strcat(geno[i][1], geno[i - n_geno_prev][1]);
      }
      /* fill in next portion of genotype */
      for (i = 0; i < n_geno; i++)
      {
        if (i < n_geno / 2)  /* fill in in normal order */
        {
          strcat(geno[i][0], data_ar[0][col_0]);
          strcat(geno[i][1], data_ar[0][col_1]);
        }
        else      /* fill in in reverse order */
        {
          strcat(geno[i][0], data_ar[0][col_1]);
          strcat(geno[i][1], data_ar[0][col_0]);
        }
      }
    }
    else      /* n_geno is 1 or curr site is homozygous */
    {
      for (i = 0; i < n_geno; i++)
      {
        strcat(geno[i][0], data_ar[0][col_0]);
        strcat(geno[i][1], data_ar[0][col_1]);
      }
    }
    n_hetero_prev = n_hetero;
  }        /* end of loop for a locus */

  unique_pheno_count = 0;
  unique_geno_count = n_geno - 1;
  numgeno[0] = n_geno;
  obspheno[0] = 1;

  /* assign genotype-phenotype relationships */
  for (i = 0; i < numgeno[0]; i++)
  {
    genopheno[i][0] = 1;
  }

  /* process remaining data records */
  /* loop starts at one because we've already done one line */
  for (obs = 1; obs < n_recs; obs++)
  {
    temp_pheno[0] = '\0';
    for (locus = 0; locus < n_loci; locus++)
    {
      col_0 = locus * 2;
      col_1 = col_0 + 1;

      if ((strcmp(data_ar[obs][col_0], data_ar[obs][col_1])) > 0)
      {
        strcpy(buff, data_ar[obs][col_0]);
        strcpy(data_ar[obs][col_0], data_ar[obs][col_1]);
        strcpy(data_ar[obs][col_1], buff);
      }

      strcat(temp_pheno, data_ar[obs][col_0]);
      strcat(temp_pheno, data_ar[obs][col_1]);
    }
    /* check whether this is a new distinct phenotype */
    unique_pheno_flag = TRUE;
    for (i = 0; i <= unique_pheno_count; i++)  /* RS changed from < to <= */
    {
      if (!strcmp(temp_pheno, pheno[i]))
      {
        unique_pheno_flag = FALSE;
        obspheno[i] += 1;
      }
    }

    if (unique_pheno_flag == TRUE)
    {
      /* determine genotypes for the new phenotype */

      n_hetero_prev = n_hetero = 0;
      n_geno_prev = n_geno = 1;

      for (i = 0; i < (int)pow(2, n_loci - 1); i++) 
      {
        strcpy(temp_geno[i][0], "\0");
        strcpy(temp_geno[i][1], "\0");
      }

      for (locus = 0; locus < n_loci; locus++)
      {
        col_0 = locus * 2;
        col_1 = col_0 + 1;

        if (strcmp(data_ar[obs][col_0], data_ar[obs][col_1]))
          n_hetero++;
        n_geno_prev = n_geno;

        if (n_hetero > 0)
          n_geno = (int)pow(2, n_hetero - 1);
        else
          n_geno = 1;

        if ((n_geno > 1) && (n_hetero - n_hetero_prev == 1))
        {
          /* copy current sequence to create multiple genos for this pheno */
          for (i = n_geno_prev; i < 2 * n_geno_prev; i++)
          {
            strcat(temp_geno[i][0], temp_geno[i - n_geno_prev][0]);
            strcat(temp_geno[i][1], temp_geno[i - n_geno_prev][1]);
          }

          /* fill in next portion */
          for (i = 0; i < n_geno; i++)
          {
            if (i < n_geno / 2)
            {
              strcat(temp_geno[i][0], data_ar[obs][col_0]);
              strcat(temp_geno[i][1], data_ar[obs][col_1]);
            }
            else    /* fill in reverse order */
            {
              strcat(temp_geno[i][0], data_ar[obs][col_1]);
              strcat(temp_geno[i][1], data_ar[obs][col_0]);
            }
          }
        }
        else      /* n_geno == 1 or current site not heterozygous */
        {
          for (i = 0; i < n_geno; i++)
          {
            strcat(temp_geno[i][0], data_ar[obs][col_0]);
            strcat(temp_geno[i][1], data_ar[obs][col_1]);
          }
        }

        n_hetero_prev = n_hetero;

      }        /* END for each locus */

      unique_pheno_count += 1;
      strcpy(pheno[unique_pheno_count], temp_pheno);
      numgeno[unique_pheno_count] = n_geno;
      obspheno[unique_pheno_count] = 1;

      /* check for new distinct genotypes */
      for (i = 0; i < n_geno; i++)
      {
        unique_geno_flag = TRUE;

        for (j = 0; j <= unique_geno_count; j++)  /* RS changed from < to <= */
        {
          if (((!strcmp(temp_geno[i][0], geno[j][0])) &&
               (!strcmp(temp_geno[i][1], geno[j][1]))) ||
              ((!strcmp(temp_geno[i][0], geno[j][1])) &&
               (!strcmp(temp_geno[i][1], geno[j][0]))))
          {
            unique_geno_flag = FALSE;
          }
        }

        if (unique_geno_flag == TRUE)
        {
          unique_geno_count++;
          strcpy(geno[unique_geno_count][0], temp_geno[i][0]);
          strcpy(geno[unique_geno_count][1], temp_geno[i][1]);
          genopheno[unique_geno_count][unique_pheno_count] = 1;
        }
      }
    }        /* END of if unique_pheno_flag == TRUE */
  }          /* END of loop for each observation */

  n_unique_pheno = unique_pheno_count + 1;
  n_unique_geno = unique_geno_count + 1;

  /********* end: arranging unique phenotypes and genotypes ************/

  id_unique_alleles(data_ar, unique_allele, n_unique_allele, allele_freq, 
    n_loci, n_recs);

  n_haplo = count_unique_haplos(geno, haplo, haplocus, unique_allele, 
    n_unique_allele, n_unique_geno, n_loci, xgeno, xhaplo);

  if (permu == 0)
  {
    fprintf(fp_out, "n_unique_pheno: %d \n", n_unique_pheno);
    fprintf(fp_out, "n_unique_geno: %d \n", n_unique_geno);
    fprintf(fp_out, "n_haplo: %d \n\n", n_haplo);
  }

/*** --- List each obs pheno and corresponding possible genos
  for(i = 0; i < n_unique_pheno; i++) 
  { 
    fprintf(fp_out, "pheno: %s obspheno: %d numgeno %d \n", pheno[i], obspheno[i], numgeno[i]); 
    count = 0;
    for(j = 0; j < n_unique_geno; j++) 
    { 
      if(genopheno[j][i] == 1)
      { 
        count += 1;
        fprintf(fp_out, "possible geno: %d %s %s xgeno: %d %d j: %d \n", count, geno[j][0],  geno[j][1], 
          xgeno[j][0],  xgeno[j][1], j); 
      } 
    } 
    fprintf(fp_out, "\n"); 
  } 
***/

/*** --- List all genos observed and haplos
  for(i = 0; i < n_unique_geno; i++)
  {
    fprintf(fp_out, "geno[%d][0]:%s geno[%d][1]:%s\n", i, geno[i][0], i, geno[i][1]);
  }
  for(i = 0; i < n_haplo; i++)
  {
    fprintf(fp_out, "haplo[%d]: %s\n", i, haplo[i]);
  }
***/

  if (permu == 0)
  {
    /* Compute haplotype freqs under no LD and store them temporarily in freq_zero */
    haplo_freqs_no_ld(freq_zero, allele_freq, haplocus, n_unique_allele, 
      n_loci, n_haplo);

    /* Compute log likelihood under no LD */
    loglike0 = loglikelihood(genopheno, freq_zero, obspheno, n_haplo, 
      n_unique_geno, n_unique_pheno, xhaplo, xgeno);
  
    fprintf(fp_out, "Log likelihood under no LD: %f \n", loglike0);
  }

  /* Set initial haplotype frequencies  before EM calc */
  for (i = 0; i < n_haplo; i++)
  {
    freq_zero[i] = 1.0 / (double)n_haplo;
  }

  emcalc(genopheno, numgeno, obspheno, freq_zero, mle, n_haplo,
    n_unique_geno, n_unique_pheno, n_recs, xhaplo, xgeno, 
    &error_flag, &iter_count, &loglike);

  if (permu == 0)
  {
    fprintf(fp_iter, "\n   --- Iteration Summary for Original Data -------------------------------------------\n");
      fprintf(fp_iter, "   Init. condition   0: Log likelihood after %3d iterations: %f, error_flag: %d \n",
      iter_count, loglike, error_flag);
  }

  loglike_best = loglike;
  iter_count_best = iter_count;
  error_flag_best = error_flag;
  for (i = 0; i < n_haplo; i++)
  { 
    mle_best[i] = mle[i]; 
  } 

  for (init_cond = 1; init_cond < max_init_cond; init_cond++)
  {
    freq_sum = 0;
    for (i = 0; i < n_haplo; i++)
    { 
      freq_zero[i] = drand48(); 
      freq_sum += freq_zero[i];
    }
    for (i = 0; i < n_haplo; i++)
    { 
      freq_zero[i] = freq_zero[i] / freq_sum; 
    }
  
    emcalc(genopheno, numgeno, obspheno, freq_zero, mle, n_haplo,
      n_unique_geno, n_unique_pheno, n_recs, xhaplo, xgeno, 
      &error_flag, &iter_count, &loglike);

    if (permu == 0)
    {
      fprintf(fp_iter, "   Init. condition %3d: Log likelihood after %3d iterations: %f, error_flag: %d \n",
        init_cond, iter_count, loglike, error_flag);
    }

    if (error_flag_best == 0)
    {
      if ((loglike > loglike_best) && (error_flag == 0))
      {
        loglike_best = loglike;
        iter_count_best = iter_count;
        error_flag_best = error_flag;
        for (i = 0; i < n_haplo; i++)
        { 
          mle_best[i] = mle[i]; 
        } 
      }
    }
    else /* (error_flag_best != 0) */ 
    {
      if (error_flag == 0)
      {
        loglike_best = loglike;
        iter_count_best = iter_count;
        error_flag_best = error_flag;
        for (i = 0; i < n_haplo; i++)
        { 
          mle_best[i] = mle[i]; 
        } 
      }
    }
  }

  if (permu_flag == 1)
  {
    fprintf(fp_permu, "Log likelihood under no LD: %f \n", loglike0);
    fprintf(fp_permu, "permu = %3d, ", permu );
  }

  if (permu == 0)
  {
    fprintf(fp_iter, "\n"); 
    fprintf(fp_iter, "   --- Codes for error_flag ----------------------------------------------------------\n"); 
    fprintf(fp_iter, "    0: Iterations Converged, no errors \n");
    fprintf(fp_iter, "    1: There are no ambiguous haplotypes \n");
    fprintf(fp_iter, "    2: Normalization constant near zero. Est. HFs unstable \n");
    fprintf(fp_iter, "    3: Wrong # allocated for at least one phenotype based on est. HFs \n");
    fprintf(fp_iter, "    4: Phenotype freq., based on est. HFs, is 0 for an observed phenotype \n");
    fprintf(fp_iter, "    5: Log likelihood has decreased for more than 5 iterations \n");
    fprintf(fp_iter, "    6: Est. HFs do not sum to 1.0 \n");
    fprintf(fp_iter, "    7: Log likelihood failed to converge in %d iterations \n", MAX_ITER);
    fprintf(fp_iter, "   -----------------------------------------------------------------------------------\n"); 
    fprintf(fp_iter, "\n"); 

    if (error_flag_best == 0)
      fprintf(fp_out, "Log likelihood converged in %3d iterations to : %f \n", 
        iter_count_best, loglike_best);
    else if (error_flag_best == 1)
      fprintf(fp_out, "There are no ambiguous haplotypes.              %f\n", loglike_best);
    else if (error_flag_best == 2)
      fprintf(fp_out, "Normalization constant near zero. Estimated HFs unstable.\n");
    else if (error_flag_best == 3)
      fprintf(fp_out, "Wrong # allocated for at least one phenotype based on estimated HFs.\n");
    else if (error_flag_best == 4)
      fprintf(fp_out, "Phenotype freq., based on estimated HFs, was 0 for an observed phenotype.\n");
    else if (error_flag_best == 5)
      fprintf(fp_out, "Log likelihood has decreased for more than 5 iterations.\n");
    else if (error_flag_best == 6)
      fprintf(fp_out, "Estimated HFs do not sum to 1.\n");
    else /* (error_flag_best == 7) */
      fprintf(fp_out, "Log likelihood failed to converge in %d iterations \n", MAX_ITER);

    j = 0;
    fprintf(fp_out, "\n \t MLE frequency \t haplo (MLE > .00001) \n");
    for (i = 0; i < n_haplo; i++)
    {
      if (mle_best[i] > .00001)
      {
        j += 1;
        fprintf(fp_out, "%d \t %f \t %s\n", j, mle_best[i], haplo[i]);
      }
    }

    fprintf(fp_out, "\nAllele frequencies\n");
    fprintf(fp_out, "------------------\n");
    fprintf(fp_out, "Frequency \t Locus \t Allele\n");
    for (i = 0; i < n_loci; i++)
    {
      for (j = 0; j < n_unique_allele[i]; j++)
      {
        fprintf(fp_out, "%f \t %d \t %s \n", allele_freq[i][j], i, 
          unique_allele[i][j]);
      }
    }

    linkage_diseq(fp_out, mle_best, haplocus, allele_freq, unique_allele, n_unique_allele, 
      n_loci, n_haplo, n_recs);
  }

  if (permu_flag == 1)
  {
    if (error_flag_best == 0)
      fprintf(fp_permu, "Log likelihood converged in %3d iterations to : %f \n", 
        iter_count_best, loglike_best);
    else if (error_flag_best == 1)
      fprintf(fp_permu, "There are no ambiguous haplotypes.              %f\n", loglike_best);
    else if (error_flag_best == 2)
      fprintf(fp_permu, "Normalization constant near zero. Estimated HFs unstable.\n");
    else if (error_flag_best == 3)
      fprintf(fp_permu, "Wrong # allocated for at least one phenotype based on estimated HFs.\n");
    else if (error_flag_best == 4)
      fprintf(fp_permu, "Phenotype freq., based on estimated HFs, was 0 for an observed phenotype.\n");
    else if (error_flag_best == 5)
      fprintf(fp_permu, "Log likelihood has decreased for more than 5 iterations.\n");
    else if (error_flag_best == 6)
      fprintf(fp_permu, "Estimated HFs do not sum to 1.\n");
    else /* (error_flag_best == 7) */
      fprintf(fp_permu, "Log likelihood failed to converge in %d iterations \n", MAX_ITER);
  }

  like_ratio[permu] = -2.0 * (loglike0 - loglike_best);

  } /* end for (permu) */
  
  /*** begin: post-processing for permutations ***/
  if (permu_flag == 1)
  {
    pvalue = 0.0;
    fprintf(fp_permu, "permu =   0, LR = -2*(LL_0 - LL_1) = %f \n", like_ratio[0]); 
    for (i = 1; i < max_permutations; i++)
    {
      fprintf(fp_permu, "permu = %3d, LR = -2*(LL_0 - LL_1) = %f \n", i, like_ratio[i]); 
      if (like_ratio[i] > like_ratio[0]) pvalue += 1;
    }
    pvalue = pvalue/max_permutations;
    fprintf(fp_out, "\nLD permutation pvalue = %f \n", pvalue); 
    fprintf(fp_permu, "pvalue = %f \n", pvalue); 
    fclose(fp_permu);
  }
  /*** end: post-processing for permutations ***/

  return (EXIT_SUCCESS);
}

/************************************************************************/
int count_unique_haplos(char (*geno_ar)[2][LINE_LEN / 2],
      char (*haplo_ar)[LINE_LEN / 2], int (*haplocus)[MAX_LOCI], 
      char (*unique_allele)[MAX_ALLELES][NAME_LEN],
      int *n_unique_allele, int num_genos, int num_loci,
      int (*xgeno)[2], int *xhaplo)
/* 
  * run through the array of possible genotypes 
  * create an array of possible haplotypes 
  * create haplocus[i][j]: a 2-dim array of allele# at jth locus of ith haplotype
*/
{
  int i, j, k;
  int unique_haplo_flag, unique_haplo_count;
  char *temp_ptr;
  char temp_array[MAX_LOCI][NAME_LEN];  
  int l, m;
  static char temp_buff[LINE_LEN / 2];

  /* 0th assignment */
  unique_haplo_count = 0;
  strcpy(haplo_ar[0], geno_ar[0][0]);
  xhaplo[0] = 0;
  xgeno[0][0] = 0;

  /* split haplo_ar[0] into temp_array on ":" and add trailing ":" */
  strcpy(temp_buff, haplo_ar[0]);
  temp_ptr = strtok(temp_buff,":");
  if (temp_ptr) 
  {
    strcpy(temp_array[0], temp_ptr);
    strcat(temp_array[0], ":");
    for (k = 1; k < num_loci; k++) /* start at 1 since 0th is done */
    {
      temp_ptr = strtok(NULL,":");
      if (temp_ptr) 
      {  
        strcpy(temp_array[k], temp_ptr);
        strcat(temp_array[k], ":");
      }  
    }
  }
/* RS --- CHECKING
  for (k = 0; k < num_loci; k++) 
  {
    fprintf(stdout, "haplo_ar[0]: %s temp_array[%d]: %s \n", 
            haplo_ar[0], k, temp_array[k]); 
  }
*/

  /* identify allele# at lth locus for 0th haplotype */
  for (l = 0; l < num_loci; l++) 
  {
    for (m = 0; m < n_unique_allele[l]; m++) 
    {
      if (!strcmp(temp_array[l], unique_allele[l][m])) 
        haplocus[0][l] = m;
    }
  }

  for (i = 0; i < num_genos; i++)
  {
    for (j = 0; j < 2; j++)
    {
      unique_haplo_flag = TRUE;
      for (k = 0; k <= unique_haplo_count && unique_haplo_flag == TRUE; k++)
      {
        if (!strcmp(geno_ar[i][j], haplo_ar[k]))
        {  
          unique_haplo_flag = FALSE;
          xgeno[i][j] = k;
        }  
      }
      if (unique_haplo_flag == TRUE)
      {
        strcpy(haplo_ar[++unique_haplo_count], geno_ar[i][j]);
        xhaplo[unique_haplo_count] = unique_haplo_count; 
        xgeno[i][j] = unique_haplo_count;
/*   fprintf(stdout, "xgeno[%d][%d]:%d \n", i,j,xgeno[i][j]); */

        /* split haplo_ar[unique_haplo_count] into temp_array ... */
        strcpy(temp_buff, haplo_ar[unique_haplo_count]);
        temp_ptr = strtok(temp_buff,":");
        if (temp_ptr) 
        {
          strcpy(temp_array[0], temp_ptr);
          strcat(temp_array[0], ":");
          for (k = 1; k < num_loci; k++) /* start at 1 since 0th is done */
          {
            temp_ptr = strtok(NULL,":");
            if (temp_ptr) 
            {  
              strcpy(temp_array[k], temp_ptr);
              strcat(temp_array[k], ":");
            }  
          }
        }
/* RS --- CHECKING
        for (k = 0; k < num_loci; k++) 
        {
          fprintf(stdout, "haplo_ar[%d]: %s temp_array[%d]: %s \n", 
                  unique_haplo_count, haplo_ar[unique_haplo_count], 
                  k, temp_array[k]); 
        }
*/

        /* identify allele# at lth locus for unique_haplo_count haplotype */
        for (l = 0; l < num_loci; l++) 
        {
          for (m = 0; m < n_unique_allele[l]; m++) 
          {
            if (!strcmp(temp_array[l], unique_allele[l][m])) 
              haplocus[unique_haplo_count][l] = m;
          }
        }

      }
    }
  }

  return unique_haplo_count + 1;
}

/************************************************************************/
void id_unique_alleles(char (*data_ar)[MAX_COLS][NAME_LEN],
           char (*unique_allele)[MAX_ALLELES][NAME_LEN],
           int *n_unique_allele, double (*allele_freq)[MAX_ALLELES],
           int n_loci, int n_recs)
/* 
   * Creates unique_allele[i][j]: jth unique allele for the ith locus        
   * Creates n_unique_allele[i]: number of unique alleles for the ith locus 
   * Creates allele_freq[i][j]:  freq for jth allele at the ith locus 
*/
{
  int i, j, locus, col_0, col_1;
  int unique_allele_flag, unique_allele_count;

/* CHECKING
  for (i = 0; i < n_recs; i++)
  for (j = 0; j < 2*n_loci; j++)
  fprintf(stdout, "data[%d][%d]: %s\n", i, j, data_ar[i][j]); 
  fprintf(stdout, "data0[%d][%d]: %s, uniq[%d][%d]:\n", i, col_0, 
    data_ar[i][j], locus, j, unique_allele[locus][j]); 
*/

  for (locus = 0; locus < n_loci; locus++)
  {
    col_0 = locus * 2;
    col_1 = col_0 + 1;
    strcpy(unique_allele[locus][0], data_ar[0][col_0]);
    unique_allele_count = 0;

    for (i = 0; i < n_recs; i++)
    {
      /* Process col_0 of current locus */
      unique_allele_flag = TRUE;
      for (j = 0; j <= unique_allele_count; j++)
      {
        if (!strcmp(data_ar[i][col_0], unique_allele[locus][j]))
        {
          unique_allele_flag = FALSE;
          allele_freq[locus][j] += 1;

        }
      }
      if (unique_allele_flag == TRUE)
      {
        unique_allele_count += 1;
        strcpy(unique_allele[locus][unique_allele_count], data_ar[i][col_0]);
        allele_freq[locus][unique_allele_count] += 1;
      }

      /* Process col_1 of current locus */
      unique_allele_flag = TRUE;
      for (j = 0; j <= unique_allele_count; j++)
      {
        if (!strcmp(data_ar[i][col_1], unique_allele[locus][j]))
        {
          unique_allele_flag = FALSE;
          allele_freq[locus][j] += 1;
        }
      }
      if (unique_allele_flag == TRUE)
      {
        unique_allele_count += 1;
        strcpy(unique_allele[locus][unique_allele_count], data_ar[i][col_1]);
        allele_freq[locus][unique_allele_count] += 1;
      }
    }
    n_unique_allele[locus] = unique_allele_count + 1;

    for(j = 0; j < n_unique_allele[locus]; j++)
    {
      allele_freq[locus][j] = allele_freq[locus][j] / (2*(double)n_recs);
    }
  }

}

/************************************************************************/
double min(double a, double b)
{
  if (a < b)
    return (a);
  else
    return (b);
}

/************************************************************************/
void linkage_diseq(FILE * fp_out, double (*mle), int (*hl)[MAX_LOCI],
       double (*af)[MAX_ALLELES], 
       char (*unique_allele)[MAX_ALLELES][NAME_LEN],
       int *n_unique_allele, int n_loci, int n_haplo, int n_recs)
       /* hl: haplocus array           */
       /* af: allele_frequencies array */
{
  int i, j, k, l, m, coeff_count;
  static double dij[MAX_LOCI*(MAX_LOCI - 1)/2][MAX_ALLELES][MAX_ALLELES];
  double dmax, norm_dij; 
  double summary_dprime[MAX_LOCI*(MAX_LOCI - 1)/2]; 
  double summary_q[MAX_LOCI*(MAX_LOCI - 1)/2]; 
  double summary_wn[MAX_LOCI*(MAX_LOCI - 1)/2]; 
  double sum; /* used to check sums */

  /* After 1st pass dij[coeff_count][locusA_allele#][locusB_allele#] */
  /*   contains Estimated 2-locus HFs based on full MLE HFs          */
  /*   coeff_count runs from 0 to nCr(n_loci,2)                      */                     
  for (i = 0; i < n_haplo; i++)
  {
    coeff_count = 0;
    for (j = 0; j < n_loci; j++)
    {
      for (k = j+1; k < n_loci; k++)
      {
        dij[coeff_count][ hl[i][j] ][ hl[i][k] ] = 
          dij[coeff_count][ hl[i][j] ][ hl[i][k] ] + mle[i];
        coeff_count += 1;
      }
    }
  }

/* CHECKING inner loop
          fprintf(stdout,"Loci: %d %d dij[%d][%d][%d]: %f \n", 
            j, k, coeff_count, l, m, dij[coeff_count][l][m]);
*/
  /* print Estimated Observed Counts (2*n_recs*dij) */
  fprintf(fp_out,"\nEstimated Observed Counts\n");
  fprintf(fp_out,"-------------------------\n");
  coeff_count = 0;
  for (j = 0; j < n_loci; j++)
  {
    for (k = j+1; k < n_loci; k++)
    {
      fprintf(fp_out,"--Loci:%2d\\%2d-- (Estimated Observed Counts)\n", j, k);
      fprintf(fp_out,"%10s ", " ");
      for (m = 0; m < n_unique_allele[k]; m++)
        fprintf(fp_out,"%10s ", unique_allele[k][m]);
      fprintf(fp_out,"\n");
      sum = 0.0; /* CHECKING sum */
      for (l = 0; l < n_unique_allele[j]; l++)
      {
        fprintf(fp_out,"%10s ", unique_allele[j][l]);
        for (m = 0; m < n_unique_allele[k]; m++)
        {
          fprintf(fp_out,"%10.4f ", 2 * (double)n_recs * dij[coeff_count][l][m]);
          sum += 2 * (double)n_recs * dij[coeff_count][l][m];
        }
        fprintf(fp_out,"\n"); 
      }
      coeff_count += 1;
/* CHECKING sum
      fprintf(stdout,"\t 2*n_recs: %d sum: %f \n", 2*n_recs, sum); 
*/
    }
  }

  /* print Expected Counts under No LD */
  fprintf(fp_out,"\nExpected Counts with No LD\n");
  fprintf(fp_out,"--------------------------\n");
  coeff_count = 0;
  for (j = 0; j < n_loci; j++)
  {
    for (k = j+1; k < n_loci; k++)
    {
      fprintf(fp_out,"--Loci:%2d\\%2d-- (Expected Counts with No LD)\n", j, k);
      fprintf(fp_out,"%10s ", " ");
      for (m = 0; m < n_unique_allele[k]; m++)
        fprintf(fp_out,"%10s ", unique_allele[k][m]);
      fprintf(fp_out,"\n");
      sum = 0.0; /* CHECKING sum */
      for (l = 0; l < n_unique_allele[j]; l++)
      {
        fprintf(fp_out,"%10s ", unique_allele[j][l]);
        for (m = 0; m < n_unique_allele[k]; m++)
        {
          fprintf(fp_out,"%10.4f ", 2 * (double)n_recs * af[j][l] * af[k][m]);
          sum += 2 * (double)n_recs * af[j][l] * af[k][m];
        }
        fprintf(fp_out,"\n");
      }
      coeff_count += 1;
/* CHECKING sum
      fprintf(stdout,"\t 2*n_recs: %d sum: %f \n", 2*n_recs, sum); 
*/
    }
  }

  /* print   Individual 1-df Chi-square Statistics */
  /* compute disequilibrium values overwriting dij[][][] */
  fprintf(fp_out,"\nSingle d.f. Chi-squares\n");
  fprintf(fp_out,"-----------------------\n");
  coeff_count = 0;
  for (j = 0; j < n_loci; j++)
  {
    for (k = j+1; k < n_loci; k++)
    {
      fprintf(fp_out,"--Loci:%2d\\%2d-- (Single d.f. Chi-squares)\n", j, k);
      fprintf(fp_out,"%10s ", " ");
      for (m = 0; m < n_unique_allele[k]; m++)
        fprintf(fp_out,"%10s ", unique_allele[k][m]);
      fprintf(fp_out,"\n");
      for (l = 0; l < n_unique_allele[j]; l++)
      {
        fprintf(fp_out,"%10s ", unique_allele[j][l]);
        for (m = 0; m < n_unique_allele[k]; m++)
        {
          dij[coeff_count][l][m] -= af[j][l] * af[k][m];
          fprintf(fp_out,"%10.4f ", pow(dij[coeff_count][l][m], 2) * 
            2 * (double)n_recs / ( af[j][l]*(1-af[j][l])*af[k][m]*(1-af[k][m]) ));
        }
        fprintf(fp_out,"\n");
      }
      coeff_count += 1;
    }
  }

  /* print   d_ij values */
  /* compute summary_q and summary_wn */
  fprintf(fp_out,"\nDisequilibrium Values (d_ij)\n");
  fprintf(fp_out,"----------------------------\n");
  coeff_count = 0;
  for (j = 0; j < n_loci; j++)
  {
    for (k = j+1; k < n_loci; k++)
    {
      summary_q[coeff_count] = 0;
      fprintf(fp_out,"--Loci:%2d\\%2d-- (d_ij)\n", j, k);
      fprintf(fp_out,"%10s ", " ");
      for (m = 0; m < n_unique_allele[k]; m++)
        fprintf(fp_out,"%10s ", unique_allele[k][m]);
      fprintf(fp_out,"\n");
      for (l = 0; l < n_unique_allele[j]; l++)
      {
        fprintf(fp_out,"%10s ", unique_allele[j][l]);
        for (m = 0; m < n_unique_allele[k]; m++)
        {
          fprintf(fp_out,"%10.4f ", dij[coeff_count][l][m]);
          summary_q[coeff_count] += 2 * (double)n_recs * 
            pow(dij[coeff_count][l][m], 2) / ( af[j][l] * af[k][m] ) ;
        }
        fprintf(fp_out,"\n");
      }
      summary_wn[coeff_count]  = sqrt( summary_q[coeff_count] / 
        ( 2*(double)n_recs * (min(n_unique_allele[j],n_unique_allele[k])-1) ) );
      coeff_count += 1;
    }
  }

  /* print   dprime_ij values */
  /* compute dprime_ij values and summary_dprime */
  fprintf(fp_out,"\nNormalized Disequilibrium Values (d'_ij)\n");
  fprintf(fp_out,"----------------------------------------\n");
  coeff_count = 0;
  for (j = 0; j < n_loci; j++)
  {
    for (k = j+1; k < n_loci; k++)
    {
      summary_dprime[coeff_count] = 0;
      fprintf(fp_out,"--Loci:%2d\\%2d-- (d'_ij = d_ij/dmax)\n", j, k);
      fprintf(fp_out,"%10s ", " ");
      for (m = 0; m < n_unique_allele[k]; m++)
        fprintf(fp_out,"%10s ", unique_allele[k][m]);
      fprintf(fp_out,"\n");
      for (l = 0; l < n_unique_allele[j]; l++)
      {
        fprintf(fp_out,"%10s ", unique_allele[j][l]);
        for (m = 0; m < n_unique_allele[k]; m++)
        {
          if (dij[coeff_count][l][m] > 0)
          {
            dmax = min( af[j][l]*(1-af[k][m]), (1-af[j][l])*af[k][m] );
            norm_dij = dij[coeff_count][l][m] / dmax;
          }
          else if (dij[coeff_count][l][m] < 0)
          {
            dmax = min( af[j][l]*af[k][m], (1-af[j][l])*(1-af[k][m]) );
            norm_dij = dij[coeff_count][l][m] / dmax;
          }
          else
            norm_dij = 0; 
          fprintf(fp_out,"%10.4f ", norm_dij);
          summary_dprime[coeff_count] += af[j][l] * af[k][m] * fabs(norm_dij);
        }
        fprintf(fp_out,"\n");
      }
      coeff_count += 1;
    }
  }

  /* print   summary measures */
  fprintf(fp_out,"\nDisequilibrium Summary Measures\n");
  fprintf(fp_out,"-------------------------------\n");
  coeff_count = 0;
  for (j = 0; j < n_loci; j++)
  {
    for (k = j+1; k < n_loci; k++)
    {
      fprintf(fp_out,"--Loci:%2d\\%2d--\n", j, k);
      fprintf(fp_out,"             Wn [Cohen, 1988]: %10.4f\n", summary_wn[coeff_count]);
      fprintf(fp_out,"               Q [Hill, 1975]: %10.4f (approx. Chi-square %d)\n", 
        summary_q[coeff_count], (n_unique_allele[j]-1)*(n_unique_allele[k]-1) );
      fprintf(fp_out,"       Dprime [Hedrick, 1987]: %10.4f\n", summary_dprime[coeff_count]);
      coeff_count += 1;
    }
  }

}

/************************************************************************/
void sort2arrays(char (*array1)[LINE_LEN / 2], double *array2, int n_haplo)
/* insertion sort in ascending order for 1st array also applied to 2nd array */
{
  int i, j;
  char temp1[LINE_LEN / 2];
  double temp2;

  for (i = 1; i < n_haplo; ++i)
  {
    for (j = i; (j - 1) >= 0 && strcmp(array1[j - 1], array1[j]) > 0; --j)
    {
      strcpy(temp1, array1[j]);
      strcpy(array1[j], array1[j - 1]);
      strcpy(array1[j - 1], temp1);
      temp2 = array2[j];
      array2[j] = array2[j - 1];
      array2[j - 1] = temp2;
    }
  }
}

/************************************************************************/
void emcalc(int (*genopheno)[MAX_ROWS], int *numgeno, int *obspheno,
      double *freq_zero, double *mle, int n_haplo, int n_unique_geno,
      int n_unique_pheno, int n_recs, int *xhaplo, int (*xgeno)[2], 
      int *error_flag, int *iter_count, double *loglike)
{
  int i, j, k, l;
  int done, decr_loglike_count, tot_hap;
  int iter, k_pheno, i_geno, i_haplo, j_haplo, keep;
  double unambig[MAX_HAPLOS], ambig[MAX_HAPLOS], ambig_sum;
  static double hap_freq[MAX_HAPLOS][MAX_ITER], addto_ambig[MAX_HAPLOS];
  double expected_freq, expected_freq_sum, normed_addto_ambig_sum, diff; 
  double geno_freq[MAX_GENOS], pheno_freq[MAX_ROWS], prev_loglike, freqsum;

  done = FALSE;
  decr_loglike_count = 0;
  tot_hap = 2 * n_recs;
  *error_flag = 0;

  for (i = 0; i < n_haplo; i++)
  {
    unambig[i] = 0;
    ambig[i] = 0;
  }

  /* Pre-process for first iteration */
  for (i = 0; i < n_unique_geno; i++)
  {
    for (j = 0; j < 2; j++)
    {
      for (k = 0; k < n_haplo; k++)
      {
        for (l = 0; l < n_unique_pheno; l++)
        {
          if ((xgeno[i][j] == xhaplo[k]) && (genopheno[i][l] != 0))
          {
            if (numgeno[l] == 1)
            {
              unambig[k] += (double)obspheno[l];
            }
            else /* (numgeno[l] > 1) */
            {
              ambig[k] += (double)obspheno[l] / (double)numgeno[l];
            }
          }
        }
      }
    }
  }

  iter = 0;

  ambig_sum = 0;
  for (i = 0; i < n_haplo; i++)
  {
    ambig_sum += ambig[i];
    hap_freq[i][iter] = freq_zero[i];
  }

  /* Test for observed ambiguous phenos */
  if (ambig_sum == 0)
  {
    iter = 1;
    *error_flag = 1;
    for (i = 0; i < n_haplo; i++)
    {
      hap_freq[i][iter] = unambig[i] / (double)tot_hap;
      mle[i] = hap_freq[i][iter];
    }
    *loglike = loglikelihood(genopheno, mle, obspheno, n_haplo,
      n_unique_geno, n_unique_pheno, xhaplo, xgeno);
  }

  /* Begin E-M iterations on ambiguous phenos */
  else /* (ambig_sum > 0) */
  {
    for (iter = 1; iter < MAX_ITER && done == FALSE; iter++)
    {
      for (k = 0; k < n_haplo; k++)
      {
        ambig[k] = 0;
      }
      for (k_pheno = 0; k_pheno < n_unique_pheno; k_pheno++)
      {
        if ((numgeno[k_pheno] > 1) && (obspheno[k_pheno] >= 1))
        {
          for (k = 0; k < n_haplo; k++)
          {
            addto_ambig[k] = 0;
          }
          expected_freq_sum = 0;
          for (i_geno = 0; i_geno < n_unique_geno; i_geno++)
          {
            if (genopheno[i_geno][k_pheno] > 0)
            {
              for (k = 0; k < n_haplo; k++)
              {
                if (xgeno[i_geno][0] == xhaplo[k])
                {
                  i_haplo = k;
                }
                if (xgeno[i_geno][1] == xhaplo[k])
                {
                  j_haplo = k;
                }
              }
              /* Compute expected frequency of this geno using hap_freq */
              /* estimates from the previous iteration                  */
              if (i_haplo == j_haplo)
              {
                expected_freq = hap_freq[i_haplo][iter - 1] * hap_freq[j_haplo][iter - 1];
              }
              else
              {
                expected_freq = 2 * hap_freq[i_haplo][iter - 1] * hap_freq[j_haplo][iter - 1];
              }

              /* Add expected proportion of current pheno to addto_ambig[] for the appropriate haplo */
              addto_ambig[i_haplo] += expected_freq * (double)obspheno[k_pheno];
              addto_ambig[j_haplo] += expected_freq * (double)obspheno[k_pheno];
              expected_freq_sum += expected_freq;
            }
          }

          /* Normalize addto_ambig[] for the current pheno */
          /* Add normalized amount to ambiguous count      */
          if (expected_freq_sum < .000001)
          {
            done = TRUE;
            *error_flag = 2;
          }
          normed_addto_ambig_sum = 0;
          for (i = 0; i < n_haplo; i++)
          {
            addto_ambig[i] = addto_ambig[i] / expected_freq_sum;
            normed_addto_ambig_sum += addto_ambig[i];
            ambig[i] += addto_ambig[i];
          }

          diff = normed_addto_ambig_sum - 2 * (double)obspheno[k_pheno];
          if (fabs(diff) > .1)
          {
            done = TRUE;
            *error_flag = 3;
          }
        }
      }        /* end of loop for k_pheno */

      for (i = 0; i < n_haplo; i++)
      {
        hap_freq[i][iter] = (unambig[i] + ambig[i]) / (double)tot_hap;
      }

      /* Calculate geno freqs from current estimate of haplo freqs */
      for (i = 0; i < n_unique_geno; i++)
      {
        geno_freq[i] = 1;
        keep = 0;
        for (j = 0; j < 2; j++)
        {
          for (k = 0; k < n_haplo; k++)
          {
            if (xhaplo[k] == xgeno[i][j])
            {
              geno_freq[i] = geno_freq[i] * hap_freq[k][iter];
              if (j == 0)
              {
                keep = k;
              }
              if (k != keep)
              {
                geno_freq[i] = geno_freq[i] * 2;
              }
            }
          }
        }
      }

      /* Compute pheno freqs based on the computed geno freqs */
      for (i = 0; i < n_unique_pheno; i++)
      {
        pheno_freq[i] = 0;
        for (j = 0; j < n_unique_geno; j++)
        {
          if (genopheno[j][i] == 1)
          {
            pheno_freq[i] += geno_freq[j];
          }
        }
      }

      /* Compute the log likelihood for the current iteration */
      *loglike = 0;
      for (i = 0; i < n_unique_pheno; i++)
      {
        if (pheno_freq[i] > DBL_EPSILON)
        {
          *loglike += (double)obspheno[i] * log(pheno_freq[i]);
        }
        else
        {
          done = TRUE;
          *error_flag = 4;
        }
      }

      if (iter <= 1)
      {
        prev_loglike = *loglike;
      }
      else /* (iter > 1) */
      {
        /* Test for convergence */
        diff = *loglike - prev_loglike;
        if (fabs(diff) > CRITERION)
        {
          /* If not converged, test if likelihood is decreasing */
          if (prev_loglike > *loglike)
          {
            decr_loglike_count += 1;
            if (decr_loglike_count >= 5)
            {
              done = TRUE;
              *error_flag = 5;
            }
          }
          prev_loglike = *loglike;
        }
        else      /* ( abs(diff) <= CRITERION ) */
        {
          done = TRUE;

          freqsum = 0;
          for (i = 0; i < n_haplo; i++)
          {
            mle[i] = hap_freq[i][iter];
            freqsum += hap_freq[i][iter];
          }
          if (freqsum < .99 || freqsum > 1.01)
          {
            *error_flag = 6;
          }
        }
      }
      *iter_count = iter + 1; 
    }      /* end of loop for iter */
    if (*iter_count >= MAX_ITER) *error_flag = 7;
  }        /* end of else if ( ambig_sum > 0 ) */
}

/************************************************************************/
void haplo_freqs_no_ld(double *hap_freq, double (*allele_freq)[MAX_ALLELES],
       int (*haplocus)[MAX_LOCI], int *n_unique_allele, int n_loci, int n_haplo)
{
  int i, j, k;

  for (k = 0; k < n_haplo; k++) 
  { 
    hap_freq[k] = 1.0;
  }

  for (i = 0; i < n_loci; i++)
  {
    for (j = 0; j < n_unique_allele[i]; j++)
    {
      for (k = 0; k < n_haplo; k++)
      {
        if (haplocus[k][i] == j)
          hap_freq[k] =  hap_freq[k] * allele_freq[i][j];
      }
    }
  }
}

/************************************************************************/
double loglikelihood(int (*genopheno)[MAX_ROWS], double (*hap_freq), 
         int *obspheno, int n_haplo, int n_unique_geno, int n_unique_pheno, 
         int *xhaplo, int (*xgeno)[2])

{
  int i, j, k, keep;
  double geno_freq[MAX_GENOS], pheno_freq[MAX_ROWS], loglike;

  /* Calculate geno freqs from haplo freqs */
  for (i = 0; i < n_unique_geno; i++)
  {
    geno_freq[i] = 1.0;
    keep = 0;
    for (j = 0; j < 2; j++)
    {
      for (k = 0; k < n_haplo; k++)
      {
        if (xhaplo[k] == xgeno[i][j])
        {
          geno_freq[i] = geno_freq[i] * hap_freq[k];
          if (j == 0)
          {
            keep = k;
          }
          if (k != keep)
          {
            geno_freq[i] = geno_freq[i] * 2;
          }
        }
      }
    }
  }

  /* Compute pheno freqs based on the computed geno freqs */
  for (i = 0; i < n_unique_pheno; i++)
  {
    pheno_freq[i] = 0;
    for (j = 0; j < n_unique_geno; j++)
    {
      if (genopheno[j][i] == 1)
      {
        pheno_freq[i] += geno_freq[j];
      }
    }
  }

  /* Compute the log likelihood */
  loglike = 0;
  for (i = 0; i < n_unique_pheno; i++)
  {
    if (pheno_freq[i] > DBL_EPSILON)
    {
      loglike += (double)obspheno[i] * log(pheno_freq[i]);
    }
    else
    {
      fprintf(stdout, "\n ** Warning - Est. freq. for pheno %d < 0 + epsilon", i);
    }
  }
  return(loglike);
}

/************************************************************************/
void permute_alleles(char (*data_ar)[MAX_COLS][NAME_LEN], int n_loci, int n_recs)
{
  int i, j, locus, col_0, col_1, drawn;
  char buff[NAME_LEN];

  /* last locus not permuted */
  for (locus = 0; locus < n_loci-1; locus ++) 
  {
    col_0 = locus * 2;
    col_1 = col_0 + 1;
    for (j = n_recs-1; j >= 0; j--)
    {
      drawn = (int) (j * drand48());
      strcpy(buff, data_ar[drawn][col_0]);
      strcpy(data_ar[drawn][col_0], data_ar[j][col_0]);
      strcpy(data_ar[j][col_0], buff);
  
      strcpy(buff, data_ar[drawn][col_1]);
      strcpy(data_ar[drawn][col_1], data_ar[j][col_1]);
      strcpy(data_ar[j][col_1], buff);
    }
  }
}

