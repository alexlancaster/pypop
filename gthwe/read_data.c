/************************************************************************
  program name: read_data.c

  funtion to read data

  status: modified from g-t program

  date: 12/15/99

*************************************************************************/
#include "hwe.h"

int read_data(int a[LENGTH], int *no_allele, int *total,\
 struct randomization *sample, FILE **infile, char *title)
{
	register int i, j, l, err = 1;

	*total = 0;

	if (fscanf(*infile, "%s", title) != 1)
	{
		fprintf(stderr, "Please supply title\n");
		printf("title %s", title);
		return (err);
	}

	if (fscanf(*infile, "%d", no_allele) != 1)
	{
		fprintf(stderr, "Please supply number of alleles\n");
		return (err);
	}

	if (*no_allele < 3)
	{
		fprintf(stderr, "***Error! Number of alleles less than 3. \n");
		return (err);
	}

	for (i = 0; i < *no_allele; ++i)
	{
		for (j = 0; j <= i; ++j)
		{
			l = LL(i, j);
			fscanf(*infile, "%d ", &a[l]);
			*total += a[l];
		}
	}

	if (fscanf(*infile, "%d %d %d \n", &sample->step,
						 &sample->group, &sample->size) != 3)
	{
		fprintf(stderr, " Please supply parameters.\n");
		return (err);
	}
	else if (sample->step < 1 || sample->group <= 1)
	{
		fprintf(stderr, "***Error in parameter specification.\n");
		return (err);
	}

	return (0);

}

