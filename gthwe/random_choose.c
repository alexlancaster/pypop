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
  function to randomly choose two integer numbers, k1 and k2, between 0 
  and k - 1.  ( 0 <= k1 < k2 < k )

  status: modified from g-t program

  date: 12/14/99
************************************************************************/
#include "hwe.h"
#include "func.h"

void random_choose(int *k1, int *k2, int k)
{
	register int temp, i, not_find;
	double new_rand();
	int *work= (int *)calloc(k, sizeof(int));

	for (i = 0; i < k; ++i)
		work[i] = i;

	*k1 = (int)(new_rand() * (double)k);


	--k;

	for (i = *k1; i < k; ++i)
		work[i] = i + 1;

	not_find = 1;

	while (not_find)
	{
		i = (int)(new_rand() * (double)k);
		*k2 = work[i];
		not_find = 0;
	}

	if (*k1 > *k2)
	{
		temp = *k1;
		*k1 = *k2;
		*k2 = temp;
	}
	free(work);
}

