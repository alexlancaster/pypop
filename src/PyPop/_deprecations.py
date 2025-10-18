import importlib
import importlib.abc
import sys
import warnings

deprecated_modules = {
    "PyPop.Arlequin": {
        "new": "PyPop.arlequin",
        "reason": "PEP8 compliance: module names should be lowercase.",
        "deprecated": "1.0.0",
        "removal": "1.5.0",
    },
    "PyPop.DataTypes": {
        "new": "PyPop.datatypes",
        "reason": "PEP8 compliance and consistency with plural naming for data structures.",
        "changed": "1.4.0",
    },
    "PyPop.HardyWeinberg": {
        "new": "PyPop.hardyweinberg",
        "reason": "PEP8 compliance; Hardy-Weinberg is treated as one term in population genetics.",
        "changed": "1.4.0",
    },
    "PyPop.Homozygosity": {
        "new": "PyPop.homozygosity",
        "reason": "PEP8 compliance.",
        "changed": "1.4.0",
    },
    "PyPop.Haplo": {
        "new": "PyPop.haplo",
        "reason": "PEP8 compliance and consistency with other short module names.",
        "changed": "1.4.0",
    },
    "PyPop.Filter": {
        "new": "PyPop.filters",
        "reason": "Clarified plural form since module defines multiple filter functions.",
        "changed": "1.4.0",
    },
    "PyPop.ParseFile": {
        "new": "PyPop.parsers",
        "reason": "Renamed for clarity: module parses multiple file types, not just one file.",
        "changed": "1.4.0",
    },
    "PyPop.RandomBinning": {
        "new": "PyPop.randombinning",
        "reason": "PEP8 compliance; compound term lowercased for consistency.",
        "changed": "1.4.0",
    },
    "PyPop.CommandLineInterface": {
        "new": "PyPop.command_line_interface",
        "reason": "PEP8 compliance; underscores separate readable words.",
        "changed": "1.4.0",
    },
    "PyPop.Main": {
        "new": "PyPop.popanalysis",
        "reason": "Renamed for clarity; represents per-population analysis rather than script entry point.",
        "changed": "1.4.0",
    },
    "PyPop.Meta": {
        "new": "PyPop.popaggregate",
        "reason": "Renamed for clarity; aggregates results across populations, not 'metadata'.",
        "changed": "1.4.0",
    },
    "PyPop.Utils": {
        "new": "PyPop.utils",
        "reason": "PEP8 compliance.",
        "changed": "1.4.0",
    },
}


class PyPopModuleRenameDeprecationWarning(DeprecationWarning):
    """Deprecation warning for PyPop module renames."""


class DeprecatedModuleFinder(importlib.abc.MetaPathFinder):
    """Meta path finder to intercept imports of deprecated modules."""

    def __init__(self, mapping):
        """mapping: dict of old module -> dict with keys.

        'new': new module name
        'reason': optional text explaining renaming.
        """
        self.mapping = mapping

    def find_spec(self, fullname, _path, _target=None):
        if fullname in self.mapping:
            info = self.mapping[fullname]
            new_name = info["new"]
            reason = info.get("reason", "")

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
                stacklevel=5,
            )

            # Return the spec for the module so import machinery can continue
            return module.__spec__

        return None
