/******************************************
* Random number generator
* Splus style
* John Chen
* 12/14/99
*******************************************/

#include <math.h>
#include "func.h"
#include "hwe.h"

double new_rand()
		{
	extern unsigned long congrval, tausval;
	unsigned long n, lambda = 69069;
		congrval = congrval * lambda;
		tausval ^=tausval >> 15;
		tausval ^= tausval << 17;
		n  = tausval ^ congrval;

/*		printf("\nnew= %u\t %u \t %u\n", congrval, tausval, n );
*/		return((((n>>1) & 017777777777)) / 2147483648.);
		}
