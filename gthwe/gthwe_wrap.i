/* SWIG interface generation file */

%module _Gthwe

%include "typemap.i"

/* 
 * Python entry point to program.
 */

extern int run_data(int [LENGTH], int [MAX_ALLELE], int, int, int, int, int, char *, FILE *);

extern int run_randomization(int [LENGTH], int [MAX_ALLELE], int, int, int, FILE *);

/* 
 * Local variables:
 * mode: c
 * End:
 */
