/* a translation from Richard Single's awk programme */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <float.h>  /* needed for DBL_EPSILON */

#include "emhaplofreq.h"

/************************ function prototypes****************************/

void print_usage(void);

FILE *parse_args(int, char **);
/* argc, argv */
/* returns open filehandle of input file */

int read_infile(FILE *, char (*)[], char (*)[][], int *);
/* open filehandle for data, ref array, data array, number of records */
/* returns number of loci */

int main_proc(char (*)[][], int, int);
/* data array, number of loci, number of records */
/* main procedure that handles memory allocation and creation of arrays, 
  * spawns the rest of the data preparation and processing functions, 
  * performs the EM calculation, and prints out the results. 
  * we only return from it to exit. 
*/

int count_unique_haplos(char (*)[][], char (*)[], int);
/* array of genotypes, array of haplotypes, number of unique genotypes */
/* returns number of haplotypes */
/* 
  * creates array of possible haplotypes from 
  * array of possibly observed genotypes 
*/

/* RS added (begin) */
void id_unique_alleles(char (*)[][], char (*)[][], int *, int, int);
/* data array, unique_allele array, no. of unique alleles array, no. of loci, no. of records */
/* 
  * creates array of alleles unique to each locus 
*/

void sort2dim(char (*)[][], int *, int);
/* unique_allele array, no. of unique alleles array, no. of loci */
/* 
  * insertion sort in ascending order for 2nd dimension of 2-dim array
*/

void sort2arrays(char (*)[], double *, int);
/* haplo array, mle array, no. of haplotypes */
/*
  * insertion sort in ascending order for 1st array also applied to 2nd array
*/

void emcalc(char (*)[], char (*)[][], int (*)[], int *, int *, double *,
      double *, int, int, int, int);
/* haplo, geno, genopheno, numgeno, obspheno, freq_zero, mle, n_haplo, n_unique_geno, 
   n_unique_pheno, n_recs */
/*
  * perform EM iterations with results in the mle array
*/

/* RS added (end) */

int main(int argc, char **argv)
{
  FILE *if_handle;
  char ref[MAX_ROWS][NAME_LEN];
  char data[MAX_ROWS][MAX_COLS][NAME_LEN];
  int num_loci, num_recs;
  int ret_val;

  if_handle = parse_args(argc, argv);

  num_loci = read_infile(if_handle, ref, data, &num_recs);

  ret_val = main_proc(data, num_loci, num_recs);

  return (ret_val);
}

/************************************************************************/

void print_usage(void)
{
  fprintf(stderr, "\nUsage: emhaplofreq [inputfilename].\n\n");
}

/************************************************************************/

