/* SWIG interface generation file */

%module emhaplofreq

%include "emhaplofreq.h"

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
