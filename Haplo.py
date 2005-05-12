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


"""Module for estimating haplotypes.

"""
import sys, string, os, re, cStringIO

from Arlequin import ArlequinBatch
from Utils import getStreamType, appendTo2dList

class Haplo:
    """*Abstract* base class for haplotype parsing/output.

    Currently a stub class (unimplemented).
    """
    pass

class HaploArlequin(Haplo):
    """Haplotype estimation implemented via Arlequin
    
    Outputs Arlequin format data files and runtime info, also runs and
    parses the resulting Arlequin data so it can be made available
    programatically to rest of Python framework.

    Delegates all calls Arlequin to an internally instantiated
    ArlequinBatch Python object called 'batch'.  """
    
    def __init__(self,
                 arpFilename,
                 idCol,
                 prefixCols,
                 suffixCols,
                 windowSize,
                 mapOrder = None,
                 untypedAllele = '0',
                 arlequinPrefix = "arl_run",
                 debug=0):

        """Constructor for HaploArlequin object.

        Expects:

        - arpFilename: Arlequin filename (must have '.arp' file
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
        self.arsFilename = 'arl_run.ars'
        self.idCol = idCol
        self.prefixCols = prefixCols
        self.suffixCols = suffixCols
        self.windowSize = windowSize
        self.arlequinPrefix = arlequinPrefix
        self.mapOrder = mapOrder
        self.untypedAllele = untypedAllele
        self.debug = debug
        
        # arsFilename is default because we generate it
        self.batch = ArlequinBatch(arpFilename = self.arpFilename,
                              arsFilename = self.arsFilename,
                              idCol = self.idCol,
                              prefixCols = self.prefixCols,
                              suffixCols = self.suffixCols,
                              windowSize = self.windowSize,
                              mapOrder = self.mapOrder,
                              debug = self.debug)

    def outputArlequin(self, data):
        """Outputs the specified .arp sample file.
        """
        self.batch.outputArlequin(data)

    def _outputArlRunArs(self, arsFilename):
        """Outputs the run-time Arlequin setting file.

        """
        file = open(arsFilename, 'w')
        file.write("""[Setting for Calculations]
