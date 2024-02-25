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


"""Module for exposing Arlequin functionality in Python.

"""
import sys, os, re, shutil, stat
from PyPop.Utils import Group

class ArlequinWrapper:
    """New wrapper for Arlequin"""

    def __init__(self,
                 matrix=None,
                 arlequinPrefix = "arl_run",
                 arlequinExec="arlecore.exe",
                 untypedAllele='****',
                 arpFilename = 'output.arp',
                 arsFilename = 'arl_run.ars',
                 debug=None):

        self.matrix = matrix
        self.untypedAllele = untypedAllele
        self.arlequinPrefix = arlequinPrefix
        self.arlequinExec = arlequinExec
        self.separator = '\t'
        self.debug = debug

        # append PID to make directory name unique, so that multiple
        # instances of PyPop can be running without interference with
        # each other, note: this is specific to Unix and Windows
        # (possibly also MacOS X)
        self.arlSubdir = 'arlequinRuns-%d' % os.getpid()

        # make a subdirectory
        if not os.path.exists(self.arlSubdir):
            os.mkdir(self.arlSubdir)
        
        self.arpFilename = arpFilename
        self.arsFilename = arsFilename
        
        if self.arpFilename[-4:] == '.arp':
            self.arpFilename = self.arpFilename
            self.arlResPrefix = self.arpFilename[:-4]
        else:
            sys.exit("Error: Arlequin filename: %s does not have a .arp suffix", arpFilename)
        if self.arsFilename[-4:] == '.ars':
            self.arsFilename = self.arsFilename
        else:
            sys.exit("Error: Arlequin settings filename: %s does not have a .ars suffix", arpFilename)
            

    def outputArpFile(self, group):

        dataLoci = [l for l in group \
                    if len(self.matrix.filterOut(l, self.untypedAllele)) > 0]

        if len(dataLoci) == 1:
            keys = dataLoci[0]
        else:
            keys = ':'.join(dataLoci)

        self.arpFile = open(os.path.join(self.arlSubdir, self.arpFilename), 'w')
        
        self._outputHeader(1)
        self._outputSample(keys)

        self.arpFile.close()

    def _outputHeader(self, groupCount):

        self.arpFile.write("""[Profile]
        
        Title=\"Arlequin sample run\"

        NbSamples=%d
        GenotypicData=1
        GameticPhase=0
        DataType=STANDARD
        LocusSeparator=WHITESPACE
        MissingData='%s'
        RecessiveData=0                         
        RecessiveAllele=\"null\"
        """ % (groupCount, '?'))

        self.arpFile.write("""
[Data]
[[Samples]]
""")
        
    def _outputSample(self, keys):

        numSamples = len(self.matrix[keys])
        
        self.arpFile.write("""
        SampleName=\"A pop with %d individuals from loci %s\"
        SampleSize=%d
        SampleData={
        """ % (numSamples, keys, numSamples))

        sampleNum = 1

        for sample in self.matrix[keys]:

            # get all even alleles (first phase of genotype data)
            # then filter them through the function to convert any
            # missing data into the form that Arlequin expects
            even = ' '.join([self._fixData(sample[i]) \
                                for i in range(0,len(sample),2)])

            # do the same for the odd alleles
            odd = ' '.join([self._fixData(sample[i]) \
                               for i in range(1,len(sample),2)])

            # output them on adjacent lines so that the alleles for
            # each locus are paired up like so:
            #
            # sampleId 1 allele1-locus1 allele1-locus2
            #            allele2-locus1 allele2-locus2

            self.arpFile.write("%10d 1 %s" % (sampleNum, even) + '\n')
            self.arpFile.write("%13s%s" % (" ", odd) + '\n')
            sampleNum += 1

        self.arpFile.write("}")

    def _fixData(self, data):
        """Fix data for Arlequin input.

        Convert embedded spaces to 'x'

        Convert missing data using the untypedAllele parameter to
        class to the standard single character missing data signifier
        '?' that Arlequin uses"""

        # add a colon ':' to the match, because all alleles in the original
        # data structure have a trailing colon
        if data == self.untypedAllele + ":":
            output = '?'
        else:
            output = data.replace(' ', 'x')
        return output


    def _outputArlRunTxt(self, txtFilename, arpFilename):
        """Outputs the run-time Arlequin program file.
        """
        file = open(os.path.join(self.arlSubdir, txtFilename), 'w')
        file.write("""%s
use_interf_settings
%s
0
0
end""" % (os.path.join(os.getcwd(), self.arlSubdir), \
          os.path.join(os.getcwd(), self.arlSubdir, arpFilename)))

    def outputArsFile(self, arsFilename, arsContents):
        """Outputs the run-time Arlequin program file.
        """
        file = open(os.path.join(self.arlSubdir, arsFilename), 'w')
        file.write(arsContents)
        file.close()
        
    def outputRunFiles(self):
        """Generates the expected '.txt' set-up files for Arlequin.
        """
        self._outputArlRunTxt(self.arlequinPrefix + ".txt", self.arpFilename)

    def runArlequin(self):
        """Run the Arlequin haplotyping program.
         
        Forks a copy of 'arlecore.exe', which must be on 'PATH' to
        actually generate the desired statistics estimates from the
        generated '.arp' file.  """

        # save current directory
        cwd = os.getcwd()

        # change into subdirectory
        os.chdir(self.arlSubdir)

        # spawn external Arlequin process and store stdout
        stdout = os.popen(self.arlequinExec, 'r').readlines()

        if self.debug:
            print("Arlequin stdout", stdout)

        # fix permissions on result directory because Arlequin is
        # brain-dead with respect to file permissions on Unix
        os.chmod(self.arlResPrefix + ".res", stat.S_IXGRP)

        # restore original directory
        os.chdir(cwd)

    def cleanup(self):
        # remove the working arlequin subdirectory
        shutil.rmtree(self.arlSubdir)

