/**************************************************************************
  program name: cal_const.c

  function to compute the constant part of the probability function for
  testing the H-W equilibrium

  constant = log N! - log (2N)! + sum(i) log n(i)! 

  status: modified from g-t program

  date: 12/14/99

**************************************************************************/
#include "hwe.h"

double cal_const(int no_allele, int *n, int total)
{
  register int i;
  double constant;
  double log_factorial();
  
  constant = log_factorial(total) - log_factorial(2 * total);
  
  for (i = 0; i < no_allele; ++i)
    constant += log_factorial(n[i]);
  
  return (constant);
}

