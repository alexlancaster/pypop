PROFILING=no
CC=gcc

CFLAGS=-O2 -g -static -funroll-loops
LIBS=-lm
ifeq ($(PROFILING),yes)
	CFLAGS+=-pg
	LIBS+=-lc_p
endif

OBJS=emhaplofreq.o

emhaplofreq: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o emhaplofreq $(LIBS)
# make a symlink to run for backwards-compatibility
	ln -s emhaplofreq run

.c.o:
	$(CC) $(CFLAGS) -c -o $*.o $<

final: emhaplofreq
	strip emhaplofreq

clean:
	- rm -f $(OBJS) run emhaplofreq
