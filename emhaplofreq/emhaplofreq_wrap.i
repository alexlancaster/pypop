/* SWIG interface generation file */

%module Emhaplofreq

%{
#include "emhaplofreq.h"
%}

/* convert python file to C file pointer */
%typemap(python,in) FILE * {
  if (!PyFile_Check($source)) {
      PyErr_SetString(PyExc_TypeError, "Need a file!");
      return NULL;
  }
  $target = PyFile_AsFile($source);
}

%{
int pymain(FILE *if_handle)
{
  /* FILE *if_handle; */
  char ref[MAX_ROWS][NAME_LEN];
  char data[MAX_ROWS][MAX_COLS][NAME_LEN];
  int num_loci, num_recs;
  int ret_val;

  /*  if_handle = parse_args(argc, argv); */

  num_loci = read_infile(if_handle, ref, data, &num_recs);

  fprintf(stdout, "num_loci: %d\n", num_loci);
  if (num_loci > MAX_LOCI) {
    fprintf(stderr, "Error: number of loci: %d, exceeds maximum of: %d\n", 
	    num_loci, MAX_LOCI);
    exit(EXIT_FAILURE);
  }

  ret_val = main_proc(data, num_loci, num_recs);

  return (ret_val);
}
%}

/* Python entry point */

extern int pymain(FILE *if_handle);

extern void print_usage(void);

FILE *parse_args(int, char **);

extern int read_infile(FILE *, char (*)[], char (*)[][], int *);

extern int main_proc(char (*)[][], int, int);

extern int main(int argc, char **argv);

extern int count_unique_haplos(char (*)[][], char (*)[], int (*)[], 
			       char (*)[][], int *, int, int, int (*)[], 
			       int *);

extern void id_unique_alleles(char (*)[][], char (*)[][], int *, 
			      double (*)[], int, int);

extern double min(double, double);

extern void linkage_diseq(double *, int (*)[], double (*)[], 
			  char (*)[][], int *, int, int, int); 

extern void sort2arrays(char (*)[], double *, int);

extern void emcalc(int (*)[], int *, int *, double *, double *, int, int, 
		   int, int, int *, int (*)[], int *, int *, double *);

extern void haplo_freqs_no_ld(double *, double (*)[], int (*)[], int *, 
			      int, int);

extern double loglikelihood(int (*)[], double *, int *, int, int, int, 
			    int *, int (*)[]);

extern void srand48(long int seedval);

extern double drand48(void);

/* 
 * Local variables:
 * mode: c
 * End:
 */
