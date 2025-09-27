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
"""PyPop is a framework for performing population genetics analyses, originally
designed as an end-to-end pipeline that reads configuration files and datasets
and produces standardized outputs. While the primary workflow is file-based,
most internal functionality is exposed as Python modules and classes.

.. note::

   This public API is primarily intended for developers who are
   working on PyPop itself. PyPop is not yet optimized for use in
   end-user programs (i.e. where data structures can be passed in and
   out of the library) via a programmatic interface.  PyPop is mostly
   used as a command-line script. However, it is possible to drive
   PyPop programmatically by importing the :mod:`PyPop.Main` module.

For example, you can instantiate a :class:`PyPop.Main.Main` object with
a configuration instance and optional parameters:

.. code-block:: python

    from PyPop import Main
    from PyPop.Config import ConfigFile

    config = ConfigFile("example.ini")

    application = Main(
        config=config,
        debugFlag=False,
        fileName="datafile.txt",
        datapath="data/",
        xslFilename="transform.xsl",
        xslFilenameDefault="default.xsl",
        outputDir="results/",
        version="1.0",
        testMode=False,
    )

This creates an application instance that will process according to the
given configuration and input files.

"""

import locale
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


def setup_logging(debug=False, filename=None):
    """Provide defaults for logging using the :mod:`logging` module.

    Important:
      Not currently used.
    """
    level = logging.DEBUG if debug else logging.INFO
    if filename is None:
        filename = "-"

    hand = logging.StreamHandler() if filename == "-" else logging.FileHandler(filename)

    fmt = (
        "%(asctime)s %(levelname)s %(funcName)s: %(message)s"
        if level == logging.DEBUG
        else "%(asctime)s %(message)s"
    )
    datefmt = "%Y.%m.%d %H:%M:%S"
    hand.setFormatter(logging.Formatter(fmt, datefmt))

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = []
    root_logger.addHandler(hand)

    logging.debug("PyPop: %s", __version__)
    logging.debug("Python: %s", sys.version.replace("\n", " "))
    logging.debug("Platform: %s", platform.platform())
    logging.debug("Locale: %s", locale.setlocale(locale.LC_ALL))
