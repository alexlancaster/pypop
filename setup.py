#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2003. The Regents of the University of California (Regents)
# All Rights Reserved.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

# IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT,
# INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING
# LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS
# DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.

# REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING
# DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED "AS
# IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT,
# UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

from distutils.core import setup, Extension
from distutils.file_util import copy_file

import sys, os, string

from distutils.command.build_ext import build_ext
        
# override implementation of swig_sources method in standard build_ext
# class, so we can change the way SWIG is called by Python's default
# configuration of distutils
class my_build_ext(build_ext):

    def swig_sources (self, sources):

        """Walk the list of source files in 'sources', looking for SWIG
        interface (.i) files.  Run SWIG on all that are found, and
        return a modified 'sources' list with SWIG source files replaced
        by the generated C (or C++) files.
        """

        new_sources = []
        swig_sources = []
        swig_targets = {}

        # XXX this drops generated C/C++ files into the source tree, which
        # is fine for developers who want to distribute the generated
        # source -- but there should be an option to put SWIG output in
        # the temp dir.

        if self.swig_cpp:
            target_ext = '.cpp'
        else:
            target_ext = '.c'

        for source in sources:
            (base, ext) = os.path.splitext(source)
            if ext == ".i":             # SWIG interface file
                new_sources.append(base + target_ext)
                swig_sources.append(source)
                swig_targets[source] = new_sources[-1]
            else:
                new_sources.append(source)

        if not swig_sources:
            return new_sources

        swig = self.find_swig()

        if os.environ.has_key('SWIG_VERSION') and os.environ['SWIG_VERSION'] == '1.3.11':
            # in newer version of SWIG, need to use these options
            # to build old style classes/typemaps, required under
            # Cygwin, because newer SWIG version attempts to build
            # extensions in a weird way that Python doesn't understand
            swig_cmd = [swig, "-python", "-classic", "-noproxy", "-ISWIG"]
        else:
            # invoke old-style python, remove the "-dnone" option
            swig_cmd = [swig, "-python", "-ISWIG"]

        if self.swig_cpp:
            swig_cmd.append("-c++")

        for source in swig_sources:
            target = swig_targets[source]
            self.announce("swigging %s to %s" % (source, target))
            self.spawn(swig_cmd + ["-o", target, source])

        return new_sources

    # swig_sources ()

# distutils doesn't currently have an explicit way of setting CFLAGS,
# it takes CFLAGS from the environment variable of the same name, so
# we set the environment to emulate that.
#os.environ['CFLAGS'] = '-funroll-loops'

# flag to determine whether or not we are using the CVS version
if os.path.isdir("CVS"):
    cvs_version=1
else:
    cvs_version=0

    

# define each extension
ext_Emhaplofreq = Extension("_Emhaplofreqmodule",
                            ["emhaplofreq/emhaplofreq_wrap.i",
                             "emhaplofreq/emhaplofreq.c"],
                            include_dirs=["emhaplofreq"],
                            define_macros=[('fprintf', 'pyfprintf'),
                                           ('DEBUG', '0'),
                                           ('EXTERNAL_MODE', '1'),
                                           ('XML_OUTPUT', '1')]
                            )
ext_EWSlatkinExact = Extension("_EWSlatkinExactmodule",
                               ["slatkin-exact/monte-carlo_wrap.i",
                                "slatkin-exact/monte-carlo.c"],
                               )

ext_Pvalue = Extension("_Pvaluemodule",
                       ["pval/pval_wrap.i",
                        "pval/pval.c",
                        "pval/pchisq.c",
                        "pval/chebyshev.c",
                        "pval/ftrunc.c",
                        "pval/lgamma.c",
                        "pval/mlutils.c",
                        "pval/pgamma.c",
                        "pval/fmin2.c",
                        "pval/gamma.c",
                        "pval/lgammacor.c",
                        "pval/pnorm.c"],
                       include_dirs=["pval"],
                       define_macros=[('MATHLIB_STANDALONE', '1')]
                       )

ext_Gthwe = Extension("_Gthwemodule",
                      [ "gthwe/gthwe_wrap.i",
                        "gthwe/hwe.c",
                        "gthwe/cal_const.c",
                        "gthwe/cal_n.c", "gthwe/cal_prob.c",
                        "gthwe/check_file.c",
                        "gthwe/do_switch.c", 
                        "gthwe/new_rand.c",
                        "gthwe/ln_p_value.c",
                        "gthwe/to_calculate_log.c",
                        "gthwe/print_data.c",
                        "gthwe/random_choose.c",
                        "gthwe/read_data.c",
                        "gthwe/select_index.c",
                        "gthwe/stamp_time.c",
                        "gthwe/test_switch.c",
                        "gthwe/statistics.c"],
                      #  "gthwe/gamma.c"], no standalone compilation right now
                      include_dirs=["gthwe"],
                      libraries=["gsl", "gslcblas"],
                      define_macros=[('fprintf', 'pyfprintf'),
                                     ('DEBUG', '0'),
                                     ('INDIVID_GENOTYPES', '1'),
                                     ('XML_OUTPUT', '1'),
                                     ('SUPPRESS_ALLELE_TABLE', '1'),
                                     ('MAX_ALLELE', '35'),
                                     ('LENGTH',
                                      'MAX_ALLELE*(MAX_ALLELE+1)/2')
                                     ]
                      )

