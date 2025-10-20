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
"""Sphinx configuration for website."""

import sys
from pathlib import Path

from setuptools_scm import get_version
from sphinx.highlighting import PygmentsBridge

sys.path.insert(0, str(Path(__file__).parent))  # add website/ to path

# local customizations
from helpers import (
    CustomLatexFormatter,
    CustomLaTeXTranslator,
    MyLiteralInclude,
    get_api_version_tag,
    get_autoapi_dirs,
    patch_latex_files,
    prepare_autoapi_index,
    renumber_footnotes,
    skip_instance_vars,
    substitute_toc_maxdepth,
)

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.autosectionlabel",
    "myst_parser",
    "rst2pdf.pdfbuilder",
    "sphinx_togglebutton",
    "sphinxarg.ext",
    "sphinx_copybutton",
    "sphinxcontrib.bibtex",
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
]

# override user-agent so that linkcheck works
# FIXME: disabled, doesn't currently have an effect
# user_agent= "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0"

# autosectionlabel_prefix_document = True
# suppress warnings because autoapi generates many
suppress_warnings = ["autosectionlabel.*"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
# project = "PyPop: Python for Population Genomics"
project = "PyPop"
copyright = "2025 PyPop contributors"
contribs_copyright = f"Copyright © {copyright}"
uc_copyright = "Copyright © 2003-2009 Regents of the University of California"
gfdl_license_text = "Permission is granted to copy, distribute and/or modify this document under the terms of the GNU Free Documentation License, Version 1.2 or any later version published by the Free Software Foundation; with no Invariant Sections no Front-Cover Texts and no Back-Cover Texts. A copy of the license is included in the License chapter."

author_list = [
    "Alexander K. Lancaster",
    "Mark P. Nelson",
    "Diogo Meyer",
    "Richard M. Single",
    "Owen D. Solberg",
]
author = "\\and ".join(author_list)
htmlauthor = ", ".join(author_list)

# enable author directives
show_authors = True

# figures
numfig = True

# override default text on toggle buttons (sphinx_togglebutton extension)
togglebutton_hint = "Click to show"
togglebutton_hint_hide = "Click to hide"


# -- Options for Auto API output ----------------------------------------------

# autoapi_dirs = ["../src/PyPop"]
# need  first try a *released* version
autoapi_dirs = get_autoapi_dirs("PyPop", "../src/PyPop")
autoapi_type = "python"
autoapi_root = "api"
autoapi_add_toctree_entry = False
autoapi_keep_files = False
autoapi_own_page_level = "module"
autoapi_template_dir = "_templates/autoapi"
autoapi_file_pattern = "*.py"
# autoapi_ignore = [ "**/conf.py"]

autoapi_member_order = "source"
autoapi_options = [
    "members",
    "undoc-members",
    #           "private-members",  # remove for production
    #           "special-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
    "show-inheritance-diagram",
]

# graphviz options: reduce space around diagrams in LaTeX backend
graphviz_dot_args = ["-Gmargin=0", "-Granksep=0.2"]

# concatenate the class and constructor
autoapi_python_class_content = "both"

# parse the doc strings as rST
autoapi_python_use_autodoc_docstring = True

# keep docs less verbose by skipping module names in front of each
# class/method
add_module_names = False

# create links to base python classes
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    # you can add more, e.g.
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# -- Options for declaring includes ----------------------------------------------

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

# The full version of local copy, including alpha/beta/rc tags, don't
# normalize for documentation
full_release = get_version("..", normalize=True, version_scheme="post-release")
# The version without the .post or .dev variants
version = full_release.split(".post")[0]
release = version  # make the release and version be the same

api_version, api_tag = get_api_version_tag(full_release=full_release)
# add tag for the API version to be used in user guide examples
tags.add(api_tag)  # noqa: F821

# define for "sphinx-build -b doctest" builds for conditional skipping
doctest_global_setup = f"""
__sphinx_tags__ = {list(tags)!r}
"""  # noqa: F821

guide_prefix = "pypop-guide-" + release  # include version in PDF filename
guide_name = "PyPop User Guide"
guide_subtitle = "User Guide for Python for Population Genomics"
guide_name_with_subtitle = f"{guide_name}: {guide_subtitle}"
guide_pdf_relative_file = f"../{guide_prefix}.pdf"
guide_pdf_link = f"*{guide_name}*: `HTML <http://pypop.org/docs>`__ | `PDF <http://pypop.org/{guide_prefix}.pdf>`__"

apidocs_prefix = "pypop-api-" + release  # include version in PDF filename
apidocs_name = "PyPop API Reference"
apidocs_subtitle = "Developer documentation"
apidocs_name_with_subtitle = f"{apidocs_name}: {apidocs_subtitle}"
apidocs_pdf_relative_file = f"../{apidocs_prefix}.pdf"
apidocs_pdf_link = f"*{apidocs_name}*: `HTML <http://pypop.org/{autoapi_root}>`__ | `PDF <http://pypop.org/{apidocs_prefix}.pdf>`__"

# other substitutions
rst_epilog = """
.. |pkgname| replace:: {}
.. |guide_subtitle| replace:: **{}**
.. |apidocs_subtitle| replace:: **{}**
.. |htmlauthor| replace:: {}
.. |full_release| replace:: {}
.. |api_version| replace:: {}
.. |uc_copyright| replace:: {}
.. |copyright| replace:: {}
.. |gfdl_license_text| replace:: {}
.. |guide_pdf_relative_file| replace:: {}
.. |guide_pdf_link| replace:: {}
.. |guide_pdf_download_box| raw:: html

   <div style="text-align: right; font-size: 120%; margin-top: -1em; margin-bottom: 1em;">
   <a href="../{}.pdf">📥 PDF version</a>
   </div>
.. |apidocs_pdf_relative_file| replace:: {}
.. |apidocs_pdf_link| replace:: {}
.. |api_pdf_download_box| raw:: html

   <div style="text-align: right; font-size: 120%; margin-top: -1em; margin-bottom: 1em;">
   <a href="../{}.pdf">📥 PDF version</a>
   </div>
""".format(
    "``pypop-genomics``",
    guide_subtitle,
    apidocs_subtitle,
    htmlauthor,
    full_release,
    api_version,
    uc_copyright,
    copyright,
    gfdl_license_text,
    guide_pdf_relative_file,
    guide_pdf_link,
    guide_prefix,
    apidocs_pdf_relative_file,
    apidocs_pdf_link,
    apidocs_prefix,
)

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
# language = english

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
    "_build",
    "README.md",
    "reference",
    "doctest",
    "Thumbs.db",
    ".DS_Store",
    "_static",
]


# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Bibligraphy output using sphinxcontrib-bibtex and pybtex --------------------------------------

bibtex_bibfiles = ["pypop.bib"]

## custom citation styles
## overwrite the default square brackets with round-brackets style
## allow for pre and post-text for :cite:year and :cite:yearpar
## remove space between citation and post-text, so that it supports
## output like: "Author (2024a, 2024b)"

from bibtex_styles import AlphaInitialsStyle, MyReferenceStyle  # noqa: E402, F401

bibtex_reference_style = "author_year_round"
bibtex_default_style = "alpha-initials"

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

html_short_title = "PyPop"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {  # some are theme-specific
    "show_nav_level": 3,
    "navigation_depth": 3,
    "collapse_navigation": False,
    "secondary_sidebar_items": {
        "**": [],  # "page-toc"
    },
    "navbar_align": "left",
    "pygments_light_style": "manni",
    "github_url": "https://github.com/alexlancaster/pypop/",
    "announcement": "https://raw.githubusercontent.com/alexlancaster/pypop/refs/heads/main/website/_templates/announcement_banner.html",
    "logo": {
        # In a left-to-right context, screen readers will read the alt text
        # first, then the text, so this example will be read as "P-G-G-P-Y
        # (short pause) Home A pretty good geometry package"
        "alt_text": "PyPop - Home",
        "text": "PyPop",
        # "image_light": "../pypop-logo.png",
        # "image_dark": "../pypop-logo.png",
    },
}

