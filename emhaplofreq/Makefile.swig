SWIG       = swig
SRCS       = emhaplofreq.c
TARGET     = emhaplofreq
INTERFACE  = emhaplofreq.i

IWRAP      = $(INTERFACE:.i=_wrap.i)
ISRCS      = $(IWRAP:.i=.c)
ICXXSRCS   = $(IWRAP:.i=.cxx)
IOBJS      = $(IWRAP:.i=.o)

# Compiler flags
CC         = gcc

# Symbols used for using shared libraries
SO=		.so
LDSHARED=	gcc -shared
CCSHARED=	-fpic
CXXSHARED=      gcc -shared

# This is used for building shared libraries with a number of C++
# compilers.   If it doesn't work,  comment it out.

CXXSHARED=      c++ -shared 

OBJS      = $(SRCS:.c=.o) $(CXXSRCS:.cxx=.o)

##################################################################
#####                       PYTHON                          ######
##################################################################

# Make sure these locate your Python installation
PYTHON_INCLUDE= -DHAVE_CONFIG_H -I/usr/include/python2.1 -I/usr/lib/python2.1/config
PYTHON_LIB    = /usr/lib/python2.1/config

# ----------------------------------------------------------------
# Build a C dynamically loadable module
# ----------------------------------------------------------------

python: $(SRCS)
	$(SWIG) -python $(SWIGOPT) $(INTERFACE)
	$(CC) -c $(CCSHARED) $(CFLAGS) $(ISRCS) $(SRCS) $(INCLUDE) $(PYTHON_INCLUDE)
	$(LDSHARED) $(OBJS) $(IOBJS) $(LIBS) -o $(TARGET)module$(SO)

# -----------------------------------------------------------------
# Build a C++ dynamically loadable module
# -----------------------------------------------------------------

python_cpp: $(SRCS)
	$(SWIG) -c++ -python $(SWIGOPT) $(INTERFACE)
	$(CXX) -c $(CCSHARED) $(CFLAGS) $(ICXXSRCS) $(SRCS) $(CXXSRCS) $(INCLUDE) $(PYTHON_INCLUDE)
	$(CXXSHARED) $(OBJS) $(IOBJS) $(LIBS) $(CPP_DLLIBS) -o $(TARGET)module$(SO)

# -----------------------------------------------------------------
# Build a dynamically loadable module, linked against SWIG Runtime lib
# -----------------------------------------------------------------

PYTHON_RUNTIME=-L$(RUNTIMEDIR) -lswigpy

python_multi: $(SRCS)
	$(SWIG) -c -python $(SWIGOPT) $(INTERFACE)
	$(CC) -c $(CCSHARED) $(CFLAGS) $(ISRCS) $(SRCS) $(INCLUDE) $(PYTHON_INCLUDE)
	$(LDSHARED) $(OBJS) $(IOBJS) $(LIBS) $(PYTHON_RUNTIME) -o $(TARGET)module$(SO)

python_multi_cpp: $(SRCS)
	$(SWIG) -c -c++ -python $(SWIGOPT) $(INTERFACE)
	$(CXX) -c $(CCSHARED) $(CFLAGS) $(ICXXSRCS) $(SRCS) $(CXXSRCS) $(INCLUDE) $(PYTHON_INCLUDE)
	$(CXXSHARED) $(OBJS) $(IOBJS) $(LIBS) $(PYTHON_RUNTIME) $(CPP_DLLIBS) -o $(TARGET)module$(SO)


# -----------------------------------------------------------------
# Build statically linked Python interpreter
#
# These should only be used in conjunction with the %include embed.i
# library file
# -----------------------------------------------------------------

#TKINTER = -L/usr/X11R6.3/lib -L/usr/local/compat/lib -ltk4.0 -ltcl7.4 -lX11
TKINTER =
PYTHON_LIBOPTS = -lpython2.1 -ldl  $(TKINTER) $(SYSLIBS)

python_static: $(SRCS)
	$(SWIG) -python -lembed.i $(SWIGOPT) $(INTERFACE)
	$(CC) $(CFLAGS) -Xlinker -export-dynamic $(ISRCS) $(SRCS) $(INCLUDE) \
	$(PYTHON_INCLUDE) $(LIBS) -L$(PYTHON_LIB) $(PYTHON_LIBOPTS) -o $(TARGET)

python_static_cpp: $(SRCS)
	$(SWIG) -c++ -python -lembed.i $(SWIGOPT) $(INTERFACE)
	$(CXX) $(CFLAGS) $(ICXXSRCS) $(SRCS) $(CXXSRCS) $(INCLUDE) \
	$(PYTHON_INCLUDE) $(LIBS)  -L$(PYTHON_LIB) $(PYTHON_LIBOPTS) -o $(TARGET)



all::
	$(MAKE)  SRCS='$(SRCS)' SWIG='$(SWIG)' \
	TARGET='$(TARGET)' INTERFACE='$(INTERFACE)' python

static::
	$(MAKE)  SRCS='$(SRCS)' SWIG='$(SWIG)' \
	TARGET='mypython' INTERFACE='$(INTERFACE)' python_static

clean::
	rm -f *_wrap* *.o *~ *.so mypython *.pyc .~* core

check: all

# Local variables:
# mode: makefile
# End: