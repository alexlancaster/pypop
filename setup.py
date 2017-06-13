#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2003-2007.
# The Regents of the University of California (Regents)
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

import sys, os, string

#from distutils.core import setup, Extension
from setuptools import setup
from setuptools.extension import Extension
#from distutils.file_util import copy_file
#from distutils.sysconfig import PREFIX, get_config_vars, get_config_var
from sysconfig import _PREFIX, get_config_vars, get_config_var
#from distutils.command.build_ext import build_ext

# Override the overzealous use of _FORTIFY_SOURCE CFLAGS flags that
# are in /usr/lib/python2.4/config/Makefile used on Fedora Core 4
# releases with Python 2.4.  Nasty hack to achieve this suggested on
# http://mail.python.org/pipermail/distutils-sig/2002-December/003123.html
cv = get_config_var("OPT")
cv = cv.replace("-D_FORTIFY_SOURCE=2", "-D_FORTIFY_SOURCE=1")

# override implementation of swig_sources method in standard build_ext
# class, so we can change the way SWIG is called by Python's default
# configuration of distutils
# class my_build_ext(build_ext):

#     def swig_sources (self, sources, extension=None):

#         """Walk the list of source files in 'sources', looking for SWIG
#         interface (.i) files.  Run SWIG on all that are found, and
#         return a modified 'sources' list with SWIG source files replaced
#         by the generated C (or C++) files.
#         """

#         new_sources = []
#         swig_sources = []
#         swig_targets = {}

#         # XXX this drops generated C/C++ files into the source tree, which
#         # is fine for developers who want to distribute the generated
#         # source -- but there should be an option to put SWIG output in
#         # the temp dir.

#         if self.swig_cpp:
#             target_ext = '.cpp'
#         else:
#             target_ext = '.c'

#         for source in sources:
#             (base, ext) = os.path.splitext(source)
#             if ext == ".i":             # SWIG interface file
#                 new_sources.append(base + target_ext)
#                 swig_sources.append(source)
#                 swig_targets[source] = new_sources[-1]
#             else:
#                 new_sources.append(source)

#         if not swig_sources:
#             return new_sources

#         swig = self.find_swig()
#         swig_cmd = [swig, "-python", "-ISWIG"]
#         if self.swig_cpp:
#             swig_cmd.append("-c++")

#         for source in swig_sources:
#             target = swig_targets[source]
#             self.announce("swigging %s to %s" % (source, target))
#             self.spawn(swig_cmd + ["-o", target, source])

#         return new_sources

    # swig_sources ()

# distutils doesn't currently have an explicit way of setting CFLAGS,
# it takes CFLAGS from the environment variable of the same name, so
# we set the environment to emulate that.
#os.environ['CFLAGS'] = '-funroll-loops'

# look for libraries in _PREFIX
library_dirs = [os.path.join(_PREFIX, "lib")]
include_dirs = [os.path.join(_PREFIX, "include")]
# also look in LIBRARY_PATH, CPATH (needed for macports etc.)
if "LIBRARY_PATH" in os.environ:
    library_dirs += os.environ["LIBRARY_PATH"].rstrip(os.pathsep).split(os.pathsep)
if "CPATH" in os.environ:
    include_dirs += os.environ["CPATH"].rstrip(os.pathsep).split(os.pathsep)

print include_dirs

# flag to determine whether or not we are using the CVS version
if os.path.isdir("CVS"):
    cvs_version=1
else:
    cvs_version=0

# flag to determine whether we are generating a distribution version
if os.environ.has_key('DISTRIB') and \
   os.environ['DISTRIB'] == 'true':
    distrib_version=1
else:
    distrib_version=0


# define each extension
ext_Emhaplofreq = Extension("_Emhaplofreqmodule",
                            ["emhaplofreq/emhaplofreq_wrap.i",
                             "emhaplofreq/emhaplofreq.c"],
                            swig_opts = ["-ISWIG"],
                            include_dirs=include_dirs + ["emhaplofreq"],
                            define_macros=[('__SWIG__', '1'),
                                           ('DEBUG', '0'),
                                           ('EXTERNAL_MODE', '1'),
                                           ('XML_OUTPUT', '1')]
                            )
ext_EWSlatkinExact = Extension("_EWSlatkinExactmodule",
                               ["slatkin-exact/monte-carlo_wrap.i",
                                "slatkin-exact/monte-carlo.c"],
                               swig_opts = ["-ISWIG"],
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
                        "pval/fmax2.c",
                        "pval/dnorm.c",
                        "pval/dpois.c",
                        "pval/gamma.c",
                        "pval/bd0.c",
                        "pval/stirlerr.c",
                        "pval/lgammacor.c",
                        "pval/pnorm.c"],
                       swig_opts = ["-ISWIG"],
                       include_dirs=include_dirs + ["pval"],
                       define_macros=[('MATHLIB_STANDALONE', '1')]
                       )

