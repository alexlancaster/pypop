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

import os
import sys
from distutils.command import clean
from glob import glob
from pathlib import Path
from sysconfig import get_config_var

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.extension import Extension

from src.PyPop import __pkgname__, __version_scheme__
from src.PyPop.citation import citation_output_formats, convert_citation_formats

src_dir = "src"
pkg_dir = "PyPop"

# distutils doesn't currently have an explicit way of setting CFLAGS,
# it takes CFLAGS from the environment variable of the same name, so
# we set the environment to emulate that.
# os.environ['CFLAGS'] = '-funroll-loops'


class CleanCommand(clean.clean):
    """Customized clean command - removes in_place extension files if they exist"""

    def run(self):
        DIR = Path(__file__).resolve().parent / src_dir
        # generate glob pattern from extension name and suffix
        ext_files = [
            DIR / pkg_dir / ext.name.split(pkg_dir + ".").pop()
            + ("*.pyd" if sys.platform == "win32" else "*.so")
            for ext in extensions
        ]
        for ext_file in ext_files:
            # FIXME: use `glob.glob` for the moment, Path.glob not working
            for the_ext_file in glob(ext_file):  # noqa: PTH207
                if Path(the_ext_file).exists():
                    print(f"Removing in-place extension {the_ext_file}")
                    Path(ext_file).unlink()
        clean.clean.run(self)


# look for libraries in _PREFIX
prefix = Path(get_config_var("prefix"))
library_dirs = [str(prefix / "lib")]
include_dirs = [str(prefix / "include")]
# also look in LIBRARY_PATH, CPATH (needed for macports etc.)
if "LIBRARY_PATH" in os.environ:
    library_dirs += os.environ["LIBRARY_PATH"].rstrip(os.pathsep).split(os.pathsep)
if "CPATH" in os.environ:
    include_dirs += os.environ["CPATH"].rstrip(os.pathsep).split(os.pathsep)


# generate the appropriate relative path to source directory, given
# paths within that source directory (this means we need to define
# this directory in just one place
def path_to_src(source_path_list):
    new_source_list = []
    for file_path in source_path_list:
        new_source_list.append(str(Path(src_dir) / file_path))
    return new_source_list


swig_opts = ["-I{}".format(Path(src_dir) / "SWIG"), f"-I{Path(src_dir)}"]

# define each extension
ext_Emhaplofreq = Extension(
    "PyPop._Emhaplofreq",
    path_to_src(["emhaplofreq/emhaplofreq_wrap.i", "emhaplofreq/emhaplofreq.c"]),
    swig_opts=swig_opts,
    include_dirs=include_dirs + path_to_src(["emhaplofreq"]),
    define_macros=[
        ("__SWIG__", "1"),
        ("DEBUG", "0"),
        ("EXTERNAL_MODE", "1"),
        ("XML_OUTPUT", "1"),
    ],
)
ext_EWSlatkinExact = Extension(
    "PyPop._EWSlatkinExact",
    path_to_src(["slatkin-exact/monte-carlo_wrap.i", "slatkin-exact/monte-carlo.c"]),
    swig_opts=swig_opts,
    include_dirs=include_dirs,
)

ext_Gthwe_files = path_to_src(
    [
        "gthwe/gthwe_wrap.i",
        "gthwe/hwe.c",
        "gthwe/cal_const.c",
        "gthwe/cal_n.c",
        "gthwe/cal_prob.c",
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
        "gthwe/statistics.c",
    ]
)


ext_Gthwe_macros = [
    ("__SWIG__", "1"),
    ("DEBUG", "0"),
    ("XML_OUTPUT", "1"),
    ("SUPPRESS_ALLELE_TABLE", "1"),
    ("INDIVID_GENOTYPES", "1"),
]

ext_Gthwe = Extension(
    "PyPop._Gthwe",
    ext_Gthwe_files,
    swig_opts=swig_opts,
    include_dirs=include_dirs + path_to_src(["gthwe"]),
    library_dirs=library_dirs,
    libraries=["gsl", "gslcblas"],
    define_macros=ext_Gthwe_macros,
)

ext_Haplostats = Extension(
    "PyPop._Haplostats",
    path_to_src(["haplo-stats/haplostats_wrap.i", "haplo-stats/haplo_em_pin.c"]),
    swig_opts=swig_opts,
    include_dirs=include_dirs + path_to_src(["haplo-stats"]),
    define_macros=[
        ("MATHLIB_STANDALONE", "1"),
        ("__SWIG__", "1"),
        ("DEBUG", "0"),
        ("R_NO_REMAP", "1"),
    ],
)