FILE *parse_args(int arg_count, char *arg_buff[])
{
  FILE *fh;

  if (arg_count < 2)
  {
    print_usage();
    exit(EXIT_FAILURE);
  }

  for (; arg_count > 1 && arg_buff[1][0] == '-'; arg_count--, arg_buff++)
  {
    switch (arg_buff[1][1])
    {
    case 'h':
    default:
      print_usage();
      exit(EXIT_FAILURE);
      break;      /* not reached */
    }
  }

  /* what's left at argv[1] should be the name of the data file */

  if ((fh = fopen(arg_buff[1], "r")) == NULL)
  {
    perror("Unable to open file");
    fprintf(stderr, "\tOffending filename: %s\n\n", arg_buff[1]);
    exit(EXIT_FAILURE);
  }
  /* skip this until we're through testing */
  /*--mpn--*/
  /* 
     else 
     { 
     fprintf(stdout, "\nOpened file %s\n", arg_buff[1]); 
     fprintf(stdout, "\nN.B. The first line is expected to contain comments, "); 
     fprintf(stdout, "and will not be parsed.\n\n"); 
     } 
   */

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

int main_proc(char (*data_ar)[MAX_COLS][NAME_LEN], int n_loci, int n_recs)
{

  int i, j, obs, locus, col_0, col_1;
  int unique_pheno_flag, unique_geno_flag;
  char buff[NAME_LEN];

  int n_hetero, n_hetero_prev;  /* heterozygous sites through current and previous locus loop */
  int n_geno, n_geno_prev;  /* distinct genotypes through current and previous locus loop */
  int unique_pheno_count, n_unique_pheno, unique_geno_count, n_unique_geno;
  int count;      /* RS added */

  /* these should be malloced, but the stack will experience meltdown: */
  /* RS LINE_LEN changed to LINE_LEN/2 in temp_geno and geno */
  /* RS MAX_GENOS changed to MAX_ROWS in pheno, numgeno, obspheno, and 2nd dim of genopheno */
  static char pheno[MAX_ROWS][LINE_LEN], geno[MAX_GENOS][2][LINE_LEN / 2];
  static char temp_geno[MAX_GENOS][2][LINE_LEN / 2];
  static int numgeno[MAX_ROWS], obspheno[MAX_ROWS],
    genopheno[MAX_GENOS][MAX_ROWS];

  char temp_pheno[LINE_LEN];

  /* needed for the count_unique_haplotypes function */
  int n_haplo;
  static char haplo[MAX_HAPLOS][LINE_LEN / 2];  /* RS changed to MAX_HAPLOS from 2*MAX_ROWS */

  /* RS added (begin) */
  /* needed for the id_unique_alleles function */
  static char unique_allele[MAX_LOCI][MAX_ALLELES][NAME_LEN];
  static int n_unique_allele[MAX_LOCI];

  /* nothing needed for sort2dim function */

  /* nothing needed for sort2arrays function */

  /* needed for the emcalc function */
  double mle[MAX_HAPLOS], freq_zero[MAX_HAPLOS];

  /* RS added (end) */

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
    unique_pheno_flag = 1;
    for (i = 0; i <= unique_pheno_count; i++)  /* RS changed from < to <= */
    {
      if (!strcmp(temp_pheno, pheno[i]))
      {
  unique_pheno_flag = 0;
  obspheno[i] += 1;
      }
    }

    if (unique_pheno_flag == 1)
    {
      /* determine genotypes for the new phenotype */

      n_hetero_prev = n_hetero = 0;
      n_geno_prev = n_geno = 1;

      for (i = 0; i < numgeno[unique_pheno_count]; i++)
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
  unique_geno_flag = 1;

  for (j = 0; j <= unique_geno_count; j++)  /* RS changed from < to <= */
  {
    if (((!strcmp(temp_geno[i][0], geno[j][0])) &&
         (!strcmp(temp_geno[i][1], geno[j][1]))) ||
        ((!strcmp(temp_geno[i][0], geno[j][1])) &&
         (!strcmp(temp_geno[i][1], geno[j][0]))))
    {
      unique_geno_flag = 0;
    }
  }

  if (unique_geno_flag == 1)
  {
    unique_geno_count++;
    strcpy(geno[unique_geno_count][0], temp_geno[i][0]);
    strcpy(geno[unique_geno_count][1], temp_geno[i][1]);
    genopheno[unique_geno_count][unique_pheno_count] = 1;
  }
      }
    }        /* END of if unique_pheno_flag == 1 */
  }        /* END for for loop for each observation */

  n_unique_pheno = unique_pheno_count + 1;
  n_unique_geno = unique_geno_count + 1;

  /* finished arranging unique phenotypes and genotypes */
  /* here endeth the code from the original count_unique_phenos_genos */
  /* ---------------------------------------------------------------- */

  fprintf(stdout, "n_unique_pheno: %d n_unique_geno: %d \n", n_unique_pheno,
    n_unique_geno);

  n_haplo = count_unique_haplos(geno, haplo, n_unique_geno);
  fprintf(stdout, "n_haplo: %d \n", n_haplo);

/* RS --- List each obs pheno and corresponding possible genos
  for(i = 0; i < n_unique_pheno; i++) 
  { 
    fprintf(stdout, "pheno: %s obspheno: %d numgeno %d \n", pheno[i], obspheno[i], numgeno[i]); 
    count = 0;
    for(j = 0; j < n_unique_geno; j++) 
    { 
      if(genopheno[j][i] == 1)
      { 
        count += 1;
        fprintf(stdout, "possible geno: %d %s %s \n", count, geno[j][0],  geno[j][1]); 
      } 
    } 
    fprintf(stdout, "\n"); 
  } 
*/

