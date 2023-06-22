************************************************
Installation instructions for old 0.7.0 binaries
************************************************

.. danger::

   These instructions refer to the now out-of-date 0.7.0 binaries for
   the Python 2 version of PyPop and will likely not work on newer
   systems. They are provided only for historical purposes, and will
   soon be removed once 1.0.0 binaries for the new Python 3-based
   version are available via `PyPI <https://pypi.org/>`__.  Please
   refer to the newer instructions in :doc:`guide-chapter-install` for
   how to compile and install pre-release version(s).
   
.. _install-standalone:

Installing standalone binary
============================

Standalone binary versions are provided for PyPop that make minimal
assumptions about external software installed on your system, and for
the majority of users, will be the simplest way to install PyPop. We
have only tested them on a subset of the possible operating systems and
have noted them in the relevant section below.

.. note::

   * GNU/Linux (the Linux binary needs a recent distribution that a
     recent glibc (2.8 has been tested): Fedora Core 9 is known to
     work, earlier versions of Red Hat such as the 7.x series and 8.0
     are known to not work).
   * Windows (originally tested on Windows 98, 2000 and XP)   


.. _install-standalone-linux:

Installing on GNU/Linux
-----------------------

**System requirements.**

Your GNU/Linux system should contain at least 2.6 version of ``glibc``
(the GNU C library).

**Systems tested.**

Fedora 8 (may work on other distributions but untested at present,
earlier versions were tested on Red Hat 9 Fedora Core 2, 3, 7, Slackware
9.1 but may now have out of date versions of glibc)

1. Download the latest stable release and save it somewhere in your home
   directory:

   - `PyPopLinux-0.7.0.tar.gz <../PyPopLinux-0.7.0.tar.gz>`__

2. From the command-line terminal untar and uncompress the package
   (typically using the GNU ``tar`` program):

   ::

      $ tar zxf PyPopLinux-0.7.0.tar.gz

At this point PyPop should be successfully installed. To test your
installation, run the program and use the sample test files with the
following steps:

1. Change directory into the extracted directory

   ::

      $ cd PyPopLinux-0.7.0

2. Now you can run the interactive version of the program, by typing
   ``./pypop``, at the command line.

   A short message describing PyPop will be displayed, followed by
   prompts to supply the name of the configuration file and then the
   population file. Select the file, ``sample.ini`` and ``sample.pop``,
   respectively (noted in the sample screen output below, in **bold**).

   ::

      PyPop: Python for Population Genomics (0.4.3)
      Copyright (C) 2003 Regents of the University of California
      This is free software.  There is NO warranty; not even for
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
       
      You may redistribute copies of PyPop under the terms of the
      GNU General Public License.  For more information about these
      matters, see the file named COPYING.
       
      To accept the default in brackets for each filename, simply press
      return for each prompt.
      Please enter config filename [config.ini]: sample.ini
      Please enter population filename [no default]: sample.pop
      PyPop is processing sample.pop 

      (Note: some messages with the prefix "LOG:" may appear here.
      They are informational only and do not indicate improper operation 
      of the program)

      PyPop run complete!
      XML output can be found in: sample-out.xml
      Plain text output can be found in: sample-out.txt

   PyPop will remember the names of the configuration and population
   files you used last, and will provide those as defaults in subsequent
   runs.

.. _install-standalone-windows:

Installing on Windows
---------------------

**System requirements.**

At least Windows 98

**Systems tested.**

Windows 2000, Windows XP (may work on other platforms but untested at
present)

1. Before starting an install on Windows, you must first make sure you
   have a copy of a zip file extractor such as PowerArchiver or WinZip.

2. Download the latest stable Windows release of PyPop and save it in
   one of your directories or on the Desktop:

   -  `PyPopWin32-0.7.0.zip <../PyPopWin32-0.7.0.zip>`__

3. Once you have downloaded the file, you should double-click it. If you
   have correctly installed one of the zip compression utilities, it
   should open using that zip program. Extract the contents of the zip
   file to your desktop, or wherever you normally save your programs and
   data. Consult the documentation for your archiving utility for
   details on how to do this (it should be reasonably self-explanatory).

To test your installation:

1. Once you have the ``PyPopWin32-0.7.0`` directory extracted, open the
   directory and double-click on the ``pypop.bat`` file.

2. A DOS shell should then open running the program inside it.

   A short message describing PyPop will be displayed, followed by
   prompts to supply the name of the configuration file and then the
   population file. Select the file, ``sample.ini`` and ``sample.pop``,
   respectively (noted in the sample screen output below, in **bold**).

   ::

      PyPop: Python for Population Genomics (0.4.3)
      Copyright (C) 2003 Regents of the University of California
      This is free software.  There is NO warranty; not even for
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
       
      You may redistribute copies of PyPop under the terms of the
      GNU General Public License.  For more information about these
      matters, see the file named COPYING.
       
      To accept the default in brackets for each filename, simply press
      return for each prompt.
      Please enter config filename [config.ini]: sample.ini
      Please enter population filename [no default]: sample.pop
      PyPop is processing sample.pop 

      (Note: some messages with the prefix "LOG:" may appear here.
      They are informational only and do not indicate improper operation 
      of the program)

      PyPop run complete!
      XML output can be found in: sample-out.xml
      Plain text output can be found in: sample-out.txt

.. _install-from-source:

Installing from source
======================

The source code for PyPop can be obtained here:

-  http://www.pypop.org/pypop-0.7.0.tar.gz

-  In addition, because the Windows binary distributes a copy of the
   ``cygwin1.dll``, we are required under the terms of the GNU GPL to
   provide a copy of the Cygwin source which we compiled the binary
   from: ` <http://www.pypop.org/cygwin-1.5.24-2.tar.bz2>`__.

   .. note::

      Note that this only required for Windows and is *not* required for
      compilation even under Windows if you install within the Cygwin
      environment (because it already contains a copy ``cygwin1.dll``)
      and is only provided for legal reasons.

.. _install-from-source-sysreq:

System requirements
-------------------

-  `Python 2.4 <http://www.python.org/>`__ or later.

-  `Numerical Python (Numpy) (Numpy)
   24.0 <http://numpy.sourceforge.net/>`__

-  `Simple Wrapper Interface Generator (SWIG) <http://www.swig.org/>`__:
   uses "development" version (should now be compatible with all recent
   SWIG versions: last tested against SWIG 1.3.31).

-  `libxml2/libxslt <http://xmlsoft.org/>`__ including
   `libxml2-python <http://xmlsoft.org/XSLT/python.html>`__, a Python
   interface to the GNOME XML/XSLT parser (This is a fast C
   library-based parser. Most recent GNU/Linux distributions will
   install libxml2/libxslt as part of the base distribution, but you may
   need to install libxml2-python and libxslt-python separately).

   (Untested recently: `4Suite <http://www.4suite.org/>`__ a pure Python
   XML/XSLT parsing engine.)

-  The GNU Scientific Library
   (`GSL <http://www.gnu.org/software/gsl/>`__) On Fedora you will want
   to install the gsl-devel package.

.. _install-from-source-install:

Installation
------------

*Before starting, you must ensure you have installed all the system
requirements listed above. In particular, make sure Python is installed
correctly.*

Unzip and untar the above tar ball. Build and install PyPop by changing
into the ``PyPop-0.7.0`` directory, and type:

::

   python setup.py build
   python setup.py install

If you need to do additional configuration (e.g. changing the base
directory) please type ``python setup.py``, or see the documentation for
Distutils.

.. _install-from-source-distribution:

Distribution structure
----------------------

::

   AUTHORS --      A list of people who have contributed.
   emhaplofreq/ -- LD and haplotype estimation extension module
   pval/ --        Modified code from R project for p-value calculation
   slatkin-exact/  Slatkin's code for Ewens-Watterson exact test
   gthwe/          Modified Guo and Thompson Hardy-Weinberg code
   SWIG/ --        Helper code for SWIG for generating C-Python wrappers
   xslt/ --        XSLT for generating text and other output from XML
   COPYING --      License information for this package
   MANIFEST.in --  Tells distutils what files to distribute
   NEWS --         Release notes and news
   README --       Information and TODO list.
   INSTALL --      This file
   setup.py --     Installation file.
        
