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

/*********************************************************************

  program name: do_switch.c

  function to make switch according to given switchability and switch
  type.

  status: modified from g-t program 

  date: 12/14/99

**********************************************************************/

#include "hwe.h"

void do_switch(int *a, Index index, int type)
{
	register int k11, k22, k12, k21;

	k11 = L(index.i1, index.j1);
	k12 = L(index.i1, index.j2);
	k21 = L(index.i2, index.j1);
	k22 = L(index.i2, index.j2);


	if (type == 0)
	{															/* D-switch */
		--a[k11];
		--a[k22];
		++a[k12];
		++a[k21];
	}
	else
	{															/* R-switch */
		++a[k11];
		++a[k22];
		--a[k12];
		--a[k21];
	}
}
