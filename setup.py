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

from setuptools import setup
from setuptools.extension import Extension
from sysconfig import _PREFIX, get_config_vars, get_config_var

# Override the overzealous use of _FORTIFY_SOURCE CFLAGS flags that
# are in /usr/lib/python2.4/config/Makefile used on Fedora Core 4
# releases with Python 2.4.  Nasty hack to achieve this suggested on
# http://mail.python.org/pipermail/distutils-sig/2002-December/003123.html
cv = get_config_var("OPT")
cv = cv.replace("-D_FORTIFY_SOURCE=2", "-D_FORTIFY_SOURCE=1")

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

ext_Haplostats = Extension("_Haplostatsmodule",
                       ["haplo-stats/haplostats_wrap.i",
                        "haplo-stats/haplo_em_pin.c",],
                       swig_opts = ["-ISWIG"],
                       include_dirs=include_dirs + ["haplo-stats", "pval"],
                       define_macros=[('MATHLIB_STANDALONE', '1'),
                                      ('__SWIG__', '1'),
                                      ('DEBUG', '0'),
                                      ('R_NO_REMAP', '1')]
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
ext_Haplostats.depends=['SWIG/typemap.i', "haplo-stats/haplo_em_pin.h"]
    
# default list of extensions to build
extensions = [ext_Emhaplofreq, ext_EWSlatkinExact, ext_Pvalue, ext_Gthwe]

# don't include HWEEnum or haplostats yet
# extensions.append(ext_HweEnum)
extensions.append(ext_Haplostats)

from PyPop import __version__, __pkgname__

from distutils.command import clean

class CleanCommand(clean.clean):
    """Customized clean command - removes in_place extension files if they exist"""
    def run(self):
        DIR = os.path.dirname(__file__)
        ext_files = [os.path.join(DIR, ext.name + (".pyd" if sys.platform == "win32" else ".so")) for ext in extensions]
        for ext_file in ext_files:
            if os.path.exists(ext_file):
                print("Removing in-place extension {}".format(ext_file))
                os.unlink(ext_file)
        clean.clean.run(self)

data_file_paths = []
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
       packages = ["PyPop"],
       #install_requires = [
       #  'numpy'
       #  ],
       scripts= ['bin/pypop.py', 'bin/popmeta.py'],
       data_files=[('share/pypop', data_file_paths)],
       ext_modules=extensions,
       cmdclass={'clean': CleanCommand,},
       setup_requires=['pytest-runner'],
       tests_require=['pytest', 'psutil'],
       )
