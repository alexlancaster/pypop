CC=gcc
ALL_CPPFLAGS=-DMATHLIB_STANDALONE -I.

%.o:%.c
	$(CC) $(ALL_CPPFLAGS) $(ALL_CFLAGS) -c $< -o $@

SOURCES_NMATH = mlutils.c fmin2.c ftrunc.c chebyshev.c lgammacor.c	\
gamma.c lgamma.c pgamma.c pnorm.c pchisq.c pval.c

SOURCES = $(SOURCES_NMATH)
OBJECTS = $(SOURCES:.c=.o)

.SUFFIXES: .c .o

all: pval

pval: $(OBJECTS)
	$(CC) -o $@ $(ALL_CPPFLAGS) $(ALL_CFLAGS) $(OBJECTS) -lm

.PHONY: clean

clean:
	rm $(OBJECTS) pval