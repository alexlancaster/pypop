/*  
This program implements a Monte Carlo algorithm to perform both the 
homozygosity and exact tests on a sampling of alleles.  It uses an 
algorithm devised by Frank Stewart to generate random configurations 
from the Ewens sampling distribution.

To use the program, you need to list the number of copies of each allele as 
elements of the vector r_obs listed just below the beginning of the main 
program below.  The data do not have to be in decreasing order, as they 
do for the program that enumerates all configurations.

Two sample data sets are included.  The first is the sample data set used in
the 1994 paper in Genetical Research (64: 71-74).  This data set can also be 
analyzed using ENUMERATE.  The second data set contains the numbers of the 
24 most frequent cystic fibrosis alleles in a sample of CF cases in northern 
Europe.  This data set is much too large to be analyzed using the other 
program.  The second data set should produce the output

n = 16975, k = 24, theta = 2.681168, F = 0.768561, maxrep = 100000
P_E(approx) = 0.28207
P_H(approx) = 0.99802

It took about 25 minutes on a 100 mhz HP workstation for 100,000 replicates.

To use a data set, remove the / and * symbols that indicate a comment 
from one of the r_obs.

The program produces two output values.  The first is the value of P_H, 
the tail probability for the Ewens-Watterson test using homozygosity as 
a test statistic.  The second is P_E, the tail probability for the exact 
test.  For small data sets, including the first sample data set, the two 
values are the same.  The 1994 paper was wrong in claiming otherwise and 
that error was corrected in the 1996 paper in Genetical Research 
{68: 259-260).  For larger data sets, the P values can differ, sometimes 
substantially, as in the second sample data set.

MONTE CARLO requires a random number seed (initseed), which you can change 
by editing the file.  If you change initseed or the data set, you have 
to recompile the program.  Once the program is compiled, you run it by 
specifying the number of replicates on the command line.  Usually, 100,000 
replicates is more than sufficient but you can try different values to 
find out for yourself. 
*/
  
#include <stdio.h>
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <time.h>

#define min(x, y)  (((x) < (y)) ? x : y)

static int seed;

void main(int argc, char *argv[]) {

	int initseed = 13840399;

	/*  int r_obs[] = {0, YOUR DATA HERE, 0};  */
	/*  int r_obs[] = {0, 9, 2, 1, 1, 1, 1, 1, 0};  */
	/*  int r_obs[] = {0, 30, 62, 97, 15, 53, 18, 55, 35, 57, 14866, 
		160, 439, 18, 356, 165, 40, 41, 14, 27, 36, 39, 23, 120, 209, 0};  
		//  CF alleles from North Europe: P_H = 0.9977   */

	int i, j, k, n, repno, maxrep, Ecount, Fcount;
	int *r_random, testE, testF;
	double ewens_stat(int *r), F(int k, int n, int *r);
	double theta_est(int k_obs, int n);
	double E_obs, F_obs;
	void print_config(int k, int *r);
	void generate(int k, int n, int *r, double *ranvec, double **b);
	long start_time, finish_time, net_time;
	double **b, **matrix(long nrl, long nrh, long ncl, long nch), *ranvec;
	double *vector(long nl, long nh);
	int *ivector(long nl, long nh);
	void gsrand(int seed);

	start_time = time(NULL);
	if (argc != 2)  {
	printf("Specify the number of replicates on the command line\n");
		exit(0);
		}
	maxrep = atoi(argv[1]);
	gsrand(initseed);
	
	/* Find k and n from the observed configuration  */
	
	k = 0;
	n = 0;
	while (r_obs[k+1]) {
		k++;
		n+=r_obs[k];
		}
	r_random = ivector(0, k+1);
	r_random[0] = r_random[k+1] = 0;
	ranvec = vector(1, k-1);  // to avoid doing this in each replicate
	
	/*  fill b matrix  */
	
	b = matrix(1, k, 1, n);
	for (j=1; j<=n; j++)
		b[1][j] = 1.0 / j;
	for (i=2; i<=k; i++)  {
		b[i][i] = 1.0;
		for (j=i; j<n; j++)
			b[i][j+1] = (i * b[i-1][j] + j * b[i][j]) / (j + 1.0);
		}
		
	F_obs = F(k, n, r_obs);
	E_obs = ewens_stat(r_obs);
	printf("\nn = %d, k = %d, theta = %g, F = %g, maxrep = %d\n",
		n, k, theta_est(k, n), F_obs, maxrep);
	Ecount = 0;
	Fcount = 0;
	for (repno=1; repno<=maxrep; repno++)  {
		generate(k, n, r_random, ranvec, b);
		if (ewens_stat(r_random) <= E_obs) 
			Ecount++;
		if (F(k, n, r_random) <= F_obs)
			Fcount++;
		}
	printf("P_E(approx) = %g\nP_H(approx) = %g\n", 
		(double) Ecount / maxrep, (double) Fcount / maxrep);
	finish_time = time(NULL);
	net_time = time(NULL) - start_time;
	if (net_time < 60)
		printf("Program took %ld seconds\n", net_time);
	else
		printf("Program took %4.2f minutes\n", net_time / 60.0);
  }  /*  end, main  */