html_logo = "../pypop-logo.png"

html_favicon = "_static/pypop-favicon.ico"

html_sidebars = {"index": [], "**": ["sidebar-nav-bs", "page-toc"]}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# put all files that should be root of the pypop.org/ webserver into this directory
# and they will be included in the build directory (and therefore on the website)
html_extra_path = ["html_root"]

# -- Options for LaTeX output ---------------------------------------------


PygmentsBridge.latex_formatter = CustomLatexFormatter

# latex_show_urls = 'inline'
latex_show_urls = "footnote"

# Copy logo so LaTeX can find it
latex_additional_files = [
    "../pypop-logo.png",
]

latex_logo = "../pypop-logo.png"

# need to declare a template for the LaTeX preamble for later substitution

my_latex_preamble_template = r"""\DeclareRobustCommand{\and}{%
\end{tabular}\kern-\tabcolsep\\\begin{tabular}[t]{c}%
}%
\setcounter{secnumdepth}{1}%

\usepackage{graphicx}
\graphicspath{{docs/_static/}{_static/}{./}}

\usepackage{pagenote}
\makepagenote
% \renewcommand*{\notesname}{End Notes}
\renewcommand*{\notedivision}{\subsubsection*{\notesname}}
\renewcommand*{\pagenotesubhead}[2]{}

% ensure pagenote counter is global and not reset per chapter/section
%\counterwithout{pagenote}{chapter}  % if using manual
\counterwithout{pagenote}{section}  % if using howto

POINTSIZE

\usepackage{etoolbox}% http://ctan.org/pkg/etoolbox

\makeatletter
\@ifclassloaded{sphinxhowto}{
  % "howto" class: no chapter, use \section
  % Only for sphinxhowto class

 \setcounter{tocdepth}{2}

  % Hook into top-level section (index) to print notes
  \pretocmd{\printindex}{%
    % only print footnotes if there are any
    \ifnumcomp{\thepagenote}{>}{0}{%
      \begingroup
      \scriptsize
      \linespread{0.5}%
      \printnotes*%
      \vfill
      \endgroup
    }{}%
  }{}{}

}{
  % "manual" class: use \chapter
  \pretocmd{\chapter}{%
    \ifnumcomp{\thepagenote}{>}{0}{%
      \begingroup
      \scriptsize
      \linespread{0.5}%
      \printnotes*%
      \vfill
      \endgroup
    }{}%
  }{}{}
}
\makeatother

\usepackage{environ}% http://ctan.org/pkg/environ

\newcommand{\OverwriteEnviron}[1]{%
  \expandafter\let\csname #1\endcsname\relax%
  \expandafter\let\csname end#1\endcsname\relax%
  \expandafter\let\csname env@#1@parse\endcsname\relax%
  \expandafter\let\csname env@#1@save@env\endcsname\relax%
  \expandafter\let\csname env@#1@process\endcsname\relax%
  \NewEnviron{#1}%
}


% Reuse Sphinx styling for admonitions
% We'll define a 'sphinxversionbox' environment

\usepackage{xcolor}
\usepackage{tcolorbox} % loads breakable and skins libraries
\tcbuselibrary{breakable} % only breakable boxes

\newtcolorbox{sphinxversionbox}[1][]{
  breakable,
  parbox=false,   % important: preserves normal line spacing
  sharp corners,
  fonttitle=\bfseries\itshape,
  #1
}

% override default title page to add subtitle
\makeatletter
\renewcommand{\sphinxmaketitle}{%
  \let\sphinxrestorepageanchorsetting\relax
  \ifHy@pageanchor\def\sphinxrestorepageanchorsetting{\Hy@pageanchortrue}\fi
  \hypersetup{pageanchor=false}% avoid duplicate destination warnings
  \begin{titlepage}%
    \let\footnotesize\small
    \let\footnoterule\relax
    \noindent\rule{\textwidth}{1pt}\par
      \begingroup % for PDF information dictionary
       \def\endgraf{ }\def\and{\& }%
       \pdfstringdefDisableCommands{\def\\{, }}% overwrite hyperref setup
       \hypersetup{pdfauthor={\@author}, pdftitle={\@title}}%
      \endgroup
    \vspace{3em}
    \makebox[\textwidth][c]{\scalebox{0.65}{\sphinxlogo}}
    \vspace{3em}
    \begin{flushright}%
      \py@HeaderFamily
      {\Huge \@title \par}
      {\Large SUBTITLE \par}
      {\itshape\LARGE \py@release\releaseinfo \par}
      \vfill
      {\LARGE
        \begin{tabular}[t]{c}
          \@author
        \end{tabular}\kern-\tabcolsep
        \par}
      \vfill\vfill
      {\large
       \@date \par
       \vfill
       \py@authoraddress \par
      }%
    \end{flushright}%\par
    \@thanks
  \end{titlepage}%
  \setcounter{footnote}{0}%
  \let\thanks\relax\let\maketitle\relax
  %\gdef\@thanks{}\gdef\@author{}\gdef\@title{}
  \clearpage
  \ifdefined\sphinxbackoftitlepage\sphinxbackoftitlepage\fi
  \if@openright\cleardoublepage\else\clearpage\fi
  \sphinxrestorepageanchorsetting
}"""

