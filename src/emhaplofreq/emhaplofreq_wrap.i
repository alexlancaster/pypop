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

/* SWIG interface generation file */

%module Emhaplofreq

%include "typemap.i"

%include "emhaplofreq/emhaplofreq.h"

/* prototype for internal inclusion */
%{
extern int main_proc(char *, char *, int, int, int, int, int, int, int, int, int, char [], char []);  
%}

/* 
 * Python entry point to program.
 *
 * Redeclare parameter to extern function as a 3 dimensional array.
 * This is different from the emhaplofreq.c file to coax SWIG into *
 * generating the right typemap for converting a Python list-of-a-list
 * of strings into the appropriate C data structure.
 */

extern int main_proc(char *, char [MAX_ROWS][MAX_COLS][NAME_LEN], int, int, int, int, int, int, int, int, int, char [], char []);

/* 
 * Local variables:
 * mode: c
 * End:
 */
