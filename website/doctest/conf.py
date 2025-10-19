"""Sphinx configuration for doctests."""

import os
import sys
from pathlib import Path

# local customizations
sys.path.insert(0, str(Path(__file__).parent.parent))
from helpers import get_api_version_tag

extensions = [
    "sphinx.ext.doctest",  # only this extension
]

# get the tags for exclusions
api_version, api_tag = get_api_version_tag(
    full_release=os.environ.get("SETUPTOOLS_SCM_PRETEND_VERSION", "")
)
# add tag for the API version to be used in user guide examples
tags.add(api_tag)  # noqa: F821

# define for "sphinx-build -b doctest" builds for conditional skipping
# Any global setup for doctest
doctest_global_setup = f"""
__sphinx_tags__ = {list(tags)!r}
"""  # noqa: F821

# Minimal source suffix / master doc
source_suffix = ".rst"
master_doc = "index"
