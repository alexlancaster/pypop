.. _guide-preface-intro:

=====================================
PyPop: Python for Population Genomics
=====================================

.. _news:

.. _guide-preface-1-start:

**PyPop (Python for Population Genomics)** is an environment for doing
large-scale population genetic analyses including:

-  conformity to Hardy-Weinberg expectations

-  tests for balancing or directional selection

-  estimates of haplotype frequencies and measures and tests of
   significance for linkage disequilibrium (LD).

.. _guide-preface-1-end:

.. admonition:: PyPop News
  :class: dropdown, toggle-shown

  * 2025-01-05: Pre-release `PyPop 1.1.3rc1
    <https://github.com/alexlancaster/pypop/releases/tag/v1.1.3-rc1>`__
    is now available. Experimental wheels for Windows ARM64 are
    available via `Test PyPI
    <https://test.pypi.org/project/pypop-genomics/>`__. If you're on
    Windows ARM64, install using:

    .. code-block:: shell

       pip install --pre --extra-index-url https://test.pypi.org/simple/ pypop-genomics

    Please test and report issues `via the bug tracker
    <https://github.com/alexlancaster/pypop/issues/new?assignees=&labels=bug&projects=&template=bug_report.yml&title=%5BWindows+ARM64+bug%5D%3A+Please+replace+this+with+a+clear+and+concise+description+of+your+bug>`__. Note
    that if you are installing on a non-Windows ARM64, you can use the
    regular PyPI repository:

    .. code-block:: shell

       pip install --pre pypop-genomics

  * 2024-11-18: `PyPop 1.1.2
    <https://github.com/alexlancaster/pypop/releases/tag/v1.1.2>`__
    released: adds ``--citation`` command-line option to print citation
    information and updates ``numpy`` to 2.1.3

  * 2024-09-10: `PyPop 1.1.1
    <https://github.com/alexlancaster/pypop/releases/tag/v1.1.1>`__
    released, enables support for Python 3.13 and build Python 3.13 wheels.

  * 2024-05-30: `PyPop 1.1.0
    <https://github.com/alexlancaster/pypop/releases/tag/v1.1.0>`__
    released. Increases the minimum macOS requirements to Catalina
    (Intel) and Big Sur (Silicon) to ensure binary compatibility with
    the GNU Scientific Library (`gsl`). Thanks to Steve Mack for
    testing.

  * 2024-04-01: PyPop paper `published
    <https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2024.1378512/full>`__
    in *Frontiers in Immunology*, :ref:`see citing PyPop <citing-pypop>` for details.

  * More details, including recent previous releases:

   .. toggle::
    - 2024-03-08: PyPop paper, provisionally accepted.
    - 2024-02-24: `PyPop 1.0.2
      <https://github.com/alexlancaster/pypop/releases/tag/v1.0.2>`__
      released. Code scanning updates and updated ``numpy`` to 1.26.4

    - 2024-02-11: `PyPop 1.0.1
      <https://github.com/alexlancaster/pypop/releases/tag/v1.0.1>`__
      released. Added support for ``ARM64`` for Linux, and also
      ``muslinux`` wheels. Improved support for scientific notation.

    - 2024-02-01: `Preprint <https://zenodo.org/records/10602940>`__
      describing 1.0.0 released on Zenodo.
    - 2023-11-07: `PyPop 1.0.0
      <https://github.com/alexlancaster/pypop/releases/tag/v1.0.0>`__
      released

    - Highlights of PyPop 1.0.0 include:

      * PyPop now fully ported to Python 3.
      * New asymmetric linkage disequilibrium (ALD) computations
        :cite:p:`thomson_conditional_2014`:.
      * Improved tab-separated values (TSV) output file handling.
      * Preliminary support for `Genotype List (GL) String
        <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3715123/>`__.
      * Unit tests, new documentation system, continuous integration
        framework and PyPI package
      * and even more minor features and bug fixes... (see
        `NEWS.md <https://github.com/alexlancaster/pypop/blob/main/NEWS.md#100---2023-11-07>`__).

    - 2023-11-04: release candidate 2 (1.0.0rc2) released. Fixes some
      missing TSV output.
    - 2023-11-01: release candidate 1 (1.0.0rc1) released.
    - 2023-10-27: seventh beta pre-release 1.0.0b7, Previous ``arm64``
      issues have been resolved. Thanks to Owen Solberg for extensive
      testing and debugging.
    - 2023-10-13: fourth beta pre-release 1.0.0b4, . Although this
      release contains packages that will install on ``arm64``/M1
      machines, these ``arm64`` packages should be considered as
      **alpha**-only and are strictly for testing only. Please do not
      use PyPop on M1 machines for any production analyses, until we
      fix some underlying ``arm64`` numerical issues.
    - 2023-10-10: second beta pre-release 1.0.0b2
    - 2023-09-26: first beta pre-release 1.0.0b1
    - 2023: ported to Python 3, pre-release alpha versions of 1.0.0
      under development - no formal release yet.
    - 2022: 0.7.0 binaries deprecated.
    - 2020: pypop is no longer a Fedora package (to be replaced by PyPI package)
    - 2017: all new development is now in GitHub

  * See the :ref:`PyPop Release History` in the *Python User Guide*
    for even earlier history and full release notes.

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
from the human leukocyte antigen (HLA) region.

An outline of PyPop can be found in our 2024 paper, and two
previous :ref:`papers <citing-pypop>`.

.. _guide-preface-2-end:

**Installation and documentation**

Documentation, including instructions on :doc:`installing
<docs/guide-chapter-install>`, :doc:`using <docs/guide-chapter-usage>`
and :doc:`interpreting output of <docs/guide-chapter-instructions>`
PyPop, is contained in the :ref:`PyPop User Guide
<user-guide>`.

.. admonition:: Contact and questions

   Please file all questions, support requests, and bug reports via
   our `GitHub issue tracker
   <https://github.com/alexlancaster/pypop/issues>`__. More details on
   how to file bug reports can be found in our :ref:`contributors
   chapter <guide-contributing-bug-report>` of the *User Guide*.
   Please don't email developers individually.

.. _source-code:

**Source code**

PyPop is `free software
<http://www.gnu.org/philosophy/free-sw.html>`__ (sometimes referred to
as `open source <https://opensource.org/>`__ software) and the
source code is released under the terms of the "copyleft" GNU General
Public License, or GPL (https://www.gnu.org/licenses/gpl.html)
(specifically GPLv2, but any later version applies).  All source code is
available and maintained on our `GitHub website
<https://github.com/alexlancaster/pypop>`__.

.. _citing-pypop:

.. include:: ../README.rst
   :start-after: guide-include-pypop-cite-start:
   :end-before: guide-include-pypop-cite-end:

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
:cite:p:`meyer_single_2007,single_haplotype_2007,single_statistical_2007`. For
more details on the design and technical details of PyPop, please
consult :cite:t:`lancaster_pypop_2003`,
:cite:t:`lancaster_pypop_2007`, and :cite:t:`lancaster_software_2007`.

.. _acknowlegements:

**Acknowledgements**

This work has benefited from the support of NIH grant AI49213 (13th
IHW) and NIH/NIAID Contract number HHSN266200400076C
N01-AI-40076. Thanks to Steven J. Mack, Kristie A. Mather, Steve G.E.
Marsh, Mark Grote and Leslie Louie for helpful comments and testing.

.. _guide-preface-3-end:

.. _popdata-files:

**Supplementary data files**

`Population data files and online supporting materials <popdata/>`__ for
published studies listed in the :cite:t:`solberg_balancing_2008` meta-analysis paper.

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
