/* This file is part of PyPop
  
  Copyright (C) 1992. Sun-Wei Guo.
  Modifications Copyright (C) 1999, 2003, 2004. 
  The Regents of the University of California (Regents) All Rights Reserved.

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

/***********************************************************************
  program name: stamp_time.c

  function to stamp the date and time the program is executed.

  Status: modified from g-t program

  Date: 12/14/99 

************************************************************************/
#include "hwe.h"

void stamp_time(t1, outfile)

		 long t1;
		 FILE **outfile;

{
	char *ctime();
	long t2, now;
	long time();

	time(&t2);
	t2 -= t1;
	time(&now);

#ifndef XML_OUTPUT
	fprintf(*outfile, "\nTotal elapsed time: %ld''\n", t2);
	fprintf(*outfile, "Date and time: %s\n", ctime(&now));
#else
	xmlfprintf(*outfile, "<elapsed-time>%ld</elapsed-time>\n", t2);
	xmlfprintf(*outfile, "<timestamp>%s</timestamp>\n", ctime(&now));
#endif
}
