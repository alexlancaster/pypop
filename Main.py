#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2003. The Regents of the University of California (Regents)
# All Rights Reserved.

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

"""Python population genetics statistics.
"""

import sys, os, string, time

from ParseFile import ParseGenotypeFile, ParseAlleleCountFile
from DataTypes import Genotypes, AlleleCounts
from Arlequin import ArlequinExactHWTest
from Haplo import Emhaplofreq, HaploArlequin
from HardyWeinberg import HardyWeinberg, HardyWeinbergGuoThompson, HardyWeinbergGuoThompsonArlequin
from Homozygosity import Homozygosity, HomozygosityEWSlatkinExact
from ConfigParser import ConfigParser, NoOptionError, NoSectionError
from Utils import XMLOutputStream, TextOutputStream, convertLineEndings, StringMatrix, checkXSLFile, getUserFilenameInput
from Filter import PassThroughFilter, AnthonyNolanFilter, AlleleCountAnthonyNolanFilter, BinningFilter
from RandomBinning import RandomBinsForHomozygosity


def getConfigInstance(configFilename = None,
                      altpath = None,
                      usage_message = None):
    """Create and return ConfigParser instance.

    Taken a specific .ini filename and an alternative path to search
    if no .ini filename is given.
    """
    config = ConfigParser()

    if os.path.isfile(configFilename):
        config.read(configFilename)
    else:
        if os.path.isfile(altpath):
          config.read(altpath)
        else:
          sys.exit("Could not find config file either in current directory or " +
                     altpath + os.linesep + usage_message)

    if len(config.sections()) == 0:
        sys.exit("No output defined!  Exiting...")

    return config


