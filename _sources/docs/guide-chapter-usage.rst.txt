**************************
Getting started with PyPop
**************************

Introduction
============

You may use :program:`PyPop` to analyze many different kinds of data, including
allele-level genotype data (as in :numref:`data-minimal-noheader-noids`), allele-level
frequency data (as in :numref:`data-allelecount`),
microsatellite data, SNP data, and nucleotide and amino acid sequence
data.

As mentioned in the installation chapter, a minimal working example 
of a `configuration file (.ini) <https://github.com/alexlancaster/pypop/blob/main/tests/data/USAFEL-UchiTelle-small.pop>`_, 
and a `population file (.pop) <https://github.com/alexlancaster/pypop/blob/main/tests/data/minimal.ini>`_, 
can be found by clicking the respective links. 

There are two ways to run PyPop:

-  interactive mode (where the program will prompt you to directly type
   the input it needs); and

-  batch mode (where you supply all the command line options the program
   needs).

For the most simplest application of PyPop, where you wish to analyze
a single population, the interactive mode is the simplest to use. We
will describe this mode first then describe batch mode.

.. note::

   The following assumes you have already :ref:`installed PyPop
   <Installing PyPop>`, done any :ref:`post-install adjustments
   <Post-install \`\`PATH\`\` adjustments>` needed for your platform, and
   verified that you can run the main commands (see the
   :ref:`Examples` section).

Interactive mode
----------------

To run PyPop in interactive mode, with a minimal "GUI", on Windows or
MacOS, you can directly click on the ``pypop-interactive`` file in the
directory where the scripts were installed (see :ref:`post-install
adjustments <Post-install \`\`PATH\`\` adjustments>`).

