#
# ${R_HOME}/src/nmath/standalone/Makefile

#VPATH = @srcdir@
#srcdir = @srcdir@
#top_srcdir = @top_srcdir@

#top_builddir = ../../..
#subdir = src/nmath/standalone

#include $(top_builddir)/Makeconf

ALL_CPPFLAGS=-DMATHLIB_STANDALONE

.c.o:
	C_INCLUDE_PATH=. $(CC) $(ALL_CPPFLAGS) $(ALL_CFLAGS) -c $< -o $@

SOURCES_NMATH = mlutils.c fmin2.c ftrunc.c chebyshev.c lgammacor.c	\
gamma.c lgamma.c pgamma.c pnorm.c pchisq.c pval.c

SOURCES = $(SOURCES_NMATH) #std_unif.c
OBJECTS = $(SOURCES:.c=.o)


.SUFFIXES:
.SUFFIXES: .c .o

all: pval

pval: $(OBJECTS)
	$(CC) -o $@ $(ALL_CPPFLAGS) $(ALL_CFLAGS) $(OBJECTS) -lm

