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