# Shared LaTeX maketitle template

maketitle_template = r"""
\newcommand\sphinxbackoftitlepage{%%
  \sphinxstrong{%(doc_name_with_subtitle)s}\\ \\
  %(copyright)s. \\%(extra_copyright)s. \\ \\
  %(gfdl_license_text)s \\ \\
  \emph{Document revision}: %(full_release)s
}
\sphinxmaketitle
"""

# Fill in guide variables
guide_maketitle = maketitle_template % {
    "doc_name_with_subtitle": guide_name_with_subtitle,
    "copyright": uc_copyright,
    "extra_copyright": contribs_copyright,
    "gfdl_license_text": gfdl_license_text,
    "full_release": full_release,
}

# fill in API variables
apidocs_maketitle = maketitle_template % {
    "doc_name_with_subtitle": apidocs_name_with_subtitle,
    "copyright": contribs_copyright,
    "extra_copyright": "",
    "gfdl_license_text": gfdl_license_text,
    "full_release": full_release,
}

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',
    # make PDF shorter by allowing chapters to start immediately
    "extraclassoptions": "openany,oneside",
    # Additional stuff for the LaTeX preamble.
    "preamble": my_latex_preamble_template,
    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
    # "maketitle": r"\newcommand\sphinxbackoftitlepage{}\sphinxmaketitle",
    # margins
    "sphinxsetup": "hmargin=0.8in, vmargin={1in,0.9in}",
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).

latex_documents = [
    (
        "docs/index",
        guide_prefix + ".tex",
        guide_name,
        author,
        "manual",
        False,
        {
            "maketitle": guide_maketitle,
            "placeholders": {"SUBTITLE": guide_subtitle},
        },
    ),
    (
        "api/index",
        apidocs_prefix + ".tex",
        apidocs_name,
        "Alexander K. Lancaster",
        "howto",
        False,
        {
            # "maketitle": apidocs_maketitle,
            "placeholders": {
                "SUBTITLE": apidocs_subtitle,
                "POINTSIZE": "8pt",
            },
        },
    ),
]
pdf_documents = [
    ("docs/index", guide_prefix, guide_name, author),
]


def setup(app):
    """Run the customization hooks."""
    app.connect("builder-inited", prepare_autoapi_index)  # override default index
    app.connect(
        "autoapi-skip-member", skip_instance_vars
    )  # don't document instance variables in public API
    app.set_translator(
        "latex", CustomLaTeXTranslator
    )  # handle version directives in LaTeX
    app.add_directive(
        "literalinclude", MyLiteralInclude, override=True
    )  # fix literalinclude to respect tabs in LaTeX
    app.connect("source-read", substitute_toc_maxdepth)  # dynamic TOC depth
    app.connect("build-finished", renumber_footnotes)
    app.connect("build-finished", patch_latex_files)