class ArlequinExactHWTest(ArlequinWrapper):
    """Wraps the Arlequin Hardy-Weinberg exact functionality

    """

    hwExactTest = """[Setting for Calculations]
TaskNumber=32
DeletionWeight=1.0
TransitionWeight=1.0
TranversionWeight=1.0
UseOriginalHaplotypicInformation=0
EliminateRedondHaplodefs=1
AllowedLevelOfMissingData=0.0
GameticPhaseIsKnown=0
HardyWeinbergTestType=0
MakeHWExactTest=1
MarkovChainStepsHW=%d
MarkovChainDememorisationStepsHW=%d
PrecisionOnPValueHW=0.0
SignificanceLevelHW=2
TypeOfTestHW=0
LinkageDisequilibriumTestType=0
MakeExactTestLD=0
MarkovChainStepsLD=100000
MarkovChainDememorisationStepsLD=1000
PrecisionOnPValueLD=0.01
SignificanceLevelLD=0.05
PrintFlagHistogramLD=0
InitialCondEMLD=10
ComputeDvalues=0
ComputeStandardDiversityIndices=0
DistanceMethod=0
GammaAValue=0.0
ComputeTheta=0
MismatchDistanceMethod=0
MismatchGammaAValue=0.0
PrintPopDistMat=0
InitialConditionsEM=50
MaximumNumOfIterationsEM=5000
RecessiveAllelesEM=0
CompactHaplotypeDataBaseEM=0
NumBootstrapReplicatesEM=0
NumInitCondBootstrapEM=10
ComputeAllSubHaplotypesEM=0
ComputeAllHaplotypesEM=1
ComputeAllAllelesEM=0
EpsilonValue=1.0e-7
FrequencyThreshold=1.0e-5
ComputeConventionalFST=0
IncludeIndividualLevel=0
ComputeDistanceMatrixAMOVA=0
DistanceMethodAMOVA=0
GammaAValueAMOVA=0.0
PrintDistanceMatrix=0
TestSignificancePairewiseFST=0
NumPermutationsFST=100
ComputePairwiseFST=0
TestSignificanceAMOVA=0
NumPermutationsAMOVA=1000
NumPermutPopDiff=10000
NumDememoPopDiff=1000
PrecProbPopDiff=0.0
PrintHistoPopDiff=1
SignLevelPopDiff=0.05
EwensWattersonHomozygosityTest=0
NumIterationsNeutralityTests=1000
NumSimulFuTest=1000
NumPermMantel=1000
NumBootExpDem=100
LocByLocAMOVA=0
PrintFstVals=0
PrintConcestryCoeff=0
PrintSlatkinsDist=0
PrintMissIntermatchs=0
UnequalPopSizeDiv=0
PrintMinSpannNetworkPop=0
PrintMinSpannNetworkGlob=0
KeepNullDistrib=0"""

    def __init__(self,
                 matrix=None,
                 lociList=None,
                 markovChainStepsHW=100000,
                 markovChainDememorisationStepsHW=1000,
                 **kw):
        """Setup run HW exact test.

        Run Hardy-Weinberg exact test on list specified in 'lociList'.

        - 'markovChainStepsHW': Number of steps to use in Markov chain
          (default: 100000).

        - 'markovChainDememorisationStepsHW': "Burn-in" time for
          Markov chain (default: 1000).

        """
        self.markovChainStepsHW=markovChainStepsHW
        self.markovChainDememorisationStepsHW=markovChainDememorisationStepsHW

        ArlequinWrapper.__init__(self, matrix=matrix, **kw)


        self.outputArpFile(lociList)
        self.outputArsFile(self.arsFilename, \
                           self.hwExactTest % \
                           (self.markovChainStepsHW, \
                            self.markovChainDememorisationStepsHW))
        self.outputRunFiles()
        self.runArlequin()

    def getHWExactTest(self):
        """Returns a dictionary of loci.

        Each dictionary element contains a tuple of the results from
        the Arlequin implementation of the Hardy-Weinberg exact test,
        namely:

        - number of genotypes,

        - observed heterozygosity,

        - expected heterozygosity,

        - the p-value,

        - the standard deviation,

        - number of steps,

        If locus is monomorphic, the HW exact test can't be run, and
        the contents of the dictionary element simply contains the
        string 'monomorphic', rather than the tuple of values.
        """
        
        outFile = os.path.join(self.arlSubdir, self.arlResPrefix + ".res" , self.arlResPrefix + ".htm")
        
        dataFound = 0
        headerFound = 0

        patt1 = re.compile(r"Exact test using a Markov chain")
        patt2 = re.compile(r"Locus  #Genot     Obs.Heter.   Exp.Heter.  P. value     s.d.  Steps done")
        patt3 = re.compile(r"^\s+(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\d+)")
        patt4 = re.compile(r"^\s+(\d+)\s+This locus is monomorphic: no test done.")

        hwExact = {}
        
        for line in open(outFile, 'r').readlines():
            matchobj2 = re.search(patt2, line)
            if matchobj2:
                headerFound = 1
            if headerFound:
                matchobj3 = re.search(patt3, line)
                matchobj4 = re.search(patt4, line)

                # look for values
                if matchobj3:
                    if self.debug:
                        print(matchobj3.groups())
                    locus, numGeno, obsHet, expHet, pval, sd, steps \
                           = matchobj3.groups()
                    hwExact[locus] = (int(numGeno), float(obsHet), \
                                      float(expHet), float(pval), float(sd), \
                                      int(steps))

                # if not, check to see if monomorphic
                else:
                    if matchobj4:
                        locus = matchobj4.group(1)
                        if self.debug:
                            print("locus", locus, "is monomorphic")
                        hwExact[locus] = 'monomorphic'
                        
        return hwExact


    

