# NEWS

All notable changes to this project (especially user-visible ones)
will be documented in this file.  It mostly consists of the
concatenated release notes.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org).

## [1.1.1] - 2024-09-10

### Features

- Enable support for Python 3.13 by @alexlancaster ([#217](https://github.com/alexlancaster/pypop/pull/217))

### Bug Fixes

- Pin `gsl` bottles to 2.7.1 on macOS to preserve 10.15/Catalina on x86 and 11.0/Big Sur compatibility + update `cibuildwheels` by @alexlancaster ([#212](https://github.com/alexlancaster/pypop/pull/212))

### Internal

- Update numpy requirement from \<=2.1.0 to \<=2.1.1 by @dependabot ([#218](https://github.com/alexlancaster/pypop/pull/218))
- Update numpy requirement from \<=2.0.1 to \<=2.1.0 by @dependabot ([#216](https://github.com/alexlancaster/pypop/pull/216))
- Update lxml requirement from \<=5.2.2 to \<=5.3.0 by @dependabot ([#215](https://github.com/alexlancaster/pypop/pull/215))
- Bump pypa/cibuildwheel from 2.19.2 to 2.20.0 in the actions group by @dependabot ([#214](https://github.com/alexlancaster/pypop/pull/214))
- Update numpy requirement from \<=2.0.0 to \<=2.0.1 by @dependabot ([#213](https://github.com/alexlancaster/pypop/pull/213))
- Update numpy requirement from \<=1.26.4 to \<=2.0.0 by @dependabot ([#209](https://github.com/alexlancaster/pypop/pull/209))
- Bump pypa/cibuildwheel from 2.19.0 to 2.19.1 in the actions group by @dependabot ([#210](https://github.com/alexlancaster/pypop/pull/210))
- Bump pypa/cibuildwheel from 2.18.1 to 2.19.0 in the actions group by @dependabot ([#208](https://github.com/alexlancaster/pypop/pull/208))

[1.1.1]: https://github.com/alexlancaster/pypop/releases/tag/v1.1.1

## [1.1.0] - 2024-05-30

This release increases the minimum macOS requirements to Catalina (Intel) and Big Sur (Silicon) to ensure binary compatibility with the GNU Scientific Library (`gsl`) on those platforms. Thanks to @sjmack for testing.

### Internal

- Bump `cibuildwheel` from 2.17.0 to 2.18.1, increase minimum macOS requirements by @dependabot ([#206](https://github.com/alexlancaster/pypop/pull/206))
- Update lxml requirement from \<=5.2.1 to \<=5.2.2 by @dependabot ([#205](https://github.com/alexlancaster/pypop/pull/205))
- Bump peaceiris/actions-gh-pages from 3 to 4 in the actions group by @dependabot ([#201](https://github.com/alexlancaster/pypop/pull/201))
- Update lxml requirement from \<=5.2.0 to \<=5.2.1 by @dependabot ([#202](https://github.com/alexlancaster/pypop/pull/202))
- Update lxml requirement from \<=5.1.0 to \<=5.2.0 by @dependabot ([#200](https://github.com/alexlancaster/pypop/pull/200))
- Enable native MacOS Apple Silicon runners by @alexlancaster ([#199](https://github.com/alexlancaster/pypop/pull/199))
- Update `cibuildwheel` GitHub action to 2.17.0 by @dependabot ([#198](https://github.com/alexlancaster/pypop/pull/198))
- Update `softprops/action-gh-release` github action that uploads builds to releases by @dependabot ([#197](https://github.com/alexlancaster/pypop/pull/197))

### Documentation

- fix reversed links (#203) by @alexlancaster ([#204](https://github.com/alexlancaster/pypop/pull/204))

[1.1.0]: https://github.com/alexlancaster/pypop/releases/tag/v1.1.0

## [1.0.2] - 2024-02-24

### Bug Fixes

- Synchronize with upstream `haplo.stats`, fix some redundant checks by @alexlancaster ([#196](https://github.com/alexlancaster/pypop/pull/196))

### Internal

- customize code security scanning for C extensions by @alexlancaster ([#195](https://github.com/alexlancaster/pypop/pull/195))
- Update numpy requirement from \<=1.26.3 to \<=1.26.4 by @dependabot ([#193](https://github.com/alexlancaster/pypop/pull/193))

### Documentation

- Documentation updates including security policy by @alexlancaster ([#194](https://github.com/alexlancaster/pypop/pull/194))

[1.0.2]: https://github.com/alexlancaster/pypop/releases/tag/v1.0.2

## [1.0.1] - 2024-02-11

### Features

- Add  `[CustomBinning]` filtering unit tests for G and P-codes by @alexlancaster ([#186](https://github.com/alexlancaster/pypop/pull/186))

### Bug Fixes

- switch to scientific notation when frequencies can't be displayed as decimals by @alexlancaster ([#192](https://github.com/alexlancaster/pypop/pull/192))
- Port `[RandomBinningFilter]` to Python 3, include more complex filtering tests by @alexlancaster ([#187](https://github.com/alexlancaster/pypop/pull/187))

### Internal

- Bump the `cibuildwheel` version from `2.16.4` to `2.16.5`: fixes Windows CI builds by @dependabot ([#189](https://github.com/alexlancaster/pypop/pull/189))
- Bump the version of `cibuildwheel` from 2.16.2 to 2.16.4 by @dependabot ([#188](https://github.com/alexlancaster/pypop/pull/188))
- increase test strictness: make test warnings into errors by @alexlancaster ([#185](https://github.com/alexlancaster/pypop/pull/185))
- Enable wheels on `aarch64` architecture by @alexlancaster ([#184](https://github.com/alexlancaster/pypop/pull/184))
- Update `actions/upload-artifact` from 3 to 4 in Build on ARM64 by @dependabot ([#183](https://github.com/alexlancaster/pypop/pull/183))
- Streamline continuous integration: reduce number of wheels, concurrency by @alexlancaster ([#182](https://github.com/alexlancaster/pypop/pull/182))
- Parallelize wheel builds, re-enable `musllinux` wheels for Python 3.9+ by @alexlancaster ([#181](https://github.com/alexlancaster/pypop/pull/181))
- Update lxml requirement from \<=5.0.0 to \<=5.1.0; disable PyPy 3.7 on Linux by @dependabot ([#178](https://github.com/alexlancaster/pypop/pull/178))
- Update numpy requirement from \<=1.26.2 to \<=1.26.3 by @dependabot ([#177](https://github.com/alexlancaster/pypop/pull/177))
- Update lxml requirement from \<=4.9.4 to \<=5.0.0 by @dependabot ([#174](https://github.com/alexlancaster/pypop/pull/174))
- Update lxml requirement from \<=4.9.3 to \<=4.9.4 by @dependabot ([#173](https://github.com/alexlancaster/pypop/pull/173))
- update to `v4` of `download-artifact` / `upload-artifact` by @alexlancaster ([#172](https://github.com/alexlancaster/pypop/pull/172))
- Bump actions/setup-python from 4 to 5 by @dependabot ([#168](https://github.com/alexlancaster/pypop/pull/168))
- Update numpy requirement from \<=1.26.1 to \<=1.26.2 by @dependabot ([#167](https://github.com/alexlancaster/pypop/pull/167))

### Documentation

- Link to new preprint in docs by @alexlancaster ([#190](https://github.com/alexlancaster/pypop/pull/190))
- Convert bibliography to bibtex by @alexlancaster ([#176](https://github.com/alexlancaster/pypop/pull/176))
- Convert `NEWS.rst` to `NEWS.md`, improve PDF documentation output by @alexlancaster ([#175](https://github.com/alexlancaster/pypop/pull/175))

[1.0.1]: https://github.com/alexlancaster/pypop/releases/tag/v1.0.1


## [1.0.0] - 2023-11-07

PyPop 1.0.0 is the first official release of PyPop using Python 3, and
the first release to be included on [PyPI](https://pypi.org/project/pypop-genomics/). In addition to using
modern libraries, there are some new features, such as the new
asymmetric LD measures, and better handling of TSV files, along with
the typical slew of bug fixes. Many more changes are of an "under the
hood" nature, such as a new unit testing and documentation framework,
and are detailed below.  Many people contributed to this latest
release, which has been a while in coming. Thanks especially to all
new contributors including Vanessa Sochat, Gordon Webster,
Jurriaan H. Spaaks, Karl Kornel and Michael Mariani.  Thanks also to
all of our bug reporters, and ongoing contributors, especially Richard
Single, Owen Solberg and Steve Mack.

### New features

- PyPop now fully ported to run under Python 3 (thanks to Vanessa
  Sochat for major patch)

- Added new asymmetric linkage disequilibrium (ALD) calculations
  (thanks to Richard Single), see [Thomson & Single, 2014](https://doi.org/10.1534/genetics.114.165266)
  for more details. Added in both the plain text (`.txt`) as well as
  the `2-locus-summary.tsv` TSV file outputs.

- Improved tab-separated values (TSV) output file handling:

  - old IHWG headers are disabled by default, so the `-disable-ihwg`
    option has been replaced by the `--enable-ihwg` option, which
    will re-enable them.
  - `popmeta`: allow TSV files to be put in separate directory with
    `-o`/ `--outputdir` command-lineoption for saving generated
    files.
  - `pypop`: renamed `--generate-tsv` to `--enable-tsv`
  - dynamic generation of TSV files based on XML input, so the list of
    files is no longer hard-coded (thanks to Steve Mack for
    suggestion), this also adds support for haplotypes involving more
    than 4 loci

- Preliminary support for Genotype List (GL) String
  (<https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3715123/>)

- Added unit-tests using `pytest` testing framework.

- New documentation system using `sphinx`, replacing the old DocBook
  XML, to generate both the website and the *PyPop User Guide* (HTML
  and PDF):

  - sphinx-based documentation is now written in ReStructuredText
    (`.rst`)
  - improve `popmeta` and other documentation for command-line
    programs
  - documentation additions and improvements from Richard Single,
    Michael Mariani, Gordon Webster and Steve Mack
  - overhaul release process and add a contribution-guide to the
    *PyPop User Guide*.
  - update documentation to use new HLA nomenclature throughout

- PyPop now uses `numpy` in place of the old `Numeric` library
  `Numpy`, and `lxml` in place of `libxml_mod`

### Bug fixes

- TSV file fixes:

  - fix missing columns in TSV files (thanks to Steve Mack for report)

  - fix headers in 3 and 4 locus TSV files

  - output 2 locus haplotypes in TSV if they are explicitly specified
    (thanks to Steve Mack)

  - `2-locus-haplo.tsv`: fixed missing output in `ld.d`,
    `ld.dprime`, `ld.chisq`, and `exp` columns (thanks to Nabil
    M for the report)

  - rename, remove and add some columns headers, including the new
    `ALD` measures:

    - `2-locus-haplo.tsv`: rename columns: `allele` ->
      `haplotype`, `exp` -> `haplotype.no-ld.count`
    - `2-locus-haplo.tsv`: remove `obs` and `obs.freq` columns
      which were duplicative of `haplotype.count` and
      `haplotype.freq`, respectively
    - `2-locus-summary.tsv`: add two new ALD measure columns:
      `ald.1_2` and `ald.2_1`
    - `*-locus-summary.tsv`: rename columns for multilocus
      haplotypes for 3 or more loci, `allele` -> `haplotype` and
      `locus` -> `loci`

- Fix `DigitBinning` and `CustomBinning` filters `[Filters]`
  (report from Steve Mack)

- Fix issues with using colons in alleles, and other separation
  isssues (thanks to Steve Mack)

- Use `~` as the genotype terminator rather than `|` (fixes some
  haplotype estimation bugs)

- Round all haplotype frequencies to 5 decimal places to avoid
  truncation issues (thanks to Steve Mack for report)

- Restore semi-GUI interactive mode by using built-in `TkInter` file
  dialog, and use more informative default "placeholder" file names

- Fix warnings generated by `numpy` and `re` libraries.

- Windows fixes:

  - `Emhaplofreq` will now give identical results on Windows as all
    other platform (needed to port POSIX-version of `drand48()` to
    Windows).
  - Fixed `CustomBinning` filters that were failing on Windows.
  - Enable all unit tests for Windows.

### Internal

- Replace old `getopt` with `argparse` library
- Major code refactoring, including moving code into `src`
  directory, and using packages in `setup.py`
- Added continuous integration via GitHub Actions for releases and
  website updates
- Prepare package for inclusion in `PyPI`
- Add code examples used in documentation as unit tests
- Create GitHub action for upload to Zenodo (thanks to
  Jurriaan H. Spaaks)
- Support for arm64 builds on MacOS, e.g. M1-based Macs (thanks to
  Owen Solberg for report and extensive testing).
- Remove dependency on `psutil`, rarely needed.
- Only build wheels on platforms for which binary wheels are available
  for all dependencies.

[1.0.0]: https://github.com/alexlancaster/pypop/releases/tag/v1.0.0

## [0.7.0] - 2008-09-09

### New features

- `makeNewPopFile` option has been changed.  This option allows user to
  generate intermediate output of filtered files. Now option should
  be of the format: `type:order` where `type` is one of
  `separate-loci` or `all-loci` so that the user can specify whether
  a separate file should be generated for each locus
  (`separate-loci`) or a single file with all loci (`all-loci`).
  `order` should be the order in the filtering chain where the
  matrix is generated, there is no default, for example, for
  generating files after the first filter operation use `1`.

- New command-line option `--generate-tsv`, will generate the `.dat`
  tab-separated values (TSV) files on the the generated -out.xml
  files (aka "popmeta") directly from pypop without needing to run
  additional script.  Now output from pypop can be directly read
  into spreadsheet.

- New feature: add individual genotype tests to Hardy-Weinberg module
  (gthwe), now computes statistics based on individual genotypes in
  the HWP table. The `[HardyWeinbergGuoThompson]` or
  `[HardyWeinbergGuoThompsonMonteCarlo]` options must be enabled in the
  configuration ".ini" file in order for these tests to be carried out.

- Major improvements to custom and random binning filters (Owen Solberg).

- New feature: generate homozygosity values using the Ewens-Watterson test for
  all pairwise loci, or all sites within a gene for sequence data
  (`[homozygosityEWSlatkinExactPairwise]` in .ini file).  Note: this
  really only works for sequence data where the phase for sites
  within an allele are known.

- Haplotype and LD estimation module `emhaplofreq` improvements

  - improved memory usage and speed for emhaplofreq module.
  - maximum sample size for emhaplofreq module increased from 1023 to
    5000 individuals.
  - maximum length of allele names increased to 20

### Bug fixes

- Support Python 2.4 on GCC 4.0 platforms.
- Add missing initialisation for non-sequence data when processing
  haplotypes.  Thanks to Jill Hollenbach for the report.
- Fix memory leak in xslt translation.
- Various fixes relating to parsing XML output.
- Fixed an incorrect parameter name.
- Handle some missing sections in .ini better. Thanks to
  Owen Solberg for report.
- Various build and installation fixes (SWIG, compilation flags)
- Make name of source package be lowercase "pypop".
- Change data directory: /usr/share/pypop/ to /usr/share/PyPop/
- Print out warning when maximum length of allele exceeded, rather than
  crashing.  Thanks to Steve Mack for report.

### Other issues

- Sequence filter

  - In the Sequence filter, add special case for Anthony Nolan HLA data:
    mark null alleles ending in "N" (e.g. HLA-B\*5127N) as "missing
    data" (`****`).
  - Also in Sequence, keep track of unsequenced sites separately
    (via unsequencedSites variable) from "untyped" (aka "missing
    data"). Treat unsequencedSite as a unique allele to make sure that
    those sites don't get treated as having a consensus sequence if
    only one of the sequences in the the set of matches is typed.
  - If no matching sequence is found in the MSF files, then return a
    sequence of * symbols (ie, will be treated as truly missing data,
    not untyped alleles.
  - Add another special case for HLA data: test for 7 digits in allele names
    (e.g. if 2402101 is not found insert a zero after the first 4
    digits to form 24020101, and check for that).  This is to cope
    with yet-another HLA nomenclature change.

- Change semantics of batchsize, make "0" (default) process files separately
  if only R dat files is enabled.  If batchsize not set explicitly
  (and therefore 0) set batchsize to `1` is PHYLIP mode is enabled.

[0.7.0]: https://github.com/alexlancaster/pypop/releases/tag/PYPOP_SRC-0_7_0

## 0.6.0 - 2005-04-13

### New features

- Allow for odd allele counts when processing an allele count data
  (i.e "semi"-typing).  When PyPop is dealing with data that is
  originally genotyped, the current default is preserved i.e.  we
  dis-allow individuals that are typed at only allele, and set
  allowSemiTyped to false.
- New command-line option `-f` (long version `--filelist`) which
  accepts a file containing a list of files (one per line) to
  process (note that this is mutually exclusive with supplying
  INPUTFILEs, and will abort with an error message if you supply
  both simultaneously).
- In batch version, handle multiple INPUTFILEs supplied as command-line
  arguments and support Unix shell-globbing syntax (e.g. `pypop.py
  -c config.ini *.pop`). (NOTE: This is supported *only* in
  batch version, not in the interactive version, which expects one
  and only one file supplied by user.
- Allele count files can now be filtered through the filter apparatus
  (particularly the Sequence and AnthonyNolan) in the same was as
  genotype files transparently.  \[This has been enabled via a code
  refactor that treats allele count files as pseudo-genotype files
  for the purpose of filtering\].  This change also resulted in the
  removal of the obsolete lookup-table-based homozygosity test.
- Add `--disable-ihwg` option to popmeta script to disable hardcoded
  generation of the IHWG header output, and use the output as
  defined in the header in the original .pop input text file.  This
  is disabled by default to preserve backwards compatibility.
- Add `--batchsize` (`-b` short version) option  for popmeta.  Does the
  processing in "batches".  If set and greater than one, list of XML
  files is split into batchsize group.  For example, if there are 20
  XML files and option is via using ("-b 2" or "--batchsize=2") then
  the files will be processed in two batches, each consisting of 10
  files.  If the number does not divide evenly, the last list will
  contain all the "left-over" files.  This option is particularly
  useful with large XML files that may not fit in memory all at
  once.  Note this option is mutually exclusive with the
  `--enable-PHYLIP` option because the PHYLIP output needs to
  calculate allele frequencies across all populations before
  generating files.
- New .ini file option: `[HardyWeinbergGuoThompsonMonteCarlo]`: add a plain
  Monte-Carlo (randomization, without the Markov chain test) test
  for the HardyWeinberg "exact test".  Add code for Guo & Thompson
  test to distribution (now under GNU GPL).

### Bug fixes

- HardyWeinbergGuoThompson overall p-value test was numerically unstable
  because it attempted to check for equality in greater than or
  equal to constructs ("\<=") which is not reliable in C.  Replaced
  this with a GNU Scientific Library (GSL) function gsl_fcmp() which
  compares floats to within an EPSILON (defaults to 1e-6).
- Allow `HardyWeinbergGuoThompson` test to be run if at least two alleles
  present (test was originally failing with a `too-few-alleles`
  message if there were not at least 3 alleles).  Thanks to Kristie
  Mather for the report.
- Checks to see if a locus is monomorphic, if it is, it generates an
  allele summary report, but skips the rest of the single locus
  analyses which do not make sense for monomorphic locus.  Thanks to
  Steve Mack and Owen Solberg for the bug report(s).
- Now builds against recent versions of SWIG (no longer stuck at version
  1.3.9), should be compatible with versions of SWIG > 1.3.10.
  (Tested against SWIG 1.3.21).
- Homozygosity module: Prevent math errors by in Slatkin's exact test by
  forcing the homozygosity to be positive (only a problem for rare
  cases, when the result is so close to zero that the floating point
  algorithms cause a negative result.)

## 0.5.2 (public beta) - 2004-03-09

### Bug fixes

- Add missing RandomBinning.py file to source distribution
  Thanks to Hazael Maldonado Torres for the bug report.
- Fixed line endings for .bat scripts for Win32 so they work under
  Windows 98 thanks to Wendy Hartogensis for the bug report.

## 0.5.1 (public beta) - 2004-02-26

### Changes

- New parameter `numInitCond`, number of initial conditions by the
  haplotype estimation and LD algorithm used before performing
  permutations. Defaults to 50.
- Remove some LOG messages/diagnostics that were erroneously implying
  an error to the user (if nothing is wrong, don't say anything).  Add
  some more useful messages for what is being done in haplo/LD
  estimation step.
- Add popmeta.py to the distribution: this is undocumented and unsupported
  as yet, it is at alpha stage only, use at your own risk!

### Bug fixes

- Remember to output plaintext version of LD for specified loci.

## 0.5 (public beta) - 2003-12-31

### Changes

- All Linux wrapper scripts no longer have .sh file suffixes for
  consistency with DOS (all DOS bat files can be executed without
  specifying the .bat extension).

### Bug fixes

- Add wrapper scripts for interactive and batch mode for
  both DOS and Linux so that correct shared libraries are called.
- Pause and wait for user to press a key at end of DOS .bat file
  so that output can be viewed before window close.
- Set PYTHONHOME in wrapper scripts to prevent messages about
  missing \<prefix> being displayed.

## 0.4.3beta

### Bug fixes

- Fixed bug in processing of `popname` field.
  Thanks to Richard Single for the report.
