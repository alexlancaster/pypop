/* SWIG interface generation file */

%module _Gthwe

%include "typemap.i"

/* 
 * Python entry point to program.
 *
 * Redeclare parameter to extern function as a 3 dimensional array.
 * This is different from the emhaplofreq.c file to coax SWIG into *
 * generating the right typemap for converting a Python list-of-a-list
 * of strings into the appropriate C data structure.
 */

extern int run_data(int [LENGTH], int [MAX_ALLELE], int, int, int, int, int, char *, FILE *);

/* 
 * Local variables:
 * mode: c
 * End:
 */
