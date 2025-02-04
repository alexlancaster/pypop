.. _user-guide:

################
PyPop User Guide
################

.. only:: html

   |guide_subtitle|

   |htmlauthor|

   .. admonition:: *Documenting release*  |version|  *of PyPop*.

      This guide is also available as a |guide_pdf_link|  |br|
      *Document revision:* |full_release|

.. only:: latex or pdf

   .. raw:: latex

      % Place contents of footnote in a \pagenote
      \OverwriteEnviron{footnote}[4]{\pagenote{\BODY}}
      % FIXME: disable footnotetext, don't play nice with pagenote
      \OverwriteEnviron{footnotetext}[4]{\relax}
      \renewcommand{\sphinxfootnotemark}[4]{\relax}

   .. include:: ../index.rst
      :start-after: guide-preface-1-start:
      :end-before: guide-preface-1-end:

   .. include:: ../index.rst
      :start-after: guide-preface-2-start:
      :end-before: guide-preface-2-end:

   .. include:: ../../README.rst
      :start-after: guide-include-pypop-cite-start:
      :end-before: guide-include-pypop-cite-end:

   .. include:: ../index.rst
      :start-after: guide-preface-3-start:
      :end-before: guide-preface-3-end:


**How to use this guide**

This guide to PyPop contains four main parts:

- :doc:`guide-chapter-install` describes how to install PyPop,
  including pre-release binaries.

- :doc:`guide-chapter-usage` describes how to run PyPop.

- :doc:`guide-chapter-instructions` details the population genetic
  methods and statistics that PyPop computes.

- :doc:`guide-chapter-contributing` details how to contribute to
  ongoing PyPop code and documentation.

.. only:: html

   **License terms**

   |uc_copyright| |br|
   Copyright © |copyright|

   |gfdl_license_text| (:ref:`gfdl`).

.. _user-guide-toc:

.. toctree::
   :numbered: 2
   :maxdepth: |toc_maxdepth|

   guide-chapter-install
   guide-chapter-usage
   guide-chapter-instructions
   guide-chapter-contributing
   guide-chapter-changes
   licenses

.. toctree::

   biblio

.. |br| raw:: html

   <br/>