class ArlequinBatch:
    """A Python `wrapper' class for Arlequin.
    
    Given a delimited text file of multi-locus genotype data: provides
    methods to output Arlequin format data files and runtime info and
    execution of Arlequin itself.

    Is used to provide a `batch' (command line) mode for generating
    appropriate Arlequin input files and for forking Arlequin
    itself."""
    
    def __init__(self,
                 arpFilename,
                 arsFilename,
                 idCol,
                 prefixCols,
                 suffixCols,
                 windowSize,
                 mapOrder=None,
                 untypedAllele = '0',
                 arlequinPrefix = "arl_run",
                 debug=0):

        """Constructor for HaploArlequin object.

        Expects:

        - arpFilename: Arlequin filename (must have '.arp' file
          extension)

        - arsFilename: Arlequin settings filename (must have '.ars' file
          extension)

        - idCol: column in input file that contains the individual id.
        
        - prefixCols: number of columns to ignore before allele data
          starts
        
        - suffixCols: number of columns to ignore after allele data
          stops

        - windowSize: size of sliding window

        - mapOrder: list order of columns if different to column order in file
          (defaults to order in file)
        
        - untypedAllele:  (defaults to '0')
        
        - arlequinPrefix: prefix for all Arlequin run-time files
          (defaults to 'arl_run').

        - debug: (defaults to 0)
        
        """
        self.arpFilename = arpFilename
        self.arsFilename = arsFilename
        self.idCol = idCol
        self.prefixCols = prefixCols
        self.suffixCols = suffixCols
        self.mapOrder = mapOrder
        self.windowSize = windowSize
        self.arlequinPrefix = arlequinPrefix
        self.untypedAllele = untypedAllele
        self.debug = debug

        if arpFilename[-4:] == '.arp':
            self.arpFilename = arpFilename
            self.arlResPrefix = arpFilename[:-4]
        else:
            sys.exit("Error: Arlequin filename: %s does not have a .arp suffix", arpFilename)
        if arsFilename[-4:] == '.ars':
            self.arsFilename = arsFilename
        else:
            sys.exit("Error: Arlequin settings filename: %s does not have a .ars suffix", arpFilename)
            
    def _outputHeader(self, sampleCount):

        headerLines = []
        headerLines.append("""[Profile]
        
        Title=\"Arlequin sample run\"
        NbSamples=%d

             GenotypicData=1
             GameticPhase=0
             DataType=STANDARD
             LocusSeparator=WHITESPACE
             MissingData='%s'
             RecessiveData=0                         
             RecessiveAllele=\"null\" """ % (sampleCount, self.untypedAllele))

        headerLines.append("""[Data]

        [[Samples]]""")

        return headerLines

    def _outputSample (self, data, chunk, slice):

        # store output Arlequin-formatted genotypes in an array
        samples = []
        sampleLines = []
        

        if self.debug:
            print("_outputSample:chunk:", chunk)
        for line in data:
            words = line.split()
            unphase1 = "%10s 1 " % words[self.idCol]
            unphase2 = "%13s" % " "
            for i in chunk:
                print(chunk, i)
                allele = words[i]
                # don't output individual if *any* loci is untyped
                if allele == self.untypedAllele:
                    if self.debug:
                        print("untyped allele %s in (%s), (%s)"
                              % (allele, unphase1, unphase2))
                    break
                if ((chunk.index(i) + 1) % 2): unphase1 = unphase1 + " " + allele
                else: unphase2 = unphase2 + " " + allele
            else:
                # store formatted output samples
                samples.append(unphase1 + '\n')
                samples.append(unphase2 + '\n')

        # adjust the output count of samples for the `SamplesSize'
        # metadata field

        if len(samples) != 0:
            sampleLines.append("""
            
            SampleName=\"%s pop with %s individuals from loci %s\"
            SampleSize= %s
            SampleData={"""  % (self.arlResPrefix, len(samples)/2, str(slice), len(samples)/2))

            sampleLines.append('\n')

            # output previously-stored samples to stream only after
            # calculation of number of samples is made
            for line in samples:
                sampleLines.append(line)
            sampleLines.append("}")
            validSample = 1
        else:
            validSample = 0

        return sampleLines, validSample

    def _genChunk(self, offset, start, window, order):
        """Generate a list of adjacent columns for '.arp' file.

        Given a map 'order', generate the list of adjacent columns.

        Return a tuple consisting of two lists:

        - adjacent columns (NOTE: assumes column order starts at ZERO!!)
        - window on current map order
           (a `slice' of the overall map order,  NOTE: starts at ONE!!).
        """
        
        newChunk = []
        slice = order[start:(window + start)]
        for x in slice:
            # subtract one, since we want column numbers, not locus numbers
            col1 = offset + ((x-1)*2)
            col2 = col1 + 1
            newChunk.append(col1)
            newChunk.append(col2)
        return newChunk, slice

    def outputArlequin(self, data):
        """Outputs the specified .arp sample file.
        """
        
        if self.debug:
            print("Counted", len(data), "lines.")
        firstLine = data[0]

        # calculate the number of loci from the number of columns
        # and the prefix and suffix columns which can be ignored  
        cols = len(firstLine.split())
        colCount = cols - (self.prefixCols + self.suffixCols)

        # sanity check to ensure column number is even (2 alleles for
        # each loci)
        if colCount % 2 != 0:
            sys.exit ("Error: col count (%d) is not even" % colCount)
        else:
            locusCount = int((colCount)/2)

        # create default map order if none given
        if self.mapOrder == None:
            self.mapOrder = [i for i in range(1, locusCount + 1)]
            
        # sanity check for map order if it is given
        else:
            if (locusCount <= len(self.mapOrder)):
                sys.exit("Error: \
                there are %d loci but %d were given to sort order"\
                         % (locusCount, len(self.mapOrder)))
            else:
                for i in self.mapOrder:
                    if self.mapOrder.count(i) > 1:
                        sys.exit("Error: \
                        locus %d appears more than once in sort order" % i)
                    elif (i > locusCount) or (i < 0):
                        sys.exit("Error: \
                        locus %d out of range of number of loci" % i)
                        
            
        if self.debug:
            print("First line", firstLine, "has", cols, "columns and",
                  locusCount, "allele pairs")
            print("Map order:", self.mapOrder)

        # if windowSize is set to zero, the default to using
        # locusCount as windowSize

        if self.windowSize == 0:
            self.windowSize = locusCount

        #chunk = xrange(0, locusCount - self.windowSize + 1)
        chunk = range(0, len(self.mapOrder) - self.windowSize + 1)

        sampleCount = 0
        totalSamples = []

        for locus in chunk:

            # create the list of adjacent columns and the 'slice' of loci
            # within the current map order we are looking at
            colChunk, locusSlice = self._genChunk(self.prefixCols,
                                                  locus,
                                                  self.windowSize,
                                                  self.mapOrder)
            if self.debug:
                print(locus, colChunk, locusSlice)

            # generate the sample
            sampleLines, validSample = self._outputSample(data,
                                                          colChunk,
                                                          locusSlice)
            totalSamples.extend(sampleLines)
            sampleCount += validSample

        headerLines = self._outputHeader(sampleCount)

        if self.debug:
            print("sample count", sampleCount)
            
        # open specified arp
        self.arpFile = open(self.arpFilename, 'w')
        for line in headerLines:
            self.arpFile.write(line)
        for line in totalSamples:
            self.arpFile.write(line)
        # close .arp file
        self.arpFile.close()

    def _outputArlRunTxt(self, txtFilename, arpFilename):
        """Outputs the run-time Arlequin program file.
        """
        file = open(txtFilename, 'w')
        file.write("""%s
use_interf_settings
%s%s%s
0
0
end""" % (os.getcwd(), os.getcwd(), os.sep, arpFilename))

    def _outputArlRunArs(self, systemArsFilename, arsFilename):
        """Outputs the run-time Arlequin program file.
        """
        shutil.copy(arsFilename, systemArsFilename)

    def outputRunFiles(self):
        """Generates the expected '.txt' set-up files for Arlequin.
        """
        self._outputArlRunTxt(self.arlequinPrefix + ".txt", self.arpFilename)
        self._outputArlRunArs(self.arlequinPrefix + ".ars", self.arsFilename)
    
    def runArlequin(self):
        """Run the Arlequin haplotyping program.
         
        Forks a copy of 'arlecore.exe', which must be on 'PATH' to
        actually generate the desired statistics estimates from the
        generated '.arp' file.  """

        # spawn external Arlequin process
        os.system("arlecore.exe")

        # fix permissions on result directory because Arlequin is
        # brain-dead with respect to file permissions on Unix
        os.chmod(self.arlResPrefix + ".res", stat.S_IXGRP)

