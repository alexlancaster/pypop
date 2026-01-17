# This file is part of PyPop

# Copyright (C) 2025.
# PyPop contributors

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
"""API changes
-----------

In PyPop 1.4.0, modules have been renamed to follow the lower-case
convention of `PEP8
<https://peps.python.org/pep-0008/#package-and-module-names>`_.  In
addition to lowercasing, some have further renaming to clarify their
purpose and follow standard conventions. Backwards-compatibile
bindings have been created that allow end-user Python scripts using
the PyPop API to continue to work with the old module names.  However
such use will raise a
:exc:`~PyPop.PyPopModuleRenameDeprecationWarning` (a custom
:exc:`DeprecationWarning`). In the following minor release, 1.5.0, the
warnings will become more visible :exc:`UserWarning`. These bindings
will be completely removed in the next major release.

Note:
  Command-line users of ``pypop`` will not be affected by these
  changes, which are completely internal, scripts will continue to
  work with no changes needed in any configuration files.

Below are the list of all API changes, including removals and any
other ongoing API deprecations, and notifications of upcoming
removals.

"""  # noqa: D205 D415

import importlib
import importlib.abc
import sys
import warnings

deprecated_modules = {
    "PyPop.Arlequin": {
        "new": "PyPop.arlequin",
        "reason": "Lowercased for PEP8 compliance.",
        "deprecated": "1.0.0",
        "removal": "1.5.0",
    },
    "PyPop.DataTypes": {
        "new": "PyPop.datatypes",
        "reason": "Lowercased for PEP8 compliance and consistency with plural naming for data structures.",
        "changed": "1.4.0",
    },
    "PyPop.HardyWeinberg": {
        "new": "PyPop.hardyweinberg",
        "reason": "Lowercased for PEP8 compliance.",
        "changed": "1.4.0",
    },
    "PyPop.Homozygosity": {
        "new": "PyPop.homozygosity",
        "reason": "Lowercased for PEP8 compliance.",
        "changed": "1.4.0",
    },
    "PyPop.Haplo": {
        "new": "PyPop.haplo",
        "reason": "Lowercased for PEP8 compliance.",
        "changed": "1.4.0",
    },
    "PyPop.Filter": {
        "new": "PyPop.filters",
        "reason": "Lowercased and clarified plural form since module defines multiple filter functions.",
        "changed": "1.4.0",
    },
    "PyPop.ParseFile": {
        "new": "PyPop.parsers",
        "reason": "Lowercased for and renamed for clarity: module parses multiple file types, not just one file.",
        "changed": "1.4.0",
    },
    "PyPop.RandomBinning": {
        "new": "PyPop.randombinning",
        "reason": "Lowercased for PEP8 compliance.",
        "changed": "1.4.0",
    },
    "PyPop.CommandLineInterface": {
        "new": "PyPop.command_line_interface",
        "reason": "Lowercased for PEP8 compliance; underscores separate readable words.",
        "changed": "1.4.0",
    },
    "PyPop.Main": {
        "new": "PyPop.popanalysis",
        "reason": "Lowercased and renamed for clarity; represents per-population analysis rather than script entry point.",
        "changed": "1.4.0",
    },
    "PyPop.Meta": {
        "new": "PyPop.popaggregate",
        "reason": "Lowercased and renamed for clarity; aggregates results across populations, not 'metadata'.",
        "changed": "1.4.0",
    },
    "PyPop.Utils": {
        "new": "PyPop.utils",
        "reason": "Lowercased for PEP8 compliance.",
        "changed": "1.4.0",
    },
    "PyPop.Utils.OrderedDict": {
        "removed": "1.4.0",
        "reason": "Obsolete, replaced with :class:`collections.OrderedDict`",
    },
    "PyPop.Utils.Index": {
        "removed": "1.4.0",
        "reason": "Obsolete, replaced with :class:`collections.OrderedDict` with it's own ``Index`` class",
    },
    "PyPop.GUIApp": {
        "removed": "1.4.0",
        "reason": "Obsolete, never fully implemented a full ``wxPython`` UI. Replaced by built-in Tkinter file-picker",
    },
}


class PyPopModuleRenameDeprecationWarning(DeprecationWarning):
    """Deprecation warning for PyPop module renames.

    .. versionadded:: 1.4.0
    """


class DeprecatedModuleFinder(importlib.abc.MetaPathFinder):
    """Meta path finder to intercept imports of deprecated modules.

    .. versionadded:: 1.4.0
    """

    def __init__(self, mapping):
        """mapping: dict of old module -> dict with keys.

        'new': new module name
        'reason': optional text explaining renaming.
        """
        self.mapping = mapping

    def find_spec(self, fullname, _path, _target=None):
        if fullname not in self.mapping:
            return None

        info = self.mapping[fullname]
        reason = info.get("reason", "")

        # ---- Case 1: renamed module ----
        if "new" in info:
            new_name = info["new"]

            # Import the replacement module
            module = importlib.import_module(new_name)

            # Inject the old name into sys.modules
            sys.modules[fullname] = module

            # Construct the warning message
            msg = f"Module '{fullname}' is deprecated; use '{new_name}' instead."
            if reason:
                msg += f" Reason: {reason}"

            warnings.warn(
                msg,
                PyPopModuleRenameDeprecationWarning,
                stacklevel=4,
            )

            # Return the spec for the module so import machinery can continue
            return module.__spec__

        # ---- Case 2: removed module ----
        if "removed" in info:
            removed_in = info["removed"]

            msg = f"Module '{fullname}' was removed in PyPop {removed_in}."
            if reason:
                msg += f" {reason}"

            raise ModuleNotFoundError(msg)

        return None
