/************************************************************************

  function to check execution command and file

  status: modified from g-t program

  date: 12/14/99

*************************************************************************/

#include "hwe.h"

int check_file(int argc, char *argv[], FILE **infile, FILE **outfile)
{

	int exit_value = 0;

	/* file manipulation */

	if (argc != 3)
	{
		fprintf(stderr, "\nUsage: gthwe infile outfile.\n\n");
		exit_value = 1;
	}

	else if ((*infile = fopen(argv[1], "r")) == (FILE *) NULL)
	{
		fprintf(stderr, "Can't read %s\n\n", argv[1]);
		exit_value = 2;
	}

	else if ((*outfile = fopen(argv[2], "w")) == (FILE *) NULL)
	{
		fprintf(stderr, "Can't write %s\n\n", argv[2]);
		exit_value = 3;
	}

	return (exit_value);
}

