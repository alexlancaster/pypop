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
  program name: select_index.c

  function to randomly choose three integers i1, i2, i3 with
  0 <= i1 < i2 <= no_allele, 0 <= i3 <= no_allele

  status: modified from g-t program

  date: 12/14/99

************************************************************************/
#include "hwe.h"

void select_index(index, no_allele)

		 Index *index;
		 int no_allele;

{

	void random_choose();

	int i1, i2, j1, j2;
	int k = 0;
	int l = 0;

/* generate row indices */

	random_choose(&i1, &i2, no_allele);

	index->i1 = i1;
	index->i2 = i2;

/* generate column indices */

	random_choose(&j1, &j2, no_allele);

	index->j1 = j1;
	index->j2 = j2;

/* calculate Delta = d(i1,j1) + d(i1,j2) + d(i2,j1) + d(i2,j2) */

	if (i1 == j1)
		++k;

	if (i1 == j2)
		++k;

	if (i2 == j1)
		++k;

	if (i2 == j2)
		++k;

	index->type = k;

	if ((i1 == j1) || (i2 == j2))
		++l;

	index->cst = (l == 1) ? pow((double)2, (double) k) : pow((double)2, -(double) k);
}