class Main:
    """Main interface to the PyPop modules.

    Given a config instance, which can be:

    - created from a filename passed from command-line argument or;

    - from values populated by the GUI (currently selected from an
      .ini file, but can ultimately be set directly from the GUI or
      values based from a form to a web server or the).
      
    runs the specified modules.
    """
    def __init__(self,
                 config=None,
                 xslFilename=None,
                 xslFilenameDefault=None,
                 debugFlag=0,
                 fileName=None,
                 datapath=None,
                 use_libxsltmod=1,
                 use_FourSuite=0,
                 thread=None,
                 outputDir=None,
                 version=None):

        self.config = config
        self.debugFlag = debugFlag
        self.fileName = fileName
        self.datapath = datapath
        self.use_libxsltmod = use_libxsltmod
        self.use_FourSuite = use_FourSuite
        self.xslFilename = xslFilename
        self.xslFilenameDefault = xslFilenameDefault
        self.outputDir = outputDir
        self.version = version

        # for threading to work
        self.thread = thread

        # switch off filtering and random binning by default
        self.filteringFlag = 0
        self.randomBinningFlag = 0

        # parse out the parts of the filename
        baseFileName = os.path.basename(self.fileName)
        prefixFileName = string.split(baseFileName, ".")[0]

        # generate date and time

        now = time.time()
        datestr = time.strftime("%Y-%m-%d", time.localtime(now))
        timestr = time.strftime("%H-%M-%S", time.localtime(now))

        # Parse "General" section

        try:
          self.debug = self.config.getboolean("General", "debug")
        except NoOptionError:
          self.debug=0
        except ValueError:
          sys.exit("require a 0 or 1 as debug flag")

        # if "-d" command line option used, then respect that, overriding
        # self.config file setting

        if debugFlag == 1:
          self.debug = 1

        # generate file prefix
        try:
          outFilePrefixType = self.config.get("General", "outFilePrefixType")
          if outFilePrefixType == 'filename':
            uniquePrefix = prefixFileName
          elif outFilePrefixType == 'date':
            uniquePrefix = "%s-%s-%s" % (prefixFileName, datestr, timestr)  
          else:
            sys.exit("outFilePrefixType: %s must be 'filename' or 'date'" % outFilePrefixType)
        except NoOptionError:
            # just use default prefix
            uniquePrefix = prefixFileName

        # generate filenames for both text and XML files

        #
        # start with text filename
        #
        defaultTxtOutFilename = uniquePrefix + "-out.txt"
        try:
          self.txtOutFilename = self.config.get("General", "txtOutFilename")
          if self.txtOutFilename == '':
            self.txtOutFilename = defaultTxtOutFilename
        except NoOptionError:
          self.txtOutFilename = defaultTxtOutFilename

        #
        # now XML filename
        #
        defaultXmlOutFilename = uniquePrefix + "-out.xml"
        try:
          self.xmlOutFilename = self.config.get("General", "xmlOutFilename")
          if self.xmlOutFilename == '':
            self.xmlOutFilename = defaultXmlOutFilename
        except NoOptionError:
          self.xmlOutFilename = defaultXmlOutFilename

        #
        # generate filename for logging filter output
        #
        self.defaultFilterLogFilename = uniquePrefix + "-filter.xml"

        #
        # generate filename for pop file dump (only used if option is set)
        #
        self.defaultPopDumpFilename = uniquePrefix         # + "-filtered.pop"    FIXME

        # prepend directory to all files if one was supplied
        if self.outputDir:
            [self.txtOutPath, \
             self.xmlOutPath, \
             self.defaultFilterLogPath, \
             self.defaultPopDumpPath] = \
             [os.path.join(self.outputDir, x) \
              for x in self.txtOutFilename, \
              self.xmlOutFilename, \
              self.defaultFilterLogFilename, \
              self.defaultPopDumpFilename]
        else:
            self.txtOutPath = self.txtOutFilename
            self.xmlOutPath = self.xmlOutFilename
            self.defaultFilterLogPath = self.defaultFilterLogFilename
            self.defaultPopDumpPath = self.defaultPopDumpFilename

        if self.debug:
          for section in self.config.sections():
            print section
            for option in self.config.options(section):
              print " ", option, "=", self.config.get(section, option)

        # if not provided on command line or provided check .ini
        # options, and use that location, if provided
        if self.xslFilename == None:
            try:
                self.xslFilename = self.config.get("General", "xslFilename")
                if self.debug:
                    print "using .ini option for xslFilename:", self.xslFilename
                checkXSLFile(self.xslFilename, abort=1, \
                             debug=self.debug, msg='specified in .ini file')
            except NoOptionError:
                # otherwise fall back to xslFilenameDefault
                if self.debug:
                    print "xslFilename .ini option not set"
                if self.xslFilenameDefault:
                    self.xslFilename = self.xslFilenameDefault
                else:
                    sys.exit("No default XSL file found, must specify in .ini or on the command line")

        else:
            if self.debug:
                print "using user supplied version in: ", self.xslFilename

        # check to see what kind of file we are parsing

        if self.config.has_section("ParseGenotypeFile"):
            self.fileType = "ParseGenotypeFile"
        elif self.config.has_section("ParseAlleleCountFile"):
            self.fileType = "ParseAlleleCountFile"
        else:
            sys.exit("File type is not recognised.  Exiting")
            
        
        # Parse self.fileType section

        # do fields common to both types of files
        try:
            validPopFields = self.config.get(self.fileType, "validPopFields")
        except NoOptionError:
            validPopFields = None
            print "LOG: Data file has no header data block"
            #sys.exit("No valid population fields defined")

        try:
            validSampleFields = self.config.get(self.fileType, "validSampleFields")
        except NoOptionError:
            sys.exit("No valid sample fields defined")


        # BEGIN PARSE for a genotype file (ParseGenotypeFile)
        if self.fileType == "ParseGenotypeFile":

            try:
              popNameDesignator = self.config.get(self.fileType, "popNameDesignator")
            except NoOptionError:
              popNameDesignator = "+"

            try:
              self.alleleDesignator = self.config.get(self.fileType, "alleleDesignator")
            except NoOptionError:
              self.alleleDesignator = '*'

            try:
              self.untypedAllele = self.config.get(self.fileType, "untypedAllele")
            except NoOptionError:
              self.untypedAllele = '****'

            try:
              fieldPairDesignator = self.config.get(self.fileType, "fieldPairDesignator")
            except NoOptionError:
              fieldPairDesignator = '_1:_2'


            # Generate the parse file object, which simply creates
            # a matrix (no allele count stuff done!)
            self.parsed = ParseGenotypeFile(self.fileName,
                                validPopFields=validPopFields,
                                validSampleFields=validSampleFields,
                                alleleDesignator=self.alleleDesignator, 
                                untypedAllele=self.untypedAllele,
                                popNameDesignator=popNameDesignator,
                                fieldPairDesignator=fieldPairDesignator,
                                debug=self.debug)

            # we copy the parsed data to self.filtered, to be ready for the gamut of filters coming
            self.matrixHistory = []
            self.matrixHistory.append(self.parsed.getMatrix().copy())
            
            # figure out what filters we will be using, if any
            if self.config.has_section("Filters"):

                try:
                    self.filtersToApply = self.config.get("Filters", "filtersToApply")
                    self.filtersToApply = string.split(self.filtersToApply, ':')
                except:
                    self.filtersToApply = []
                try:
                    self.popDump = self.config.getint("Filters","makeNewPopFile")
                except:
                    self.popDump = 0

                # this allows the user to have "filtersToApply=" without ill consequences
                if len(self.filtersToApply) > 0 and len(self.filtersToApply[0]) > 0:

                    # get filtering options and open log file for
                    # filter in append mode
                    self.filterLogFile = XMLOutputStream(open(self.defaultFilterLogPath, 'w'))
                    self.filterLogFile.opentag('filterlog', filename=self.fileName)
                    self.filterLogFile.writeln()
                    self.filteringFlag = 1

                    # run the filtering gamut
                    self._runFilters()

            # and then we pass the filtered matrix to be put in format
            # for rest of processing
            self.input = Genotypes(matrix=self.matrixHistory[-1],
                                   untypedAllele=self.untypedAllele,
                                   debug=self.debug)

        # END PARSE for a genotype file (ParseGenotypeFile)



        # BEGIN PARSE: allelecount file (ParseAlleleCountFile)
        elif self.fileType == "ParseAlleleCountFile":

            # Generate the parse file object
            self.parsed = ParseAlleleCountFile(self.fileName,
                             validPopFields=validPopFields,
                             validSampleFields=validSampleFields,
                             separator='\t',
                             debug=self.debug)

            self.input = AlleleCounts(alleleTable=self.parsed.getAlleleTable(),
                                      locusName=self.parsed.getLocusName(),
                                      debug=self.debug)
            
        # END PARSE: allelecount file (ParseAlleleCountFile)
        
        else:
            sys.exit("Unrecognised file type")



        # BEGIN common XML output section
        
        # create XML stream
        self.xmlStream = XMLOutputStream(open(self.xmlOutPath, 'w'))

        # opening tag
        self.xmlStream.opentag('dataanalysis xmlns:xi="http://www.w3.org/2001/XInclude"', date="%s-%s" % (datestr, timestr), role=self.fileType)
        self.xmlStream.writeln()


        # if and only if filtering is done, generate XInclude XML
        # file output reference, to include
        # <popfilename>-filter.log
        if self.filteringFlag:
            
            self.xmlStream.opentag('xi:include', href=self.defaultFilterLogFilename, parse="xml")
            self.xmlStream.writeln()
            self.xmlStream.emptytag('xi:fallback')
            self.xmlStream.writeln()
            self.xmlStream.closetag('xi:include')
            self.xmlStream.writeln()


        # more meta-data
        self.xmlStream.tagContents('filename', baseFileName)
        self.xmlStream.writeln()
        self.xmlStream.tagContents('pypop-version', self.version)
        self.xmlStream.writeln()

        # serialize summary info for population in XML (common)
        self.parsed.serializeMetadataTo(self.xmlStream)

        # serialize the specific information for kind of file
        self.input.serializeSubclassMetadataTo(self.xmlStream)

        # process the file depending on type
        if self.fileType == "ParseAlleleCountFile":
            self._doAlleleCountFile()
        elif self.fileType == "ParseGenotypeFile":
            self._doGenotypeFile()
        else:
            pass

        # now close the filter log file, if and only if we have done
        # some kind of filtering, moving it here, means that the open
        # and close are at the same level and are called in the same
        # method.
        if self.filteringFlag:
            self.filterLogFile.closetag('filterlog')
            self.filterLogFile.close()

        # END common XML output section

        # closing tag
        self.xmlStream.closetag('dataanalysis')
        # close XML stream
        self.xmlStream.close()

        # lastly, generate the text output
        self._genTextOutput()


    def _runFilters(self):

        if self.config.has_section("RandomAlleleBinning"):
            try:
                self.binningMethod = self.config.get("RandomAlleleBinning", "binningMethod")
            except:
                self.binningMethod = "random"
            try:
                self.binningStartPoint = self.config.getint("RandomAlleleBinning","binningStartPoint")
            except:
                self.binningStartPoint = 0
            try:
                self.binningReplicates = self.config.getint("RandomAlleleBinning", "binningReplicates")
            except NoOptionError:
                self.binningReplicates = 10000
            try:
                self.binningLoci = self.config.get("RandomAlleleBinning", "binningLoci")
                self.binningLoci = string.split(self.binningLoci, ',')
            except:
                self.binningLoci = []
            if len(self.binningLoci) > 0:
                self.randomBinningFlag = 1


        for filterCall in self.filtersToApply:
            if filterCall == 'AnthonyNolan' or \
                   filterCall == 'DigitBinning' or \
                   filterCall == 'CustomBinning' or \
                   filterCall == 'Sequence':
                filterType = filterCall
            else:
                try:
                    filterType = self.config.get(filterCall, "filterType")
                except:
                    sys.exit("No valid filter type specified under filter heading " + filterCall)

            if filterType == 'AnthonyNolan':
                try:
                    anthonynolanPath = self.config.get(filterCall, "directory")
                except:
                    anthonynolanPath = os.path.join(self.datapath, "anthonynolan", "msf")
                    if self.debug:
                        print "LOG: Defaulting to system datapath %s for anthonynolanPath data" % anthonynolanPath
                try:
                    alleleFileFormat = self.config.get(filterCall, "alleleFileFormat")
                except:
                    alleleFileFormat = 'msf'
                filter = AnthonyNolanFilter(debug=self.debug,
                                            directoryName=anthonynolanPath,
                                            alleleFileFormat=alleleFileFormat,
                                            alleleDesignator=self.alleleDesignator,
                                            untypedAllele=self.untypedAllele,
                                            filename=self.fileName,
                                            logFile=self.filterLogFile)
                self.matrixHistory.append(filter.doFiltering((self.matrixHistory[-1]).copy()))
                
            elif filterType == 'DigitBinning':
                try:
                    binningDigits = self.config.getint(filterCall, "binningDigits")
                except:
                    binningDigits = 4
                filter = BinningFilter(debug=self.debug,
                                       binningDigits=binningDigits,
                                       untypedAllele=self.untypedAllele,
                                       filename=self.fileName,
                                       logFile=self.filterLogFile)
                self.matrixHistory.append(filter.doDigitBinning((self.matrixHistory[-1]).copy()))

            elif filterType == 'CustomBinning':
                try:
                    binningPath=self.config.get(filterCall, "file")
                except:
                    sys.exit("Could not find the CustomBinning filter file: " + binningPathspecified)
                filter = BinningFilter(debug=self.debug,
                                       binningPath=binningPath,
                                       untypedAllele=self.untypedAllele,
                                       filename=self.fileName,
                                       logFile=self.filterLogFile)
                self.matrixHistory.append(filter.doCustomBinning((self.matrixHistory[-1]).copy()))

            elif filterType == 'Sequence':
                try:
                    sequenceFileSuffix = self.config.get(filterCall, "sequenceFileSuffix")
                except:
                    sequenceFileSuffix='_prot'
                try:
                    anthonynolanPath = self.config.get(filterCall, "directory")
                except:
                    anthonynolanPath = os.path.join(self.datapath, "anthonynolan", "msf")
                    if self.debug:
                        print "LOG: Defaulting to system datapath %s for anthonynolanPath data" % anthonynolanPath
                filter = AnthonyNolanFilter(debug=self.debug,
                                            directoryName=anthonynolanPath,
                                            alleleFileFormat='msf',
                                            alleleDesignator=self.alleleDesignator,
                                            sequenceFileSuffix=sequenceFileSuffix,
                                            untypedAllele=self.untypedAllele,
                                            filename=self.fileName,
                                            logFile=self.filterLogFile)
                self.matrixHistory.append(filter.translateMatrix((self.matrixHistory[-1]).copy()))

            else:
                sys.exit("The filter type '" + filterType + "' specified under filter heading '" + filterCall + "' is not recognized.")

        if self.debug:
            print "matrixHistory"
            print self.matrixHistory

        # outputs a pop file, of sorts.  method should be moved to data type class.
        if self.popDump:

            originalMatrix = self.matrixHistory[0]

            for locus in originalMatrix.colList:

                popDumpPath = self.defaultPopDumpPath + "-" + locus + "-filtered.pop"
                dumpFile = TextOutputStream(open(popDumpPath, 'w'))
                
                dumpMatrix = self.matrixHistory[self.popDump]

                for locusPos in dumpMatrix.colList:
                    if dumpMatrix.colList.index(locusPos) > 0 and locusPos[0:len(locus)] == locus:
                        dumpFile.write('\t')
                        dumpFile.write(locusPos + '_1\t' + locusPos + '_2')

                dumpFile.write(os.linesep)

                individCount = 0
                while individCount < len(dumpMatrix):
                    for locusPos in dumpMatrix.colList:
                        individ = dumpMatrix[locusPos][individCount]
                        if dumpMatrix.colList.index(locusPos) > 0 and locusPos[0:len(locus)] == locus:
                            dumpFile.write('\t')
                            dumpFile.write(individ[0] + '\t' + individ[1])
                    individCount += 1
                    dumpFile.write(os.linesep)
                dumpFile.close()
            


    def _doAlleleCountFile(self):

        # get the locus name
        locus = self.input.getLocusName()

        # wrap the output in a locus tag with the name of the
        # locus, thus the output XML has the same hierarchy as the
        # ParseGenotypeFile output.
        
        self.xmlStream.opentag('locus', name=locus)
        self.xmlStream.writeln()
        
        # generate the allele count statistics
        self.input.serializeAlleleCountDataAt(self.xmlStream, locus)

        # disabled old table-based Homozygosity

        if 0:
            try:
                rootPath=self.config.get("Homozygosity", "rootPath")
            except NoOptionError:
                rootPath='/net/share/PyPop/homozygosity'
                print "LOG: Defaulting to system datapath %s for homozygosity tables" % rootPath

            hzObject = Homozygosity(self.input.getAlleleCount(),
                                    rootPath=rootPath,
                                    debug=self.debug)

            hzObject.serializeHomozygosityTo(self.xmlStream)

        # HomozygosityEWSlatkinExact

        try:
            numReplicates = self.config.getint("HomozygosityEWSlatkinExact",
                                          "numReplicates")
        except NoOptionError:
            numReplicates = 10000

        hzExactObj =  HomozygosityEWSlatkinExact(self.input.getAlleleCount(), 
                                                 numReplicates=numReplicates,
                                                 debug=self.debug)

        hzExactObj.serializeHomozygosityTo(self.xmlStream)
        
        self.xmlStream.closetag('locus')
        self.xmlStream.writeln()


    def _doGenotypeFile(self):


        loci = self.input.getLocusList()

        for locus in loci:

