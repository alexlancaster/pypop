import importlib
import importlib.abc
import sys
import warnings

deprecated_modules = {
    "PyPop.Arlequin": "PyPop.arlequin",
    "PyPop.DataTypes": "PyPop.datatypes",
    "PyPop.HardyWeinberg": "PyPop.hardyweinberg",
    "PyPop.Homozygosity": "PyPop.homozygosity",
    "PyPop.Haplo": "PyPop.haplo",
    "PyPop.Filter": "PyPop.filters",
    "PyPop.ParseFile": "PyPop.parsefiles",
    "PyPop.RandomBinning": "PyPop.randombinning",
    "PyPop.CommandLineInterface": "PyPop.command_line_interface",
    "PyPop.Main": "PyPop.main",
    "PyPop.Meta": "PyPop.meta",
    "PyPop.Utils": "PyPop.utils",
}


class PyPopModuleRenameDeprecationWarning(DeprecationWarning):
    """Deprecation warning for PyPop module renames."""


class DeprecatedModuleFinder(importlib.abc.MetaPathFinder):
    def __init__(self, mapping):
        self.mapping = mapping

    def find_spec(self, fullname, _path, _target=None):
        if fullname in self.mapping:
            new_name = self.mapping[fullname]
            module = importlib.import_module(new_name)
            sys.modules[fullname] = module

            warnings.warn(
                f"Module '{fullname}' is deprecated; use '{new_name}' instead",
                PyPopModuleRenameDeprecationWarning,
                stacklevel=5,
            )

            return module.__spec__
        return None
