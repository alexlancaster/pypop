PROFILING=no
CC=gcc

CFLAGS=-O3 -g -funroll-loops
LIBS=-lm
ifeq ($(PROFILING),yes)
	CFLAGS+=-pg -a
#	LIBS+=-lc_p
endif

OBJS=emhaplofreq.o

emhaplofreq: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o emhaplofreq $(LIBS)
# make a symlink to run for backwards-compatibility
	ln -sf emhaplofreq run

%.o: %.c %.h
	$(CC) $(CFLAGS) -c -o $*.o $<

final: emhaplofreq
	strip emhaplofreq

clean:
	- rm -f $(OBJS) run emhaplofreq