ext_Gthwe_files = ["gthwe/gthwe_wrap.i",
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
                   "gthwe/statistics.c"]


ext_Gthwe_macros = [('__SWIG__', '1'),
                    ('DEBUG', '0'),
                    ('XML_OUTPUT', '1'),
                    ('SUPPRESS_ALLELE_TABLE', '1'),
                    ('INDIVID_GENOTYPES', '1')] 


ext_Gthwe = Extension("_Gthwemodule",
                      ext_Gthwe_files,
                      swig_opts = ["-ISWIG"],
                      include_dirs=include_dirs + ["gthwe"],
                      library_dirs=library_dirs,
                      libraries=["gsl", "gslcblas"],
                      define_macros=ext_Gthwe_macros
                      )

ext_HweEnum = Extension("_HweEnum",
                      [ "hwe-enumeration/src/hwe_enum_wrap.i",
                        "hwe-enumeration/src/hwe_enum.c",
                        "hwe-enumeration/src/factorial.c",
                        "hwe-enumeration/src/main.c",
                        "hwe-enumeration/src/common.c",
                        "hwe-enumeration/src/statistics.c",
                        "hwe-enumeration/src/external.c"
                        ],
                        swig_opts = ["-ISWIG"],
                        include_dirs=include_dirs + ["hwe-enumeration/src/include",
                                                     "/usr/include/glib-2.0",
                                                     "/usr/include/glib-2.0/include",
                                                     "/usr/lib/glib-2.0/include",
                                                     "/usr/lib64/glib-2.0/include/",
                                                     "/usr/include/libxml2"],
                        libraries=["glib-2.0", "xml2", "popt",
                                   "m", "gsl", "gslcblas"],
                        define_macros=[('__SORT_TABLE__', '1'),
                                       ('g_fprintf', 'pyfprintf'),
                                       ('VERSION', '"internal"'),
                                       ('PACKAGE_NAME','"hwe-enumeration"'),
                                       ('INDIVID_GENOTYPES', '1'),
                                       ('HAVE_LIBGSL', '1')]
                        )

ext_Emhaplofreq.depends=['SWIG/typemap.i', "emhaplofreq/emhaplofreq.h"]
ext_Pvalue.depends=['SWIG/typemap.i', 'pval/Rconfig.h', 'pval/Rmath.h', 'pval/dpq.h', 'pval/nmath.h']
ext_Gthwe.depends=['SWIG/typemap.i', 'gthwe/func.h', 'gthwe/hwe.h']
    
# default list of extensions to build
extensions = [ext_Emhaplofreq, ext_EWSlatkinExact, ext_Pvalue, ext_Gthwe]

# don't include HWE
# extensions.append(ext_HweEnum)

from pypop import __version__, __pkgname__

# data files to install
data_file_paths = ['config.ini']
# xslt files are in a subdirectory
xslt_files = ['xslt' + os.sep + i + '.xsl' for i in ['text', 'html', 'lib', 'common', 'filter', 'hardyweinberg', 'homozygosity', 'emhaplofreq', 'meta-to-r', 'sort-by-locus', 'haplolist-by-group', 'phylip-allele', 'phylip-haplo']]
data_file_paths.extend(xslt_files)

setup (name = __pkgname__,
       version = __version__,
       description = "Python for Population Genetics",
       long_description = \
       """PyPop is a framework for population genetics statistics
particularly large-scale multilocus genotype data""",
       url = "http://www.pypop.org/",
       maintainer = "Alex Lancaster",
       maintainer_email = "alexl@cal.berkeley.edu",
       license = "GNU GPL",
       platforms = ["GNU/Linux", "Windows", "MacOS"],
       packages = ["pypop"],
       #install_requires = [
       #  'Numeric',
       #  'libxml2-python'
       #  ],
       #py_modules = ["Arlequin", "HardyWeinberg", "Utils", "Haplo",
       #              "Homozygosity", "ParseFile", "Filter", "Main",
       #              "DataTypes", "GUIApp", "RandomBinning", "Meta"],
       scripts= ['pypop.py', 'popmeta.py'],
       data_files=[('share/pypop', data_file_paths)],
       #cmdclass = {'build_ext': my_build_ext,},  # compile SWIG module
       ext_modules=extensions
       )

