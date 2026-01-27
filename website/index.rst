.. _guide-preface-intro:

=====================================
PyPop: Python for Population Genomics
=====================================

.. _guide-preface-1-start:

.. container:: logo-container

   .. container:: logo-cell

      .. image:: ../pypop-logo.png
	 :class: no-background
         :width: 120px
         :align: center

   .. container:: text-cell

      **PyPop (Python for Population Genomics)** is an environment for
      doing large-scale population genetic analyses including:

      - conformity to Hardy-Weinberg expectations

      -  tests for balancing or directional selection

      - estimates of haplotype frequencies and measures and tests of
        significance for linkage disequilibrium (LD).

.. _guide-preface-1-end:

.. _news:

.. admonition:: PyPop News
   :class: dropdown, toggle-shown

   .. include:: _news.rst

.. _guide-preface-2-start:

PyPop is an object-oriented framework implemented in `Python
<https://www.python.org/>`__, but also contains C extensions for some
computationally intensive tasks. Output of analyses are stored in XML
format for maximum downstream flexibility. PyPop also has an internal
facility for additionally aggregating the output XML and generating
output tab-separated (TSV) files, as well as well as generating a
default plain text file summary for each population.

Although it can be run on any kind of genotype data, it has additional
support for analyzing population genotype with allelic nomenclature
from the human leukocyte antigen (HLA) region.  An outline of PyPop
can be found in our 2024 paper :cite:`lancaster_pypop_2024`, and two
previous :ref:`papers <Citing PyPop>`.

.. _guide-preface-2-end:

Installation and documentation
------------------------------

Documentation, including instructions on :doc:`installing
<docs/guide-chapter-install>`, :doc:`using <docs/guide-chapter-usage>`
and :doc:`interpreting output of <docs/guide-chapter-instructions>`
PyPop, is contained in the :ref:`PyPop User Guide <user-guide>`.  We
also provide an :doc:`api/index` for that describes the
programmatic access to PyPop and for contributors to PyPop itself.

.. admonition:: Contact and questions

   Please file all questions, support requests, and bug reports via
   our `GitHub issue tracker
   <https://github.com/alexlancaster/pypop/issues>`__. More details on
   how to file bug reports can be found in our :ref:`contributors
   chapter <guide-contributing-bug-report>` of the *User Guide*.
   Please don't email developers individually.

.. _source-code:

Source code
-----------

PyPop is `free software
<http://www.gnu.org/philosophy/free-sw.html>`__ (sometimes referred to
as `open source <https://opensource.org/>`__ software) and the
source code is released under the terms of the "copyleft" GNU General
Public License, or GPL (https://www.gnu.org/licenses/gpl.html)
(specifically GPLv2, but any later version applies).  All source code is
available and maintained on our `GitHub website
<https://github.com/alexlancaster/pypop>`__.

Citing PyPop
------------

.. include:: ../README.rst
   :start-after: guide-include-pypop-cite-start:
   :end-before: guide-include-pypop-zenodo-start:

.. admonition:: Click for Zenodo details
   :class: dropdown

   .. include:: ../README.rst
      :start-after: guide-include-pypop-zenodo-start:
      :end-before: guide-include-pypop-zenodo-end:

.. _guide-preface-3-start:

Two previous papers are also available (but not necessary to cite):

- Lancaster AK, Single RM, Solberg OD, Nelson MP, Thomson G (2007)
  "PyPop update - a software pipeline for large-scale multilocus
  population genomics" *Tissue Antigens* 69 (s1), 192-197.  [`journal
  page <http://dx.doi.org/10.1111/j.1399-0039.2006.00769.x>`__,
  `preprint PDF (112 kB)
  <http://pypop.org/tissue-antigens-lancaster-2007.pdf>`__].

- Lancaster A, Nelson MP, Single RM, Meyer D, Thomson G (2003)
  "PyPop: a software framework for population genomics: analyzing
  large-scale multi-locus genotype data", in *Pacific Symposium on
  Biocomputing* vol. 8:514-525 (edited by R B Altman. et al., World
  Scientific, Singapore, 2003) [`PubMed Central
  <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3891851/>`__, `PDF
  (344 kB) <http://pypop.org/psb-pypop.pdf>`__].

PyPop was originally developed for the analysis of data for the 13th
`International Histocompatiblity Workshop and Conference
<http://www.ihwg.org/>`__ held in Seattle, Washington in 2002
(:cite:alp:`meyer_single_2007`, Single *et al.*
:cite:year:`single_haplotype_2007{a},single_statistical_2007{b}`). For
more details on the design and technical details of PyPop, please
consult Lancaster *et al.*
:cite:yearpar:`lancaster_pypop_2003,lancaster_software_2007{a},lancaster_pypop_2007{b},lancaster_pypop_2024`.

.. _guide-preface-3-end:

Acknowledgements
----------------

.. _guide-preface-acknowlegements-start:

This work has benefited from the support of NIH grant AI49213 (13th
IHW) and NIH/NIAID Contract number HHSN266200400076C
N01-AI-40076. Thanks to Steven J. Mack, Kristie A. Mather, Steve G.E.
Marsh, Mark Grote and Leslie Louie for helpful comments and testing.

.. _guide-preface-acknowlegements-end:

.. _popdata-files:

Supplementary data files
------------------------

`Population data files and online supporting materials <popdata/>`__ for
published studies listed in the :cite:t:`solberg_balancing_2008` meta-analysis paper.

ImmPort.org
-----------

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
   api/index

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Supplementary data sets

   Solberg et al. (2008) <http://pypop.org/popdata/>
