/***********************************************************************

  program name: hwe.c
  
  main program


  Status: modified from g-t program

  Date: 12/14/99

************************************************************************/

#include <time.h>
#include "hwe.h"
#include "func.h"
#include <math.h>

int main(int argc, char *argv[])
/* correct execution of this program: hwe infile outfile */
{
	int a[LENGTH], n[MAX_ALLELE];
	unsigned long xxx[12];

	unsigned long  conorig=0;
	unsigned long  tauorig=0;

	extern unsigned long congrval, tausval;

	double ln_p_observed, ln_p_simulated, p_mean, p_square; 
	double constant, p_simulated, total_step;
	int no_allele, total, counter, actual_switch;
	Index index;
	struct randomization sample;
	struct outcome result;
	FILE *infile, *outfile;
	long t1;

	char title[80];

	register int i, j;

	if (check_file(argc, argv, &infile, &outfile))
		exit(1);

	printf("Just a second. \n");

	srand(time(NULL));

	/* seeds selection for Splus type random number generator. */	
	for (i = 0; i < 12; i++) {

		xxx[i] = (unsigned long) (floor((64.0 * rand())/(RAND_MAX))) ; 
		if (xxx[i] == 64)
		{ 
		xxx[i] = 63;
		}
		 
}

		for (j = 0; j < 6; ++j) {
		   tauorig =  (((tauorig + (xxx[j + 6] * (pow(2, (6 * j))))))) ;
		   conorig =  (((conorig + (xxx[j] * (pow(2, (6 * j)))))));
}		
		while (conorig > 4294967295. )
			conorig -= 4294967295.;
			congrval = (unsigned long) conorig ;
		while (tauorig > 4294967295. )
			tauorig -= 4294967295.;
			tausval = (unsigned long) tauorig;
	time(&t1);

	if (read_data(a, &no_allele, &total, &sample, &infile, &title))
		exit(2);

#ifdef XML_OUTPUT
	fprintf(outfile, "<?xml? version='1.0'>\n");
	fprintf(outfile, "<singlelocus type=\"gthwe\">\n");
#endif

	print_data(a, no_allele, sample, &outfile, title);
	
	constant = cal_const ( no_allele, n, total );

	ln_p_observed = ln_p_value ( a, no_allele, constant );  
	
	ln_p_simulated = ln_p_observed; 

	p_mean = p_square = (double) 0.0;

	result.p_value = result.se = (double) 0.0;	/* initialization */

	result.swch_count[0] = result.swch_count[1] = result.swch_count[2] = 0;

	for (i = 0; i < sample.step; ++i)
	{												/* de-memorization for given steps */

		select_index(&index, no_allele);

		ln_p_simulated = cal_prob(a, index, ln_p_simulated, &actual_switch);
		++result.swch_count[actual_switch];
	}

	for (i = 0; i < sample.group; ++i)
	{

		counter = 0;

		for (j = 0; j < sample.size; ++j)
		{
			select_index(&index, no_allele);
			ln_p_simulated = cal_prob(a, index, ln_p_simulated, &actual_switch);

			if (ln_p_simulated <= ln_p_observed)  
				++counter;
			++result.swch_count[actual_switch];

		}
		p_simulated = (double) counter / sample.size;
		p_mean += p_simulated;
		p_square += p_simulated * p_simulated;

	}
	p_mean /= sample.group;
	result.p_value = p_mean;
	result.se = p_square / ((double) sample.group) / (sample.group - 1.0)
		- p_mean / (sample.group - 1.0) * p_mean;
	result.se = sqrt(result.se);

	total_step = sample.step + sample.group * sample.size;

#ifndef XML_OUTPUT
	fprintf(outfile, "Randomization test P-value: %7.4g  (%7.4g) \n",
					result.p_value, result.se);
	fprintf(outfile, "Percentage of partial switches: %6.2f \n",
					result.swch_count[1] / total_step * 100);
	fprintf(outfile, "Percentage of full switches: %6.2f \n",
					result.swch_count[2] / total_step * 100);
	fprintf(outfile, "Percentage of all switches: %6.2f \n",
					(result.swch_count[1] + result.swch_count[2]) / total_step * 100);
#else
	fprintf(outfile, "<pvalue>%7.4g</pvalue><stderr>%7.4g</stderr>\n",
					result.p_value, result.se);
	fprintf(outfile, "<switches>\n");
	fprintf(outfile, "<percent-partial>%6.2f</percent-partial>\n",
					result.swch_count[1] / total_step * 100);
	fprintf(outfile, "<percent-full>%6.2f</percent-full>\n",
					result.swch_count[2] / total_step * 100);
	fprintf(outfile, "<percent-all>%6.2f</percent-all>\n",
					(result.swch_count[1] + result.swch_count[2]) / total_step * 100);
	fprintf(outfile, "</switches>\n");
#endif

	stamp_time(t1, &outfile);

#ifdef XML_OUTPUT
	fprintf(outfile, "</singlelocus>");
#endif
	return (0);

}

