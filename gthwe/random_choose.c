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

