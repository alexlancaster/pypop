# This file is part of PyPop

# Copyright (C) 2003, 2004, 2005, 2006.
# The Regents of the University of California (Regents) All Rights Reserved.

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

r"""Primary access to PyPop's population genetics statistics modules.

This module handles processing :class:`configparser.ConfigParser`
instance.  The :class:`Main` class coordinates running the analysis
packages specified in this :class:`configparser.ConfigParser` instance
which can be:

- created from a filename passed from command-line argument oar;

- from values populated by the GUI (for example,  selected from an
  ``.ini`` file,

- created programmatically as part of an external Python program

Here is an example of calling :class:`Main` programmatically,
explicitly specifying the ``untypedAllele`` and ``alleleDesignator``
in the ``.pop`` file:

.. testsetup::

   >>> import PyPop
   >>> PyPop.setup_logger(doctest_mode=True)

>>> from PyPop.popanalysis import Main
>>> from configparser import ConfigParser
>>>
>>> config = ConfigParser()
>>> config.read_dict({
...     "ParseGenotypeFile": {"untypedAllele": "****",
...                           "alleleDesignator": "*",
...                           "validSampleFields": "*a_1\n*a_2"}})
>>>
>>> pop_contents = '''a_1\ta_2
... ****\t****
... 01:01\t02:01
... 02:10\t03:01:02'''
>>> with open("my.pop", "w") as f:
...     _ = f.write(pop_contents)
...
>>> application = Main(
...     config=config,
...     fileName="my.pop",
...     version="fake",
... )
LOG: no XSL file, skipping text output
LOG: Data file has no header data block

"""

import logging
import os
import sys
import time
from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path

# now use python3-lxml
from lxml import etree

from PyPop import logger, setup_logger
from PyPop.datatypes import Genotypes, getLumpedDataLevels
from PyPop.filters import AnthonyNolanFilter, BinningFilter
from PyPop.haplo import Emhaplofreq, Haplostats
from PyPop.hardyweinberg import (
    HardyWeinberg,
    HardyWeinbergEnumeration,
    HardyWeinbergGuoThompson,
    HardyWeinbergGuoThompsonArlequin,
)
from PyPop.homozygosity import (
    HomozygosityEWSlatkinExact,
    HomozygosityEWSlatkinExactPairwise,
)
from PyPop.parsers import ParseAlleleCountFile, ParseGenotypeFile
from PyPop.randombinning import RandomBinsForHomozygosity
from PyPop.utils import (
    TextOutputStream,
    XMLOutputStream,
    checkXSLFile,
    convertLineEndings,
    critical_exit,
    unique_elements,
)


