#!/usr/bin/env python
import sys
from pathlib import Path

import tomli


def generate_metadata(output_path):
    """
    Generate _metadata.py from pyproject.toml.
    """

    with open("pyproject.toml", "rb") as pyproj_file:
        pyproject_data = tomli.load(pyproj_file)
        pkgname = pyproject_data["project"]["name"]
        version_scheme = pyproject_data["tool"]["setuptools_scm"]["version_scheme"]

    metadata_content = f"""# auto-generated
__pkgname__ = "{pkgname}"
__version_scheme__ = "{version_scheme}"
"""

    Path(output_path).write_text(metadata_content)
    print(f"Generated {output_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        output_path = Path(sys.argv[1])
    else:
        output_path = Path("src/PyPop/_metadata.py")
    generate_metadata(output_path)
