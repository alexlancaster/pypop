/* SWIG interface generation file */

%module _Emhaplofreq

%{
#include "emhaplofreq.h"
%}

/* Convert a Python list of list of strings into a 2d array C of strings */

%typemap(python,in) char [ANY][ANY][ANY] {
  printf("Converting Python list of list of strings into a 2d array C of strings \n");
  if (PyList_Check($source)) {
    int size0 = PyList_Size($source);
    int i = 0;
    int j = 0;
    printf("Before malloc!\n");
    printf("outer list size: %d\n", size0);
    $target = ($ltype)malloc(($dim0+1)*($dim1+1)*($dim2+1));
    if ($target != NULL) {
      printf("After malloc!\n");
      for (i = 0; i < size0; i++) {
	PyObject *o = PyList_GetItem($source, i);
	printf("outer index: %d\n", i);
	if (PyList_Check(o)) {
	  int size1 = PyList_Size(o);
	  for (j = 0; j < size1; j++) {
	    PyObject *p = PyList_GetItem(o, j);
	    printf("inner index: %d\n", j); 
	    if (PyString_Check(p)) {
	      printf("before assigning string: %s\n", PyString_AsString(p));
	      strcpy($target[i][j], PyString_AsString(p));
	    printf("after assigning string\n");
	    printf("[%d, %d]: %s\n", i, j, $target[i][j]);
	    }
	    else {
	      PyErr_SetString(PyExc_TypeError, 
			      "list must contain strings");
	      free($target);
	    return NULL;
	    }
	  }
	}
	else {
	  PyErr_SetString(PyExc_TypeError, 
			  "inner array must be a list");
	  free($target);
	  return NULL;
	}
      }
    } else {
      fprintf(stderr, "Malloc of memory failed\n");
      exit(-1);
    }
  } else {
    PyErr_SetString(PyExc_TypeError, 
		    "outer array must be a list");
    free($target);
    return NULL;
  }
}

/* This cleans up the char [][][] array we malloc'd before the function call */
%typemap(python,freearg) char [ANY][ANY][ANY] {
  free(($ltype) $source);
}

/* convert python file to C file pointer */
%typemap(python,in) FILE * {
  if (!PyFile_Check($source)) {
      PyErr_SetString(PyExc_TypeError, "Need a file!");
      return NULL;
  }
  $target = PyFile_AsFile($source);
}


/* 
 * Python entry point to program.
 *
 * Redeclare parameter to extern function as a 3 dimensional array.
 * This is different from the emhaplofreq.c file to coax SWIG into *
 * generating the right typemap for converting a Python list-of-a-list
 * of strings into the appropriate C data structure.
 */

extern int main_proc(char [MAX_ROWS][MAX_COLS][NAME_LEN], int, int);

/* 
 * Local variables:
 * mode: c
 * End:
 */
