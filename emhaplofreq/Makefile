CC=gcc
#CFLAGS=-O2 -m486
CFLAGS=-g -static
LIBS=-lm

OBJS=emhaplofreq.o

emhaplofreq: $(OBJS)
	$(CC) $(OBJS) -o emhaplofreq $(LIBS)
	ln -s emhaplofreq run

.c.o:
	$(CC) $(CFLAGS) -c -o $*.o $<

final: emhaplofreq
	strip emhaplofreq

clean:
	- rm $(OBJS) run emhaplofreq
