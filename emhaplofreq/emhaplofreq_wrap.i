/* SWIG interface generation file */

%module _Emhaplofreq

%include "typemap.i"

%include "emhaplofreq/emhaplofreq.h"

/* 
 * Python entry point to program.
 *
 * Redeclare parameter to extern function as a 3 dimensional array.
 * This is different from the emhaplofreq.c file to coax SWIG into *
 * generating the right typemap for converting a Python list-of-a-list
 * of strings into the appropriate C data structure.
 */

extern int main_proc(FILE *fp, char [MAX_ROWS][MAX_COLS][NAME_LEN], int, int, int, int);

/* 
 * Local variables:
 * mode: c
 * End:
 */
