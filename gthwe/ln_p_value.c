/*************************************************************************

  program name: ln_p_value.c

  function to compute the log p value for given genotype frequencies

  status: modified from g-t program 

  date: 12/14/99

*************************************************************************/
#include "hwe.h"

double ln_p_value(int *a, int no_allele, double constant)

{
  int i=0, j=0, l=0, temp=0;
  double ln_prob = 0.0;
  double log_factorial();

#ifdef PERMU_DEBUG  
  printf("const=%e, ", constant);
#endif
  ln_prob = constant;
  temp = 0;
  
  for (i = 0; i < no_allele; ++i)
    {
      for (j = 0; j < i; ++j)
	{
	  l = LL(i, j);
	  temp += a[l];
	  ln_prob = ln_prob - log_factorial(a[l]);
	}
      l = LL(i, i);
      ln_prob = ln_prob - log_factorial(a[l]); 
    }

  ln_prob = ln_prob + (temp * log(2.0));

#ifdef PERMU_DEBUG
  printf("no_allele=%d, temp=%d, ln_prob=%e\n", no_allele, temp, ln_prob);
#endif
  return (ln_prob);
}
