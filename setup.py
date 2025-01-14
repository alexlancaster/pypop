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

import tomli
from setuptools import setup
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools.command.build_py import build_py as _build_py
from setuptools.extension import Extension

# from src.PyPop import __pkgname__, __version_scheme__
from src.PyPop.citation import citation_output_formats, convert_citation_formats

src_dir = "src"

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
            DIR
            / "PyPop"
            / str(
                ext.name.split("PyPop.").pop()
                + ("*.pyd" if sys.platform == "win32" else "*.so")
            )
            for ext in extensions
        ]
        for ext_file in ext_files:
            # FIXME: use `glob.glob` for the moment, Path.glob not working
            for the_ext_file in glob(str(ext_file)):  # noqa: PTH207
                if Path(the_ext_file).exists():
                    print(f"Removing in-place extension {the_ext_file}")
                    Path(the_ext_file).unlink()
        clean.clean.run(self)


class CustomBuildExt(_build_ext):
    def finalize_options(self):
        super().finalize_options()

        # look for libraries in _PREFIX
        prefix = Path(get_config_var("prefix"))
        self.library_dirs += [str(prefix / "lib")]
        self.include_dirs += [str(prefix / "include")]
        # also look in LIBRARY_PATH, CPATH (needed for macports etc.)
        if "LIBRARY_PATH" in os.environ:
            self.library_dirs += (
                os.environ["LIBRARY_PATH"].rstrip(os.pathsep).split(os.pathsep)
            )
        if "CPATH" in os.environ:
            self.include_dirs += (
                os.environ["CPATH"].rstrip(os.pathsep).split(os.pathsep)
            )


ext_HweEnum = Extension(
    "PyPop._HweEnum",
    [
        "src/hwe-enumeration/src/hwe_enum_wrap.i",
        "src/hwe-enumeration/src/hwe_enum.c",
        "src/hwe-enumeration/src/factorial.c",
        "src/hwe-enumeration/src/main.c",
        "src/hwe-enumeration/src/common.c",
        "src/hwe-enumeration/src/statistics.c",
        "src/hwe-enumeration/src/external.c",
    ],
    swig_opts=["-Isrc/SWIG", "-Isrc"],
    include_dirs=[
        ["src/hwe-enumeration/src/include"],
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
# most extensions moved to extensions.toml
extensions = []
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


def add_more_ext_modules_from_toml(toml_path, extensions):
    with open(toml_path, "rb") as f:
        config = tomli.load(f)

    ext_modules_config = (
        config.get("tool", {}).get("setuptools", {}).get("ext-modules", [])
    )
    # ext_modules = []
    # existing extensions names
    existing_extensions = [ext.name for ext in extensions]
    ext_modules = extensions

    print("***********************************************")
    print("parsing extensions in:", toml_path)
    print("***********************************************")

    print("existing extensions:", existing_extensions)

    for ext in ext_modules_config:
        if ext["name"] not in existing_extensions:
            print("*******************************************")
            print("Building extension:", ext["name"])
            print("*******************************************")

            ext_modules.append(
                Extension(
                    name=ext["name"],
                    sources=ext.get("sources", []),
                    swig_opts=ext.get("swig-opts", []),
                    include_dirs=ext.get("include-dirs", []),
                    libraries=ext.get("libraries", []),
                    library_dirs=ext.get("library-dirs", []),
                    extra_compile_args=ext.get("extra-compile-args", []),
                    extra_link_args=ext.get("extra-link-args", []),
                    depends=ext.get("depends", []),
                )
            )
        else:
            print("*******************************************")
            print("Skipping extension:", ext, "already exists")
            print("*******************************************")

    return ext_modules


citation_data_file_paths = []
# citation files are in a subdirectory of PyPop, but not a separate module
citation_files = [
    str(Path("citation") / f"CITATION.{suffix}") for suffix in citation_output_formats
]
citation_data_file_paths.extend(citation_files)


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


setup(
    # package_dir={"": src_dir},
    # packages=["PyPop", "PyPop.xslt"],
    # package_data={
    #     "PyPop.xslt": xslt_data_file_paths,
    #     "PyPop": citation_data_file_paths,
    # },
    ext_modules=add_more_ext_modules_from_toml("extensions.toml", extensions),
    cmdclass={
        "clean": CleanCommand,
        # enable the custom build
        "build_py": CustomBuildPy,
        # customize the build extension to read environment variables
        "build_ext": CustomBuildExt,
    },
)
