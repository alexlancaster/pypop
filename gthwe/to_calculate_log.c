/************************************************************************

 function to calculate log ( k! )

 status: modified from g-t program

 date: 12/14/99

************************************************************************/
#include  "hwe.h"
#include <gsl/gsl_sf_gamma.h>

double log_factorial(int k)
{

  return(gsl_sf_lnfact(k));

  /*
    register double result;
    if (k == 0)
	result = (double)0.0;
    else
	result = log((double)k) + log_factorial(k - 1);
    return (result);
  */
}

