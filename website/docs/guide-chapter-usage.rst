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

There are two ways to run PyPop:

-  interactive mode (where the program will prompt you to directly type
   the input it needs); and

-  batch mode (where you supply all the command line options the program
   needs).

For the most straightforward application of PyPop, where you wish to
analyze a single population, the interactive mode is the simplest to
use. We will describe this mode first then describe batch mode.

Interactive mode
----------------

To run PyPop, click the ``pypop.bat`` file (Windows) or type ``./pypop``
at the command prompt (GNU/Linux). You should see something like the
following output (this is also described in detail in the instructions
in the installation guide):

.. code-block:: text

   PyPop: Python for Population Genomics (0.4.3)
   Copyright (C) 2003 Regents of the University of California
   This is free software.  There is NO warranty; not even for
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    
   You may redistribute copies of PyPop under the terms of the
   GNU General Public License.  For more information about these
   matters, see the file named COPYING.
    
   To accept the default in brackets for each filename, simply press
   return for each prompt.
   Please enter config filename [config.ini]: sample.ini
   Please enter population filename [no default]: sample.pop
   PyPop is processing sample.pop 

   (Note: some messages with the prefix "LOG:" may appear here.
   They are informational only and do not indicate improper operation 
   of the program)

   PyPop run complete!
   XML output can be found in: sample-out.xml
   Plain text output can be found in: sample-out.txt

You should substitute the names of your own configuration (e.g.,
:file:`config.ini`) and population file (e.g., :file:`Guatemalan.pop`) for
:file:`sample.ini` and :file:`sample.pop`. The formats for these files
are described in the sections on the :ref:`data file
<guide-usage-datafile>` and :ref:`configuration file
<guide-usage-configfile>`, below.

Batch mode
----------

To run PyPop in batch mode, you can start PyPop from the command line
(in Windows: open a DOS shell, GNU/Linux: open a terminal window),
change to the directory where you unpacked PyPop and type

.. code-block:: text

   pypop-batch Guatemalan.pop

.. note::

   If your system administrator has installed PyPop the name of the
   script may be renamed to something different.

Batch mode assumes two things: that you have a file called
:file:`config.ini` in your current folder and that you also have your
population file also in the current folder. You can specify a particular
configuration file for PyPop to use, by supplying the ``-c`` option as
follows:

.. code-block:: text

   pypop-batch -c newconfig.ini Guatemalan.pop

You may also redirect the output to a different directory (which must
already exist) by using the ``-o`` option:

.. code-block:: text

   pypop-batch -c newconfig.ini -o altdir Guatemalan.pop

For a full list of options supported by PyPop, type ``pypop-batch
--help``. You should receive a screen resembling the following:

.. code-block:: text

   Usage: pypop [OPTION] INPUTFILE
   Process and run population genetics statistics on an INPUTFILE.
   Expects to find a configuration file called 'config.ini' in the
   current directory or in /usr/share/PyPop/config.ini.

     -l, --use-libxslt    filter XML via XSLT using libxslt (default)
     -s, --use-4suite     filter XML via XSLT using 4Suite
     -x, --xsl=FILE       use XSLT translation file FILE
     -h, --help           show this message
     -c, --config=FILE    select alternative config file
     -d, --debug          enable debugging output (overrides config file setting)
     -i, --interactive    run in interactive mode, prompting user for file names
     -g, --gui            run GUI (currently disabled)
     -o, --outputdir=DIR  put output in directory DIR
     -V, --version        print version of PyPop
      
       INPUTFILE   input text file

.. warning::

   Documentation for these options is underway, but not currently
   available.

.. _guide-usage-intro-run-details:

What happens when you run PyPop?
--------------------------------

The most common types of analysis will involve the editing of your
:file:`config.ini` file to suit your data (see `The configuration
file <guide-usage-configfile>`__) followed by the selection of either
the interactive or batch mode described above. If your input
configuration file is :file:`{configfilename}` and your population file name
is :file:`{popfilename}.txt` the initial output will be generated quickly, but
your the PyPop execution will not be finished until the text output file
named :file:`{popfilename}-out.txt` has been created. A successful run will
produce two output files: :file:`{popfilename}-out.xml`,
:file:`{popfilename}-out.txt`. A third output file will be created if you are
using the Anthony Nolan HLA filter option for HLA data to check your
input for valid/known HLA alleles: :file:`popfilename-filter.xml`).

The :file:`popfilename-out.xml` file is the primary output created by
PyPop and the human-readable :file:`popfilename-out.txt` file is a
summary of the complete XML output. It is generated from the XML
output via XSLT (eXtensible Stylesheet Language for Transformations)
using the default XSLT stylesheet :file:`text.xsl`, which is located
in the ``xslt`` directory.  The XML output can be further transformed
using customized XSLT stylesheets into other formats for input to
statistical software (e.g., :program:`R`, :program:`SAS`) or other
population genetic software (e.g., :program:`PHYLIP`). The ``popmeta``
script (``popmeta.bat`` on Windows, ``popmeta`` on GNU/Linux) calls on
other XSLT stylesheets to aggregate results from a number of output
XML files from individual populations into a set of tab-separated
(TSV) files containing summary statistics. These TSV files can be
directly imported into a spreadsheet or statistical software.  This
script will be further documented in the next release.

