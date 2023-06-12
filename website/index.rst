.. _guide-preface-intro:

=====================================   
PyPop: Python for Population Genomics
=====================================

.. warning::
   
    The old Python 2 binary releases are deprecated and no longer
    maintained. We are working making PyPop available via `pypi.org
    <https://pypi.org>`__, but for the time being, please follow
    the instructions on the GitHub** `README.rst
    <https://github.com/alexlancaster/pypop#readme>`__ for how to
    build the new Python 3-compatible |release| PyPop from source on
    a modern Python 3 system.

.. _news:

.. admonition:: Release history and news
  :class: dropdown	

  - 2023: ported to Python 3, developer can compile the v1.0.0-alpha
    version - no formal release yet.
  - 2022: v0.7.0 binaries are now officially deprecated.
  - 2020: pypop is no longer an official Fedora package. Future releases
    will be made available via PyPi.org
  - 2017: all new development is now in GitHub, no official release
    yet
  - 2008-09-09: 0.7.0 release (many new features and bug fixes)
  - 2005-04-13: 0.6.0 released (new features and bug fixes)
  - 2004-03-09: 0.5.2 released (bug fix release, fixes Windows 98
    .bat file problems)
  - 2004-02-26: 0.5.1 released (mainly a bug fix and maintainance
    release)
  - 2003-12-31: 0.5 released (first public beta)


.. _guide-preface-1-start:

**PyPop (Python for Population Genomics)** is an environment for doing
large-scale population genetic analyses including:

-  conformity to Hardy-Weinberg expectations

-  tests for balancing or directional selection

-  estimates of haplotype frequencies and measures and tests of
   significance for linkage disequilibrium (LD).

It is an object-oriented framework implemented in `Python
<http://www.pypop.org/>`__, a language with powerful features for
interfacing with other languages, such as C (in which we have already
implemented many routines and which is particularly suited to
computationally intensive tasks).

The output of the analyses are stored in XML. These output files can
then be transformed using standard tools into many other data formats
suitable for machine input (such as PHYLIP or input for spreadsheet
programs such as Excel or statistical packages, such as R), plain
text, or HTML for human-readable format. Storing the output in XML
allows the final viewable output format to be redesigned at will,
without requiring the (often time-consuming) re-running of the
analyses themselves.

An outline of PyPop can be found in our 2007 *Tissue Antigens* and
2003 *PSB* :ref:`papers <citing-pypop>`.

.. _guide-preface-1-end:

**Installation and documentation**

Documentation, including instructions on :doc:`installing
<docs/guide-chapter-install>`, :doc:`using <docs/guide-chapter-usage>`
and :doc:`interpreting output of <docs/guide-chapter-instructions>`
PyPop, is contained in the :ref:`PyPop User Guide
<user-guide>`.

.. admonition:: Contact and questions

   Please file all questions, support requests, and bug reports via
   our `GitHub issue tracker
   <https://github.com/alexlancaster/pypop/issues>`__.

.. _source-code:

**Source code**

PyPop is `free software
<http://www.gnu.org/philosophy/free-sw.html>`__ (sometimes referred to
as `open source <http://www.opensource.org/>`__ software) and the
source code is released under the terms of the "copyleft" GNU General
Public License, or GPL (http://www.gnu.org/licenses/gpl.html).  All
source code is available and maintained on our `GitHub website
<https://github.com/alexlancaster/pypop>`__.

.. _citing-pypop:

.. _guide-preface-2-start:

**How to cite PyPop**

When citing PyPop, please cite the (2007) paper from *Tissue Antigens*:

-  A. K. Lancaster, R. M. Single, O. D. Solberg, M. P. Nelson and
   G. Thomson (2007) "PyPop update - a software pipeline for
   large-scale multilocus population genomics" *Tissue Antigens* 69 (s1), 192-197.
   [`journal page <http://dx.doi.org/10.1111/j.1399-0039.2006.00769.x>`__,
   `preprint PDF (112 kB) <tissue-antigens-lancaster-2007.pdf>`__].

In addition, you can also cite our 2003 Pacific Symposium on Biocomputing paper:

- Alex Lancaster, Mark P. Nelson, Richard M. Single, Diogo Meyer, and
  Glenys Thomson (2003) "PyPop: a software framework for population
  genomics: analyzing large-scale multi-locus genotype data", in
  *Pacific Symposium on Biocomputing* vol. 8:514-525 (edited by R B
  Altman. et al., World Scientific, Singapore, 2003) [`PubMed
  Central <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3891851/>`__,
  `PDF (344 kB) <psb-pypop.pdf>`__].

PyPop was originally developed for the analysis of data for the 13th
`International Histocompatiblity Workshop and
Conference <http://www.ihwg.org/>`__ held in Seattle, Washington in 2002
([Meyer:etal:2007]_, [Single:etal:2007a]_, [Single:etal:2007a]_). For more
details on the design and technical details of PyPop, please consult
[Lancaster:etal:2003]_, [Lancaster:etal:2007a]_ and [Lancaster:etal:2007b]_.

.. _acknowlegements:

**Acknowlegements**

This work has benefited from the support of NIH grant AI49213 (13th
IHW) and NIH/NIAID Contract number HHSN266200400076C
N01-AI-40076. Thanks to Steven J. Mack, Kristie A. Mather, Steve G.E.
Marsh, Mark Grote and Leslie Louie for helpful comments and testing.

.. _guide-preface-2-end:


.. _popdata-files:

**Supplementary data files**

`Population data files and online supporting materials <popdata/>`__ for
published studies listed in the [Solberg:etal:2008]_ meta-analysis paper.

.. _immport-org:

**ImmPort.org**

PyPop is affiliated with https://ImmPort.org, the Immunology Database and
Analysis Portal. The ImmPort system provides advanced information
technology support in the production, analysis, archiving, and
exchange of scientific data for the diverse community of life science
researchers supported by NIAID/DAIT. The development of the ImmPort
system was supported by the NIH/NIAID Bioinformatics Integration
Support Contract (BISC), Phase II.


.. toctree::
   :caption: Documentation
   :maxdepth: 3
   :hidden:

   docs/index

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Supplementary data sets

   Solberg et al. (2008) <http://pypop.org/popdata/>
