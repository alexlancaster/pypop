/************************************************************************

  program name: cal_n.c

  funtion to calculate n(i)

  status: modified from g-t program 

  date: 12/14/99

*************************************************************************/

#include "hwe.h"

void cal_n(int no_allele, int *a, int *n)
{
  register int i, j, l;
  
  for (i = 0; i < no_allele; ++i)
    {
      l = LL(i, i);
      n[i] = a[l];
      
      for (j = 0; j < no_allele; ++j)
	{
	  l = L(i, j);
	  n[i] += a[l];
	}
    }
}

