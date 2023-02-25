/* This file is part of PyPop
  
  Copyright (C) 1992. Sun-Wei Guo.
  Modifications Copyright (C) 1999, 2003, 2004. 
  The Regents of the University of California (Regents) All Rights Reserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
USA.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF
ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION
TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS. */

/************************************************************************
  program name: print_data.c

  functio to print out the data

  status: modified from g-t program

  date: 12/14/99

*************************************************************************/

#include "hwe.h"

void print_data(a, no_allele, sample, outfile, title)

		 int *a;
		 int no_allele;
		 char title[80];
		 struct randomization sample;
		 FILE **outfile;


{

	register int i, j, k, l;
	char line[256];

	line[0] = '-';

	k = 1;
	
#ifndef XML_OUTPUT
 	fprintf(*outfile, "Data set: %s\n\n", title);
	fprintf(*outfile, "Observed genotype frequencies: \n\n");
#else
 	xmlfprintf(*outfile, "<name>%s</name>\n", title);
	xmlfprintf(*outfile, "<frequencies kind=\"genotype\" type=\"observed\">\n");
#endif
	
	for (i = 0; i < no_allele; ++i)
	{

		for (j = k; j < k + 5; ++j)
			line[j] = '-';

		line[j] = STR_END;
		k = j;

#ifndef XML_OUTPUT
		fprintf(*outfile, "%s\n", line);

		fprintf(*outfile, "|");
#endif
		for (j = 0; j <= i; ++j)
		{
			l = LL(i, j);
#ifndef XML_OUTPUT
			fprintf(*outfile, "%4d|", a[l]);
#else
			xmlfprintf(*outfile, "<count allele1=\"%d\" allele2=\"%d\">%d</count>\n", i, j, a[l]);
#endif
		}
#ifndef XML_OUTPUT
		fprintf(*outfile, "\n");
#else
		xmlfprintf(*outfile, "\n");
#endif
	}

#ifndef XML_OUTPUT
	fprintf(*outfile, "%s\n\n", line);
	fprintf(*outfile, "Total number of alleles: %2d\n\n", no_allele);

	fprintf(*outfile, "Number of initial steps: %d\n", sample.step);
	fprintf(*outfile, "Number of chunks: %d\n", sample.group);
	fprintf(*outfile, "Size of each chunk: %d\n\n", sample.size);
#else
	xmlfprintf(*outfile, "</frequencies>");
	xmlfprintf(*outfile, "<allelecount>%d</allelecount>\n", no_allele);

	xmlfprintf(*outfile, "<initialsteps>%d</initialsteps>\n", sample.step);
	xmlfprintf(*outfile, "<chunks>%d</chunks>\n", sample.group);
	xmlfprintf(*outfile, "<chunksize>%d</chunksize>\n", sample.size);
#endif


}
