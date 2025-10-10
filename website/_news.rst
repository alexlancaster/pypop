* 2025-10-10: Add initial version of :doc:`api/index` automatically
  generated from code to document code for developers and users (see
  :ref:`guide-usage-examples-api`).

* 2025-10-07: `PyPop 1.3.1
  <https://github.com/alexlancaster/pypop/releases/tag/v1.3.1>`__ is
  released. Bump ``numpy`` and ``lxml`` dependencies.

  Experimental support for wheels built for Windows ARM64 is also
  available in the `Test PyPI
  <https://test.pypi.org/project/pypop-genomics/>`__ repo, to test,
  run:

  .. code-block:: shell

     pip install --extra-index-url https://test.pypi.org/simple/ pypop-genomics

  Please test and report issues `via the bug tracker
  <https://github.com/alexlancaster/pypop/issues/new?assignees=&labels=bug&projects=&template=bug_report.yml&title=%5BWindows+ARM64+bug%5D%3A+Please+replace+this+with+a+clear+and+concise+description+of+your+bug>`__.


* 2024-04-01: PyPop paper `published
  <https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2024.1378512/full>`__
  in *Frontiers in Immunology*, :ref:`see citing PyPop <Citing PyPop>`
  for details.

* More details, including recent previous releases:

 .. toggle::

  - 2025-09-08: `PyPop 1.3.0
    <https://github.com/alexlancaster/pypop/releases/tag/v1.3.0>`__ is
    released, adds Python wheels 3.14 and new behavior of the
    ``--filelist FILELIST`` (files are :ref:`resolved
    <guide-usage-filelist>` relative to directory where ``FILELIST``
    is located, rather than working directory).

  - 2025-07-28: `PyPop 1.2.2
    <https://github.com/alexlancaster/pypop/releases/tag/v1.2.2>`__ is
    released, includes dependency updates and ``nox`` task framework
    useful for contributors and developers.

  - 2025-04-29: `PyPop 1.2.1
    <https://github.com/alexlancaster/pypop/releases/tag/v1.2.1>`__
    released, includes a bug fix in text output, and internal
    changes and updates to dependencies.

  - 2025-02-04: `PyPop 1.2.0
    <https://github.com/alexlancaster/pypop/releases/tag/v1.2.0>`__
    is released: includes updates and restoration of full
    functionality for ``[Sequence]`` options as part of the
    ``[Filters]``, including dynamic downloads of HLA sequence data
    and major updates to documentation, using new HLA nomenclature
    throughout.

  - 2025-01-16: Beta release `PyPop 1.2.0b2
    <https://github.com/alexlancaster/pypop/releases/tag/v1.2.0-b2>`__
    is released.

  - 2025-01-05: Pre-release `PyPop 1.1.3rc1
    <https://github.com/alexlancaster/pypop/releases/tag/v1.1.3-rc1>`__
    is now available. Experimental wheels for Windows ARM64 are
    added in this release.

  - 2024-11-18: `PyPop 1.1.2
    <https://github.com/alexlancaster/pypop/releases/tag/v1.1.2>`__
    released: adds ``--citation`` command-line option to print citation
    information and updates ``numpy`` to 2.1.3

  - 2024-09-10: `PyPop 1.1.1
    <https://github.com/alexlancaster/pypop/releases/tag/v1.1.1>`__
    released, enables support for Python 3.13 and build Python 3.13 wheels.

  - 2024-05-30: `PyPop 1.1.0
    <https://github.com/alexlancaster/pypop/releases/tag/v1.1.0>`__
    released. Increases the minimum macOS requirements to Catalina
    (Intel) and Big Sur (Silicon) to ensure binary compatibility with
    the GNU Scientific Library (`gsl`). Thanks to Steve Mack for
    testing.

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
