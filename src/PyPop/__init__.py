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

PyPop was originally designed as an end-to-end pipeline that reads
configuration files and datasets and produces standardized
outputs. While the primary workflow is file-based, most internal
functionality is exposed as Python modules and classes.

.. important::

   Updates to PyPop's API to better expose and streamline "library"
   access to PyPop's functionality in end-user programs is still a
   work-in-progress. Although this API is intended to serve end-users
   and developers of PyPop, parts of it are not yet optimized for
   end-users.

Driving PyPop programmatically can be done via the
:mod:`~PyPop.popanalysis` and :mod:`~PyPop.popaggregate` modules. In
the example below, we run an simple analysis on a single input
``.pop`` file and generate output TSV files. There are two main steps:

1. Create the :class:`~configparser.ConfigParser` instance (see
   :ref:`configuration file section <guide-usage-configfile>` in the
   *PyPop User Guide* for the description of the configuration
   options), supply this to the :class:`~PyPop.popanalysis.Main`
   class, along with an input ``.pop`` file, to perform the analysis.

2. Next get the name of output XML file from the generated ``Main``
   instance, and pass it to the :class:`~PyPop.popaggregate.Meta` to
   generate TSV output files.

.. testsetup::

   >>> import PyPop
   >>> PyPop.setup_logger(doctest_mode=True)

>>> from PyPop.popanalysis import Main
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
>>> from PyPop.popaggregate import Meta
>>> _ = Meta (TSV_output=True, xml_files=[outXML])   # doctest: +NORMALIZE_WHITESPACE
./1-locus-hardyweinberg.tsv
./1-locus-summary.tsv
./1-locus-allele.tsv
./1-locus-genotype.tsv

See Also:
   The :ref:`PyPop API examples <guide-usage-examples-api>` in the
   *PyPop User Guide* for a more detailed breakdown of use of the API.

"""
# allow package name itself to be CamelCase, even if modules are not
# ruff: noqa: N999

import logging
import platform
import sys

from ._deprecations import (
    DeprecatedModuleFinder as _DeprecatedModuleFinder,
)
from ._deprecations import (
    PyPopModuleRenameDeprecationWarning as PyPopModuleRenameDeprecationWarning,
)
from ._deprecations import (
    deprecated_modules as _deprecated_modules,
)

# insert finder at the very start of meta_path
sys.meta_path.insert(0, _DeprecatedModuleFinder(_deprecated_modules))

logger = logging.getLogger("pypop")
"""Package-wide logger used throughout a PyPop run.

.. versionadded:: 1.4.0
"""

# FIXME: ensure these need be remain synced with pyproject.toml
try:
    from ._metadata import __pkgname__, __version_scheme__
except ModuleNotFoundError:
    from PyPop import critical_exit

    critical_exit(
        "PyPop metadata not found, PyPop has likely not been built, please build or install via `pip install` or `setup.py build`"
    )

try:
    import importlib.metadata as metadata_lib  # look for built-in
except (ModuleNotFoundError, ImportError):
    import importlib_metadata as metadata_lib  # otherwise need the backport

try:
    __version__ = metadata_lib.version(__pkgname__)  # use the installed version first
    """PyPop version. If installed, this is the package version, otherwise it returns repository version."""
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


class _LevelBasedFormatter(logging.Formatter):
    """Formatter that uses different formats for INFO vs DEBUG+."""

    def __init__(
        self,
        info_fmt="LOG: %(message)s",
        debug_fmt="%(asctime)s [%(levelname)s] %(name)s:%(module)s.%(funcName)s: %(message)s",
        datefmt="%Y.%m.%d %H:%M:%S",
    ):
        super().__init__()
        self.info_fmt = info_fmt
        self.debug_fmt = debug_fmt
        self.datefmt = datefmt

        # Pre-create two internal formatters for speed
        self._info_formatter = logging.Formatter(info_fmt)
        self._debug_formatter = logging.Formatter(debug_fmt, datefmt)

    def format(self, record):
        if record.levelno == logging.INFO:
            return self._info_formatter.format(record)
        return self._debug_formatter.format(record)


def setup_logger(level=logging.INFO, filename=None, doctest_mode=True):
    """Configure the 'pypop' logger with stdout/file handler, optional debug verbosity, and doctest mode.

    .. versionadded:: 1.4.0

    Args:
      level (str, optional): ``INFO`` (default), ``DEBUG`` (more
       detailed), ``WARNING``, ``CRITICAL``
      filename (str, optional): Optional file to log to. If ``None``,
       logs to ``stdout``.
      doctest_mode (bool, optional): If True, forcibly rebinds the
       logger to sys.stdout and disables propagation so doctests see
       output.

    """
    if doctest_mode:
        # Remove any existing StreamHandlers to avoid duplicates
        for h in list(logger.handlers):
            if isinstance(h, logging.StreamHandler):
                logger.removeHandler(h)

    # Determine handler: file or stdout
    if filename is None or filename == "-":
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.FileHandler(filename)

    handler.setFormatter(_LevelBasedFormatter())
    # Remove old handlers to avoid duplicates
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(level)

    # Only propagate to root when not in doctest mode
    logger.propagate = not doctest_mode


# Run once at import to ensure default logging for normal usage
setup_logger()
