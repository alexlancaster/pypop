PROFILING=no
CC=gcc
EXTRACFLAGS=

CFLAGS=-O3 -g -funroll-loops $(EXTRACFLAGS)
LIBS=-lm
ifeq ($(PROFILING),yes)
	CFLAGS+=-pg -a
#	LIBS+=-lc_p
endif

OBJS=emhaplofreq.o

all: emhaplofreq

emhaplofreq.o: emhaplofreq.c emhaplofreq.h

emhaplofreq: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o emhaplofreq $(LIBS)
# make a symlink to run for backwards-compatibility
	ln -sf emhaplofreq run

final: emhaplofreq
	strip emhaplofreq

clean:
	- rm -f $(OBJS) run emhaplofreq