/* RS --- List all genos observed 
  for(i = 0; i < n_unique_geno; i++)
  {
    fprintf(stdout, "%d %s %s\n", i+1, geno[i][0], geno[i][1]);
  }
*/

  id_unique_alleles(data_ar, unique_allele, n_unique_allele, n_loci, n_recs);

  sort2dim(unique_allele, n_unique_allele, n_loci);

  for (locus = 0; locus < n_loci; locus++)
  {
    fprintf(stdout, "\n");
    for (j = 0; j < n_unique_allele[locus]; j++)
    {
      fprintf(stdout, "unique_allele[%d][%d]: %s\n", locus, j,
        unique_allele[locus][j]);
    }
  }

  for (i = 0; i < n_haplo; i++)
  {
    freq_zero[i] = 1.0 / (double)n_haplo;
  }

  emcalc(haplo, geno, genopheno, numgeno, obspheno, freq_zero, mle, n_haplo,
   n_unique_geno, n_unique_pheno, n_recs);

/* TO DO: allele_frequencies(), add haplocus[][] to count_unique_haplotypes() */

  /* N.B. can't sort arrays before using haplocus[][], since the order is needed */
  sort2arrays(haplo, mle, n_haplo);

  j = 0;
  fprintf(stdout, "\n\n \t MLE frequency \t haplo (MLE > .00001) \n");
  for (i = 0; i < n_haplo; i++)
  {
    if (mle[i] > .00001)
    {
      j += 1;
      fprintf(stdout, "%d \t %f \t %s\n", j, mle[i], haplo[i]);
    }
  }

  fprintf(stdout, "\n");

  return (EXIT_SUCCESS);
}

/************************************************************************/
int count_unique_haplos(char (*geno_ar)[2][LINE_LEN / 2],
      char (*haplo_ar)[LINE_LEN / 2], int num_genos)
/* RS LINE_LEN changed to LINE_LEN/2 in geno_ar */
/* 
  * run through the array of possible genotypes 
  * and create an array of possible haplotypes 
*/
{
  int i, j, k;
  int unique_haplo_flag, unique_haplo_count;

  /* 0th assignment */
  unique_haplo_count = 0;
  strcpy(haplo_ar[0], geno_ar[0][0]);

  for (i = 0; i < num_genos; i++)
  {
    for (j = 0; j < 2; j++)
    {
      unique_haplo_flag = TRUE;
      for (k = 0; k <= unique_haplo_count && unique_haplo_flag == TRUE; k++)
      {
  if (!strcmp(geno_ar[i][j], haplo_ar[k]))
    unique_haplo_flag = FALSE;
      }
      if (unique_haplo_flag == TRUE)
      {
  strcpy(haplo_ar[++unique_haplo_count], geno_ar[i][j]);
      }
    }
  }

  return unique_haplo_count + 1;
}

/************************************************************************/
void id_unique_alleles(char (*data_ar)[MAX_COLS][NAME_LEN],
           char (*unique_allele)[MAX_ALLELES][NAME_LEN],
           int *n_unique_allele, int n_loci, int n_recs)
/* Creates unique_allele[i,j]: jth unique allele for the ith locus         */
/*         n_unique_allele[i]: number of unique alleles for the ith locus  */
{
  int i, j, locus, col_0, col_1;
  int unique_allele_flag, unique_allele_count;

/* CHECKING
  for (i = 0; i < n_recs; i++)
  for (j = 0; j < 2*n_loci; j++)
  fprintf(stdout, "data[%d][%d]: %s\n", i, j, data_ar[i][j]); 
  fprintf(stdout, "data0[%d][%d]: %s, uniq[%d][%d]:\n", i, col_0, data_ar[i][j], locus, j, unique_allele[locus][j]); 
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
  }
      }
      if (unique_allele_flag == TRUE)
      {
  unique_allele_count += 1;
  strcpy(unique_allele[locus][unique_allele_count], data_ar[i][col_0]);
      }

      /* Process col_1 of current locus */
      unique_allele_flag = TRUE;
      for (j = 0; j <= unique_allele_count; j++)
      {
  if (!strcmp(data_ar[i][col_1], unique_allele[locus][j]))
  {
    unique_allele_flag = FALSE;
  }
      }
      if (unique_allele_flag == TRUE)
      {
  unique_allele_count += 1;
  strcpy(unique_allele[locus][unique_allele_count], data_ar[i][col_1]);
      }
    }
    n_unique_allele[locus] = unique_allele_count + 1;

    fprintf(stdout, "\n n_unique_allele[%d]: %d\n", locus,
      n_unique_allele[locus]);

/* CHECKING
    for(j = 0; j < n_unique_allele[locus]; j++)
    {
      fprintf(stdout, "unique_allele[%d][%d]: %s\n", locus, j, unique_allele[locus][j]); 
    }
*/

  }

}

