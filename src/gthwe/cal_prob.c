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

  program name: cal_prob.c

  function to calculate 

  status: modified from g-t program

  date: 12/99

***************************************************************************/

#include "hwe.h"

double cal_prob(a, index, ln_p_old, actual_switch)
  
     int *a;
     Index index;
     double ln_p_old;
     int *actual_switch;
     
{
  
  double p1_ratio, p2_ratio;
  register double ln_p_new;
  double rand_num;
  int switch_ind, type;
  double new_rand();
  void test_switch(), do_switch();
  
  *actual_switch = 0;
  
  /* determine the switchability and direction of switch for given face */
  
  test_switch(a, index, &switch_ind, &type, &p1_ratio, &p2_ratio);
  
  switch (switch_ind)
    {
    case 0:	/* non-switchable */
      
      ln_p_new = ln_p_old;   /* retain the pattern, probability unchanged */
      break;
      
    case 1:	/* partially-switchable */
      
      if (type == 1)
	p1_ratio = p2_ratio;
      rand_num = new_rand();
      
      if (rand_num < TRANS(p1_ratio))
	{				/* switch w/ transition P TRANS */
	  do_switch(a, index, type);
	  ln_p_new = ln_p_old + log(p1_ratio);	/* ln P_after-switch */
	  *actual_switch = 1;
	}
      else		/* remain the same w/ P = 1 - TRANS */
	ln_p_new = ln_p_old;			/* probability unchanged */
      break;
      
    default:	/* fully switchable */
      rand_num = new_rand();
      
      if (rand_num <= TRANS(p1_ratio))
	{
	  do_switch(a, index, 0);		/* D-switch */
	  ln_p_new = ln_p_old + log(p1_ratio);	/* ln P_after-switch */
	  *actual_switch = 2;
	}
      else if (rand_num <= TRANS(p1_ratio) + TRANS(p2_ratio))
	{
	  do_switch(a, index, 1);		/* R-switch */
	  ln_p_new = ln_p_old + log(p2_ratio);
	  *actual_switch = 2;
	}
      else
	ln_p_new = ln_p_old;
      break;
    }
  
  return (ln_p_new);
}

