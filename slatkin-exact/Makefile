CC=gcc
EXTRACFLAGS=

CFLAGS=-O3 -g -funroll-loops -ansi -pedantic -Wall -Wstrict-prototypes $(EXTRACFLAGS) 

all: monte-carlo monte-carlo_distribution

monte-carlo: monte-carlo.c
	$(CC) $(CFLAGS) -o monte-carlo monte-carlo.c

monte-carlo_distribution: monte-carlo.c
	$(CC) $(CFLAGS) -DDISTRIBUTION_OUTPUT=1 -o monte-carlo_distribution monte-carlo.c

clean:
	- rm -f monte-carlo monte-carlo_distribution