You can also type ``pypop-interactive`` after starting a console
application on all platforms (on MacOS and GNU/Linux, this is normally
the :program:`Terminal` program, on Windows, it's :program:`Command
prompt`).

In most cases, this will launch a console with the following:

.. code-block:: text

   PyPop: Python for Population Genomics (1.0.0)
   [Python 3.10.9 | Linux.x86_64-x86_64 | x86_64]
   Copyright (C) 2003-2006 Regents of the University of California
   Copyright (C) 2007-2023 PyPop team.
   This is free software.  There is NO warranty; not even for
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    
   You may redistribute copies of PyPop under the terms of the GNU
   General Public License.  For more information about these
   matters, see the file named COPYING.

   Select both an '.ini' configuration file and a '.pop' file via the
   system file dialog.

Following this:

1. the system file dialog will appear prompting you to select an
   ``.ini`` :ref:`configuration file <guide-usage-configfile>`. 

2. a second system file dialog will prompt you for a ``.pop``
   :ref:`data file <guide-usage-datafile>`.

3. after both files are selected the console will display the
   processing of the file:

   .. code-block:: text
      :emphasize-lines: 5
		
      PyPop is processing sample.pop ...
      PyPop run complete!
      XML output(s) can be found in: ['sample-out.xml']
      Plain text output(s) can be found in: ['sample-out.txt']
      Press Enter to continue...

4. when the run is completed, the last line will prompt you to press
   ``Enter`` to leave the console window (highlighted above).
		
If the system file GUI dialog does not appear (e.g. if you are running
on a terminal without a display), it will fall-back to text-mode entry
for the files, where you need to type the full (either relative or
absolute) paths to the files. The output should resemble:

.. code-block:: text
   :emphasize-lines: 14,15

   PyPop: Python for Population Genomics (1.0.0)
   [Python 3.10.9 | Linux.x86_64-x86_64 | x86_64]
   Copyright (C) 2003-2006 Regents of the University of California
   Copyright (C) 2007-2023 PyPop team.
   This is free software.  There is NO warranty; not even for
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    
   You may redistribute copies of PyPop under the terms of the GNU
   General Public License.  For more information about these
   matters, see the file named COPYING.
   
   To accept the default in brackets for each filename, simply press
   return for each prompt.
      
   Please enter config filename [config.ini]: sample.ini
   Please enter population filename [no default]: sample.pop
   PyPop is processing sample.pop ...
   PyPop run complete!
   XML output(s) can be found in: ['sample-out.xml']
   Plain text output(s) can be found in: ['sample-out.txt']
   Press Enter to continue...

.. note::		

   Some messages with the prefix "LOG:" may appear during the console
   operation.  They are informational only and do not indicate
   improper operation of the program.
   
In both cases you should substitute the names of your own
configuration (e.g., :file:`config.ini`) and population file (e.g.,
:file:`Guatemalan.pop`) for :file:`sample.ini` and :file:`sample.pop`
(highlighted above). The formats for these files are described in the
sections on the :ref:`data file <guide-usage-datafile>` and
:ref:`configuration file <guide-usage-configfile>`, below.

Batch mode
----------

To run PyPop in the more common "batch mode", you can run PyPop from
the console (as noted above, on Windows: open :program:`Command
prompt`, aka a "DOS shell"; on MacOS or GNU/Linux: open the
:program:`Terminal` application). Change to a directory where your
``.pop`` file is located, and type the command:

.. code-block:: text

   pypop Guatemalan.pop

.. note::

   If your system administrator has installed PyPop the name of the
   script may be renamed to something different.

Batch mode assumes two things: that you have a file called
:file:`config.ini` in your current folder and that you also have your
population file is in the current folder, otherwise you will need to
supply the full path to the file. You can specify a particular
configuration file for PyPop to use, by supplying the ``-c`` option as
follows:

.. code-block:: text

   pypop -c newconfig.ini Guatemalan.pop

You may also redirect the output to a different directory (which must
already exist) by using the ``-o`` option:

.. code-block:: text

   pypop -c newconfig.ini -o altdir Guatemalan.pop

Please see :ref:`guide-pypop-cli` for the full list of command-line
options.

.. _guide-usage-intro-run-details:

What happens when you run PyPop?
--------------------------------

The most common types of analysis will involve the editing of your
:file:`config.ini` file to suit your data (see :ref:`the configuration
file <guide-usage-configfile>`) followed by the selection of either
the interactive or batch mode described above. If your input
configuration file is :file:`{configfilename}` and your population
file name is :file:`{popfilename}.txt` the initial output will be
generated quickly, but your the PyPop execution will not be finished
until the text output file named :file:`{popfilename}-out.txt` has
been created. A successful run will produce two output files:
:file:`{popfilename}-out.xml`, :file:`{popfilename}-out.txt`. A third
output file will be created if you are using the Anthony Nolan HLA
filter option for HLA data to check your input for valid/known HLA
alleles: :file:`popfilename-filter.xml`).

The :file:`popfilename-out.xml` file is the primary output created by
PyPop and the human-readable :file:`popfilename-out.txt` file is a
summary of the complete XML output. The XML output can be further
transformed into plain text TSV files, either directly via ``pypop``
if invoked on multiple input files (using the ``--enable-tsv`` option,
see :ref:`guide-pypop-cli`), or via the ``popmeta`` tool that
aggregates results from different ``pypop`` runs (see
:ref:`guide-usage-popmeta`).

A typical PyPop run might take anywhere from a few of minutes to a few
hours, depending on how large your data set is and who else is using the
system at the same time. Note that performing the
``allPairwiseLDWithPermu`` test may take several **days** if you have
highly polymorphic loci in your data set.


.. _guide-usage-popmeta:
      
Using ``popmeta`` to aggregate results
======================================

The ``popmeta`` script can aggregate results from a number of output
XML files from individual populations into a set of tab-separated
(TSV) files containing summary statistics via customized XSLT
(eXtensible Stylesheet Language for Transformations) stylesheets.
These TSV files can be directly imported into a spreadsheet or
statistical software (e.g., :program:`R`, :program:`SAS`).  In
addition, there is some preliminary support for export into other
formats, such as the population genetic software (e.g.,
:program:`PHYLIP`).

Here is an example of a ``popmeta`` run, following on from the XML outputs
generated in similar fashion in the previous ``pypop`` runs:

.. code-block:: text

   popmeta -o altdir Guatemalan-out.xml NorthAmerican-out.xml

This will generate a number of ``.tsv`` files, in the output directory
``altdir``, of the form :file:`1-locus-allele.tsv`,
:file:`1-locus-summary.tsv`, etc.

You can also supply a prefix to the command-line option
``--prefix-tsv`` so that all ``.tsv`` files are given a prefix, e.g.,

.. code-block:: text

   popmeta -o altdir --prefix-tsv myoutput Guatemalan-out.xml NorthAmerican-out.xml

Will result in files with a prefix, e.g. :file:`myoutput-1-locus-allele.tsv`.

.. note::

   It's highly recommended to use the ``-o`` option to save the output
   in a separate subdirectory, as the output ``.tsv`` files have
   fixed names, and will overwrite any files in the local directory with the
   same name.  See :ref:`guide-popmeta-cli` for the full list of options.
      
Note that a similar effect can be achieved directly from a ``pypop``
run (assuming that the configuration file can be used for both
``.pop`` population files), by invoking ``pypop`` with the
``--enable-tsv`` option:

.. code-block:: text

   pypop -c newconfig.ini -o altdir Guatemalan.pop NorthAmerican.pop --enable-tsv


Command-line interfaces
=======================

Described below is the usage for both programs, including a full list
of the current command-line options and arguments.  Note that you can
also view this full list of options from the program itself by
supplying the ``--help`` option, i.e. ``pypop --help``, or ``popmeta
--help``, respectively.

.. _guide-pypop-cli:

``pypop`` usage
---------------
	
.. argparse::
   :filename: src/PyPop/CommandLineInterface.py
   :func: get_pypop_cli
   :prog: pypop
   :nodescription:
   :noepilog:
   :nodefaultconst:
      
.. _guide-popmeta-cli:

``popmeta`` usage
-----------------

.. argparse::
   :filename: src/PyPop/CommandLineInterface.py
   :func: get_popmeta_cli
   :prog: popmeta
   :nodescription:
   :noepilog:
   :nodefaultconst:
      
.. _guide-usage-datafile:

The data file
=============

Sample files
------------

Data can be input either as genotypes, or in an allele count format,
depending on the format of your data.

.. admonition:: Data files are tab-delimited

   These population files are plain text files, such as you might save
   out of the :program:`Notepad` application on Windows (or
   :program:`Emacs`). The columns are all tab-delimited, so you can
   include spaces in your labels. If you have your data in a
   spreadsheet application, such as :program:`Excel` or
   :program:`LibreOffice`, export the file as tab-delimited text, in
   order to use it as PyPop data file.

As you will see in the following examples, population files begin with
header information. In the simplest case, the first line contains the
column headers for the genotype, allele count, or, sequence information
from the population. If the file contains a population data-block, then
the first line consists of headers identifying the data on the second
line, and the third line contains the column headers for the genotype or
allele count information.

Note that for genotype data, each locus corresponds to two columns in
the population file. The locus name must repeated, with a suffix such as
``_1``, ``_2`` (the default) or ``_a``, ``_b`` and must match the format
defined in the :file:`config.ini` (see
:ref:`validSampleFields <validSampleFields>`). Although PyPop needs this
distinction to be made, phase is NOT assumed, and if known it is
ignored.

:numref:`config-minimal-example` shows the relevant lines for the
configuration to read in the data shown in
:numref:`data-minimal-noheader-noids` and :numref:`data-minimal-noheader`.

.. literalinclude:: ../../tests/data/doc-examples/data-minimal-noheader-noids.pop
   :name: data-minimal-noheader-noids
   :caption: Multi-locus allele-level genotype data
   :language: text

This is an example of the simplest kind of data file. Note that the columns in the header 
do not appear to align, but that is due to tab separation. You can copy and paste the data
into a text editor to see the tabs.

.. literalinclude:: ../../tests/data/doc-examples/data-minimal-noheader.pop
   :name: data-minimal-noheader
   :caption: Multi-locus allele-level HLA genotype data with sample information
   :language: text

This example shows a data file which has non-allele data in some
columns, here we have population (``populat``) and sample identifiers
(``id``).

.. literalinclude:: ../../tests/data/doc-examples/data-hla.pop
   :name: data-hla
   :caption: Multi-locus allele-level HLA genotype data with sample and header information
   :language: text

This is an example of a data file which is identical to
:numref:`data-minimal-noheader`, but which includes population level
information.

.. literalinclude:: ../../tests/data/doc-examples/data-hla-microsat.pop
   :name: data-hla-microsat
   :caption: Multi-locus allele-level HLA genotype and microsatellite genotype data with header information
   :language: text

This example mixes different kinds of data: HLA allele data (from DRB1
and DQB1 loci) with microsatellite data (locus D6S2222).

.. literalinclude:: ../../tests/data/doc-examples/data-nucleotide.pop
   :name: data-nucleotide
   :caption: Sequence genotype data with header information
   :language: text
     
This example includes nucleotide sequence data: the TGFB1CDN10 locus
consists of one nucleotide, the TGFBhapl locus is actually haplotype
data, but PyPop simply treats each combination as a separate "allele"
for subsequent analysis.

.. literalinclude:: ../../tests/data/doc-examples/data-allelecount.pop
   :name: data-allelecount
   :caption: Allele count data
   :language: text
     
PyPop can also process allele count data. However, you cannot mix allele
count data and genotype data together in the one file.

.. note::
   :name: data-allelecount-note

   Currently each ``.pop`` file can only contain allele count data for
   *one locus*. In order to process multiple loci for one population you
   must create a separate ``.pop`` for each locus.


Missing data
------------

Untyped or missing data may be represented in a variety of ways. The
default value for untyped or missing data is a series of four asterisks
(``****``) as specified by the :file:`config.ini`. You may not "represent"
untyped data by leaving a column blank, nor may you represent a
homozygote by leaving the second column blank. All cells for which you
have data must include data, and all cells for which you do not have
data must also be filled in, using a missing data value.

For individuals who were not typed at all loci, the data in loci for
which they are typed will be used on all single-locus analyses for that
individual and locus, so that you see the value of the number of
individuals (``n``) vary from locus to locus in the output. These
individuals' data will also be used for multi-locus analyses. Only the
loci that contain no missing data will be included in any multi-locus
analysis.

If an individual is only partially typed at a locus, it will be treated
as if it were completely untyped, and data for that individual for that
locus will be dropped from ALL analyses.

.. warning::

   -  Do not leave trailing blank lines at the end of your data file, as
      this currently causes PyPop to terminate with an error message
      that takes experience to diagnose.

   -  For haplotype estimation and linkage disequilibrium calculations
      (i.e., the emhaplofreq part of the program) you are currently
      restricted to a maximum of seven loci per haplotype request. For
      haplotype estimation there is a limit of 5000 for the number of
      individuals (``n``) [1]_

.. _guide-usage-configfile:

The configuration file
======================

The sets of population genetic analyses that are run on your population
data file and the manner in which the data file is interpreted by PyPop
is controlled by a configuration file, the default name for which is
:file:`config.ini`. This is another plain text file consisting of comments
(which are lines that start with a semi-colon), sections (which are
lines with labels in square brackets), and options (which are lines
specifying settings relevant to that section in the ``option=value``
format).

.. note::

   If any option runs over one line (such as ``validSampleFields``) then
   the second and subsequent lines must be indented by exactly **one
   space**.

.. _config-minimal:

A minimal configuration file
----------------------------

Here we present a minimal ``.ini`` file corresponding to
:numref:`data-minimal-noheader-noids` A section by section
review of this file follows. (Note comment lines have been omitted in
the above example for clarity). A description of more advanced options
is contained in :ref:`config-advanced`.

.. config-minimal-example:

.. Minimal ``config.ini`` file
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../tests/data/doc-examples/config-minimal-example.ini
   :name: config-minimal-example
   :caption: Minimal config.ini file
   :emphasize-lines: 1,4,14,17,22,25
   :language: ini		    

**Configuration file sections** (highlighted above)
   
-  ``[General]``

   This section contains variables that control the overall behavior of
   PyPop.

   -  ``debug=0``.

      This setting is for debugging. Setting it to 1 will set off a
      large amount of output of no interest to the general user. It
      should not be used unless you are running into trouble and need to
      communicate with the PyPop developers about the problems.

-  Specifying data formats

   There are two possible formats: ``[ParseGenotypeFile]`` and
   ``[ParseAlleleCountFile]``

   ``[ParseGenotypeFile]``.

   If your data is genotype data, you will want a section labeled:
   ``[ParseGenotypeFile]``.

   -  ``alleleDesignator``.

      This option is used to tell PyPop what is allele data and what
      isn't. You must use this symbol in :ref:```validSampleFields``
      option. The default is ``*``. In general, you won't need to
      change it. **[Default:** ``*`` **]**

   -  ``untypedAllele``.

      This option is used to tell PyPop what symbol you have used in
      your data files to represent untyped or unknown data
      fields. These fields MAY NOT BE LEFT BLANK. You must use
      something consistent that cannot be confused with real data
      here. **[Default:** ``****`` **]**

.. _validSampleFields:

   -  ``validSampleFields``.

      This option should contain the names of the loci immediately
      preceding your genotype data (if it has three header lines, this
      information will be on the third line, otherwise it will be the
      first line of the file).\ **[There is no default, this option must
      always be present]**

      The format is as follows, for each sample field (which may either
      be an identifying field for the sample such as ``populat``, or
      contain allele data) create a new line where:

      -  The first line (``validSampleFields=``) consists of the name of
         your sample field (if it contains allele data, the name of the
         field should be preceded by the character designated in the
         ``alleleDesignator`` option above).

      -  All subsequent lines after the first *must* be preceded by *one
         space* (again if it contains allele data, the name of the field
         should be preceded by the character designated in the
         ``alleleDesignator`` option above).

      Here is an example:

      .. code-block:: text

         validSampleFields=*a_1
          *a_2
          *c_1
          *c_2
          *b_1
          *b_2    Note initial space at start of line.

      Here is example that includes identifying (non-allele data)
      information such as sample id (``id``) and population name
      (``populat``):

      .. code-block:: text

         validSampleFields=populat
          id
          *a_1
          *a_2
          *c_1
          *c_2
          *b_1
          *b_2

   ``[ParseAlleleCountFile]``.

   If your data is not genotype data, but rather, data of the
   allele-name count format, then you will want to use the
   ``[ParseAlleleCountFile]`` section INSTEAD of the
   ``[ParseGenotypeFile]`` section. The ``alleleDesignator`` and
   ``untypedAllele`` options work identically to that described for
   ``[ParseGenotypeFile]``.

   -  ``validSampleFields``.

      This option should contain either a single locus name or a
      colon-separated list of all loci that will be in the data files
      you intend to analyze using a specific ``.ini`` file. The
      colon-separated list allows you to avoid changing the ``.ini``
      file when running over a collection of data files containing
      different loci. e.g.,

      .. code-block:: text

         validSampleFields=A:B:C:DQA1:DQB1:DRB1:DPB1:DPA1
          count

      Note that each ``.pop`` file must contain only one locus (see
      :ref:`the note <data-allelecount-note>` in
      :numref:`data-allelecount`). Listing multiple loci simply
      permits the same ``.ini`` file to be reused for each data file.

-  ``[HardyWeinberg]``

   Hardy-Weinberg analysis is enabled by the presence of this section.

   -  ``lumpBelow``.

      This option value represents a cut-off value. Alleles with an
      expected value equal to or less than ``lumpBelow`` will be lumped
      together into a single category for the purpose of calculating the
      degrees of freedom and overall ``p``-value for the chi-squared
      Hardy-Weinberg test.

-  ``[HardyWeinbergGuoThompson]``

   When this section is present, an implementation of the
   Hardy-Weinberg exact test is run using the original
   :cite:t:`guo_performing_1992` code, using a Monte-Carlo Markov
   chain (MCMC). In addition, two measures (Chen and Diff) of the
   goodness of it of individual genotypes are reported under this
   option :cite:p:`chen_hardy-weinberg_1999`.  By default this section
   is not enabled. This is a different implementation to the
   :program:`Arlequin` version listed in :ref:`config-advanced`,
   below.

   -  ``dememorizationSteps``.

      Number of steps of to “burn-in” the Markov chain before statistics
      are collected.\ **[Default:** ``2000`` **]**

   -  ``samplingNum``.

      Number of Markov chain samples **[Default:** ``1000`` **]**.

   -  ``samplingSize``.

      Markov chain sample size\ **[Default:** ``1000`` **]**.

   Note that the **total** number of steps in the Monte-Carlo Markov
   chain is the product of ``samplingNum`` and ``samplingSize``, so the
   default values described above would contain 1,000,000 (= 1000 x
   1000) steps in the MCMC chain.

   The default values for options described above have proved to be
   optimal for us and if the options are not provided these defaults
   will be used. If you change the values and have problems, please let
   us **know**.

-  ``[HomozygosityEWSlatkinExact]``

   The presence of this section enables Slatkin's :cite:yearpar:`slatkin_exact_1994` 
   implementation of the Ewens-Watterson exact test of neutrality.

   -  ``numReplicates``.

      The default values have proved to be optimal for us. There is no
      reason to change them unless you are particularly curious. If you
      change the default values and have problems, please let us know.

-  ``[Emhaplofreq]``

   The presence of this section enables haplotype frequency estimation and
   calculation of linkage disequilibrium (LD) measures. *Please note that
   PyPop assumes that the genotype data is* **unphased** *when estimating
   haplotype frequencies and LD measures.*

   -  ``lociToEstHaplo``.

      In this option you can list the multi-locus haplotypes for which
      you wish the program to estimate and to calculate the LD. It
      should be a comma-separated list of colon-joined loci. e.g.,

      .. code-block:: text

         lociToEstHaplo=a:b:drb1,a:b:c,drb1:dqa1:dpb1,drb1:dqb1:dpb1

   -  ``allPairwiseLD``.

      Set this to ``1`` (one) if you want the program to calculate all
      pairwise LD for your data, otherwise set this to ``0`` (zero).

.. _config-allPairwiseLDWithPermu:

   -  ``allPairwiseLDWithPermu``.

      Set this to a positive integer greater than 1 if you need to
      determine the significance of the pairwise LD measures in the
      previous section. The number you use is the number of permutations
      that will be run to ascertain the significance (this should be at
      least 1000 or greater). (Note this is done via permutation testing
      performed after the pairwise LD test for all pairs of loci. Note
      also that this test can take *DAYS* if your data is highly
      polymorphic.)

   -  ``numPermuInitCond``.

      Set this to change the number of initial conditions used per
      permutation. **[Default:** ``5`` **]**. (*Note: this parameter is only used
      if* ``allPairwiseLDWithPermu`` *is set and nonzero*).

.. _config-advanced:

Advanced options
----------------

The following section describes additional options to previously
described sections. Most of the time these options can be omitted and
PyPop will choose defaults, however these advanced options do offer
greater control over the application. In particular, customization will
be required for data that has sample identifiers as in
:numref:`data-minimal-noheader` or header data block as in
:numref:`data-hla` and both ``validSampleFields`` (described
above) and ``validPopFields`` (described below) will need to be
modified.

It also describes two extra sections related to using PyPop in
conjunction with :program:`Arlequin`: ``[Arlequin]`` and
``[HardyWeinbergGuoThompsonArlequin]``.

``[General]`` **advanced options**

-  ``txtOutFilename`` and ``xmlOutFilename``.

   If you wish to specify a particular name for the output file, which
   you want to remain identical over several runs, you can set these
   two items to particular values. The default is to have the program
   select the output filename, which can be controlled by the next
   variable. **[Default: not used]**

-  ``outFilePrefixType``.

   This option can either be omitted entirely (in which case the
   default will be ``filename``) or be set in several ways. The
   default is set as ``filename``, which will result in three output
   files named :file:`original-filename-minus-suffix-out.xml`,
   :file:`original-filename-minus-suffix-out.txt`, and
   :file:`original-filename-minus-suffix-filter.xml`. **[Default:**
   ``filename`` **]**

   If you set the value to ``date`` instead of filename, you'll get the
   date incorporated in the filename as follows:
   :file:`original-filename-minus-suffix-YYYY-nn-dd-HH-MM-SS-out.{xml,txt}`.
   e.g., :file:`USAFEL-UchiTelle-2003-09-21-01-29-35-out.xml` (where Y, n,
   d, H, M, S refer to year, month, day, hour, minute and second,
   respectively).

-  ``xslFilename``.

   This option specifies where to find the XSLT file to use for
   transforming PyPop's xml output into human-readable form. Most users
   will not normally need to set this option, and the default is the
   system-installed :file:`text.xsl` file.

``[ParseGenotypeFile]`` **advanced options**

-  ``fieldPairDesignator``.

   This option allows you to override the coding for the headers for
   each pair of alleles at each locus; it must match the entry in the
   config file under ``validSampleFields`` and the entries in your
   population data file. If you want to use something other than ``_1``
   and ``_2``, change this option, for instance, to use letters and
   parentheses, change it as follows: ``fieldPairDesignator=(a):(b)``
   **[Default:** ``_1:_2`` **]**

-  ``popNameDesignator``.

   There is a special designator to mark the population name field,
   which is usually the first field in the data block. **[Default:**
   ``+`` **]**

   If you are analyzing data that contains a population name for each
   sample, then the first entry in your ``validSampleFields`` section
   should have a prefixed +, as below:

   .. code-block:: text

      validSampleFields=+populat
       *a_1
       *a_2
       ...

-  ``validPopFields``.

   If you are analyzing data with an initial two line population header
   block information as in :ref:`data-hla`, then you will
   need to set this option. In this case, it should contain the field
   names in the first line of the header information of your file.
   **[Default: required when a population data-block is present in data
   file]**, e.g.:

   .. code-block:: text

      validPopFields=labcode
       method
       ethnic
       country
       latit
       longit

``[Emhaplofreq]`` **advanced options**

-  ``permutationPrintFlag``.

   Determines whether the likelihood ratio for each permutation will be
   logged to the XML output file, this is disabled by default.
   **[Default:** ``0`` **(i.e. OFF)]**.

   .. warning::

      If this is enabled it can *drastically* increase the size of the
      output XML file on the order of the product of the number of
      possible pairwise comparisons and permutations. Machines with
      lower RAM and disk space may have difficulty coping with this.

``[Arlequin]`` **extra section**

This section sets characteristics of the :program:`Arlequin`
application if it has been installed (it must be installed separately
from PyPop as we cannot distribute it). The options in this section
are only used when a test requiring :program:`Arlequin`, such as it's
implementation of Guo and Thompson's :cite:yearpar:`guo_performing_1992`
Hardy-Weinberg exact test is invoked (see below).

-  ``arlequinExec``.

   This option specifies where to find the :program:`Arlequin`
   executable on your system. The default assumes it is on your system
   path. **[Default:** :file:`arlecore.exe` **]**

``[HardyWeinbergGuoThompsonArlequin]`` **extra section**

When this section is present, :program:`Arlequin`'s implementation of the
Hardy-Weinberg exact test is run, using a Monte-Carlo Markov Chain
implementation. By default this section is not enabled.

-  ``markovChainStepsHW``.

   Length of steps in the Markov chain **[Default: 2500000]**.

-  ``markovChainDememorisationStepsHW``.

   Number of steps of to “burn-in” the Markov chain before statistics
   are collected.\ **[Default:** ``5000`` **]**

The default values for options described above have proved to be optimal
for us and if the options are not provided these defaults will be used.
If you change the values and have problems, please let us **know**.

``[Filters]`` **extra section**

When this section is present, it allows you to specify succesive filters
to the data.

-  ``filtersToApply``.

   Here you specify which filters you want applied to the data and the
   order in which you want them applied. Separate each filter name with
   a colon (``:``). Currently there are four predefined filter:
   ``AnthonyNolan``, ``Sequence``, ``DigitBinning``, and
   ``CustomBinning``. If you specify one or more of these filters, you
   will get the default behavior of the filter. If you wish to modify
   the default behavior, you should add a section with the same name as
   the specified filter(s). See next section for more on this. Please
   note that, while you are allowed to specify any ordering for the
   filters, some orderings may not make sense. For example, the ordering
   Sequence:AnthonyNolan would not make sense (because as far as PyPop
   is concerned, your alleles are now amino acid residues.) However, the
   reverse ordering, AnthonyNolan:Sequence, would be logical and perhaps
   even advisable.

``[AnthonyNolan]`` **filter section**

This section is *only* useful for HLA data. Like all filter sections, it
will only be used if present in the ``filtersToApply`` line specified
above. If so enabled, your data will be filtered through the Anthony
Nolan database of known HLA allele names before processing. The data
files this filter relies on are *not* currently distributed with PyPop
but can be obtained via the `IMGT ftp
site <ftp://ftp.ebi.ac.uk/pub/databases/imgt/mhc/hla/>`__. Invocation of
this filter will produce a ``popfile-filter.xml`` file output showing
what was resolved and what could not be resolved.

-  ``alleleFileFormat``.

   This options specifies which of the formats the Anthony Nolan
   allele data will be used. The option can be set to either ``txt``
   (for the plain free text format) or ``msf`` (for the `Multiple
   Sequence Format <https://www.ebi.ac.uk/ipd/imgt/hla/download/>`__)
   **[Default:** ``msf`` **]**

-  ``directory``.

   Specifies the path to the root of the sequence files. For ``txt``:
   **[Default:**
   :file:`{prefix}/share/PyPop/anthonynolan/HIG-seq-pep-text/`
   **]**.  For ``msf`` files **[Default:**
   :file:`{prefix}/share/PyPop/anthonynolan/msf/` **]**.

-  ``preserve-ambiguous``.

   The default behavior of the ``AnthonyNolan`` filter is to ignore
   allele ambiguity ("slash") notation. This notation, common in the
   literature, looks like: ``010101/0102/010301``. The default behavior
   will simply truncate this to ``0101``. If you want to preserve the
   notation, set the option to ``1``. This will result in a filtered
   allele "name" of ``0101/0102/0103`` in the above hypothetical
   example. **[Default:** ``0`` **]**.

-  ``preserve-unknown``.

   The default behavior of the ``AnthonyNolan`` filter is to replace
   unknown alleles with the ``untypedAllele`` designator. If you want
   the filter to keep allele names it does not recognize, set the option
   to ``1``. **[Default:** ``0`` **]**.

-  ``preserve-lowres``.

   This option is similar to ``preserve-unknown``, but only applies to
   lowres alleles. If set to ``1``, PyPop will keep allele names that are
   shorter than the default allele name length, usually 4 digits long.
   But if the preserve-unknown flag is set, this one has no effect,
   because all unknown alleles are preserved. **[Default:** ``0`` **]**.

``[Sequence]`` **filter section**

This section allows configuration of the sequence filter. Like all
filter sections, it will only will be used if present in the
``filtersToApply`` line specified above. If so enabled, your allele
names will be translated into sequences, and all ensuing analyses will
consider each position in the sequence to be a distinct locus. This
filter makes use of the same msf format alignment files as used above in
the AnthonyNolan filter. It does not work with the txt format alignment
files.

-  ``sequenceFileSuffix``.

   Determines the files that will be examined in order to read in a
   sequence for each allele. (ie, if the file for locus A is
   :file:`A_prot.msf`, the value would be ``_prot`` whereas if you
   wanted to use the nucleotide sequence files, you might use
   ``_nuc``.) **[Default:** ``_prot`` **]**.

-  ``directory``.

   Specifies the path to the root of the sequence files, in the same
   manner as in the AnthonyNolan section, above.

``[DigitBinning]`` **filter section**

This section allows configuration of the DigitBinning filter. Like all
filter sections, it will be used if present in the ``filtersToApply``
line specified above. If so enabled, your allele names will be truncated
after the nth digit.

-  ``binningDigits``.

   An integer that specifies how many digits to keep after the
   truncation. **[Default:** ``4`` **]**.

``[CustomBinning]`` **filter section**

This section allows configuration of the CustomBinning filter. Like all
filter sections, it will only be used if present in the
``filtersToApply`` line specified above.

You can provide a set of custom rules for replacing allele names. Allele
names should be separated by ``/`` marks. This filter matches any allele
names that are exactly the same as the ones you list here, and will also
find "close matches" (but only if there are no exact matches.). Here is
an example:

.. code-block:: text

   A=01/02/03
    04/05/03:06
    !06/12:01/13:01
    !07/08:05

In the example above, ``A*03`` alleles will match to ``01/02/03``,
except for ``A*03:06``, which will match to ``04/05/03:06``. In the output file, 
``A*03:06`` will be replaced with ``04/05/03:06`` and other ``A*03`` alleles will
be replaced with ``01/02/03``. If you place
a ``!`` mark in front of the first allele name, that first name will be
used as the "new name" for the binned group (for example, ``A*08:05``
will be called ``07`` in the custom-binned data.) Note that the space at
the beginning of the lines (following the first line of each locus) is
important. The above rules are just dummy examples, provided to
illustrate how the filter works. PyPop is distributed with a
biologically relevant set of ``CustomBinning`` rules that have been
compiled from several :cite:p:`mack_methods_2007,cano_common_2007` sources [2]_

.. [1]
   These hardcoded numbers can be changed if you obtain the source code
   yourself and change the appropriate #define ``emhaplofreq.h`` and
   recompile the program.

.. [2]
   The Anthony Nolan list of deleted allele names
   (https://github.com/ANHIG/IMGTHLA/blob/Latest/Deleted_alleles.txt); and the
   Ambiguous Allele Combinations, release 2.18.0 (https://www.ebi.ac.uk/ipd/imgt/hla/ambiguity).
