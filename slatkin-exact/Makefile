CC=gcc
LIBS=-lm
EXTRACFLAGS=
CFLAGS=-O3 -funroll-loops -ansi -pedantic -Wall -Wstrict-prototypes $(EXTRACFLAGS) 
DFLAGS=-g -static

all: monte-carlo monte-carlo_distribution

monte-carlo: monte-carlo.c
	$(CC) $(CFLAGS) -o monte-carlo monte-carlo.c $(LIBS)

monte-carlo_distribution: monte-carlo.c
	$(CC) $(DFLAGS) -DDISTRIBUTION_OUTPUT=1 -o monte-carlo_distribution monte-carlo.c $(LIBS) 

clean:
	- rm -f monte-carlo monte-carlo_distribution
