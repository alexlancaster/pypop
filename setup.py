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

import sys, os
from glob import glob
from setuptools import setup
from setuptools.extension import Extension
from sysconfig import _PREFIX, get_config_vars, get_config_var

from PyPop import __version__, __pkgname__

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

swig_opts = ["-ISWIG"]

# define each extension
ext_Emhaplofreq = Extension("PyPop._Emhaplofreq",
                            ["emhaplofreq/emhaplofreq_wrap.i",
                             "emhaplofreq/emhaplofreq.c"],
                            swig_opts = swig_opts,
                            include_dirs=include_dirs + ["emhaplofreq"],
                            define_macros=[('__SWIG__', '1'),
                                           ('DEBUG', '0'),
                                           ('EXTERNAL_MODE', '1'),
                                           ('XML_OUTPUT', '1')]
                            )
ext_EWSlatkinExact = Extension("PyPop._EWSlatkinExact",
                               ["slatkin-exact/monte-carlo_wrap.i",
                                "slatkin-exact/monte-carlo.c"],
                               swig_opts = swig_opts,
                               include_dirs=include_dirs,
                               )

ext_Pvalue = Extension("PyPop._Pvalue",
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
                       swig_opts = swig_opts,
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


# add local directory for win32 builds
if sys.platform == "win32":
    include_gsl_dir = [r"gsl-msvc-x86.2.4.0.8788\build\native\gsl"]
else:
    include_gsl_dir = []

ext_Gthwe = Extension("PyPop._Gthwe",
                      ext_Gthwe_files,
                      swig_opts = swig_opts,
                      include_dirs=include_dirs + ["gthwe"] + include_gsl_dir,
                      library_dirs=library_dirs,
                      libraries=["gsl", "gslcblas"],
                      define_macros=ext_Gthwe_macros
                      )

ext_Haplostats = Extension("PyPop._Haplostats",
                       ["haplo-stats/haplostats_wrap.i",
                        "haplo-stats/haplo_em_pin.c",],
                       swig_opts = swig_opts,
                       include_dirs=include_dirs + ["haplo-stats", "pval"],
                       define_macros=[('MATHLIB_STANDALONE', '1'),
                                      ('__SWIG__', '1'),
                                      ('DEBUG', '0'),
                                      ('R_NO_REMAP', '1')]
                       )

ext_HweEnum = Extension("PyPop._HweEnum",
                      [ "hwe-enumeration/src/hwe_enum_wrap.i",
                        "hwe-enumeration/src/hwe_enum.c",
                        "hwe-enumeration/src/factorial.c",
                        "hwe-enumeration/src/main.c",
                        "hwe-enumeration/src/common.c",
                        "hwe-enumeration/src/statistics.c",
                        "hwe-enumeration/src/external.c"
                        ],
                        swig_opts = swig_opts,
                        include_dirs=include_dirs + ["hwe-enumeration/src/include",
                                                     "/usr/include/glib-2.0",
                                                     "/usr/include/glib-2.0/include",
                                                     "/usr/lib/glib-2.0/include",
                                                     "/usr/lib64/glib-2.0/include/",
                                                     "/usr/include/libxml2",
                                                     "/usr/include/gsl",
                                                     ],
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
extensions = [ext_Emhaplofreq, ext_EWSlatkinExact, ext_Pvalue, ext_Haplostats, ext_Gthwe]

# don't include HWEEnum 
# extensions.append(ext_HweEnum)


from distutils.command import clean

class CleanCommand(clean.clean):
    """Customized clean command - removes in_place extension files if they exist"""
    def run(self):
        DIR = os.path.dirname(__file__)
        # generate glob pattern from extension name and suffix
        ext_files = [os.path.join(DIR, __pkgname__, ext.name.split(__pkgname__ + '.').pop() + ("*.pyd" if sys.platform == "win32" else "*.so")) for ext in extensions]
        for ext_file in ext_files:
            for ext_file in glob(ext_file):
                if os.path.exists(ext_file):
                    print("Removing in-place extension {}".format(ext_file))
                    os.unlink(ext_file)
        clean.clean.run(self)

data_file_paths = []
# xslt files are in a subdirectory
xslt_files = [f + '.xsl' for f in ['text', 'html', 'lib', 'common', 'filter', 'hardyweinberg', 'homozygosity', 'emhaplofreq', 'meta-to-r', 'sort-by-locus', 'haplolist-by-group', 'phylip-allele', 'phylip-haplo']]
data_file_paths.extend(xslt_files)

setup (name = 'pypop',
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
       packages = ["PyPop", "PyPop.xslt"],
       package_data={"PyPop.xslt": data_file_paths},
       install_requires = ["numpy", "lxml", "psutil", "importlib-resources; python_version <= '3.8'"],
       extras_require={
           "test": ['pytest']
           },
       scripts= ['bin/pypop.py', 'bin/popmeta.py'],
       ext_modules=extensions,
       cmdclass={'clean': CleanCommand,},
       )