class Main:
    """Main interface to the PyPop modules.

    Runs the analyses specified in the configuration object provided
    to the ``config`` parameter, and an input ``fileName``, and
    generates an output XML file. The XML output file name, appends
    ``-out.xml`` on to the stem of the provided ``fileName``.  For
    example, if ``fileName="MyPopulation.pop"`` is provided as a
    parameter, the output XML file will be ``MyPopulation-out.xml``.

    .. versionchanged:: 1.4.0

       If an ``xslFilename`` or ``xslFilenameDefault`` is provided,
       also generate a plain text output.  Otherwise no text output is
       generated. Previous to this version, if neither were provided,
       the program would exit with an error.

    Args:
        config (configparser.ConfigParser): configure object
        xslFilename (str, optional): XSLT file to use
        xslFilenameDefault (str, optional): fallback file name
        fileName (str): input ``.pop`` file
        datapath (str, optional): root of data path
        thread (str, optional): specified thread
        outputDir (str, optional): use a different output directory than default
        version (str, optional): current Python version for output
        testMode (bool, optional): enable testing mode

    """

    def __init__(
        self,
        config=None,
        xslFilename=None,
        xslFilenameDefault=None,
        fileName=None,
        datapath=None,
        thread=None,
        outputDir=None,
        version=None,
        testMode=False,
    ):
        self.config = config
        self.fileName = fileName
        self.datapath = datapath
        self.xslFilename = xslFilename
        self.xslFilenameDefault = xslFilenameDefault
        self.outputDir = outputDir
        self.version = version
        self.testMode = testMode

        # for threading to work
        self.thread = thread

        # switch off filtering and random binning by default
        self.filteringFlag = 0
        self.randomBinningFlag = 0

        # parse out the parts of the filename
        baseFileName = Path(self.fileName).name
        prefixFileName = ".".join(baseFileName.split(".")[:-1])

        # generate date and time

        now = time.time()
        datestr = time.strftime("%Y-%m-%d", time.localtime(now))
        timestr = time.strftime("%H-%M-%S", time.localtime(now))

        # Parse "General" section

        try:
            debug_ini_enabled = self.config.getboolean("General", "debug")
        except (NoOptionError, NoSectionError):
            debug_ini_enabled = 0
        except ValueError:
            critical_exit("require a 0 or 1 as debug flag")

        # always first default "debug" to command-line status (set by pypop script)
        # if it is not set by the command-line, then it is by default, disabled, but
        # the config.ini file can enable it, so we override the logger status

        if not logger.isEnabledFor(logging.DEBUG) and debug_ini_enabled == 1:
            # enable debug status, and override current setup
            setup_logger(level=logging.DEBUG)

        # generate file prefix
        try:
            outFilePrefixType = self.config.get("General", "outFilePrefixType")
            if outFilePrefixType == "filename":
                uniquePrefix = prefixFileName
            elif outFilePrefixType == "date":
                uniquePrefix = f"{prefixFileName}-{datestr}-{timestr}"
            else:
                critical_exit(
                    "outFilePrefixType: %s must be 'filename' or 'date'",
                    outFilePrefixType,
                )
        except (NoOptionError, NoSectionError):
            # just use default prefix
            uniquePrefix = prefixFileName

        # generate filenames for both text and XML files

        #
        # start with text filename
        #
        defaultTxtOutFilename = uniquePrefix + "-out.txt"
        try:
            self.txtOutFilename = self.config.get("General", "txtOutFilename")
            if self.txtOutFilename == "":
                self.txtOutFilename = defaultTxtOutFilename
        except (NoOptionError, NoSectionError):
            self.txtOutFilename = defaultTxtOutFilename

        #
        # now XML filename
        #
        defaultXmlOutFilename = uniquePrefix + "-out.xml"
        try:
            self.xmlOutFilename = self.config.get("General", "xmlOutFilename")
            if self.xmlOutFilename == "":
                self.xmlOutFilename = defaultXmlOutFilename
        except (NoOptionError, NoSectionError):
            self.xmlOutFilename = defaultXmlOutFilename

        #
        # generate filename for logging filter output
        #
        self.defaultFilterLogFilename = uniquePrefix + "-filter.xml"

        #
        # generate filename for pop file dump (only used if option is set)
        #
        self.defaultPopDumpFilename = uniquePrefix  # + "-filtered.pop"    FIXME

        # prepend directory to all files if one was supplied
        if self.outputDir:
            [
                self.txtOutPath,
                self.xmlOutPath,
                self.defaultFilterLogPath,
                self.defaultPopDumpPath,
            ] = [
                Path(self.outputDir) / x
                for x in [
                    self.txtOutFilename,
                    self.xmlOutFilename,
                    self.defaultFilterLogFilename,
                    self.defaultPopDumpFilename,
                ]
            ]
        else:
            self.txtOutPath = self.txtOutFilename
            self.xmlOutPath = self.xmlOutFilename
            self.defaultFilterLogPath = self.defaultFilterLogFilename
            self.defaultPopDumpPath = self.defaultPopDumpFilename

        if logger.isEnabledFor(logging.DEBUG):
            for section in self.config.sections():
                logger.debug(section)
                for option in self.config.options(section):
                    logger.debug(f" {option}={self.config.get(section, option)}")

        # if not provided on command line or provided check .ini
        # options, and use that location, if provided
        if self.xslFilename is None:
            try:
                self.xslFilename = self.config.get("General", "xslFilename")
                logger.debug("using .ini option for xslFilename: %s", self.xslFilename)
                checkXSLFile(
                    self.xslFilename,
                    abort=1,
                    msg="specified in .ini file",
                )
            except (NoOptionError, NoSectionError):
                # otherwise fall back to xslFilenameDefault
                logger.debug("xslFilename .ini option not set")
                if self.xslFilenameDefault:
                    self.xslFilename = self.xslFilenameDefault
                else:
                    # if no default XSL file found, then we skip text output
                    logger.info("no XSL file, skipping text output")

        logger.debug(f"using user supplied version in: {self.xslFilename}")

        # check to see what kind of file we are parsing

        if self.config.has_section("ParseGenotypeFile"):
            self.fileType = "ParseGenotypeFile"
        elif self.config.has_section("ParseAlleleCountFile"):
            self.fileType = "ParseAlleleCountFile"
        else:
            critical_exit("File type is not recognised.  Exiting")

        # Parse self.fileType section

        # do fields common to both types of files
        try:
            validPopFields = self.config.get(self.fileType, "validPopFields")
        except NoOptionError:
            validPopFields = None
            logger.info("Data file has no header data block")
            # print("LOG: Data file has no header data block")
            # critical_exit("No valid population fields defined")

        try:
            validSampleFields = self.config.get(self.fileType, "validSampleFields")
        except NoOptionError:
            critical_exit("No valid sample fields defined")

        try:
            self.alleleDesignator = self.config.get(self.fileType, "alleleDesignator")
        except NoOptionError:
            self.alleleDesignator = "*"

        try:
            self.untypedAllele = self.config.get(self.fileType, "untypedAllele")
        except NoOptionError:
            self.untypedAllele = "****"

        ## add an empty unsequencedSite variable
        self.unsequencedSite = None

        # BEGIN PARSE for a genotype file (ParseGenotypeFile)
        if self.fileType == "ParseGenotypeFile":
            try:
                popNameDesignator = self.config.get(self.fileType, "popNameDesignator")
            except NoOptionError:
                popNameDesignator = "+"

            try:
                fieldPairDesignator = self.config.get(
                    self.fileType, "fieldPairDesignator"
                )
            except NoOptionError:
                fieldPairDesignator = "_1:_2"

            # Generate the parse file object, which simply creates
            # a matrix (no allele count stuff done!)
            self.parsed = ParseGenotypeFile(
                self.fileName,
                validPopFields=validPopFields,
                validSampleFields=validSampleFields,
                alleleDesignator=self.alleleDesignator,
                untypedAllele=self.untypedAllele,
                popNameDesignator=popNameDesignator,
                fieldPairDesignator=fieldPairDesignator,
            )

            # if we are dealing with data that is originally genotyped
            # we dis-allow individuals that are typed at only allele
            allowSemiTyped = 0

        # END PARSE for a genotype file (ParseGenotypeFile)

        # BEGIN PARSE: allelecount file (ParseAlleleCountFile)
        elif self.fileType == "ParseAlleleCountFile":
            # Generate the parse file object
            self.parsed = ParseAlleleCountFile(
                self.fileName,
                validPopFields=validPopFields,
                validSampleFields=validSampleFields,
                separator="\t",
            )

            # if we are dealing with data that is originally simply
            # allele count data, we allow for typing at only allele
            # because the matrix is not a true set of individuals, and
            # it allows us to preserve as much data as possible
            allowSemiTyped = 1

        # END PARSE: allelecount file (ParseAlleleCountFile)

        else:
            critical_exit("Unrecognised file type")

        # we copy the parsed data to self.filtered, to be ready for
        # the gamut of filters coming
        self.matrixHistory = []
        self.matrixHistory.append(self.parsed.getMatrix().copy())

        # figure out what filters we will be using, if any
        if self.config.has_section("Filters"):
            try:
                self.filtersToApply = self.config.get("Filters", "filtersToApply")
                self.filtersToApply = self.filtersToApply.split(":")
            except NoOptionError:
                self.filtersToApply = []
            try:
                self.popDump = self.config.get("Filters", "makeNewPopFile")
                self.dumpType, self.dumpOrder = self.popDump.split(":")

                if self.dumpType in ["separate-loci", "all-loci"]:
                    self.dumpOrder = int(self.dumpOrder)
                else:
                    critical_exit(
                        "%s is not a valid keyword for population dump: must be either 'separate-loci' or 'all-loci'",
                        self.dumpType,
                    )

            except NoOptionError:
                self.popDump = 0

            # this allows the user to have "filtersToApply=" without ill consequences
            if len(self.filtersToApply) > 0 and len(self.filtersToApply[0]) > 0:
                # get filtering options and open log file for
                # filter in append mode

                # FIXME: need a better way that uses context manager
                self.filterLogFile = XMLOutputStream(
                    open(self.defaultFilterLogPath, "w")  # noqa: SIM115
                )

                if self.testMode:
                    self.filterLogFile.opentag(
                        "filterlog"
                    )  # don't write path in test mode
                else:
                    self.filterLogFile.opentag("filterlog", filename=self.fileName)
                self.filterLogFile.writeln()
                self.filteringFlag = 1

                # run the filtering gamut
                self._runFilters()

        # now convert into DataType: and then we pass the filtered
        # matrix to be put in format for rest of processing

        self.input = Genotypes(
            matrix=self.matrixHistory[-1],
            untypedAllele=self.untypedAllele,
            unsequencedSite=self.unsequencedSite,
            allowSemiTyped=allowSemiTyped,
        )

        # BEGIN common XML output section

        # create XML stream
        # FIXME: need a better way that uses context manager
        self.xmlStream = XMLOutputStream(open(self.xmlOutPath, "w"))  # noqa: SIM115

        # opening tag, don't include date if running in test mode
        if not (testMode):
            self.xmlStream.opentag(
                'dataanalysis xmlns:xi="http://www.w3.org/2001/XInclude"',
                date=f"{datestr}-{timestr}",
                role=self.fileType,
            )
        else:
            self.xmlStream.opentag(
                'dataanalysis xmlns:xi="http://www.w3.org/2001/XInclude"',
                date="",
                role=self.fileType,
            )
        self.xmlStream.writeln()

        # if and only if filtering is done, generate XInclude XML
        # file output reference, to include
        # <popfilename>-filter.log
        if self.filteringFlag:
            self.xmlStream.opentag(
                "xi:include", href=self.defaultFilterLogFilename, parse="xml"
            )
            self.xmlStream.writeln()
            self.xmlStream.emptytag("xi:fallback")
            self.xmlStream.writeln()
            self.xmlStream.closetag("xi:include")
            self.xmlStream.writeln()

        # more meta-data
        self.xmlStream.tagContents("filename", baseFileName)
        self.xmlStream.writeln()
        self.xmlStream.tagContents("pypop-version", self.version)
        self.xmlStream.writeln()

        # serialize summary info for population in XML (common)
        self.parsed.serializeMetadataTo(self.xmlStream)

        # serialize the specific information for kind of file
        self.input.serializeSubclassMetadataTo(self.xmlStream)

        # process the file depending on type
        if self.fileType in ("ParseAlleleCountFile", "ParseGenotypeFile"):
            self._doGenotypeFile()
        else:
            pass

        # now close the filter log file, if and only if we have done
        # some kind of filtering, moving it here, means that the open
        # and close are at the same level and are called in the same
        # method.
        if self.filteringFlag:
            self.filterLogFile.closetag("filterlog")
            self.filterLogFile.close()

        # END common XML output section

        # closing tag
        self.xmlStream.closetag("dataanalysis")
        # close XML stream
        self.xmlStream.close()

        # lastly, generate the text output if XSL file was specified,
        # otherwise skip text output generation
        if self.xslFilename:
            self._genTextOutput()

    def _checkMSFOptions(self, filterCall):
        try:
            directory = self.config.get(filterCall, "directory", fallback=None)
            remoteMSF = self.config.get(filterCall, "remoteMSF", fallback=None)

            if not (directory or remoteMSF):
                # neither option is provided
                critical_exit(
                    "You must provide either a 'directory' or a 'remoteMSF' option in the [Sequence] config."
                )
            if directory and remoteMSF:
                # both options are provided
                critical_exit(
                    "'directory' and 'remoteMSF' options are mutually exclusive. Provide only one in [Sequence] config."
                )
            # process the options
            if directory:
                anthonynolanPath = get_sequence_directory(directory)
                remoteMSF = None
            else:
                anthonynolanPath = None
        except Exception as e:
            critical_exit("Error parsing the configuration: %s", e)

        return anthonynolanPath, remoteMSF

    def _runFilters(self):
        if self.config.has_section("RandomAlleleBinning"):
            try:
                self.binningMethod = self.config.get(
                    "RandomAlleleBinning", "binningMethod"
                )
            except Exception:
                self.binningMethod = "random"
            try:
                self.binningStartPoint = self.config.getint(
                    "RandomAlleleBinning", "binningStartPoint"
                )
            except Exception:
                self.binningStartPoint = 0
            try:
                self.binningReplicates = self.config.getint(
                    "RandomAlleleBinning", "binningReplicates"
                )
            except NoOptionError:
                self.binningReplicates = 10000
            try:
                self.binningLoci = self.config.get("RandomAlleleBinning", "binningLoci")
                self.binningLoci = self.binningLoci.split(",")
            except Exception:
                self.binningLoci = []
            if len(self.binningLoci) > 0:
                self.randomBinningFlag = 1

        for filterCall in self.filtersToApply:
            if filterCall in (
                "AnthonyNolan",
                "DigitBinning",
                "CustomBinning",
                "Sequence",
            ):
                filterType = filterCall
            else:
                try:
                    filterType = self.config.get(filterCall, "filterType")
                except Exception:
                    critical_exit(
                        "No valid filter type specified under filter heading %s",
                        filterCall,
                    )

            if filterType == "AnthonyNolan":
                anthonynolanPath, remoteMSF = self._checkMSFOptions(filterCall)

                try:
                    alleleFileFormat = self.config.get(filterCall, "alleleFileFormat")
                except Exception:
                    alleleFileFormat = "msf"
                try:
                    preserveAmbiguousFlag = self.config.getint(
                        filterCall, "preserve-ambiguous"
                    )
                except Exception:
                    preserveAmbiguousFlag = 0
                try:
                    preserveUnknownFlag = self.config.getint(
                        filterCall, "preserve-unknown"
                    )
                except Exception:
                    preserveUnknownFlag = 0
                try:
                    preserveLowresFlag = self.config.getint(
                        filterCall, "preserve-lowres"
                    )
                except Exception:
                    preserveLowresFlag = 0

                filter = AnthonyNolanFilter(
                    directoryName=anthonynolanPath,
                    remoteMSF=remoteMSF,
                    alleleFileFormat=alleleFileFormat,
                    preserveAmbiguousFlag=preserveAmbiguousFlag,
                    preserveUnknownFlag=preserveUnknownFlag,
                    preserveLowresFlag=preserveLowresFlag,
                    alleleDesignator=self.alleleDesignator,
                    untypedAllele=self.untypedAllele,
                    filename=self.fileName,
                    logFile=self.filterLogFile,
                )
                self.matrixHistory.append(
                    filter.doFiltering((self.matrixHistory[-1]).copy())
                )

            elif filterType == "DigitBinning":
                try:
                    binningDigits = self.config.getint(filterCall, "binningDigits")
                except Exception:
                    binningDigits = 4

                filter = BinningFilter(
                    binningDigits=binningDigits,
                    untypedAllele=self.untypedAllele,
                    filename=self.fileName,
                    logFile=self.filterLogFile,
                )
                self.matrixHistory.append(
                    filter.doDigitBinning((self.matrixHistory[-1]).copy())
                )

            elif filterType == "CustomBinning":
                customBinningDict = {}
                try:
                    for option in self.config.options(filterCall):
                        customBinningDict[option] = (
                            self.config.get(filterCall, option)
                        ).split()
                        logger.debug("customBinningDict: %s", str(customBinningDict))
                except Exception:
                    critical_exit("Could not parse the CustomBinning rules.")

                filter = BinningFilter(
                    customBinningDict=customBinningDict,
                    untypedAllele=self.untypedAllele,
                    filename=self.fileName,
                    logFile=self.filterLogFile,
                )
                self.matrixHistory.append(
                    filter.doCustomBinning((self.matrixHistory[-1]).copy())
                )

            elif filterType == "Sequence":
                ## set the unsequencedSite
                ## FIXME: do more sanity checking make sure different symbol from untypedAllele
                try:
                    self.unsequencedSite = self.config.get(
                        filterCall, "unsequencedSite"
                    )
                except Exception:
                    self.unsequencedSite = "#"
                try:
                    sequenceFileSuffix = self.config.get(
                        filterCall, "sequenceFileSuffix"
                    )
                except Exception:
                    sequenceFileSuffix = "_prot"

                try:
                    sequenceFilterMethod = self.config.get(
                        filterCall, "sequenceConsensusMethod"
                    )
                    if sequenceFilterMethod != "greedy":
                        sequenceFilterMethod = "strict-default"
                except Exception:
                    sequenceFilterMethod = "strict-default"

                anthonynolanPath, remoteMSF = self._checkMSFOptions(filterCall)

                filter = AnthonyNolanFilter(
                    directoryName=anthonynolanPath,
                    remoteMSF=remoteMSF,
                    alleleFileFormat="msf",
                    alleleDesignator=self.alleleDesignator,
                    sequenceFileSuffix=sequenceFileSuffix,
                    untypedAllele=self.untypedAllele,
                    unsequencedSite=self.unsequencedSite,
                    filename=self.fileName,
                    logFile=self.filterLogFile,
                    sequenceFilterMethod=sequenceFilterMethod,
                )
                self.matrixHistory.append(
                    filter.translateMatrix((self.matrixHistory[-1]).copy())
                )

            else:
                critical_exit(
                    "The filter type '%s' specified under filter heading '%s' is not recognized.",
                    filterType,
                    filterCall,
                )

        logger.debug("matrixHistory ...")
        logger.debug(f"{self.matrixHistory} ...")

        # outputs pop file(s)
        if self.popDump:
            # FIXME: keep in case we want to output on the loci before
            # split using, for example, a Sequence filter
            originalMatrix = self.matrixHistory[0]  # noqa: F841

            if self.dumpType == "separate-loci":
                for locus in self.matrixHistory[self.dumpOrder].colList:
                    popDumpPath = (
                        self.defaultPopDumpPath + "-" + locus + "-filtered.pop"
                    )
                    dumpFile = TextOutputStream(open(popDumpPath, "w"))  # noqa: SIM115
                    dumpMatrix = self.matrixHistory[self.dumpOrder]
                    dumpMatrix.dump(locus=locus, stream=dumpFile)
                    dumpFile.close()
            elif self.dumpType == "all-loci":
                popDumpPath = self.defaultPopDumpPath + "-filtered.pop"
                # FIXME: need a better way that uses context manager
                dumpFile = TextOutputStream(open(popDumpPath, "w"))  # noqa: SIM115
                dumpMatrix = self.matrixHistory[self.dumpOrder]
                dumpMatrix.dump(stream=dumpFile)
                dumpFile.close()

    def _doGenotypeFile(self):
        loci = self.input.getLocusList()

        for locus in loci:
            self.xmlStream.opentag("locus", name=locus)
            self.xmlStream.writeln()

            self.input.serializeAlleleCountDataAt(self.xmlStream, locus)

            # check to see if given locus is monomorphic and skip the
            # rest of the analysis for this particular if it is.
            alleleTable, _totalAlleles, _untypedIndividuals, _unsequencedIndividuals = (
                self.input.getAlleleCountAt(locus)
            )
            numDistinctAlleles = len(alleleTable.keys())

            if numDistinctAlleles == 1:
                # emit closing tags and go to the next locus
                self.xmlStream.closetag("locus")
                self.xmlStream.writeln()
                continue

            # Parse [HardyWeinberg] sections

            # HardyWeinberg sections only makes sense for true genotype
            # files, so skip to the next section if not a genotype file

            if (
                self.config.has_section("HardyWeinberg")
                and len(self.config.options("HardyWeinberg")) > 0
                and self.fileType == "ParseGenotypeFile"
            ):
                try:
                    lumpBelow = self.config.getint("HardyWeinberg", "lumpBelow")
                except NoOptionError:
                    lumpBelow = 5
                except ValueError:
                    critical_exit("require integer value")

                try:
                    flagChenTest = self.config.getboolean("HardyWeinberg", "chenChisq")
                except NoOptionError:
                    flagChenTest = 0
                except ValueError:
                    critical_exit("require a 0 or 1 as a Boolean flag")

                hwObject = HardyWeinberg(
                    self.input.getLocusDataAt(locus),
                    self.input.getAlleleCountAt(locus),
                    lumpBelow=lumpBelow,
                    flagChenTest=flagChenTest,
                )

                # serialize HardyWeinberg
                hwObject.serializeTo(self.xmlStream)

                try:
                    alleleLump = self.config.get("HardyWeinberg", "alleleLump")
                    li = [int(i) for i in alleleLump.split(",")]
                    lumpData = getLumpedDataLevels(self.input, locus, li)

                    for level in lumpData:
                        locusData, alleleData = lumpData[level]
                        hwObjectLump = HardyWeinberg(
                            locusData,
                            alleleData,
                            lumpBelow=lumpBelow,
                        )

                        # serialize HardyWeinberg
                        hwObjectLump.serializeTo(self.xmlStream, allelelump=level)

                except NoOptionError:
                    pass
                except ValueError:
                    critical_exit(
                        "alleleLump: require comma-separated list of integers"
                    )

            # Parse "HardyWeinbergGuoThompson"
            if (
                self.config.has_section("HardyWeinbergGuoThompson")
                and len(self.config.options("HardyWeinbergGuoThompson")) > 0
            ):
                runMCMCTest = 1
            else:
                runMCMCTest = 0

            # Parse "HardyWeinbergGuoThompsonMonteCarlo"
            if (
                self.config.has_section("HardyWeinbergGuoThompsonMonteCarlo")
                and len(self.config.options("HardyWeinbergGuoThompsonMonteCarlo")) > 0
            ):
                runPlainMCTest = 1
            else:
                runPlainMCTest = 0

            # deal with these sections in one call to module, because data
            # structures are identical
            if runMCMCTest or runPlainMCTest:
                try:
                    dememorizationSteps = self.config.getint(
                        "HardyWeinbergGuoThompson", "dememorizationSteps"
                    )
                except (NoOptionError, NoSectionError):
                    dememorizationSteps = 2000
                except ValueError:
                    critical_exit("require integer value")

                try:
                    samplingNum = self.config.getint(
                        "HardyWeinbergGuoThompson", "samplingNum"
                    )
                except (NoOptionError, NoSectionError):
                    samplingNum = 1000
                except ValueError:
                    critical_exit("require integer value")

                try:
                    samplingSize = self.config.getint(
                        "HardyWeinbergGuoThompson", "samplingSize"
                    )
                except (NoOptionError, NoSectionError):
                    samplingSize = 1000
                except ValueError:
                    critical_exit("require integer value")

                try:
                    maxMatrixSize = self.config.getint(
                        "HardyWeinbergGuoThompson", "maxMatrixSize"
                    )
                except (NoOptionError, NoSectionError):
                    maxMatrixSize = 250
                except ValueError:
                    critical_exit("require integer value")

                try:
                    monteCarloSteps = self.config.getint(
                        "HardyWeinbergGuoThompsonMonteCarlo", "monteCarloSteps"
                    )
                except (NoOptionError, NoSectionError):
                    monteCarloSteps = 1000000
                except ValueError:
                    critical_exit("require integer value")

                # Guo & Thompson implementation
                hwObject = HardyWeinbergGuoThompson(
                    locusData=self.input.getLocusDataAt(locus),
                    alleleCount=self.input.getAlleleCountAt(locus),
                    runMCMCTest=runMCMCTest,
                    runPlainMCTest=runPlainMCTest,
                    dememorizationSteps=dememorizationSteps,
                    samplingNum=samplingNum,
                    samplingSize=samplingSize,
                    maxMatrixSize=maxMatrixSize,
                    monteCarloSteps=monteCarloSteps,
                    testing=self.testMode,
                )

                hwObject.dumpTable(locus, self.xmlStream)
                self.xmlStream.writeln()

                try:
                    alleleLump1 = self.config.get(
                        "HardyWeinbergGuoThompson", "alleleLump"
                    )
                except (NoOptionError, NoSectionError):
                    alleleLump1 = 0

                try:
                    alleleLump2 = self.config.get(
                        "HardyWeinbergGuoThompsonMonteCarlo", "alleleLump"
                    )
                except (NoOptionError, NoSectionError):
                    alleleLump2 = 0

                if alleleLump1 or alleleLump2:
                    try:
                        ## get the unique maximal number of possible lumpings
                        if alleleLump1:
                            li1 = [int(i) for i in alleleLump1.split(",")]
                        else:
                            li1 = []
                        if alleleLump2:
                            li2 = [int(i) for i in alleleLump2.split(",")]
                        else:
                            li2 = []
                            li1.extend(li2)
                            li = unique_elements(li1)

                        lumpData = getLumpedDataLevels(self.input, locus, li)
                        for level in lumpData:
                            locusData, alleleData = lumpData[level]

                            hwObjectLump = HardyWeinbergGuoThompson(
                                locusData=locusData,
                                alleleCount=alleleData,
                                runMCMCTest=runMCMCTest,
                                runPlainMCTest=runPlainMCTest,
                                dememorizationSteps=dememorizationSteps,
                                samplingNum=samplingNum,
                                samplingSize=samplingSize,
                                maxMatrixSize=maxMatrixSize,
                                monteCarloSteps=monteCarloSteps,
                                testing=self.testMode,
                            )

                            # serialize HardyWeinberg
                            hwObjectLump.dumpTable(
                                locus, self.xmlStream, allelelump=level
                            )
                            self.xmlStream.writeln()

                    except ValueError:
                        critical_exit(
                            "alleleLump: require comma-separated list of integers"
                        )

            # FIXME: need a way to disable if too many
            # alleles/individuals in a given population.
            if self.config.has_section("HardyWeinbergEnumeration"):
                # by default only to individual genotype enumeration
                # p-values, which is feasible because it only does 3x3
                # tables

                try:
                    doOverall = self.config.getboolean(
                        "HardyWeinbergEnumeration", "doOverall"
                    )
                except NoOptionError:
                    doOverall = 0
                except ValueError:
                    critical_exit("doOverall: requires 0 or 1 as a boolean flag")

                hwEnum = HardyWeinbergEnumeration(
                    locusData=self.input.getLocusDataAt(locus),
                    alleleCount=self.input.getAlleleCountAt(locus),
                    doOverall=doOverall,
                )

                hwEnum.serializeTo(self.xmlStream)

                try:
                    alleleLump = self.config.get(
                        "HardyWeinbergEnumeration", "alleleLump"
                    )
                    li = [int(i) for i in alleleLump.split(",")]
                    lumpData = getLumpedDataLevels(self.input, locus, li)

                    for level in lumpData:
                        locusData, alleleData = lumpData[level]

                        hwEnumLump = HardyWeinbergEnumeration(
                            locusData=locusData,
                            alleleCount=alleleData,
                            doOverall=doOverall,
                        )

                        # serialize HardyWeinberg
                        hwEnumLump.serializeTo(self.xmlStream, allelelump=level)

                except NoOptionError:
                    pass
                except ValueError:
                    critical_exit(
                        "alleleLump: require comma-separated list of integers"
                    )

            if self.config.has_section("HardyWeinbergGuoThompsonArlequin"):
                # default location for Arlequin executable
                arlequinExec = "arlecore.exe"

                if self.config.has_section("Arlequin"):
                    try:
                        arlequinExec = self.config.get("Arlequin", "arlequinExec")
                    except NoOptionError:
                        logger.info(
                            "Location to Arlequin executable file not given: assume `arlecore.exe' is in user's PATH"
                        )
                        # print(
                        #    "LOG: Location to Arlequin executable file not given: assume `arlecore.exe' is in user's PATH"
                        # )

                try:
                    markovChainStepsHW = self.config.getint(
                        "HardyWeinbergGuoThompsonArlequin", "markovChainStepsHW"
                    )
                except NoOptionError:
                    samplingNum = 100000
                except ValueError:
                    critical_exit("require integer value")

                try:
                    markovChainDememorisationStepsHW = self.config.getint(
                        "HardyWeinbergGuoThompsonArlequin",
                        "markovChainDememorisationStepsHW",
                    )
                except NoOptionError:
                    samplingNum = 100000
                except ValueError:
                    critical_exit("require integer value")

                hwArlequin = HardyWeinbergGuoThompsonArlequin(
                    self.input.getIndividualsData(),
                    locusName=locus,
                    arlequinExec=arlequinExec,
                    markovChainStepsHW=markovChainStepsHW,
                    markovChainDememorisationStepsHW=markovChainDememorisationStepsHW,
                    untypedAllele=self.untypedAllele,
                )
                hwArlequin.serializeTo(self.xmlStream)

            # parse [HomozygosityEWSlatkinExact] section: this makes
            # sense for both genotype *and* allele count data.

            if self.config.has_section("HomozygosityEWSlatkinExact"):
                try:
                    numReplicates = self.config.getint(
                        "HomozygosityEWSlatkinExact", "numReplicates"
                    )
                except NoOptionError:
                    numReplicates = 10000

                # make a dictionary of allele counts (don't need the last
                # two elements that are returned by this method)
                alleleCounts = self.input.getAlleleCountAt(locus)[0]

                # notice we pass just the alleleCount values.  But the
                # dictionary is still useful to have in case we have to do
                # random binning.
                hzExactObj = HomozygosityEWSlatkinExact(
                    alleleCounts.values(),
                    numReplicates=numReplicates,
                )

                hzExactObj.serializeHomozygosityTo(self.xmlStream)

                # random binning for the homozygosity test begins here
                if self.randomBinningFlag and locus in map(str.upper, self.binningLoci):
                    inputInitial = Genotypes(
                        matrix=self.matrixHistory[self.binningStartPoint],
                        untypedAllele=self.untypedAllele,
                    )

                    # as above, we create a dictionary of allele counts
                    # (made from the correct position in the
                    # matrixHistory)
                    alleleCountsInitial = inputInitial.getAlleleCountAt(locus)[0]

                    logger.debug(
                        "alleleCountsInitial %d %s",
                        len(alleleCountsInitial),
                        alleleCountsInitial,
                    )
                    logger.debug("alleleCounts %d %s", len(alleleCounts), alleleCounts)

                    randomResultsFileName = (
                        self.defaultFilterLogPath[:-4] + "-" + locus + "-randomized.tsv"
                    )

                    self.filterLogFile.opentag(
                        self.binningMethod + "Method", locus=locus
                    )
                    self.filterLogFile.writeln("<![CDATA[")

                    if len(alleleCountsInitial) <= len(alleleCounts):
                        print(
                            f"FilterLog: Locus {locus}: Initial unique allele count is not bigger than the target count; skipping random binning."
                        )
                        self.filterLogFile.writeln(
                            f"Locus {locus}: Initial unique allele count is not bigger than the target count; skipping random binning."
                        )

                    else:
                        # go ahead and do the random binning
                        randObj = RandomBinsForHomozygosity(
                            untypedAllele=self.untypedAllele,
                            filename=self.fileName,
                            numReplicates=numReplicates,
                            binningReplicates=self.binningReplicates,
                            locus=locus,
                            xmlfile=self.xmlStream,
                            logFile=self.filterLogFile,
                            randomResultsFileName=randomResultsFileName,
                        )

                        if self.binningMethod == "random":
                            randObj.randomMethod(
                                alleleCountsBefore=alleleCountsInitial,
                                alleleCountsAfter=alleleCounts,
                            )

                        elif self.binningMethod == "sequence":
                            try:
                                sequenceFileSuffix = self.config.get(
                                    "Sequence", "sequenceFileSuffix"
                                )
                            except Exception:
                                sequenceFileSuffix = "_nuc"
                            try:
                                anthonynolanPath = self.config.get(
                                    "Sequence", "directory"
                                )
                            except Exception:
                                anthonynolanPath = (
                                    Path(self.datapath) / "anthonynolan" / "msf"
                                )
                                logger.debug(
                                    "Defaulting to system datapath %s for anthonynolanPath data",
                                    anthonynolanPath,
                                )

                            seqfilter = AnthonyNolanFilter(
                                directoryName=anthonynolanPath,
                                alleleFileFormat="msf",
                                alleleDesignator=self.alleleDesignator,
                                sequenceFileSuffix=sequenceFileSuffix,
                                untypedAllele=self.untypedAllele,
                                filename=self.fileName,
                                logFile=self.filterLogFile,
                            )

                            polyseq, polyseqpos = seqfilter.makeSeqDictionaries(
                                matrix=(
                                    self.matrixHistory[self.binningStartPoint]
                                ).copy(),
                                locus=locus,
                            )

                            randObj.sequenceMethod(
                                alleleCountsBefore=alleleCountsInitial,
                                alleleCountsAfter=alleleCounts,
                                polyseq=polyseq,
                                polyseqpos=polyseqpos,
                            )

                        else:
                            critical_exit(
                                "Random binning method not recognized: %s",
                                self.binningMethod,
                            )

                    self.filterLogFile.writeln("]]>")
                    self.filterLogFile.closetag(self.binningMethod + "Method")
                    self.filterLogFile.writeln()

            self.xmlStream.closetag("locus")
            self.xmlStream.writeln()

        # Do pairwise Ewens-Watterson test

        if self.config.has_section("HomozygosityEWSlatkinExactPairwise"):
            hz = HomozygosityEWSlatkinExactPairwise(
                matrix=self.input.getIndividualsData(),
                numReplicates=numReplicates,
                untypedAllele=self.untypedAllele,
            )
            hz.serializeTo(self.xmlStream)

        # Parse [Haplostats] section to estimate haplotypes and LD
        # skip if not a genotype file, only makes sense for genotype
        # files.

        if self.config.has_section("Haplostats"):
            print(
                "WARNING: The [Haplostats] module is still currently in ALPHA-MODE ONLY and and should not be used in production."
            )
            print("Please use the [Emhaplofreq] module in the meantime.")

            try:
                numInitCond = self.config.getint("Haplostats", "numInitCond")
            except NoOptionError:
                numInitCond = 10
            except ValueError:
                critical_exit(
                    "numInitCond: option requires an positive integer greater than 1"
                )

            # set all the control parameters
            # FIXME: possibly move this into the .ini file eventually?
            control = {
                "max_iter": 5000,
                "min_posterior": 0.000000001,
                "tol": 0.00001,
                "insert_batch_size": 2,
                "random_start": 0,
                "verbose": 0,
                "max_haps_limit": 10000,
            }

            # FIXME: currently this assumes that geno StringMatrix contains only the loci required
            # need to make sure that this works with subMatrices
            haplostats = Haplostats(
                self.input.getIndividualsData(),
                untypedAllele=self.untypedAllele,
                stream=self.xmlStream,
                testMode=self.testMode,
            )

            # start by serializing the start of the XML block
            haplostats.serializeStart()

            try:
                locusKeys = self.config.get("Haplostats", "lociToEstHaplo")
            except NoOptionError:
                # or if no option given, use wildcard, which assumes all loci
                locusKeys = "*"

            # do haplotype (and LD if two locus) estimation
            haplostats.estHaplotypes(
                locusKeys=locusKeys,
                weight=None,
                control=control,
                numInitCond=numInitCond,
            )

            try:
                allPairwise = self.config.getboolean("Haplostats", "allPairwise")
            except NoOptionError:
                allPairwise = 0
            except ValueError:
                critical_exit("require a 0 or 1 as a flag")

            if allPairwise:
                # do all pairwise statistics, which always includes LD
                haplostats.allPairwise(
                    weight=None, control=control, numInitCond=numInitCond
                )

            # serialize end to XML
            haplostats.serializeEnd()

        # Parse [Emhaplofreq] section to estimate haplotypes and LD
        # skip if not a genotype file, only makes sense for genotype
        # files.

        if self.config.has_section("Emhaplofreq"):
            # create object to generate haplotype and LD statistics
            # a wrapper around the emhaplofreq module
            haplo = Emhaplofreq(
                self.input.getIndividualsData(),
                untypedAllele=self.untypedAllele,
                stream=self.xmlStream,
                testMode=self.testMode,
            )

            # before running emhaplofreq, flush the current buffered
            # output to file
            self.xmlStream.flush()

            # start by serializing the start of the XML block
            haplo.serializeStart()

            try:
                allPairwiseLD = self.config.getboolean("Emhaplofreq", "allPairwiseLD")
            except NoOptionError:
                allPairwiseLD = 0
            except ValueError:
                critical_exit("require a 0 or 1 as a flag")

            try:
                allPairwiseLDWithPermu = self.config.getint(
                    "Emhaplofreq", "allPairwiseLDWithPermu"
                )
            except NoOptionError:
                allPairwiseLDWithPermu = 0
            except ValueError:
                critical_exit("allPairwiseLDWithPermu: option requires an integer")

            # FIXME: needed for backwards-compatibility, remove when not
            # needed
            if allPairwiseLDWithPermu == 1:
                critical_exit("""semantics of 'allPairwiseLDWithPerm' option have changed.
It is no longer a boolean variable to enable the permutation test.
It should now contain the NUMBER of permutations desired.  A value of
at least 1000 is recommended.  A value of '1' is not permitted.""")

            try:
                numPermuInitCond = self.config.getint("Emhaplofreq", "numPermuInitCond")
            except NoOptionError:
                numPermuInitCond = 5
            except ValueError:
                critical_exit("numPermuInitCond: option requires an integer")

            # Parse new [Emhaplofreq] option 'numInitCond', so that the
            # number of initial conditions for the *first* iteration LD
            # calculation (and therefore haplotype estimation) is
            # user-configurable.  Default to 50.
            try:
                numInitCond = self.config.getint("Emhaplofreq", "numInitCond")
            except NoOptionError:
                numInitCond = 50
            except ValueError:
                critical_exit("numInitCond: option requires an integer")

            try:
                permutationPrintFlag = self.config.getboolean(
                    "Emhaplofreq", "permutationPrintFlag"
                )
            except NoOptionError:
                permutationPrintFlag = 0
            except ValueError:
                critical_exit("permutationPrintFlag: option requires a 0 or 1 flag")

            if allPairwiseLD:
                logger.info("estimating all pairwise LD ...")
                # (print("LOG: estimating all pairwise LD:", end=" "),)
                if allPairwiseLDWithPermu:
                    (
                        logger.info(
                            f"... with {allPairwiseLDWithPermu} permutations and {numPermuInitCond} initial conditions for each permutation",
                        ),
                    )
                    if permutationPrintFlag:
                        logger.info(
                            "... and each permutation output will be logged to XML"
                        )
                    else:
                        logger.info("")
                else:
                    logger.info("... with no permutation test")

            # first set the list of 2-locus haplotypes to show to empty
            twoLocusHaplosToShow = []

            try:
                locusKeys = self.config.get("Emhaplofreq", "lociToEstHaplo")

                if locusKeys == "*":
                    logger.info(
                        "wildcard '*' given for lociToEstHaplo, assume entire data set"
                    )
                    locusKeys = ":".join(self.input.getIndividualsData().colList)
                    # (print("LOG: estimating haplotype frequencies for", end=" "),)
                logger.info("estimating haplotype frequencies for ...")
                # if we will be running allPairwise*, then exclude any two-locus
                # haplotypes, since we will estimate them as part of 'all pairwise'
                if allPairwiseLD:
                    # (print("all two locus haplotypes,", end=" "),)
                    logger.info("... all two locus haplotypes")
                    modLocusKeys = []
                    for group in locusKeys.split(","):
                        # if a two-locus haplo, add it to the list that allPairwise
                        # will use
                        if len(group.split(":")) == 2:
                            twoLocusHaplosToShow.append(group.upper())

                        # otherwise add it to the regular output
                        else:
                            modLocusKeys.append(group)

                    locusKeys = ",".join(modLocusKeys)

                # estimate haplotypes on set of locusKeys *only* if there are
                # locus groups that remain after excluding two locus haplotypes
                if locusKeys:
                    haplo.estHaplotypes(locusKeys=locusKeys, numInitCond=numInitCond)
                    # print(f"specific haplotypes: [{locusKeys}]")
                    logger.info(f"... specific haplotypes: [{locusKeys}]")

            except NoOptionError:
                pass

            try:
                locusKeysLD = self.config.get("Emhaplofreq", "lociToEstLD")

                if locusKeysLD == "*":
                    logger.info(
                        "wildcard '*' given for lociToEstLD, assume entire data set"
                    )
                    locusKeysLD = ":".join(self.input.getIndividualsData().colList)

                # estimate LD for the specified loci
                haplo.estLinkageDisequilibrium(
                    locusKeys=locusKeysLD,
                    numInitCond=numInitCond,
                    numPermutations=1001,
                    numPermuInitCond=numPermuInitCond,
                )
                logger.info(f"estimating LD for specific loci: [{locusKeysLD}]")

            except NoOptionError:
                pass

            # do all pairwise LD, w/ or w/o permutation test
            if allPairwiseLD:
                haplo.allPairwise(
                    permutationPrintFlag=permutationPrintFlag,
                    numInitCond=numInitCond,
                    numPermutations=allPairwiseLDWithPermu,
                    numPermuInitCond=numPermuInitCond,
                    haploSuppressFlag=0,
                    haplosToShow=twoLocusHaplosToShow,
                )

            # serialize end to XML
            haplo.serializeEnd()

    def _genTextOutput(self):
        # read and parse stylesheet
        styledoc = etree.parse(self.xslFilename)
        style = etree.XSLT(styledoc)

        # read output XML file
        doc = etree.parse(self.xmlOutPath)
        # process via stylesheet
        result = style(doc, **{"new-hardyweinberg-format": "1"})

        # save result to file
        result.write_output(self.txtOutPath)

        # if running under Windows, convert output files
        # to use appropriate physical lineendings
        if sys.platform == "cygwin":
            convertLineEndings(self.xmlOutPath, 2)
            convertLineEndings(self.txtOutPath, 2)

    def getXmlOutPath(self):
        """Get name of XML file.

        Returns:
           XMLOutputStream: return XML file name
        """
        # return the name of the generated XML file
        return self.xmlOutPath

    def getTxtOutPath(self):
        """Get name of ``.txt`` output file.

        Returns:
           TextOutputStream: return txt file name
        """
        # return the name of the generated plain text (.txt) file
        return self.txtOutPath


