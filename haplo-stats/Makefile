CC=gcc
EXTRACFLAGS=
# -funroll-loops -Wall

CFLAGS=-O3 -g -Wall -DR_NO_REMAP=1 -DMATHLIB_STANDALONE=1 -I../pval $(EXTRACFLAGS) 
LIBS=-lm

OBJS=haplo_em_pin.o

all: haplo_em_pin

haplo_em_pin.o: haplo_em_pin.c haplo_em_pin.h

haplo_em_pin: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o haplo_em_pin $(LIBS)

clean:
	- rm -f $(OBJS) haplo_em_pin