TaskNumber=8
DeletionWeight=1.0
TransitionWeight=1.0
TranversionWeight=1.0
UseOriginalHaplotypicInformation=0
EliminateRedondHaplodefs=1
AllowedLevelOfMissingData=0.0
GameticPhaseIsKnown=0
HardyWeinbergTestType=0
MakeHWExactTest=0
MarkovChainStepsHW=100000
MarkovChainDememorisationStepsHW=1000
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
KeepNullDistrib=0""")
        file.close()

    def runArlequin(self):
        """Run the Arlequin haplotyping program.

        Generates the expected '.txt' set-up files for Arlequin, then
        forks a copy of 'arlecore.exe', which must be on 'PATH' to
        actually generate the haplotype estimates from the generated
        '.arp' file.
        """
        # generate the `standard' run file
        self.batch._outputArlRunTxt(self.arlequinPrefix + ".txt", self.arpFilename)
        # generate a customized settings file for haplotype estimation
        self._outputArlRunArs(self.arlequinPrefix + ".ars")
        
        # spawn external Arlequin process
        self.batch.runArlequin()
        
    def genHaplotypes(self):
        """Gets the haplotype estimates back from Arlequin.

        Parses the Arlequin output nonsense to retrieve the haplotype
        estimated data.  Returns a list of the sliding `windows' which
        consists of tuples.

        Each tuple consists of a:

        - dictionary entry (the haplotype-frequency) key-value pairs.

        - population name (original '.arp' file prefix)

        - sample count (number of samples for that window)

        - ordered list of loci considered
        """
        outFile = self.batch.arlResPrefix + ".res" + os.sep + self.batch.arlResPrefix + ".htm"
        dataFound = 0
        headerFound = 0

        haplotypes = []
        
        patt1 = re.compile("== Sample :[\t ]*(\S+) pop with (\d+) individuals from loci \[([^]]+)\]")
        patt2 = re.compile("    #   Haplotype     Freq.      s.d.")
        patt3 = re.compile("^\s+\d+\s+UNKNOWN(.*)")
        windowRange = range(1, self.windowSize)
        
        for line in open(outFile, 'r').readlines():
            matchobj = re.search(patt1, line)
            if matchobj:
                headerFound = 1
                popName = matchobj.group(1)
                sampleCount = matchobj.group(2)
                liststr = matchobj.group(3)
                # convert into list of loci
                lociList = map(int, string.split(liststr, ','))
                freqs = {}
                
            if dataFound:
                if line != os.linesep:
                    if self.debug:
                        print string.rstrip(line)
                    matchobj = re.search(patt3, line)
                    if matchobj:
                        cols = string.split(matchobj.group(1))
                        haplotype = cols[2]
                        for i in windowRange:
                            haplotype = haplotype + "_" + cols[2+i]
                        freq = float(cols[0])*float(sampleCount)
                        freqs[haplotype] = freq
                    else:
                        sys.exit("Error: unknown output in arlequin line: %s" % line)
                else:
                    headerFound = 0
                    dataFound = 0
                    haplotypes.append((freqs, popName, sampleCount, lociList))
            if re.match(patt2, line):
                dataFound = 1

        return haplotypes

class Emhaplofreq(Haplo):
    """Haplotype and LD estimation implemented via emhaplofreq.

    This is essentially a wrapper to a Python extension built on top
    of the 'emhaplofreq' command-line program.

    Will refuse to estimate haplotypes longer than that defined by
    'emhaplofreq'.
    
    """
    def __init__(self, locusData,
                 debug=0,
                 untypedAllele='****',
                 stream=None):

        # import the Python-to-C module wrapper
        # lazy importation of module only upon instantiation of class
        # to save startup costs of invoking dynamic library loader
        import _Emhaplofreq

        # assign module to an instance variable so it is available to
        # other methods in class
        self._Emhaplofreq = _Emhaplofreq
        
        self.matrix = locusData
        self.untypedAllele = untypedAllele
        
        rows, cols = self.matrix.shape
        self.totalNumIndiv = rows
        self.totalLociCount = cols / 2
        
        self.debug = debug

        # initialize flag
        self.maxLociExceeded = 0

        # must be passed a stream
        if stream:
            self.stream = stream
        else:
            sys.exit("Emhaplofreq constructor must be passed a stream, output is only available in stream form")
                
        # create an in-memory file instance for the C program to write
        # to; this remains in effect until a call to 'serializeTo()'.
        
        #import cStringIO
        #self.fp = cStringIO.StringIO()

    def serializeStart(self):
        """Serialize start of XML output to XML stream"""
        self.stream.opentag('emhaplofreq')
        self.stream.writeln()

    def serializeEnd(self):
        """Serialize end of XML output to XML stream"""
        self.stream.closetag('emhaplofreq')
        self.stream.writeln()

    def _runEmhaplofreq(self, locusKeys=None,
                        permutationFlag=None,
                        permutationPrintFlag=0,
                        numInitCond=50,
                        numPermutations=1001,
                        numPermuInitCond=5,
                        haploSuppressFlag=None,
                        showHaplo=None,
                        mode=None):
        
        """Internal method to call _Emhaplofreq shared library.

        Format of 'locusKeys' is a string as per estHaplotypes():

        - permutationFlag: sets whether permutation test will be
          performed.  No default.

        - permutationPrintFlag: sets whether the result from
          permutation output run will be included in the output XML.
          Default: 0 (disabled).

        - numInitConds: sets number of initial conditions before
          performing the permutation test. Default: 50.

        - numPermutations: sets number of permutations that will be
          performed if 'permutationFlag' *is* set.  Default: 1001.

        - numPermuInitConds: sets number of initial conditions tried
          per-permutation.  Default: 5.

        - haploSuppressFlag: sets whether haplotype information is
          generated in the output.   No default.

        """

        # create an in-memory file instance for the C program to write
        # to; this remains in effect until end of method
        fp = cStringIO.StringIO()

        if (permutationFlag == None) or (haploSuppressFlag == None):
            sys.exit("must pass a permutation or haploSuppressFlag to _runEmhaplofreq!")
	
	# make all locus keys uppercase
	locusKeys = string.upper(locusKeys)

        # if no locus list passed, assume calculation of entire data
        # set
        if locusKeys == None:
            # create key for entire matrix
            locusKeys = ':'.join(self.matrix.colList)

        for group in string.split(locusKeys, ','):
            
            # get the actual number of loci being estimated
            lociCount = len(string.split(group,':'))

            if self.debug:
                print "number of loci for haplotype est:", lociCount

                print lociCount, self._Emhaplofreq.MAX_LOCI

            if lociCount <= self._Emhaplofreq.MAX_LOCI:

                # filter-out all individual untyped at any position
                subMatrix = appendTo2dList(self.matrix.filterOut(group, self.untypedAllele), ':')

                # calculate the new number of individuals emhaplofreq is
                # being run on
                groupNumIndiv = len(subMatrix)

                if self.debug:
                    print "debug: key for matrix:", group
                    print "debug: subMatrix:", subMatrix
                    print "debug: dump matrix in form for command-line input"
                    for line in range(0, len(subMatrix)):
                        theline = subMatrix[line]
                        print "dummyid",
                        for allele in range(0, len(theline)):
                            print theline[allele], " ",
                        print
                    
                fp.write(os.linesep)

                modeAttr = "mode=\"%s\"" % mode
                haploAttr = "showHaplo=\"%s\"" % showHaplo
                lociAttr = "loci=\"%s\"" % group

                if groupNumIndiv > self._Emhaplofreq.MAX_ROWS:
                    fp.write("<group %s role=\"too-many-lines\" %s %s/>%s" % (modeAttr, lociAttr, haploAttr, os.linesep))
                    continue
                # if nothing left after filtering, simply continue
                elif groupNumIndiv == 0:
                    fp.write("<group %s role=\"no-data\" %s %s/>%s" % (modeAttr, lociAttr, haploAttr, os.linesep))
                    continue

                if mode:
                    fp.write("<group %s %s %s>%s" % (modeAttr, lociAttr, haploAttr, os.linesep))
                else:
                    sys.exit("A 'mode' for emhaplofreq must be specified")
                
##                 if permutationFlag and haploSuppressFlag:
##                     fp.write("<group mode=\"LD\" loci=\"%s\">%s" % (group, os.linesep))
##                 elif permutationFlag == 0 and haploSuppressFlag == 0:
##                     fp.write("<group mode=\"haplo\" loci=\"%s\">%s" % (group, os.linesep))
##                 elif permutationFlag and haploSuppressFlag == 0:
##                     fp.write("<group mode=\"haplo-LD\" loci=\"%s\">%s" % (group, os.linesep))
##                 else:
##                     sys.exit("Unknown combination of permutationFlag and haploSuppressFlag")
                fp.write(os.linesep)

                fp.write("<individcount role=\"before-filtering\">%d</individcount>" % self.totalNumIndiv)
                fp.write(os.linesep)
                
                fp.write("<individcount role=\"after-filtering\">%d</individcount>" % groupNumIndiv)
                fp.write(os.linesep)
                
                # pass this submatrix to the SWIG-ed C function
                self._Emhaplofreq.main_proc(fp,
                                            subMatrix,
                                            lociCount,
                                            groupNumIndiv,
                                            permutationFlag,
                                            haploSuppressFlag,
                                            numInitCond,
                                            numPermutations,
                                            numPermuInitCond,
                                            permutationPrintFlag)

                fp.write("</group>")

                if self.debug:
                    # in debug mode, print the in-memory file to sys.stdout
                    lines = string.split(fp.getvalue(), os.linesep)
                    for i in lines:
                        print "debug:", i

            else:
                fp.write("Couldn't estimate haplotypes for %s, num loci: %d exceeded max loci: %d" % (group, lociCount, self._Emhaplofreq.MAX_LOCI))
                fp.write(os.linesep)

        # writing to file must be called *after* all output has been
        # generated to cStringIO instance "fp"

        self.stream.write(fp.getvalue())
        fp.close()

        # flush any buffered output to the stream
        self.stream.flush()

    def estHaplotypes(self,
                      locusKeys=None,
                      numInitCond=None):
        """Estimate haplotypes for listed groups in 'locusKeys'.

        Format of 'locusKeys' is a string consisting of:

        - comma (',') separated haplotypes blocks for which to estimate
          haplotypes

        - within each `block', each locus is separated by colons (':')

        e.g. '*DQA1:*DPB1,*DRB1:*DQB1', means to est. haplotypes for
         'DQA1' and 'DPB1' loci followed by est. of haplotypes for
         'DRB1' and 'DQB1' loci.
        """
        self._runEmhaplofreq(locusKeys=locusKeys,
                             numInitCond=numInitCond,
                             permutationFlag=0,
                             haploSuppressFlag=0,
                             showHaplo='yes',
                             mode='haplo')
        

    def estLinkageDisequilibrium(self,
                                 locusKeys=None,
                                 permutationPrintFlag=0,
                                 numInitCond=None,
                                 numPermutations=None,
                                 numPermuInitCond=None):
        """Estimate linkage disequilibrium (LD) for listed groups in
        'locusKeys'.

        Format of 'locusKeys' is a string consisting of:

        - comma (',') separated haplotypes blocks for which to estimate
          haplotypes

        - within each `block', each locus is separated by colons (':')

        e.g. '*DQA1:*DPB1,*DRB1:*DQB1', means to est. LD for
         'DQA1' and 'DPB1' loci followed by est. of LD for
         'DRB1' and 'DQB1' loci.
        """
        self._runEmhaplofreq(locusKeys,
                             permutationFlag=1,
                             permutationPrintFlag=permutationPrintFlag,
                             numInitCond=numInitCond,
                             numPermutations=numPermutations,
                             numPermuInitCond=numPermuInitCond,
                             haploSuppressFlag=1,
                             showHaplo='no',
                             mode='LD')

    def allPairwise(self,
                    permutationPrintFlag=0,
                    numInitCond=None,
                    numPermutations=None,
                    numPermuInitCond=None,
                    haploSuppressFlag=None,
                    haplosToShow=None,
                    mode=None):
        """Run pairwise statistics.

        Estimate pairwise statistics for a given set of loci.
        Depending on the flags passed, can be used to estimate both LD
        (linkage disequilibrium) and HF (haplotype frequencies), an
        optional permutation test on LD can be run """

        if numPermutations > 0:
            permuMode = 'with-permu'
            permutationFlag = 1
        else:
            permuMode = 'no-permu'
            permutationFlag = 0

        if mode == None:
            mode = 'all-pairwise-ld-' + permuMode

        loci = self.matrix.colList

        # FIXME: hack to determine whether we are analysing sequence
        # we use a regex to match anything in the form A_32 or A_-32
        # this should be passed as a parameter
        print loci[0]
        if re.search("[a-zA-Z]+_[-]?[0-9]+", loci[0]):
            sequenceData = 1
        else:
            sequenceData = 0
        
        li = []
        for i in loci:
            lociCopy = loci[:]
            indexRemoved = loci.index(i)
            del lociCopy[indexRemoved]
            for j in lociCopy:
                if ((i+':'+j) in li) or ((j+':'+i) in li):
                    pass
                else:
                    # if we are running sequence data restrict pairs
                    # to pairs within *within* the same gene locus
                    if sequenceData:
                        genelocus_i = string.split(i,'_')[0]
                        genelocus_j = string.split(j,'_')[0]
                        # only append if gene is *within* the same locus
                        if genelocus_i == genelocus_j:
                            li.append(i+':'+j)
                    else:
                        li.append(i+':'+j)

        if self.debug:
            print li, len(li)

        for pair in li:
            # generate the reversed order in case user
            # specified it in the opposite sense
            sp = string.split(pair,':')
            reversedPair =  sp[1] + ':' + sp[0]

            if (pair in haplosToShow) or (reversedPair in haplosToShow):
                showHaplo = 'yes'
            else:
                showHaplo = 'no'

            self._runEmhaplofreq(pair,
                                 permutationFlag=permutationFlag,
                                 permutationPrintFlag=permutationPrintFlag,
                                 numInitCond=numInitCond,
                                 numPermutations=numPermutations,
                                 numPermuInitCond=numPermuInitCond,
                                 haploSuppressFlag=haploSuppressFlag,
                                 showHaplo=showHaplo,
                                 mode=mode)

            # def allPairwiseLD(self, haplosToShow=None):
            #     """Estimate all pairwise LD and haplotype frequencies.
            
            #     Estimate the LD (linkage disequilibrium)for each pairwise set
            #     of loci.
            #     """
            #     self.allPairwise(permutationFlag=0,
            #                      haploSuppressFlag=0,
            #                      mode='all-pairwise-ld-no-permu')
            
            # def allPairwiseLDWithPermu(self, haplosToShow=None):
            #     """Estimate all pairwise LD.
            
            #     Estimate the LD (linkage disequilibrium)for each pairwise set
            #     of loci.
            #     """
            #     self.allPairwise(permutationFlag=1,
            #                      haploSuppressFlag=0,
            #                      mode='all-pairwise-ld-with-permu')


        

