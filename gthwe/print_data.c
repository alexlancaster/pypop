/************************************************************************
  program name: print_data.c

  functio to print out the data

  status: modified from g-t program

  date: 12/14/99

*************************************************************************/

#include "hwe.h"

void print_data(a, no_allele, sample, outfile, title)

		 int a[LENGTH];
		 int no_allele;
		 char title[80];
		 struct randomization sample;
		 FILE **outfile;


{

	register i, j, k, l;
	char line[256];

	line[0] = '-';

	k = 1;

	fprintf(*outfile, "Data set: %s\n\n", title);
	fprintf(*outfile, "Observed genotype frequencies: \n\n");

	for (i = 0; i < no_allele; ++i)
	{

		for (j = k; j < k + 5; ++j)
			line[j] = '-';

		line[j] = STR_END;
		k = j;

		fprintf(*outfile, "%s\n", line);

		fprintf(*outfile, "|");

		for (j = 0; j <= i; ++j)
		{
			l = LL(i, j);
			fprintf(*outfile, "%4d|", a[l]);
		}

		fprintf(*outfile, "\n");
	}

	fprintf(*outfile, "%s\n\n", line);
	fprintf(*outfile, "Total number of alleles: %2d\n\n", no_allele);

	fprintf(*outfile, "Number of initial steps: %d\n", sample.step);
	fprintf(*outfile, "Number of chunks: %d\n", sample.group);
	fprintf(*outfile, "Size of each chunk: %d\n\n", sample.size);

}
