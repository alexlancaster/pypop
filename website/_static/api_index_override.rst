.. _api-reference-top:

API Reference (|api_version|)
=============================

.. only:: latex

   .. raw:: latex

      % Place contents of footnote in a \pagenote
      \OverwriteEnviron{footnote}[4]{\pagenote{\BODY}}
      % FIXME: disable footnotetext, don't play nice with pagenote
      \OverwriteEnviron{footnotetext}[4]{\relax}
      \renewcommand{\sphinxfootnotemark}[4]{\relax}

.. only:: html

   |api_pdf_download_box|

   |apidocs_subtitle|

.. admonition:: *Documenting API for release*  |api_version|  *of PyPop*.

   *Document revision:* |full_release|

   This API reference guide for PyPop is automatically generated from
   the |api_version| source code via `sphinx-autoapi
   <https://github.com/readthedocs/sphinx-autoapi>`_.

   Copyright © |copyright|

   .. only:: html

      **License terms** |gfdl_license_text| (:ref:`gfdl`)

   .. only:: latex

      **License terms** |gfdl_license_text| (:ref:`api-gfdl`)

      References to the *User Guide* can be found in the
      |guide_pdf_link|.

.. only:: latex or pdf

   .. toctree::
      :maxdepth: 3

API changes
-----------

Modules have been renamed to follow the lower-case convention of `PEP8
<https://peps.python.org/pep-0008/#package-and-module-names>`_.  In
addition to lowercasing, some have further renaming to clarify their
purpose and follow standard conventions. User-created Python scripts
that use the PyPop API will continue to work with the old module
names, but raise a
:exc:`~PyPop._deprecations.PyPopModuleRenameDeprecationWarning` (a
custom :exc:`DeprecationWarning`). In the following minor release,
1.5.0, the warnings will become :exc:`ModuleNotFoundError`. The
backwards-compatible bindings will be completely removed in the next
major release.  Command-line users of ``pypop`` will not be affected
by these changes, which are completely internal, scripts will continue
to work as normal.

{{deprecations_block}}

Package introduction
--------------------

{{generated_api_index}}

.. only:: latex

   .. raw:: latex

      \begingroup
      \footnotesize
      \sphinxsetup{%
      %TitleColor={named}{blue},
      }

   .. _api-gfdl:

   .. include:: /docs/gfdl.rst

   .. raw:: latex

      \endgroup
    """
