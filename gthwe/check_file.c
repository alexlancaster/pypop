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

/************************************************************************

  function to check execution command and file

  status: modified from g-t program

  date: 12/14/99

*************************************************************************/

#include "hwe.h"

int check_file(int argc, char *argv[], FILE **infile, FILE **outfile)
{

	int exit_value = 0;

	/* file manipulation */

	if (argc != 3)
	{
		fprintf(stderr, "\nUsage: gthwe infile outfile.\n\n");
		exit_value = 1;
	}

	else if ((*infile = fopen(argv[1], "r")) == (FILE *) NULL)
	{
		fprintf(stderr, "Can't read %s\n\n", argv[1]);
		exit_value = 2;
	}

	else if ((*outfile = fopen(argv[2], "w")) == (FILE *) NULL)
	{
		fprintf(stderr, "Can't write %s\n\n", argv[2]);
		exit_value = 3;
	}

	return (exit_value);
}