A typical PyPop run might take anywhere from a few of minutes to a few
hours, depending on how large your data set is and who else is using the
system at the same time. Note that performing the
``allPairwiseLDWithPermu`` test may take several **days** if you have
highly polymorphic loci in your data set.

.. _guide-usage-datafile:

The data file
=============

Sample files
------------

Data can be input either as genotypes, or in an allele count format,
depending on the format of your data.

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
:numref:`data-minimal-noheader-noids` through to :numref:`data-allelecount`.

.. code-block:: text
   :name: data-minimal-noheader-noids
   :caption: Multi-locus allele-level genotype data

   a_1   a_2   c_1   c_2   b_1   b_2
   ****  ****  0102  02025 1301  18012 
   0101  0201  0307  0605  1401  39021 
   0210  03012 0712  0102  1520  1301  
   0101  0218  0804  1202  35091 4005  
   2501  0201  1507  0307  51013 1401  
   0210  3204  1801  0102  78021 1301  
   03012 3204  1507  0605  51013 39021 
     
   
This is an example of the simplest kind of data file.

.. code-block:: text
   :name: data-minimal-noheader
   :caption: Multi-locus allele-level HLA genotype data with sample information

   populat    id        a_1   a_2   c_1   c_2   b_1   b_2
   UchiTelle  UT900-23  ****  ****  0102  02025 1301  18012 
   UchiTelle  UT900-24  0101  0201  0307  0605  1401  39021 
   UchiTelle  UT900-25  0210  03012 0712  0102  1520  1301  
   UchiTelle  UT900-26  0101  0218  0804  1202  35091 4005  
   UchiTelle  UT910-01  2501  0201  1507  0307  51013 1401  
   UchiTelle  UT910-02  0210  3204  1801  0102  78021 1301  
   UchiTelle  UT910-03  03012 3204  1507  0605  51013 39021 
     

This example shows a data file which has non-allele data in some
columns, here we have population (``populat``) and sample identifiers
(``id``).

.. code-block:: text
   :name: data-hla
   :caption: Multi-locus allele-level HLA genotype data with sample and header information

   labcode method              ethnic  contin  collect        latit           longit          
   USAFEL  12th Workshop SSOP  Telle   NW Asia Targen Village 41 deg 12 min N 94 deg 7 min E  
   populat     id         a_1     a_2     c_1     c_2     b_1     b_2     
   UchiTelle   UT900-23   ****    ****    0102    02025   1301    18012   
   UchiTelle   UT900-24   0101    0201    0307    0605    1401    39021   
   UchiTelle   UT900-25   0210    03012   0712    0102    1520    1301    
   UchiTelle   UT900-26   0101    0218    0804    1202    35091   4005    
   UchiTelle   UT910-01   2501    0201    1507    0307    51013   1401    
   UchiTelle   UT910-02   0210    3204    1801    0102    78021   1301    
   UchiTelle   UT910-03   03012   3204    1507    0605    51013   39021   

This is an example of a data file which is identical to
:numref:`data-minimal-noheader`, but which includes population level
information.

.. code-block:: text
   :name: data-hla-microsat
   :caption: Multi-locus allele-level HLA genotype and microsatellite genotype data with header information

   labcode ethnic  complex
   USAFEL  ****    0
   populat    id      drb1_1  drb1_2  dqb1_1  dqb1_2  d6s2222_1  d6s2222_2  
   UchiTelle  HJK_2   01      0301    0201     0501    249        249        
   UchiTelle  HJK_1   0301    0301    0201     0201    249        249        
   UchiTelle  HJK_3   01      0301    0201     0501    249        249        
   UchiTelle  HJK_4   01      0301    0201     0501    249        249        
   UchiTelle  MYU_2   02      0401    0302     0602    247        249        
   UchiTelle  MYU_1   0301    0301    0201     0201    247        249        
   UchiTelle  MYU_3   0301    0401    0201     0302    249        249        
   UchiTelle  MYU_4   0301    0401    0201     0302    247        249

This example mixes different kinds of data: HLA allele data (from DRB1
and DQB1 loci) with microsatellite data (locus D6S2222).

.. code-block:: text
   :name: data-nucleotide
   :caption: Sequence genotype data with header information

   labcode file                                                
   BLOGGS  C_New
   popName ID       TGFB1cdn10(1) TGFB1cdn10(2) TGFBhapl(1) TGFBhapl(2) 
   Urboro  XQ-1     C             T             CG          TG     
   Urboro  XQ-2     C             C             CG          CG     
   Urboro  XQ-5     C             T             CG          TG     
   Urboro  XQ-21    C             T             CG          TG     
   Urboro  XQ-7     C             T             CG          TG     
   Urboro  XQ-20    C             T             CG          TG     
   Urboro  XQ-6     T             T             TG          TG     
   Urboro  XQ-8     C             T             CG          TG     
   Urboro  XQ-9     T             T             TG          TG     
   Urboro  XQ-10    C             T             CG          TG     
     

