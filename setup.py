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

from src.PyPop import __version__, __pkgname__

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

swig_opts = ["-Isrc/SWIG", "-Isrc"]

# define each extension
ext_Emhaplofreq = Extension("PyPop._Emhaplofreq",
                            ["src/emhaplofreq/emhaplofreq_wrap.i",
                             "src/emhaplofreq/emhaplofreq.c"],
                            swig_opts = swig_opts,
                            include_dirs=include_dirs + ["src/emhaplofreq"],
                            define_macros=[('__SWIG__', '1'),
                                           ('DEBUG', '0'),
                                           ('EXTERNAL_MODE', '1'),
                                           ('XML_OUTPUT', '1')]
                            )
ext_EWSlatkinExact = Extension("PyPop._EWSlatkinExact",
                               ["src/slatkin-exact/monte-carlo_wrap.i",
                                "src/slatkin-exact/monte-carlo.c"],
                               swig_opts = swig_opts,
                               include_dirs=include_dirs,
                               )

ext_Pvalue = Extension("PyPop._Pvalue",
                       ["src/pval/pval_wrap.i",
                        "src/pval/pval.c",
                        "src/pval/pchisq.c",
                        "src/pval/chebyshev.c",
                        "src/pval/ftrunc.c",
                        "src/pval/lgamma.c",
                        "src/pval/mlutils.c",
                        "src/pval/pgamma.c",
                        "src/pval/fmin2.c",
                        "src/pval/fmax2.c",
                        "src/pval/dnorm.c",
                        "src/pval/dpois.c",
                        "src/pval/gamma.c",
                        "src/pval/bd0.c",
                        "src/pval/stirlerr.c",
                        "src/pval/lgammacor.c",
                        "src/pval/pnorm.c"],
                       swig_opts = swig_opts,
                       include_dirs=include_dirs + ["src/pval"],
                       define_macros=[('MATHLIB_STANDALONE', '1')]
                       )

ext_Gthwe_files = ["src/gthwe/gthwe_wrap.i",
                   "src/gthwe/hwe.c",
                   "src/gthwe/cal_const.c",
                   "src/gthwe/cal_n.c", "src/gthwe/cal_prob.c",
                   "src/gthwe/check_file.c",
                   "src/gthwe/do_switch.c", 
                   "src/gthwe/new_rand.c",
                   "src/gthwe/ln_p_value.c",
                   "src/gthwe/to_calculate_log.c",
                   "src/gthwe/print_data.c",
                   "src/gthwe/random_choose.c",
                   "src/gthwe/read_data.c",
                   "src/gthwe/select_index.c",
                   "src/gthwe/stamp_time.c",
                   "src/gthwe/test_switch.c",
                   "src/gthwe/statistics.c"]


ext_Gthwe_macros = [('__SWIG__', '1'),
                    ('DEBUG', '0'),
                    ('XML_OUTPUT', '1'),
                    ('SUPPRESS_ALLELE_TABLE', '1'),
                    ('INDIVID_GENOTYPES', '1')] 

if sys.platform == "win32":
    cblas_libname = "gslcblas"
else:
    cblas_libname = "gslcblas"
    
ext_Gthwe = Extension("PyPop._Gthwe",
                      ext_Gthwe_files,
                      swig_opts = swig_opts,
                      include_dirs=include_dirs + ["src/gthwe"],
                      library_dirs=library_dirs,
                      libraries=["gsl", cblas_libname],
                      define_macros=ext_Gthwe_macros
                      )

ext_Haplostats = Extension("PyPop._Haplostats",
                       ["src/haplo-stats/haplostats_wrap.i",
                        "src/haplo-stats/haplo_em_pin.c",],
                       swig_opts = swig_opts,
                       include_dirs=include_dirs + ["src/haplo-stats", "src/pval"],
                       define_macros=[('MATHLIB_STANDALONE', '1'),
                                      ('__SWIG__', '1'),
                                      ('DEBUG', '0'),
                                      ('R_NO_REMAP', '1')]
                       )

ext_HweEnum = Extension("PyPop._HweEnum",
                      [ "src/hwe-enumeration/src/hwe_enum_wrap.i",
                        "src/hwe-enumeration/src/hwe_enum.c",
                        "src/hwe-enumeration/src/factorial.c",
                        "src/hwe-enumeration/src/main.c",
                        "src/hwe-enumeration/src/common.c",
                        "src/hwe-enumeration/src/statistics.c",
                        "src/hwe-enumeration/src/external.c"
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

ext_Emhaplofreq.depends=['src/SWIG/typemap.i', "src/emhaplofreq/emhaplofreq.h"]
ext_Pvalue.depends=['src/SWIG/typemap.i', 'src/pval/Rconfig.h', 'src/pval/Rmath.h', 'src/pval/dpq.h', 'src/pval/nmath.h']
ext_Gthwe.depends=['src/SWIG/typemap.i', 'src/gthwe/func.h', 'src/gthwe/hwe.h']
ext_Haplostats.depends=['src/SWIG/typemap.i', "src/haplo-stats/haplo_em_pin.h"]
    
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
       package_dir = {"": "src"},
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