##           if self.thread and self.thread._want_abort:
##             from wxPython.wx import wxPostEvent
##             from GUIApp import ResultEvent
##             # Use a result of None to acknowledge the abort (of
##             # course you can use whatever you'd like or even
##             # a separate event type)
##             wxPostEvent(self.thread._notify_window,ResultEvent(None))
##             return
            
          self.xmlStream.opentag('locus', name=locus)
          self.xmlStream.writeln()

          self.input.serializeAlleleCountDataAt(self.xmlStream, locus)

          # Parse "HardyWeinberg" section

          if self.config.has_section("HardyWeinberg") and \
             len(self.config.options("HardyWeinberg")) > 0:

            try:
              lumpBelow =  self.config.getint("HardyWeinberg", "lumpBelow")
            except NoOptionError:
              lumpBelow=5
            except ValueError:
              sys.exit("require integer value")

            hwObject = HardyWeinberg(self.input.getLocusDataAt(locus), 
                                     self.input.getAlleleCountAt(locus), 
                                     lumpBelow=lumpBelow,
                                     debug=self.debug)

            # serialize HardyWeinberg
            hwObject.serializeTo(self.xmlStream)

          # Parse "HardyWeinbergGuoThompson"
          if self.config.has_section("HardyWeinbergGuoThompson") and \
             len(self.config.options("HardyWeinbergGuoThompson")) > 0:
              runMCMCTest = 1
          else:
              runMCMCTest = 0

          # Parse "HardyWeinbergGuoThompsonMonteCarlo"
          if self.config.has_section("HardyWeinbergGuoThompsonMonteCarlo") and \
             len(self.config.options("HardyWeinbergGuoThompsonMonteCarlo")) > 0:
              runPlainMCTest = 1
          else:
              runPlainMCTest = 0

          # deal with these sections in one call to module, because data
          # structures are identical
          if runMCMCTest or runPlainMCTest:

            try:
              dememorizationSteps = self.config.getint("HardyWeinbergGuoThompson",
                                                  "dememorizationSteps")
            except (NoOptionError, NoSectionError):
              dememorizationSteps=2000
            except ValueError:
              sys.exit("require integer value")

            try:
              samplingNum = self.config.getint("HardyWeinbergGuoThompson", "samplingNum")
            except (NoOptionError, NoSectionError):
              samplingNum=1000
            except ValueError:
              sys.exit("require integer value")

            try:
              samplingSize = self.config.getint("HardyWeinbergGuoThompson", "samplingSize")
            except (NoOptionError, NoSectionError):
              samplingSize=1000
            except ValueError:
              sys.exit("require integer value")

            try:
              maxMatrixSize = self.config.getint("HardyWeinbergGuoThompson", "maxMatrixSize")
            except (NoOptionError, NoSectionError):
              maxMatrixSize=250
            except ValueError:
              sys.exit("require integer value")

            try:
              monteCarloSteps = self.config.getint("HardyWeinbergGuoThompsonMonteCarlo", "monteCarloSteps")
            except (NoOptionError, NoSectionError):
              monteCarloSteps=1000000
            except ValueError:
              sys.exit("require integer value")

            # Guo & Thompson implementation
            hwObject= HardyWeinbergGuoThompson(\
                locusData=self.input.getLocusDataAt(locus), 
                alleleCount=self.input.getAlleleCountAt(locus),
                runMCMCTest=runMCMCTest,
                runPlainMCTest=runPlainMCTest,
                dememorizationSteps=dememorizationSteps,
                samplingNum=samplingNum,
                samplingSize=samplingSize,
                maxMatrixSize=maxMatrixSize,
                monteCarloSteps=monteCarloSteps,
                debug=self.debug)
            
            hwObject.dumpTable(locus, self.xmlStream)
            self.xmlStream.writeln()

          if self.config.has_section("HardyWeinbergGuoThompsonArlequin"):

            # default location for Arlequin executable
            arlequinExec = 'arlecore.exe'

            if self.config.has_section("Arlequin"):

              try:
                arlequinExec = self.config.get("Arlequin", "arlequinExec")
              except NoOptionError:
                print "LOG: Location to Arlequin executable file not given: assume `arlecore.exe' is in user's PATH"

            try:
              markovChainStepsHW = self.config.getint("HardyWeinbergGuoThompsonArlequin", \
                                                 "markovChainStepsHW")
            except NoOptionError:
              samplingNum=100000
            except ValueError:
              sys.exit("require integer value")

            try:
              markovChainDememorisationStepsHW = self.config.getint("HardyWeinbergGuoThompsonArlequin", "markovChainDememorisationStepsHW")
            except NoOptionError:
              samplingNum=100000
            except ValueError:
              sys.exit("require integer value")


            hwArlequin=HardyWeinbergGuoThompsonArlequin(self.input.getIndividualsData(),
                                                        locusName = locus,
                                                        arlequinExec = arlequinExec,
                                                        markovChainStepsHW = \
                                                        markovChainStepsHW,
                                                        markovChainDememorisationStepsHW=markovChainDememorisationStepsHW,
                                                        untypedAllele=self.untypedAllele,
                                                        debug=self.debug)
            hwArlequin.serializeTo(self.xmlStream)


          # Parse "Homozygosity" section

          if self.config.has_section("Homozygosity"):

            try:
              rootPath=self.config.get("Homozygosity", "rootPath")
            except NoOptionError:
              rootPath=os.path.join(self.datapath, "homozygosity")
              if self.debug:
                print "LOG: Defaulting to system datapath %s for homozygosity tables" % rootPath

            alleleCount = self.input.getAlleleCountAt(locus)
            alleleCount = alleleCount[0].values()

            hzObject = Homozygosity(alleleCount,
                                    rootPath=rootPath,
                                    debug=self.debug)

            hzObject.serializeHomozygosityTo(self.xmlStream)


          if self.config.has_section("HomozygosityEWSlatkinExact"):
            
            try:
              numReplicates=self.config.getint("HomozygosityEWSlatkinExact", \
                                          "numReplicates")
            except NoOptionError:
              numReplicates=10000

            # make a dictionary of allele counts (don't need the last
            # two elements that are returned by this method)            
            alleleCounts = self.input.getAlleleCountAt(locus)[0]

            # notice we pass just the alleleCount values.  But the
            # dictionary is still useful to have in case we have to do
            # random binning.
            hzExactObj = HomozygosityEWSlatkinExact(alleleCounts.values(),
                                                    numReplicates=numReplicates,
                                                    debug=self.debug)

            hzExactObj.serializeHomozygosityTo(self.xmlStream)

            # random binning for the homozygosity test begins here
            if self.randomBinningFlag and locus in map(string.upper,self.binningLoci):

                inputInitial = Genotypes(matrix=self.matrixHistory[self.binningStartPoint],
                                         untypedAllele=self.untypedAllele,
                                         debug=self.debug)

                # as above, we create a dictionary of allele counts
                # (made from the correct position in the
                # matrixHistory)
                alleleCountsInitial = inputInitial.getAlleleCountAt(locus)[0]

                if self.debug:
                    print "alleleCountsInitial", len(alleleCountsInitial), alleleCountsInitial
                    print "alleleCounts", len(alleleCounts), alleleCounts

                if len(alleleCountsInitial) <= len(alleleCounts):
                    if self.debug:
                        print 'skipping random binning because the initial allele count is not bigger than the target count'

                else:
                    # go ahead and do the random binning
                    randObj = RandomBinsForHomozygosity(untypedAllele=self.untypedAllele,
                                                        filename=self.fileName,
                                                        numReplicates=numReplicates,
                                                        binningReplicates=self.binningReplicates,
                                                        locus=locus,
                                                        debug=self.debug)

                    if self.binningMethod == "random":
                        randObj.randomMethod(alleleCountsBefore=alleleCountsInitial,
                                             alleleCountsAfter=alleleCounts)

                    elif self.binningMethod == "sequence":
                        try:
                            sequenceFileSuffix = self.config.get("Sequence", "sequenceFileSuffix")
                        except:
                            sequenceFileSuffix='_nuc'
                        try:
                            anthonynolanPath = self.config.get("Sequence", "directory")
                        except:
                            anthonynolanPath = os.path.join(self.datapath, "anthonynolan", "msf")
                            if self.debug:
                                print "LOG: Defaulting to system datapath %s for anthonynolanPath data" % anthonynolanPath

                        seqfilter = AnthonyNolanFilter(debug=self.debug,
                                            directoryName=anthonynolanPath,
                                            alleleFileFormat='msf',
                                            alleleDesignator=self.alleleDesignator,
                                            sequenceFileSuffix=sequenceFileSuffix,
                                            untypedAllele=self.untypedAllele,
                                            filename=self.fileName)

                        polyseq, polyseqpos = seqfilter.makeSeqDictionaries(matrix=(self.matrixHistory[self.binningStartPoint]).copy(),locus=locus)

                        randObj.sequenceMethod(alleleCountsBefore=alleleCountsInitial,
                                               alleleCountsAfter=alleleCounts,
                                               polyseq=polyseq,
                                               polyseqpos=polyseqpos)

                    else:
                        sys.exit("Random binning method not recognized:" + self.binningMethod)


          self.xmlStream.closetag('locus')
          self.xmlStream.writeln()

        # estimate haplotypes

        if self.config.has_section("Emhaplofreq"):

          # create object to generate haplotype and LD statistics
          # a wrapper around the emhaplofreq module
          haplo = Emhaplofreq(self.input.getIndividualsData(),
                              debug=self.debug,
                              untypedAllele=self.untypedAllele,
                              stream=self.xmlStream)

          # before running emhaplofreq, flush the current buffered
          # output to file
          self.xmlStream.flush()

          # start by serializing the start of the XML block
          haplo.serializeStart()

          try:
            allPairwiseLD = self.config.getboolean("Emhaplofreq", "allPairwiseLD")
          except NoOptionError:
            allPairwiseLD=0
          except ValueError:
            sys.exit("require a 0 or 1 as a flag")

          try:
            allPairwiseLDWithPermu = self.config.getint("Emhaplofreq",
                                                       "allPairwiseLDWithPermu")
          except NoOptionError:
            allPairwiseLDWithPermu=0
          except ValueError:
            sys.exit("allPairwiseLDWithPermu: option requires an integer")

          # FIXME: needed for backwards-compatibility, remove when not
          # needed
          if allPairwiseLDWithPermu == 1:
              sys.exit("""ERROR: semantics of 'allPairwiseLDWithPerm' option have changed.
It is no longer a boolean variable to enable the permutation test.
It should now contain the NUMBER of permutations desired.  A value of
at least 1000 is recommended.  A value of '1' is not permitted.""")

          try:
            numPermuInitCond = self.config.getint("Emhaplofreq",
                                                  "numPermuInitCond")
          except NoOptionError:
            numPermuInitCond=5
          except ValueError:
            sys.exit("numPermuInitCond: option requires an integer")

          # Parse new [Emhaplofreq] option 'numInitCond', so that the
          # number of initial conditions for the *first* iteration LD
          # calculation (and therefore haplotype estimation) is
          # user-configurable.  Default to 50.
          try:
            numInitCond = self.config.getint("Emhaplofreq",
                                             "numInitCond")
          except NoOptionError:
            numInitCond=50
          except ValueError:
            sys.exit("numInitCond: option requires an integer")


          try:
            permutationPrintFlag = self.config.getboolean("Emhaplofreq",
                                                          "permutationPrintFlag")
          except NoOptionError:
            permutationPrintFlag=0
          except ValueError:
            sys.exit("permutationPrintFlag: option requires a 0 or 1 flag")


          if allPairwiseLD:
            print "LOG: estimating all pairwise LD:",
            if allPairwiseLDWithPermu:
              print "with %d permutations and %d initial conditions for each permutation" % (allPairwiseLDWithPermu, numPermuInitCond),
              if permutationPrintFlag:
                  print "and each permutation output will be logged to XML"
              else:
                  print
            else:
              print "with no permutation test"


          # first set the list of 2-locus haplotypes to show to empty
          twoLocusHaplosToShow = []

          try:
            locusKeys=self.config.get("Emhaplofreq", "lociToEstHaplo")

            if locusKeys == '*':
              print "wildcard '*' given for lociToEstHaplo, assume entire data set"
              locusKeys=string.join(self.input.getIndividualsData().colList,':')
            print "LOG: estimating haplotype frequencies for",

            # if we will be running allPairwise*, then exclude any two-locus
            # haplotypes, since we will estimate them as part of 'all pairwise'
            if allPairwiseLD:

              print "all two locus haplotypes,",
              modLocusKeys = []
              for group in string.split(locusKeys, ','):

                # if a two-locus haplo, add it to the list that allPairwise
                # will use
                if len(string.split(group, ':')) == 2:
                  twoLocusHaplosToShow.append(string.upper(group))

                # otherwise add it to the regular output
                else:
                  modLocusKeys.append(group)

              locusKeys = string.join(modLocusKeys, ',')

            # estimate haplotypes on set of locusKeys *only* if there are
            # locus groups that remain after excluding two locus haplotypes
            if locusKeys:
                haplo.estHaplotypes(locusKeys=locusKeys,
                                    numInitCond=numInitCond)
                print "specific haplotypes: [%s]" % locusKeys

          except NoOptionError:
              pass

          try:
            locusKeysLD=self.config.get("Emhaplofreq", "lociToEstLD")

            if locusKeysLD == '*':
              print "LOG: wildcard '*' given for lociToEstLD, assume entire data set"
              locusKeysLD=string.join(self.input.getIndividualsData().colList,':')

            # estimate LD for the specified loci
            haplo.estLinkageDisequilibrium(locusKeys=locusKeysLD,
                                           numInitCond=numInitCond,
                                           numPermutations=1001,
                                           numPermuInitCond=numPermuInitCond)
            print "LOG: estimating LD for specific loci: [%s]" % locusKeysLD

          except NoOptionError:
              pass

          # do all pairwise LD, w/ or w/o permutation test
          if allPairwiseLD:
            haplo.allPairwise(permutationPrintFlag=permutationPrintFlag,
                              numInitCond=numInitCond,
                              numPermutations=allPairwiseLDWithPermu,
                              numPermuInitCond=numPermuInitCond,
                              haploSuppressFlag=0,
                              haplosToShow=twoLocusHaplosToShow)

          # serialize end to XML
          haplo.serializeEnd()
          #haplo.serializeTo(self.xmlStream)


    def _genTextOutput(self):

        if self.use_libxsltmod:

          # now use bindings that are part of libxml2/libxslt 
          import libxml2
          import libxslt

          # read and parse stylesheet
          styledoc = libxml2.parseFile(self.xslFilename)
          style = libxslt.parseStylesheetDoc(styledoc)

          # read output XML file
          doc = libxml2.parseFile(self.xmlOutPath)

          # resolve and perform any XIncludes the document may have
          doc.xincludeProcess()

          # process via stylesheet
          result = style.applyStylesheet(doc, None)

          # save result to file
          style.saveResultToFilename(self.txtOutPath, result, 0)

          # cleanup
          style.freeStylesheet()
          doc.freeDoc()
          result.freeDoc()

          # if running under Windows, convert output files
          # to use appropriate physical lineendings so that
          # lame Windoze editors like Notepad don't get confused
          if sys.platform == 'cygwin':
              convertLineEndings(self.xmlOutPath, 2)
              convertLineEndings(self.txtOutPath, 2)

        # use of 4Suite is currently UNTESTED and DEPRECATED!!!
        if self.use_FourSuite:
        
          from xml.xslt.Processor import Processor

          # open XSLT stylesheet
          styleSheet = open(self.xslFilename, 'r')

          # re-open text stream
          self.xmlStream = open(self.xmlOutFilename, 'r')

          # open new txt output
          newOut = TextOutputStream(open(self.txtOutPath, 'w'))

          # create xsl process
          p = Processor()

          # attach the stylesheet
          p.appendStylesheetStream(styleSheet)

          # run the stylesheet on the XML output
          p.runStream(self.xmlStream, outputStream=newOut)

          # close streams
          newOut.close()
          styleSheet.close()

    def getXmlOutPath(self):
        # return the name of the generated XML file
        return self.xmlOutPath

    def getTxtOutPath(self):
        # return the name of the generated plain text (.txt) file
        return self.txtOutPath

