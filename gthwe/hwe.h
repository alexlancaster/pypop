/***************************************************************************
  program name: hwe.h

  header file for hwe.c

  status: modified from g-t program

  date: 12/14/99

***************************************************************************/

#include  <stdio.h>
#include  <stdlib.h> 
#include  <math.h>
#include  <strings.h>

unsigned long tausval, congrval;

#define  MAX_ALLELE    35
#define  STR_END       '\0'
#define  MAXRAND       RAND_MAX

#define  MIN(x, y)     ((x) < (y)) ? (x) : (y)
#define  RATIO(u, v)   ( (double) (u) ) / ( 1.0 + (double) (v) ) 
#define  TRANS(x)     (MIN(1.0, x))/2.0  /* transition probability */

#define  LL(a, b)      a * ( a + 1 ) / 2  + b
#define  L(a, b)       ( a < b ) ? b*(b + 1)/2 + a : a*(a+1)/2 + b

#define  EXPECT(a,b,c) ((double) a) / ((double) c) * ((double) b) / 2.0

typedef struct _Index
{
  int i1;
  int i2;
  int j1;
  int j2;
  int type;
  double cst;
} Index;

struct outcome 
{
  double p_value;  /* mean p-value */
  double se;       /* standard error of the p-value */
  int swch_count[3];  /* switch counts for partial and full switch */
};

struct randomization 
{
  int group; /* total number of chunks */
  int size;  /* size of a chunk */
  int step;  /* number of steps to de-memerization */
};