ext_HweEnum = Extension("_HweEnum",
                      [ "hwe-enumeration/src/hwe_enum_wrap.i",
                        "hwe-enumeration/src/hwe_enum.c",
                        "hwe-enumeration/src/factorial.c",
                        "hwe-enumeration/src/main.c",
                        "hwe-enumeration/src/common.c"],
                      include_dirs=["hwe-enumeration/src/include",
                                    "/usr/include/glib-2.0",
                                    "/usr/include/glib-2.0/include",
                                    "/usr/lib/glib-2.0/include",
                                    "/usr/include/libxml2"],
                      libraries=["glib-2.0", "xml2", "m"],
                      define_macros=[('__SORT_TABLE__', '1'),
                                     ('g_fprintf', 'pyfprintf'),
                                     ('VERSION', '"internal"'),
                                     ('PACKAGE_NAME','"hwe-enumeration"')]
                      )

# check to see if version of Python is > 2.1
# if so,  use depends
if sys.version_info[0] == 2 and sys.version_info[1] > 1:
    ext_Emhaplofreq.depends=["emhaplofreq/emhaplofreq.h"]
    ext_Pvalue.depends=['pval/Rconfig.h', 'pval/Rmath.h', 'pval/dpq.h', 'pval/nmath.h']
    ext_Gthwe.depends=['gthwe/func.h', 'gthwe/hwe.h']
    

# default list of extensions to build
extensions = [ext_Emhaplofreq, ext_EWSlatkinExact, ext_Pvalue]

# if and only if we are making a source distribution, then regenerate
# ChangeLog
if sys.argv[1] == 'sdist':
    # first check to see if we are distributing from CVS
    if cvs_version:
        # if yes, generate a "ChangeLog"
        #print "creating ChangeLog from CVS entries"
        #os.system("rcs2log -u \"single:Richard Single:single@allele5.biol.berkeley.edu\" -u \"mpn:Mark Nelson:mpn@alleleb.biol.berkeley.edu\" -u \"alex:Alex Lancaster:alexl@socrates.berkeley.edu\" -u \"diogo:Diogo Meyer:diogo@allele5.biol.berkeley.edu\" -c /dev/null > ChangeLog")
        if os.path.isfile('VERSION') == 0:
            sys.exit("before distributing, please create a VERSION file!")
else:
    # if we are running from our internal CVS version and *not*
    # building a source distribution, then append Gthwe
    if cvs_version:
        extensions.append(ext_Gthwe)
        extensions.append(ext_HweEnum)

# get version from the file VERSION
if os.path.isfile('VERSION'):
  f = open('VERSION')
  version = string.strip(f.readline())
# check if it's a development version (i.e. in CVS tree, use this)
elif os.path.isfile('DEVEL_VERSION'):
  version = 'DEVEL_VERSION'
else:
  sys.exit("Could not find VERSION file!  Exiting...")

def Ensure_Scripts(scripts):
    """Strips '.py' from installed scripts.

    This is a hack and needs work.
    """
    for script in scripts:
        suffix = script[-3:]
        prefix = script[:-3]
        if suffix == '.py':
            #if sys.argv[1] == 'install':
            copy_file(script,prefix,preserve_mode=0)
            scripts[scripts.index(script)] = prefix
    return scripts

# data files to install
data_file_paths = ['config.ini', 'VERSION']
# xslt files are in a subdirectory
xslt_files = ['xslt' + os.sep + i + '.xsl' for i in ['text', 'html', 'lib', 'common', 'filter', 'hardyweinberg', 'homozygosity', 'emhaplofreq', 'meta-to-r', 'sort-by-locus']]
data_file_paths.extend(xslt_files)


setup (name = "PyPop",
       version = version,
       description = "Python for Population Genetics",
       long_description = \
       """PyPop is a framework for population genetics statistics
particularly large-scale multilocus genotype data""",
       url = "http://allele5.biol.berkeley.edu/",
       maintainer = "Alex Lancaster",
       maintainer_email = "alexl@berkeley.edu",
       license = "GNU GPL",
       platforms = ["GNU/Linux", "Windows"],
       
       extra_path = 'PyPop',

       py_modules = ["Arlequin", "HardyWeinberg", "Utils", "Haplo",
                     "Homozygosity", "ParseFile", "Filter", "Main",
                     "DataTypes", "GUIApp", "RandomBinning"],
       scripts= Ensure_Scripts(['pypop.py', 'popmeta.py']),

       data_files=[('share/PyPop', data_file_paths)],

# compile SWIG module

       cmdclass = {'build_ext': my_build_ext,},
       
       ext_modules=extensions

       )

