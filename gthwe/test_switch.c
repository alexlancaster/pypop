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

/***************************************************************************
  program name: test_switch.c

  function to determine the switchability 
  
  switch_ind = 0 if non-switchable, 1 if partially-switchable, 2 if switchable.

  And it returns the switch type if switchable.

  switch_type = 0 if D-switchable and 1 if R-switchable;
  
  But switch_dir = 0 if switch_ind = 2.

  In addition, it returns the probability ratio if appropriate.

  status: modified from g-t program

  date: 12/14/99

****************************************************************************/
#include "hwe.h"

void test_switch(a, index, switch_ind, switch_type, p1_rt, p2_rt)

		 int *a;
		 Index index;
		 int *switch_ind, *switch_type;		/* switchability and type of switch */
		 double *p1_rt, *p2_rt;			/* probability ratio */

{
	register int k11, k22, k12, k21;

	*switch_ind = 0;

	k11 = L(index.i1, index.j1);
	k22 = L(index.i2, index.j2);
	k12 = L(index.i1, index.j2);
	k21 = L(index.i2, index.j1);

	if (index.type <= 1)
	{															/* type = 0, 1 */
		if (a[k11] > 0 && a[k22] > 0)
		{
			*switch_ind = 1;
			*switch_type = 0;					/* D-switchable */
			*p1_rt = RATIO(a[k11], a[k12]) * RATIO(a[k22], a[k21]) * index.cst;
		}
		if (a[k12] > 0 && a[k21] > 0)
		{
			*switch_ind += 1;
			*switch_type = 1;					/* R-switchable */
			*p2_rt = RATIO(a[k12], a[k11]) * RATIO(a[k21], a[k22]) / index.cst;
		}

	}
	else
	{															/* type = 2 */
		if (a[k11] > 0 && a[k22] > 0)
		{
			*switch_ind = 1;
			*switch_type = 0;					/* D-switchable */
			*p1_rt = RATIO(a[k11], a[k12] + 1.0) * RATIO(a[k22], a[k12]) * index.cst;
		}
		if (a[k12] > 1)
		{
			*switch_ind += 1;
			*switch_type = 1;					/* R-switchable */
			*p2_rt = RATIO(a[k12], a[k11]) * RATIO(a[k12] - 1, a[k22]) / index.cst;
		}

	}

}
