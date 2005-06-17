/* This file is part of PyPop

  Copyright (C) 2003. The Regents of the University of California
  (Regents) All Rights Reserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
USA.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF
ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION
TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS. */

/* Convert a Python list of list of strings into a 2d array C of strings */
%{
#include "cStringIO.h"
%}

%typemap(python,in) char [ANY][ANY][ANY] {
#ifdef DEBUG
  fprintf(stderr,"Converting Python [['a']] ->  2d C array C of strings\n");
#endif
  if (PyList_Check($input)) {
    int size0 = PyList_Size($input);
    int i = 0;
    int j = 0;
#ifdef DEBUG
    fprintf(stderr,"Before malloc!\n");
    fprintf(stderr,"outer list size: %d\n", size0);
#endif
    $1 = ($ltype)malloc(($dim0+1)*($dim1+1)*($dim2+1));
    if ($1 != NULL) {
#ifdef DEBUG
      fprintf(stderr,"After malloc!\n");
#endif
      for (i = 0; i < size0; i++) {
	PyObject *o = PyList_GetItem($input, i);
#ifdef DEBUG
	fprintf(stderr,"outer index: %d\n", i);
#endif
	if (PyList_Check(o)) {
	  int size1 = PyList_Size(o);
	  for (j = 0; j < size1; j++) {
	    PyObject *p = PyList_GetItem(o, j);
#ifdef DEBUG
	    fprintf(stderr,"inner index: %d\n", j); 
#endif
	    if (PyString_Check(p)) {
#ifdef DEBUG
	      fprintf(stderr,"before assigning string: %s\n", PyString_AsString(p));
#endif
	      strcpy($1[i][j], PyString_AsString(p));
#ifdef DEBUG
	      fprintf(stderr,"after assigning string\n");
	      fprintf(stderr,"[%d, %d]: %s\n", i, j, $1[i][j]);
#endif
	    }
	    else {
	      PyErr_SetString(PyExc_TypeError, 
			      "list must contain strings");
	      free($1);
	      return NULL;
	    }
	  }
	}
	else {
	  PyErr_SetString(PyExc_TypeError, 
			  "inner array must be a list");
	  free($1);
	  return NULL;
	}
      }
    } else {
      fprintf(stderr,"Malloc of memory failed\n");
      exit(-1);
    }
  } else {
    PyErr_SetString(PyExc_TypeError, 
		    "outer array must be a list");
    free($1);
    return NULL;
  }
}

/* This cleans up the char [][][] array we malloc'd before the function call */
%typemap(python,freearg) char [ANY][ANY][ANY] {
  free(($ltype) $1);
}

/* Typemap to convert python file type(s) to C file pointer */
%typemap(python,in) FILE * {
  PycString_IMPORT;
  /* if file is an actual file on the filesystem, then pass directly to C */
  if (PyFile_Check($input)) {
    $1 = PyFile_AsFile($input);
  }
  /* if file is a "cStringIO" in-memory "file" then cast to FILE type */
  else if (PycStringIO_OutputCheck($input)) {
    $1 = (FILE *)$input;
  }
  /* otherwise raise an error */
  else {
    PyErr_SetString(PyExc_TypeError, "Need a file or file-like object!");
    return NULL;
  }
}

/* Typemap to convert a Python 1-d array of ints to int [] */
%typemap(python, in) int [ANY] {
#if DEBUG
  printf("converting from a 1-d array of ints\n");
#endif
  if (PyList_Check($input)) {
    int i;
    int size0 = PyList_Size($input);
#if DEBUG
    printf("length of list = %d\n", size0);
#endif
    $1 = (int *)malloc((size0+1)*sizeof(int));
    if ($1 != NULL) {
      for (i = 0; i < size0; i++) {
	PyObject *p = PyList_GetItem($input,i);
#if DEBUG
	printf("loc = %d\n", i);
#endif
	if (PyInt_Check(p)){
#if DEBUG
	  printf("$1[%d] = %d\n", i, (int)PyInt_AS_LONG(p));
#endif
	  $1[i] = (int)PyInt_AS_LONG(p);
	} else {	      
	  PyErr_SetString(PyExc_TypeError, "list must contain ints");
	}
      }
    } else {
      fprintf(stderr,"Malloc of memory failed\n");
      exit(-1);
    }
  } else {
    PyErr_SetString(PyExc_TypeError, "array must be a list");
    return NULL;
  }
}

/* This cleans up the int[] array we malloc'd before the function call */
%typemap(python,freearg) int [ANY] {
  if ($1)
    free($1);
}

%{
/* 
 * pywrite, internal function nabbed from sysmodule.c to implement
 * access to sys.{stdout,stderr}
 */
static void
pywrite(char *name, FILE *fp, const char *format, va_list va)
{
	PyObject *file;
	PyObject *error_type, *error_value, *error_traceback;

	PyErr_Fetch(&error_type, &error_value, &error_traceback);
	file = PySys_GetObject(name);
	if (file == NULL || PyFile_AsFile(file) == fp)
		vfprintf(fp, format, va);
	else {
		char buffer[1001];
		if (vsprintf(buffer, format, va) >= sizeof(buffer))
		    Py_FatalError("PySys_WriteStdout/err: buffer overrun");
		if (PyFile_WriteString(buffer, file) != 0) {
			PyErr_Clear();
			fputs(buffer, fp);
		}
	}
	PyErr_Restore(error_type, error_value, error_traceback);
}

/* 
 * pyfprintf
 *
 * redefined fprintf, if file pointer is either stdout or stderr,
 * redirect to Python sys.stdout and sys.stderr, respectively, or if
 * an in-memory "cStringIO" instance, write to that instance;
 * otherwise retain usual file pointer
 */

int pyfprintf(FILE *fp, const char *format, ...) {
  va_list va;
  PycString_IMPORT;
  va_start(va, format);

  /* redirect stdout */
  if (fp == stdout) {
    pywrite("stdout", stdout, format, va); 
  }
  /* redirect stderr */
  else if (fp == stderr) {
    pywrite("stderr", stderr, format, va); 
  }
  /* if file pointer is a cStringIO instance, then use the cStringIO
     API "cwrite" to write to string */
  else if (PycStringIO_InputCheck((PyObject *)fp)
	     || PycStringIO_OutputCheck((PyObject *)fp)) {
    /* generate a buffer for the text */
    char buffer[1001];
    
    /* check for buffer overrun */
    if (vsprintf(buffer, format, va) >= sizeof(buffer))
      Py_FatalError("pyfprintf: buffer overrun");

    /* calculate length of buffer, and use in call to cwrite */
    PycStringIO->cwrite((PyObject *)fp, buffer, strlen(buffer));
  } 
  /* otherwise just treat as normal C file pointer */
  else {
    vfprintf(fp, format, va);
  }
  va_end(va);
  return 0;
}
%}

/* Typemap to convert a 1-d array of long doubles to a Python list of
   plain doubles */
%typemap(python,out) long double*
{
	int len,i;
	len = 0;
	while($1 && $1[len])
		len++;
	$result = PyList_New(len);
	for(i = 0;i < len;++i) {
	  PyList_SetItem($result,i,PyFloat_FromDouble((double)$1[i]));
	}
}

/* This cleans up the long double array we malloc'd before the function call */
%typemap(python,free) long double* {
  if ($1)
    free($1);
}


/* 
 * Local variables:
 * mode: c
 * End:
 */