def getConfigInstance(configFilename=None, altpath=None):
    """Create and return ConfigParser instance.

    Args:
       configFilename (str): a specified ``.ini`` filename
       altpath (str): an alternative path to search if no ``.ini`` filename provided in configFilename

    Returns:
      configparser.ConfigParser: configuration object
    """
    config = ConfigParser()

    if Path(configFilename).is_file():
        config.read(configFilename)
    elif Path(altpath).is_file():
        config.read(altpath)
    else:
        critical_exit(
            "Could not find config file either in current directory or %s", altpath
        )

    if len(config.sections()) == 0:
        critical_exit("No output defined!  Exiting...")

    return config


def get_sequence_directory(directory_str):
    """Get the directory for the :class:`PyPop.Filter.AnthonyNolanFilter`.

    Args:
       directory_str (str): directory to search

    Returns:
       str: path to sequence files
    """
    path_obj = Path(directory_str)

    # if the path is relative, resolve it to an absolute path if it exists
    if not path_obj.is_absolute():
        if path_obj.exists() and path_obj.is_dir():
            path_obj = path_obj.resolve()
        elif os.environ.get("PYPOP_CURRENT_TEST_DIRECTORY"):
            # if we're running in a test environment, resolve paths relative to the parent of the "tests" directory
            path_obj = (
                Path(os.environ.get("PYPOP_CURRENT_TEST_DIRECTORY")).parent / path_obj
            )
            logger.debug("in test environment, data files: %s", str(path_obj))
        else:
            critical_exit(
                "Relative path %s for AnthonyNolan sequence files does not exist or is not a directory.",
                path_obj,
            )

    # at this point, the path is absolute, now we need to check it exits
    if path_obj.exists() and path_obj.is_dir():
        anthonynolanPath = str(path_obj)
        logger.debug("Using %s for AnthonyNolan data files", anthonynolanPath)
    else:
        critical_exit(
            "Absolute path %s for Anthony Nolan sequence files does not exist or is not a directory",
            path_obj,
        )
    return anthonynolanPath