ext_HweEnum = Extension(
    "PyPop._HweEnum",
    path_to_src(
        [
            "hwe-enumeration/src/hwe_enum_wrap.i",
            "hwe-enumeration/src/hwe_enum.c",
            "hwe-enumeration/src/factorial.c",
            "hwe-enumeration/src/main.c",
            "hwe-enumeration/src/common.c",
            "hwe-enumeration/src/statistics.c",
            "hwe-enumeration/src/external.c",
        ]
    ),
    swig_opts=swig_opts,
    include_dirs=[
        *include_dirs,
        path_to_src(["hwe-enumeration/src/include"]),
        "/usr/include/glib-2.0",
        "/usr/include/glib-2.0/include",
        "/usr/lib/glib-2.0/include",
        "/usr/lib64/glib-2.0/include/",
        "/usr/include/libxml2",
        "/usr/include/gsl",
    ],
    libraries=["glib-2.0", "xml2", "popt", "m", "gsl", "gslcblas"],
    define_macros=[
        ("__SORT_TABLE__", "1"),
        ("g_fprintf", "pyfprintf"),
        ("VERSION", '"internal"'),
        ("PACKAGE_NAME", '"hwe-enumeration"'),
        ("INDIVID_GENOTYPES", "1"),
        ("HAVE_LIBGSL", "1"),
    ],
)

ext_Emhaplofreq.depends = path_to_src(
    ["SWIG/typemap.i", "emhaplofreq/emhaplofreq.h", "emhaplofreq/drand48.c"]
)
ext_Pvalue.depends = path_to_src(
    ["SWIG/typemap.i", "pval/Rconfig.h", "pval/Rmath.h", "pval/dpq.h", "pval/nmath.h"]
)
ext_Gthwe.depends = path_to_src(["SWIG/typemap.i", "gthwe/func.h", "gthwe/hwe.h"])
ext_Haplostats.depends = path_to_src(["SWIG/typemap.i", "haplo-stats/haplo_em_pin.h"])

# default list of extensions to build
extensions = [
    ext_Emhaplofreq,
    ext_EWSlatkinExact,
    ext_Haplostats,
    ext_Gthwe,
]

# don't include HWEEnum
# extensions.append(ext_HweEnum)

xslt_data_file_paths = []
# xslt files are in a subdirectory
xslt_files = [
    f + ".xsl"
    for f in [
        "text",
        "html",
        "lib",
        "common",
        "filter",
        "hardyweinberg",
        "homozygosity",
        "emhaplofreq",
        "meta-to-tsv",
        "sort-by-locus",
        "haplolist-by-group",
        "phylip-allele",
        "phylip-haplo",
    ]
]
xslt_data_file_paths.extend(xslt_files)

citation_data_file_paths = []
# citation files are in a subdirectory of PyPop, but not a separate module
citation_files = [
    str(Path("citation") / f"CITATION.{suffix}") for suffix in citation_output_formats
]
citation_data_file_paths.extend(citation_files)


# currently disabled (these are built in a github action)
class CustomBuildPy(_build_py):
    def run(self):
        # do standard build process
        super().run()

        # if not running from a CIBUILDWHEEL environment variable
        # we need to create the citations
        if os.environ.get("CIBUILDWHEEL") != "1":
            # source citation path (single-source of truth)
            citation_path = "CITATION.cff"

            # then copy CITATION.cff to temp build directory
            # use setuptools' temp build directory
            build_lib = self.get_finalized_command("build").build_lib

            convert_citation_formats(build_lib, citation_path)


# read the contents of your README file

this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name=__pkgname__,
    use_scm_version={
        "write_to": Path(src_dir) / pkg_dir / "_version.py",
        "version_scheme": __version_scheme__,
    },
    description="PyPop: Python for Population Genomics",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="http://www.pypop.org/",
    project_urls={
        "Documentation": "http://pypop.org/docs/",
        "Changelog": "https://github.com/alexlancaster/pypop/blob/main/NEWS.md",
        "Source": "https://github.com/alexlancaster/pypop/",
        "Tracker": "https://github.com/alexlancaster/pypop/issues",
    },
    author="Alex Lancaster",
    maintainer="PyPop team",
    license="GNU GPL",
    platforms=["GNU/Linux", "Windows", "MacOS"],
    keywords=[
        "bioinformatics",
        "population-genomics",
        "evolutionary-biology",
        "population-genetics",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    package_dir={"": src_dir},
    packages=["PyPop", "PyPop.xslt"],
    package_data={
        "PyPop.xslt": xslt_data_file_paths,
        "PyPop": citation_data_file_paths,
    },
    install_requires=[
        "numpy <= 2.2.1",
        "SciPy <= 1.14.1",                           
        "lxml <= 5.3.0",
        "importlib-resources; python_version <= '3.8'",
        "importlib-metadata; python_version <= '3.8'",
    ],
    extras_require={
        "test": ["pytest"]
        # FIXME:  "psutil <= 5.9.5", not currently used, 5.9.6 and later had problems with building on Windows PyPy
    },
    entry_points={
        "console_scripts": [
            "pypop=PyPop.pypop:main",
            "popmeta=PyPop.popmeta:main",
            "pypop-interactive=PyPop.pypop:main_interactive",
        ]
    },
    ext_modules=extensions,
    cmdclass={
        "clean": CleanCommand,
        # enable the custom build
        "build_py": CustomBuildPy,
    },
)
