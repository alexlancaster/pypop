/*************************************************************************

  program name: ln_p_value.c

  function to compute the log p value for given genetype frequencies

  status: modified from g-t program 

  date: 12/14/99

*************************************************************************/
#include "hwe.h"

double ln_p_value(a, no_allele, constant)

		 int a[LENGTH];
		 int no_allele;
		 double constant;

{
	register int i, j, l, temp;
	register double ln_prob;
	double log_factorial();

	ln_prob = constant;
	temp = 0;

	for (i = 0; i < no_allele; ++i)
	{
		for (j = 0; j < i; ++j)
		{
			l = LL(i, j);
			temp += a[l];
			ln_prob -= log_factorial(a[l]);
		}

		l = LL(i, i);
		ln_prob -= log_factorial(a[l]);
	}

	ln_prob += temp * log(2.0);

	return (ln_prob);

}