/************************************************************************/
void sort2dim(char (*unique_allele)[MAX_ALLELES][NAME_LEN],
        int *n_unique_allele, int n_loci)
/* insertion sort in ascending order for 2nd dimension of 2-dim array */
{
  int i, j, locus;
  char temp[NAME_LEN];

  for (locus = 0; locus < n_loci; locus++)
  {
    for (i = 1; i < n_unique_allele[locus]; ++i)
    {
      for (j = i;
     (j - 1) >= 0
     && strcmp(unique_allele[locus][j - 1],
         unique_allele[locus][j]) > 0; --j)
      {
  strcpy(temp, unique_allele[locus][j]);
  strcpy(unique_allele[locus][j], unique_allele[locus][j - 1]);
  strcpy(unique_allele[locus][j - 1], temp);
      }
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
void emcalc(char (*haplo)[LINE_LEN / 2], char (*geno)[2][LINE_LEN / 2],
      int (*genopheno)[MAX_ROWS], int *numgeno, int *obspheno,
      double *freq_zero, double *mle, int n_haplo, int n_unique_geno,
      int n_unique_pheno, int n_recs)
{
  int i, j, k, l;
  int done, itest, totall;
  int iter, kphen, igeno, iall, jall, keep;
  double unamball[MAX_HAPLOS], ambigall[MAX_HAPLOS], sumambig;
  static double freqs[MAX_HAPLOS][MAX_ITER], tempall[MAX_HAPLOS];
  double expfreq, sum, sumall, diff, mgnfrq[MAX_GENOS], mfreq[MAX_ROWS];
  double lglik, lltest, prevlk, freqsum;

  fprintf(stdout, "\nEMCALC: \n");

  done = FALSE;
  itest = 0;
  totall = 2 * n_recs;

  for (i = 0; i < n_haplo; i++)
  {
    unamball[i] = 0;
    ambigall[i] = 0;
  }

  /* Set up for first iteration - initial allele counting */
  for (i = 0; i < n_unique_geno; i++)
  {
    for (j = 0; j < 2; j++)
    {
      for (k = 0; k < n_haplo; k++)
      {
        for (l = 0; l < n_unique_pheno; l++)
        {
          if ((!strcmp(geno[i][j], haplo[k])) && (genopheno[i][l] != 0))
          {
            if (numgeno[l] == 1)
            {
              unamball[k] += (double)obspheno[l];
            }
            else if (numgeno[l] > 1)
            {
              ambigall[k] += (double)obspheno[l] / (double)numgeno[l];
            }
            else
            {
              fprintf(stdout, "\n ** Warning - numgeno[%d] < 0", l);
            }
          }
        }
      }
    }
  }

  iter = 0;

  sumambig = 0;
  for (i = 0; i < n_haplo; i++)
  {
    sumambig += ambigall[i];
    freqs[i][iter] = freq_zero[i];
  }

  /* Test for observed ambiguous phenos */
  if (sumambig == 0)
  {
    iter = 1;

    fprintf(stdout, "\n *** There is no ambiguity ...");
    for (i = 0; i < n_haplo; i++)
    {
      freqs[i][iter] = unamball[i] / (double)totall;
      mle[i] = freqs[i][iter];
    }
  }

  /* There are ambiguous phenos. Begin E-M iterations */
  else if (sumambig > 0)
  {
    for (iter = 1; iter < MAX_ITER && done == FALSE; iter++)
    {
      for (k = 0; k < n_haplo; k++)
      {
        ambigall[k] = 0;
      }
      for (kphen = 0; kphen < n_unique_pheno; kphen++)
      {
  if ((numgeno[kphen] > 1) && (obspheno[kphen] >= 1))
  {
    for (k = 0; k < n_haplo; k++)
    {
      tempall[k] = 0;
    }
    sum = 0;
    for (igeno = 0; igeno < n_unique_geno; igeno++)
    {
      if (genopheno[igeno][kphen] > 0)
      {
        for (k = 0; k < n_haplo; k++)
        {
          if (!strcmp(geno[igeno][0], haplo[k]))
          {
            iall = k;
          }
          if (!strcmp(geno[igeno][1], haplo[k]))
          {
            jall = k;
          }
        }
        /* Calc expected frequency of this genotype using allele */
        /* frequency estimates from the previous iteration       */
        if (iall == jall)
        {
          expfreq = freqs[iall][iter - 1] * freqs[jall][iter - 1];
        }
        else
        {
          expfreq = 2 * freqs[iall][iter - 1] * freqs[jall][iter - 1];
        }

        /* Add proportionate numbers to TEMPALL */
        tempall[iall] += expfreq * (double)obspheno[kphen];
        tempall[jall] += expfreq * (double)obspheno[kphen];
        sum += expfreq;
      }
    }

    /* Normalize the numbers added for this phenotype */
    if (sum < .000001)
    {
      fprintf(stdout, "\n sum near zero in tempall[i]/sum : sum = %f",
        sum);}
    sumall = 0;
    for (i = 0; i < n_haplo; i++)
    {
      tempall[i] = tempall[i] / sum;
      sumall += tempall[i];
      /* add these obs to running count for ambiguous */
      ambigall[i] += tempall[i];
    }

    for (i = 0; i < n_haplo; i++)
    {
      freqs[i][iter] = (unamball[i] + ambigall[i]) / (double)totall;
    }

    diff = sumall - 2 * (double)obspheno[kphen];
    if (fabs(diff) > .1)
    {
      fprintf(stdout, "\n Wrong # of alleles allocated for pheno %d", kphen);
      fprintf(stdout, "\n allocated : %f \n observed  : %d", sumall,
        obspheno[kphen]);
    }
    }
      }        /* end of loop for kphen */

      /* Calculate geno freqs from current estimate of haplo freqs */
      for (i = 0; i < n_unique_geno; i++)
      {
  mgnfrq[i] = 1;
  keep = 0;
  for (j = 0; j < 2; j++)
  {
    for (k = 0; k < n_haplo; k++)
    {
      if (!strcmp(haplo[k], geno[i][j]))
      {
        mgnfrq[i] = mgnfrq[i] * freqs[k][iter];
        if (j == 0)
        {
    keep = k;
        }
        if (k != keep)
        {
    mgnfrq[i] = mgnfrq[i] * 2;
        }
      }
    }
  }
      }

      /* Calc pheno freqs based on these genotype freqs */
      for (i = 0; i < n_unique_pheno; i++)
      {
  mfreq[i] = 0;
  for (j = 0; j < n_unique_geno; j++)
  {
    if (genopheno[j][i] == 1)
    {
      mfreq[i] += mgnfrq[j];
    }
  }
      }

      /* Calc log likelihood */
      lglik = 0;
      lltest = 0;
      for (i = 0; i < n_unique_pheno; i++)
      {
  lltest += (double)obspheno[i];
  if (mfreq[i] > DBL_EPSILON)
  {
    lglik += (double)obspheno[i] * log(mfreq[i]);
  }
  else
  {
    fprintf(stdout, "\n ** Warning - Est. freq. for pheno %d < 0", i);
  }
      }
      if (lltest != n_recs)
      {
  fprintf(stdout,
    "\n ** Error - Incorrect no. of obs. counted in likelihood calc.");
      }
      /* N.B. lltest could be removed and done in mainproc() if desired */

      if (iter <= 1)
      {
  prevlk = lglik;
      }
      else if (iter > 1)
      {
  /* Test for convergence */
  diff = lglik - prevlk;
  if (fabs(diff) > CRITERION)
  {
    /* If not converged, test if likelihood is decreasing */
    if (prevlk > lglik)
    {
      itest += 1;
    }
    if (itest >= 5)
    {
      done = TRUE;
      fprintf(stdout, "\n ** Warning - iterations terminated");
      fprintf(stdout,
        "\n              Likelihood has decreased for last 5 iterations");
    }
    else      /* ( itest < 5 ) */
    {
      prevlk = lglik;
    }
  }
  else      /* ( abs(diff) <= CRITERION ) */
  {
    done = TRUE;
    fprintf(stdout,
      "\n Log likelihood converged in %d iterations to : %f",
      iter + 1, lglik);

    freqsum = 0;
    for (i = 0; i < n_haplo; i++)
    {
      mle[i] = freqs[i][iter];
      freqsum += freqs[i][iter];
    }
    if (freqsum < .99 || freqsum > 1.01)
    {
      fprintf(stdout, "\n  ** Warning - final frequencies sum to %f",
        freqsum);
    }
  }
      }

    }        /* end of loop for iter */
  }        /* end of else if ( sumambig > 0 ) */

}
