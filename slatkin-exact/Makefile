CC=gcc

CFLAGS=-O3 -g -funroll-loops $(EXTRACFLAGS)

monte-carlo: monte-carlo.c
	$(CC) $(CFLAGS) -o monte-carlo monte-carlo.c

monte-carlo_distribution:
	$(CC) $(CFLAGS) -DDISTRIBUTION_OUTPUT=1 -o monte-carlo_distribution monte-carlo.c