# this is called if this module is executed standalone
if __name__ == "__main__":

    usage_message = """Usage: Arlequin.py [OPTION] INPUTFILE ARPFILE ARSFILE
Process a tab-delimited INPUTFILE of alleles to produce an data files
(including ARPFILE), using parameters from ARSFILE for the Arlequin population
genetics program.

 -i, --idcol=NUM       column number of identifier (first column is zero)
 -l, --ignorelines=NUM number of header lines to ignore in in file
 -c, --cols=POS1,POS2  number of leading columns (POS1) before start and
                        number of trailing colums before the end (POS2) of
                        allele data (including IDCOL)
 -k, --sort=POS1,..    specify order of loci if different from column order
                        in file (must not repeat a locus)
 -w, --windowsize=NUM  number of loci involved in window size 
                        (note that this is half the number of allele columns)
 -u, --untyped=STR     the string that represents `untyped' alleles
                        (defaults to '****')
 -x, --execute         execute the Arlequin program
 -h, --help            this message
 -d, --debug           switch on debugging

  INPUTFILE   input text file
  ARPFILE     output Arlequin '.arp' project file
  ARSFILE     input Arlequin '.ars' settings file"""

    from getopt import getopt, GetoptError

    try: opts, args = \
         getopt(sys.argv[1:],"i:l:c:k:w:u:xhd",\
                ["idcol=", "ignorelines=", "cols=", "sort=", "windowsize=", "untyped=", "execute", "help","debug"])
    except GetoptError:
        sys.exit(usage_message)

    # default options
    idCol = 0
    ignoreLines = 0
    prefixCols = 1
    suffixCols = 0
    mapOrder = None
    windowSize = 0
    executeFlag = 0
    untypedAllele = '****'
    debug = 0

    # parse options
    for o, v in opts:
        if o in ("-i", "--idcol"):
            idCol = int(v)
        elif o in ("-l", "--ignorelines"):
            ignoreLines = int(v)
        elif o in ("-c", "--cols"):
            prefixCols, suffixCols = map(int, v.split(','))
        elif o in ("-k", "--sort"):
            mapOrder = map(int, v.split(','))
            print(mapOrder)
        elif o in ("-t", "--trailcols"):
            suffixCols = int(v)
        elif o in ("-w", "--windowsize"):
            windowSize = int(v)
        elif o in ("-u", "--untyped"):
            untypedAllele = v
        elif o in ("-x", "--execute"):
            executeFlag = 1
        elif o in ("-d", "--debug"):
            debug = 1
        elif o in ("-h", "--help"):
            sys.exit(usage_message)


    # check number of arguments
    if len(args) != 3:
        sys.exit(usage_message)

    # parse arguments
    inputFilename = args[0]
    arpFilename = args[1]
    arsFilename = args[2]
    
    batch = ArlequinBatch(arpFilename = arpFilename,
                          arsFilename = arsFilename,
                          idCol = idCol,
                          prefixCols = prefixCols,
                          suffixCols = suffixCols,
                          untypedAllele = untypedAllele,
                          mapOrder = mapOrder,
                          windowSize = windowSize,
                          debug=debug)
    # open file
    fileData = open(inputFilename, 'r').readlines()
    # run data ignoring `ignoreLines' worth of data
    batch.outputArlequin(fileData[ignoreLines:])
    batch.outputRunFiles()

    # run Arlequin if asked
    if executeFlag:
        batch.runArlequin()
