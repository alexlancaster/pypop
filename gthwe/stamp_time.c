/***********************************************************************
  program name: stamp_time.c

  function to stamp the date and time the program is executed.

  Status: modified from g-t program

  Date: 12/14/99 

************************************************************************/
#include "hwe.h"

void stamp_time(t1, outfile)

		 long t1;
		 FILE **outfile;

{
	char *ctime();
	long t2, now;
	long time();

	time(&t2);
	t2 -= t1;
	time(&now);

#ifndef XML_OUTPUT
	fprintf(*outfile, "\nTotal elapsed time: %d''\n", t2);
	fprintf(*outfile, "Date and time: %s\n", ctime(&now));
#else
	fprintf(*outfile, "<elapsed-time>%d</elapsed-time>\n", t2);
	fprintf(*outfile, "<timestamp>%s</timestamp>\n", ctime(&now));
#endif
}