void generate(int k, int n, int *r, double *ranvec, double **b)  {  
	double unif(), cum, x;
	int i, l, nleft;
	double *rpt;
	
	for (i=1; i<=k-1; i++)
		ranvec[i] = unif();
	nleft = n;
	for (l=1; l<k; l++)  {
		cum = 0.0;
		for (i=1; i<=nleft; i++) {
			cum += b[k-l][nleft-i] / (i * b[k-l+1][nleft]);
			if (cum >= ranvec[l]) break;
			}
		r[l] = i;
		nleft -= i;
		}
	r[k] = nleft;
	}

void print_config(int k, int *r) {
	int i;

	printf("(");
	for (i=1; i<k; i++)
		printf("%d,", r[i]);
	printf("%d)", r[k]);
	printf("\n");
	}

double ewens_stat(int *r)  {
	int *ipt;
	double coef;

	coef = 1.0;
	for (ipt=r+1; *ipt; ipt++)
		coef *= *ipt;
	return 1.0 / coef;
	}

double F(int k, int n, int *r)  {
  int i;
  double sum;

  sum = 0.0;
  for (i=1; i<=k; i++)  sum += r[i] * r[i];
  return sum / (n * n);
  }

double theta_est(int k_obs, int n)  {
/*  Estimates theta = 4N*mu using formula 9.26 in Ewens' book  */
	double kval(double theta, int n);
	double xlow, xhigh, xmid;
	double eps;
	
	eps = 0.00001;
	xlow = 0.1;
	while (kval(xlow, n) > k_obs)
		xlow /= 10.0;
	xhigh = 10.0;
	while (kval(xhigh, n) < k_obs)
		xhigh *= 10.0;
	while ((xhigh - xlow) > eps)  {
		xmid = (xhigh + xlow) / 2.0;
		if (kval(xmid, n) > k_obs)
			xhigh = xmid;
		else
			xlow = xmid;
		}
	return xmid;
	}  /*  end, theta_est  */

double kval(double x, int n)  {
	int i;
	double sum;
	
	sum = 0.0;
	for (i=0; i<n; i++)
		sum += x / (i + x);
	return sum;
	}

#define NR_END 1

double **matrix(long nrl, long nrh, long ncl, long nch)
/* allocate a double matrix with subscript range m[nrl..nrh][ncl..nch] */
{
	long i, nrow=nrh-nrl+1,ncol=nch-ncl+1;
	double **m;
	void nrerror(char error_text[]);

	/* allocate pointers to rows */
	m=(double **) malloc((size_t)((nrow+NR_END)*sizeof(double*)));
	if (!m) nrerror("allocation failure 1 in matrix()");
	m += NR_END;
	m -= nrl;

	/* allocate rows and set pointers to them */
	m[nrl]=(double *) malloc((size_t)((nrow*ncol+NR_END)*sizeof(double)));
	if (!m[nrl]) nrerror("allocation failure 2 in matrix()");
	m[nrl] += NR_END;
	m[nrl] -= ncl;

	for(i=nrl+1;i<=nrh;i++) m[i]=m[i-1]+ncol;

	/* return pointer to array of pointers to rows */
	return m;
}

double *vector(long nl, long nh)
/* allocate a double vector with subscript range v[nl..nh] */
{
	double *v;
	void nrerror(char error_text[]);
	
	v=(double *)malloc((size_t) ((nh-nl+1+NR_END)*sizeof(double)));
	if (!v) nrerror("allocation failure in vector()");
	return v-nl+NR_END;
}

int *ivector(long nl, long nh)
/* allocate an int vector with subscript range v[nl..nh] */
{
	int *v;
	void nrerror(char error_text[]);

	v=(int *)malloc((size_t) ((nh-nl+1+NR_END)*sizeof(int)));
	if (!v) nrerror("allocation failure in ivector()");
	return v-nl+NR_END;
}

void nrerror(char error_text[])
{
	fprintf(stderr,"Run-time error...\n");
	fprintf(stderr,"%s\n",error_text);
	fprintf(stderr,"...now exiting to system...\n");
	exit(1);
}


#define A 16807
#define M 2147483647
#define Q 127773
#define R 2836

void gsrand(s)
int s;
{
	seed = s;
}

#define RM 2147483647.0

double unif()  /* This is drand renamed to be consistent with my usage  */
{
	int grand();
	return ((double) grand() / RM);
}

int grand()
{
	int test;
	
    test = A * (seed % Q) - R * (seed / Q);
    if (test > 0) seed = test;
      else seed = test + M;
    return(seed);
}
