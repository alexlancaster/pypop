# This file is part of PyPop

# Copyright (C) 2017.
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
r"""**PyPop is a framework for performing population genetics analyses**.

It was originally designed as an end-to-end pipeline that reads
configuration files and datasets and produces standardized
outputs. While the primary workflow is file-based, most internal
functionality is exposed as Python modules and classes.

.. important::

   PyPop is not yet fully optimized for use as a library in end-user
   programs via a programmatic interface. Much of this public API is
   aimed at developers who are working on PyPop itself.

It is possible, however, to drive PyPop programmatically via the
:mod:`PyPop.Main` module. In the example below, we instantiate a
:class:`PyPop.Main.Main` object with a configuration instance with the
default settings, one analysis enabled, and an input ``.pop`` file. We
first create the :class:`configparser.ConfigParser` instance (see
:ref:`configuration file section <guide-usage-configfile>` in the
*PyPop User Guide* for the description of the configuration options),
supply this to the :class:`Main` class to perform the analysis, then
get the name of output XML file, and pass it to the :class:`Meta` for
the final TSV output (see also the :ref:`PyPop API examples
<guide-usage-examples-api>` in the *PyPop User Guide* for a
step-by-step breakdown of use of the API).

.. testsetup::

   >>> import PyPop
   >>> PyPop.setup_logger(doctest_mode=True)

>>> from PyPop.Main import Main
>>> from configparser import ConfigParser
>>>
>>> config = ConfigParser()
>>> config.read_dict({
...     "ParseGenotypeFile": {"validSampleFields": "*a_1\n*a_2"},
...     "HardyWeinberg": {"lumpBelow": "5"}})
>>>
>>> pop_contents = '''a_1\ta_2
... 01:01\t02:01
... 02:10\t03:01:02'''
>>> with open("my.pop", "w") as f:
...     _ = f.write(pop_contents)
...
>>> application = Main(
...     config=config,
...     fileName="my.pop",
...     version="fake",
... )
LOG: no XSL file, skipping text output
LOG: Data file has no header data block
>>> outXML = application.getXmlOutPath()
>>> from PyPop.Meta import Meta
>>> _ = Meta (TSV_output=True, xml_files=[outXML])   # doctest: +NORMALIZE_WHITESPACE
./1-locus-hardyweinberg.tsv
./1-locus-summary.tsv
./1-locus-allele.tsv
./1-locus-genotype.tsv

"""

import logging
import platform
import sys

# FIXME: ensure these need be remain synced with pyproject.toml
try:
    from ._metadata import __pkgname__, __version_scheme__
except ModuleNotFoundError:
    sys.exit(
        "PyPop metadata not found, PyPop has likely not been built, please build or install via `pip install` or `setup.py build`"
    )

try:
    import importlib.metadata as metadata_lib  # look for built-in
except (ModuleNotFoundError, ImportError):
    import importlib_metadata as metadata_lib  # otherwise need the backport

try:
    __version__ = metadata_lib.version(__pkgname__)  # use the installed version first
except metadata_lib.PackageNotFoundError:
    from setuptools_scm import get_version

    __version__ = get_version(
        version_scheme=__version_scheme__, root="../..", relative_to=__file__
    )  # next try the version in repo

copyright_message = """Copyright (C) 2003-2006 Regents of the University of California.
Copyright (C) 2007-2025 PyPop team.
This is free software.  There is NO warranty; not even for
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."""
"""
copyright information used in ``--help`` screens and elsewhere
"""


platform_info = f"[Python {platform.python_version()} | {platform.platform()} | {platform.machine()}]"
"""
platform information used in ``--help`` screens and elsewhere
"""

# Package-wide logger you should use in all modules
logger = logging.getLogger("pypop")


def setup_logger(doctest_mode=False, debug_level=0, filename=None):
    """Configure the 'pypop' logger with stdout/file handler, optional debug verbosity, and doctest mode.

    Parameters
    ----------
    doctest_mode : bool
        If True, forcibly rebinds the logger to sys.stdout and disables propagation
        so doctests see output.
    debug_level : int
        0 = INFO (default), 1 = DEBUG, 2+ = very verbose DEBUG
    filename : str | None
        Optional file to log to. If None, logs to stdout.
    """
    if doctest_mode:
        # Remove any existing StreamHandlers to avoid duplicates
        for h in list(logger.handlers):
            if isinstance(h, logging.StreamHandler):
                logger.removeHandler(h)

    # Determine log level
    if debug_level <= 0:
        level = logging.INFO
    elif debug_level == 1:
        level = logging.DEBUG  # could extend to TRACE later if desired
    else:
        level = logging.WARN  # could extend to TRACE later if desired

    # Determine handler: file or stdout
    if filename is None or filename == "-":
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.FileHandler(filename)

    # Choose format based on verbosity
    if level <= logging.INFO:
        fmt = "LOG: %(message)s"
        datefmt = None
    else:
        fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        datefmt = "%Y.%m.%d %H:%M:%S"

    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt, datefmt))

    # Remove old handlers to avoid duplicates
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(level)

    # Only propagate to root when not in doctest mode
    logger.propagate = not doctest_mode


# Run once at import to ensure default logging for normal usage
setup_logger()