This example includes nucleotide sequence data: the TGFB1CDN10 locus
consists of one nucleotide, the TGFBhapl locus is actually haplotype
data, but PyPop simply treats each combination as a separate "allele"
for subsequent analysis.

.. code-block:: text
   :name: data-allelecount
   :caption: Allele count data

   populat    method  ethnic     country    latit   longit
   UchiTelle  PCR-SSO Klingon    QZ         052.81N 100.25E
   dqa1  count
   0101  31
   0102  37
   0103  17
   0201  21
   0301  32
   0401  9
   0501  35
     

PyPop can also process allele count data. However, you cannot mix allele
count data and genotype data together in the one file.

.. note::
   :name: data-allelecount-note

   Currently each ``.pop`` file can only contain allele count data for
   *one locus*. In order to process multiple loci for one population you
   must create a separate ``.pop`` for each locus.

These population files are plain text files, such as you might save
out of the :program:`Notepad` application on Windows (or
:program:`Emacs`). The columns are all tab-delimited, so you can
include spaces in your labels. If you have your data in a spreadsheet
application, such as :program:`Excel` or :program:`LibreOffice`, export the file as
tab-delimited text, in order to use it as PyPop data file.

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

.. code-block:: ini
   :name: config-minimal-example
   :caption: Minimal config.ini file
   :emphasize-lines: 1,4,14,17,22,25

   [General]                  
   debug=0            
                  
   [ParseGenotypeFile]        
   untypedAllele=****         
   alleleDesignator=*         
   validSampleFields=*a_1     
    *a_2              
    *c_1              
    *c_2              
    *b_1              
    *b_2              
                  
   [HardyWeinberg]            
   lumpBelow=5                

   [HardyWeinbergGuoThompson] 
   dememorizationSteps=2000
   samplingNum=1000
   samplingSize=1000

   [HomozygosityEWSlatkinExact] 
   numReplicates=10000

   [Emhaplofreq]              
   allPairwiseLD=1
   allPairwiseLDWithPermu=0
   ;;numPermuInitCond=5


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
      `note_title <data-allelecount-note>`__ in
      :numref:`data-allelecount`). Listing multiple loci
      simply permits the same ``.ini`` file to be reused for each data
      file.

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
   [Guo:Thompson:1992]_ code, using a Monte-Carlo Markov chain (MCMC). In
   addition, two measures (Chen and Diff) of the goodness of it of
   individual genotypes are reported under this option [Chen:etal:1999]_
   By default this section is not enabled. This is a different
   implementation to the :program:`Arlequin` version listed in
   :ref:`config-advanced`, below.

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

   The presence of this section enables Slatkin's [Slatkin:1994]_ 
   implementation of the Ewens-Watterson exact test of neutrality.

   -  ``numReplicates``.

      The default values have proved to be optimal for us. There is no
      reason to change them unless you are particularly curious. If you
      change the default values and have problems, please let us know.

-  ``[Emhaplofreq]``

   The presence of this section enables haplotype estimation and
   calculation of linkage disequilibrium (LD) measures.

   -  ``lociToEstHaplo``.

      In this option you can list the multi-locus haplotypes for which
      you wish the program to estimate and to calculate the LD. It
      should be a comma-separated list of colon-joined loci. e.g.,

      .. code-block:: text

         lociToEstHaplo=a:b:drb1,a:b:c,drb1:dqa1:dpb1,drb1:dqb1:dpb1

   -  ``allPairwiseLD``.

      Set this to ``1`` (one) if you want the program to calculate all
      pairwise LD for your data, otherwise set this to ``0`` (zero).

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
      if ``allPairwiseLDWithPermu`` is set and nonzero*).

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
implementation of Guo and Thompson's [Guo:Thompson:1992]_ Hardy-Weinberg
exact test is invoked (see below).

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
   Sequence Format <http://www.ebi.ac.uk/imgt/hla/download.html>`__)
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
    04/05/0306
    !06/1201/1301
    !07/0805

In the example above, ``A*03`` alleles will match to ``01/02/03``,
except for ``A*0306``, which will match to ``04/05/0306``. If you place
a ``!`` mark in front of the first allele name, that first name will be
used as the "new name" for the binned group (for example, ``A*0805``
will be called ``07`` in the custom-binned data.) Note that the space at
the beginning of the lines (following the first line of each locus) is
important. The above rules are just dummy examples, provided to
illustrate how the filter works. PyPop is distributed with a
biologically relevant set of ``CustomBinning`` rules that have been
compiled from several sources [2]_

.. [1]
   These hardcoded numbers can be changed if you obtain the source code
   yourself and change the appropriate #define ``emhaplofreq.h`` and
   recompile the program.

.. [2]
   [Mack:etal:2007]_; [Cano:etal:2007]_; The Anthony Nolan list of deleted
   allele names
   (` <http://www.anthonynolan.com/HIG/lists/delnames.html>`__); and the
   Ambiguous Allele Combinations, release 2.18.0
   (` <http://www.ebi.ac.uk/imgt/hla/ambig.html>`__).