#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2003-2005. The Regents of the University of California (Regents)
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
import sys, os, re, io
import numpy
import math
import itertools as it
from tempfile import TemporaryDirectory

from PyPop.Arlequin import ArlequinBatch
from PyPop.Utils import getStreamType, appendTo2dList, GENOTYPE_SEPARATOR, GENOTYPE_TERMINATOR, XMLOutputStream
from PyPop.DataTypes import checkIfSequenceData, getLocusPairs

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

        Parses the Arlequin output to retrieve the haplotype estimated
        data.  Returns a list of the sliding `windows' which consists
        of tuples.

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
        
        patt1 = re.compile(r"== Sample :[\t ]*(\S+) pop with (\d+) individuals from loci \[([^]]+)\]")
        patt2 = re.compile(r"    #   Haplotype     Freq.      s.d.")
        patt3 = re.compile(r"^\s+\d+\s+UNKNOWN(.*)")
        windowRange = range(1, self.windowSize)
        
        for line in open(outFile, 'r').readlines():
            matchobj = re.search(patt1, line)
            if matchobj:
                headerFound = 1
                popName = matchobj.group(1)
                sampleCount = matchobj.group(2)
                liststr = matchobj.group(3)
                # convert into list of loci
                lociList = list(map(int, liststr.split(',')))
                freqs = {}
                
            if dataFound:
                if line != os.linesep:
                    if self.debug:
                        print(line.rstrip())
                    matchobj = re.search(patt3, line)
                    if matchobj:
                        cols = matchobj.group(1).split()
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
                 stream=None,
                 testMode=False):

        # import the Python-to-C module wrapper
        # lazy importation of module only upon instantiation of class
        # to save startup costs of invoking dynamic library loader
        from PyPop import _Emhaplofreq

        # assign module to an instance variable so it is available to
        # other methods in class
        self._Emhaplofreq = _Emhaplofreq

        # FIXME: by default assume we are not dealing sequence data
        self.sequenceData = 0
        
        self.matrix = locusData
        self.untypedAllele = untypedAllele
        
        rows, cols = self.matrix.shape
        self.totalNumIndiv = rows
        self.totalLociCount = cols / 2
        
        self.debug = debug

        # initialize flag
        self.maxLociExceeded = 0

        # set "testing" flag to "1" if testMode enabled
        if testMode:
            self.testing = 1
        else:
            self.testing = 0

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
                        mode=None,
                        testing=0):
        
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

        # create an in-memory file instance to append output to
        # to; this remains in effect until end of method
        fp = io.StringIO()

        if (permutationFlag == None) or (haploSuppressFlag == None):
            sys.exit("must pass a permutation or haploSuppressFlag to _runEmhaplofreq!")

        # make all locus keys uppercase
        locusKeys = locusKeys.upper()

        # if no locus list passed, assume calculation of entire data
        # set
        if locusKeys == None:
            # create key for entire matrix
            locusKeys = ':'.join(self.matrix.colList)

        for group in locusKeys.split(','):
           
            # get the actual number of loci being estimated
            lociCount = len(group.split(':'))

            if self.debug:
                print("number of loci for haplotype est:", lociCount)

                print(lociCount, self._Emhaplofreq.MAX_LOCI)

            if lociCount <= self._Emhaplofreq.MAX_LOCI:

                # filter-out all individual untyped at any position
                #subMatrix = appendTo2dList(self.matrix.filterOut(group, self.untypedAllele), ':')
                subMatrix = appendTo2dList(self.matrix.filterOut(group, self.untypedAllele), GENOTYPE_SEPARATOR)

                # calculate the new number of individuals emhaplofreq is
                # being run on
                groupNumIndiv = len(subMatrix)

                if self.debug:
                    print("debug: key for matrix:", group)
                    print("debug: subMatrix:", subMatrix)
                    print("debug: dump matrix in form for command-line input")
                    for line in range(0, len(subMatrix)):
                        theline = subMatrix[line]
                        print("dummyid"),
                        for allele in range(0, len(theline)):
                            print(theline[allele], " "),
                        print()
                    
                fp.write('\n')

                if self.sequenceData:
                    metaLoci = group.split(':')[0].split('_')[0]
                else:
                    metaLoci = None

                modeAttr = "mode=\"%s\"" % mode
                haploAttr = "showHaplo=\"%s\"" % showHaplo

                if metaLoci:
                    lociAttr = "loci=\"%s\" metaloci=\"%s\"" % (group, metaLoci)
                else:
                    lociAttr = "loci=\"%s\"" % group

                # check maximum length of allele
                maxAlleleLength = 0
                for line in range(0, len(subMatrix)):
                    theline = subMatrix[line]
                    for allelePos in range(0, len(theline)):
                        allele = theline[allelePos]
                        if len(allele) > maxAlleleLength:
                            maxAlleleLength = len(allele)
                        if len(allele) > (self._Emhaplofreq.NAME_LEN)-2:
                            print("WARNING: '%s' (%d) exceeds max allele length (%d) for LD and haplo est in %s" % (allele, len(allele), self._Emhaplofreq.NAME_LEN-2, lociAttr))

                if groupNumIndiv > self._Emhaplofreq.MAX_ROWS:
                    fp.write("<group %s role=\"too-many-lines\" %s %s/>%s" % (modeAttr, lociAttr, haploAttr, '\n'))
                    continue
                # if nothing left after filtering, simply continue
                elif groupNumIndiv == 0:
                    fp.write("<group %s role=\"no-data\" %s %s/>%s" % (modeAttr, lociAttr, haploAttr, '\n'))
                    continue
                elif maxAlleleLength > (self._Emhaplofreq.NAME_LEN-2):
                    fp.write("<group %s role=\"max-allele-length-exceeded\" %s %s>%d</group>%s" % (modeAttr, lociAttr, haploAttr, self._Emhaplofreq.NAME_LEN-2, '\n'))
                    continue
                
                if mode:
                    fp.write("<group %s %s %s>%s" % (modeAttr, lociAttr, haploAttr, '\n'))
                else:
                    sys.exit("A 'mode' for emhaplofreq must be specified")
                
##                 if permutationFlag and haploSuppressFlag:
##                     fp.write("<group mode=\"LD\" loci=\"%s\">%s" % (group, '\n'))
##                 elif permutationFlag == 0 and haploSuppressFlag == 0:
##                     fp.write("<group mode=\"haplo\" loci=\"%s\">%s" % (group, '\n'))
##                 elif permutationFlag and haploSuppressFlag == 0:
##                     fp.write("<group mode=\"haplo-LD\" loci=\"%s\">%s" % (group, '\n'))
##                 else:
##                     sys.exit("Unknown combination of permutationFlag and haploSuppressFlag")
                fp.write('\n')

                fp.write("<individcount role=\"before-filtering\">%d</individcount>" % self.totalNumIndiv)
                fp.write('\n')
                
                fp.write("<individcount role=\"after-filtering\">%d</individcount>" % groupNumIndiv)
                fp.write('\n')

                with TemporaryDirectory() as tmp:
                    # generates temporary directory and filename, and cleans-up after block ends
                    xml_tmp_filename=os.path.join(tmp, 'emhaplofreq.out.xml')

                    # pass this submatrix to the SWIG-ed C function
                    self._Emhaplofreq.main_proc(xml_tmp_filename, subMatrix, lociCount, groupNumIndiv, permutationFlag, haploSuppressFlag, numInitCond, numPermutations, numPermuInitCond, permutationPrintFlag, testing, GENOTYPE_SEPARATOR, GENOTYPE_TERMINATOR)

                    # read the generated contents of the temporary XML file
                    with open(xml_tmp_filename, 'r') as tmp_fp:
                        # copy XML output file to our StringIO
                        fp.write(tmp_fp.read())

                fp.write("</group>")

                if self.debug:
                    # in debug mode, print the in-memory file to sys.stdout
                    lines = fp.getvalue().split(os.linesep)
                    for i in lines:
                        print("debug:", i)

            else:
                fp.write("Couldn't estimate haplotypes for %s, num loci: %d exceeded max loci: %d" % (group, lociCount, self._Emhaplofreq.MAX_LOCI))
                fp.write('\n')

        # writing to file must be called *after* all output has been
        # collected in the StringIO instance "fp"

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
                             mode='haplo',
                             testing=self.testing)
        

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
                             mode='LD',
                             testing=self.testing)

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

        self.sequenceData = checkIfSequenceData(self.matrix)
        li = getLocusPairs(self.matrix, self.sequenceData)

        if self.debug:
            print(li, len(li))

        for pair in li:
            # generate the reversed order in case user
            # specified it in the opposite sense
            sp = pair.split(':')
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
                                 mode=mode,
                                 testing=self.testing)

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


def _compute_LD(haplos, freqs, compute_ALD=False, debug=False):
    """Compute LD for pairwise haplotypes from haplotype names and frequencies

    Make standalone so it can be used by any class
    """

    unique_alleles1 = numpy.unique(haplos[:,0])
    unique_alleles2 = numpy.unique(haplos[:,1])

    # FIXME: should merge the two into one loop
    freq1_dict = {}
    for item, allele in enumerate(haplos[:,0]):
        if allele in freq1_dict:
            freq1_dict[allele] += freqs[item]
        else:
            freq1_dict[allele] = freqs[item]

    freq2_dict = {}
    for item, allele in enumerate(haplos[:,1]):
        if allele in freq2_dict:
            freq2_dict[allele] += freqs[item]
        else:
            freq2_dict[allele] = freqs[item]

    # create an equivalent of a data frame with all haplotypes
    # initially as a list
    allhaplos = []
    for row in list(it.product(unique_alleles1, unique_alleles2)):
        # get current alleles
        allele1, allele2 = row
        # loop through the haplotype frequency to get the haplotype frequency
        # if it exists for this allele1, allele2 pair
        i = 0
        hap_freq = 0.0
        for hap in haplos:
            if hap[0] == allele1 and hap[1] == allele2:
                hap_freq = freqs[i]
            i += 1

        # add the hap and allele frequencies
        newrow = (allele1, allele2, freq1_dict[allele1], freq2_dict[allele2], hap_freq)
        allhaplos.append(newrow)

    # convert to numpy structured array
    allhaplos = numpy.array(allhaplos, dtype=[('allele1', 'O'), ('allele2', 'O'), ('allele.freq1', float), ('allele.freq2', float), ('haplo.freq', float)])

    # now we extract the columns we need for the computations
    hap_prob = allhaplos['haplo.freq']
    a_freq1 = allhaplos['allele.freq1']
    a_freq2 = allhaplos['allele.freq2']
    alleles1 = allhaplos['allele1']
    alleles2 = allhaplos['allele2']

    # get the maximum size of array
    num_allpossible_haplos = len(allhaplos)

    ## compute Wn & Dprime
    zero = numpy.array([0.0])
    dprime_den = zero.repeat(num_allpossible_haplos)
    d_ij = hap_prob - a_freq1 * a_freq2
    den_lt0 = numpy.minimum( a_freq1*a_freq2, (1-a_freq1)*(1-a_freq2) )
    den_ge0 = numpy.minimum( (1-a_freq1)*a_freq2, a_freq1*(1-a_freq2) )
    dprime_den[d_ij < 0] = den_lt0[d_ij < 0]
    dprime_den[d_ij >=0] = den_ge0[d_ij >=0]
    dprime_ij = d_ij/dprime_den

    if debug:
        print ("dprime_den:", dprime_den)

        print ("i a_freq1 a_freq2 d_ij dprime hap_prob haplo")
        for i in range(num_allpossible_haplos):
            print (i, a_freq1[i], a_freq2[i], d_ij[i], dprime_ij[i], hap_prob[i], "%s:%s" % (alleles1[i], alleles2[i]))

    dp_temp = abs(dprime_ij)*a_freq1*a_freq2
    dprime = dp_temp.sum()
    if debug: print ("Dprime: ", dprime)

    w_ij = (d_ij*d_ij) / (a_freq1*a_freq2)
    w = w_ij.sum()
    # FIXME: NOT SURE THIS SYNTAX FOR 'min' IS CORRECT (OR GOOD)
    # WANT:  wn <- sqrt( w / (min( length(unique(alleles1)), length(unique(alleles2)) ) - 1.0) )
    w_den = numpy.minimum(numpy.unique(alleles1).size*1.0, numpy.unique(alleles2).size*1.0) - 1.0
    wn = numpy.sqrt( w / w_den )
    if debug: print ("Wn: ", wn)

    if compute_ALD:
        ## compute ALD
        F_1 = 0.0
        F_2_1 = 0.0
        F_2 = 0.0
        F_1_2 = 0.0
        for i in numpy.unique(alleles1):
           af_1 = numpy.unique(a_freq1[alleles1==i])[0]  # take the first element of ndarray (default behaviour)
           F_1 = F_1 + af_1**2
           F_2_1 = F_2_1 + ((hap_prob[alleles1==i]**2)/af_1).sum()
        for i in numpy.unique(alleles2):
           af_2 = numpy.unique(a_freq2[alleles2==i])[0]
           F_2 = F_2 + af_2**2
           F_1_2 = F_1_2 + ((hap_prob[alleles2==i]**2)/af_2).sum()
        if F_2 == 1.0:
           F_2_1_prime = numpy.nan  
           ALD_2_1 = numpy.nan
        else:
           F_2_1_prime = (F_2_1 - F_2)/(1 - F_2)
           ALD_2_1 = math.sqrt(F_2_1_prime)
        if F_1 == 1:
           F_1_2_prime = numpy.nan
           ALD_1_2 = numpy.nan
        else:
           F_1_2_prime = (F_1_2 - F_1)/(1 - F_1)
           ALD_1_2 = math.sqrt(F_1_2_prime)
        if debug:
            print ("ALD_1_2:", ALD_1_2)
            print ("ALD_2_1:", ALD_2_1)
            # FIXME: NOT SURE YOU CAN ASSIGN nan IN ABOVE if()
    else:
        ALD_1_2 = None
        ALD_2_1 = None

    # FIXME: eventually need to add return of dprime_ij etc.
    return dprime, wn, ALD_1_2, ALD_2_1

class Haplostats(Haplo):
    """Haplotype and LD estimation implemented via haplo-stats.

    This is a wrapper to a portion of the 'haplo.stats' R package
    
    """
    def __init__(self, locusData,
                 debug=0,
                 untypedAllele='****',
                 stream=None,
                 testMode=False):

        # import the Python-to-C module wrapper
        # lazy importation of module only upon instantiation of class
        # to save startup costs of invoking dynamic library loader
        from PyPop import _Haplostats

        # assign module to an instance variable so it is available to
        # other methods in class
        self._Haplostats = _Haplostats

        # FIXME: by default assume we are not dealing sequence data
        self.sequenceData = 0
        
        self.matrix = locusData
        self.untypedAllele = untypedAllele
        
        rows, cols = self.matrix.shape
        self.totalNumIndiv = rows
        self.totalLociCount = cols / 2
        self.debug = debug
        self.testMode = testMode
        if stream:
            self.stream = stream
        else:  # create a stream if none given
            self.stream = XMLOutputStream(io.StringIO())            

    def serializeStart(self):
        """Serialize start of XML output to XML stream"""
        self.stream.opentag('haplostats')
        self.stream.writeln()

    def serializeEnd(self):
        """Serialize end of XML output to XML stream"""
        self.stream.closetag('haplostats')
        self.stream.writeln()

    def estHaplotypes(self,
                      locusKeys=None,
                      weight=None,
                      control=None,
                      numInitCond=10,
                      testMode=False):
        """Estimate haplotypes for the submatrix given in locusKeys, if
        locusKeys is None, assume entire matrix
        
        LD is estimated if there are locusKeys consists of only two loci

        FIXME: this does *not* yet remove missing data before haplotype estimations
        """

        # if wildcard, or not set, do all matrix
        if locusKeys == '*' or locusKeys == None:
            locusKeys=':'.join(self.matrix.colList)

        geno = self.matrix.getNewStringMatrix(locusKeys)

        n_loci = geno.colCount
        n_subject = geno.rowCount

        subj_id = list(range(1, n_subject + 1))
        if n_loci < 2:
            print ("Must have at least 2 loci for haplotype estimation!")
            exit(-1)

        # set up weight
        if not weight:
            weight = [1.0]*n_subject
        if len(weight) != n_subject:
            print ("Length of weight != number of subjects (nrow of geno)")
            exit(-1)

        temp_geno = geno.convertToInts()   # simulates setupGeno
        geno_vec = temp_geno.flattenCols() # gets the columns as integers

        n_alleles = []
        allele_labels = []

        for locus in geno.colList:
            unique_alleles = geno.getUniqueAlleles(locus)
            allele_labels.append(unique_alleles)
            n_alleles.append(len(unique_alleles))

        # Compute the max number of pairs of haplotypes over all subjects
        max_pairs = temp_geno.countPairs()
        max_haps = 2*sum(max_pairs)

        # FIXME: do we need this?
        if max_haps > control['max_haps_limit']:
            max_haps = control['max_haps_limit']

        loci_insert_order = list(range(0, n_loci))

        # FIXME: hardcode
        if testMode:
            iseed1 = 18717; iseed2= 16090; iseed3=14502
            random_start = 0
        else:
            seed_array = numpy.random.random(3)
            iseed1 = int(10000 + 20000*seed_array[0])
            iseed2 = int(10000 + 20000*seed_array[1])
            iseed3 = int(10000 + 20000*seed_array[2])
            random_start = control['random_start']

        converge, lnlike, n_u_hap, n_hap_pairs, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code = \
                  self._haplo_em_fitter(n_loci,
                                        n_subject,
                                        weight,
                                        geno_vec,
                                        n_alleles,
                                        max_haps,
                                        control['max_iter'],
                                        loci_insert_order,
                                        control['min_posterior'],
                                        control['tol'],
                                        control['insert_batch_size'],
                                        random_start,
                                        iseed1,
                                        iseed2,
                                        iseed3,
                                        control['verbose'])

        if numInitCond > 1:
            for i in range(1, numInitCond):
                if testMode:
                    iseed1 = iseed1 + i*300
                    iseed2 = iseed2 + i*200
                    iseed3 = iseed3 + i*100
                    random_start = 1   # need this in testMode too, apparently
                else:
                    seed_array = numpy.random.random(3)
                    iseed1 = int(10000 + 20000*seed_array[0])
                    iseed2 = int(10000 + 20000*seed_array[1])
                    iseed3 = int(10000 + 20000*seed_array[2])
                    # FIXME: check why this is the case
                    # original R code always uses random_start on second and subsequent
                    # initial conditions, regardless of how the control['random_start'] is set
                    random_start = 1   

                if self.debug:
                    print ("random seeds for initial condition", i, ":", iseed1, iseed2, iseed3)

                converge_new, lnlike_new, n_u_hap_new, n_hap_pairs_new, hap_prob_new, \
                              u_hap_new, u_hap_code_new, subj_id_new, post_new, hap1_code_new, \
                              hap2_code_new = \
                              self._haplo_em_fitter(n_loci,
                                                    n_subject,
                                                    weight,
                                                    geno_vec,
                                                    n_alleles,
                                                    max_haps,
                                                    control['max_iter'],
                                                    loci_insert_order,
                                                    control['min_posterior'],
                                                    control['tol'],
                                                    control['insert_batch_size'],
                                                    random_start,
                                                    iseed1,
                                                    iseed2,
                                                    iseed3,
                                                    control['verbose'])

                if lnlike_new > lnlike:
                    if self.debug:
                        print ("found a better lnlikelihood!", lnlike_new)
                    # FIXME: need more elegant data structure
                    converge, lnlike, n_u_hap, n_hap_pairs, hap_prob, \
                              u_hap, u_hap_code, subj_id, post, hap1_code, \
                              hap2_code = \
                              converge_new, lnlike_new, n_u_hap_new, n_hap_pairs_new, hap_prob_new, \
                              u_hap_new, u_hap_code_new, subj_id_new, post_new, hap1_code_new, \
                              hap2_code_new 

        # convert u_hap back into original allele names
        haplotype = numpy.array(u_hap, dtype='O').reshape(n_u_hap, -1)
        for j in range(0, n_loci):
            for i in range(0, n_u_hap):
                allele_offset = haplotype[i,j] - 1 #  integers are offset by 1
                allele_id = allele_labels[j][allele_offset]
                haplotype[i,j] = allele_id

        # convert back to offset by 1 for R compatibility check
        hap1_code = [i+1 for i in hap1_code]
        hap2_code = [i+1 for i in hap2_code]
        u_hap_code = [i+1 for i in u_hap_code]
        subj_id = [i+1 for i in subj_id]

        # FIXME: are these, strictly speaking, necessary in Python context?
        # these arrays can be regenerated from the vectors at any time
        uhap_df = numpy.c_[u_hap_code, hap_prob]
        subj_df = numpy.c_[subj_id, hap1_code, hap2_code]

        # XML output for group here
        self.stream.opentag('group', mode="all-pairwise-ld-no-permu", loci=locusKeys, showHaplo="yes")
        self.stream.writeln()
        # FIXME: implement ('uniquepheno') ?
        self.stream.tagContents('uniquegeno', "%d" % n_hap_pairs)
        self.stream.writeln()
        self.stream.tagContents('haplocount', "%d" % n_u_hap)
        self.stream.writeln()
        self.stream.opentag('haplotypefreq')
        self.stream.tagContents('numInitCond', "%d" % numInitCond)
        self.stream.writeln()
        self.stream.tagContents('loglikelihood', "%g" % lnlike, role="no-ld")
        self.stream.writeln()
        self.stream.writeln()
        self.stream.tagContents('condition', "", role='converged')
        self.stream.writeln()

        for i in range(0, n_u_hap):
            hapname = ""
            for j in range(0, n_loci):
                hapname += "%s" % haplotype[i, j]
                if j < n_loci - 1:
                    hapname += GENOTYPE_SEPARATOR

            self.stream.opentag('haplotype', name=hapname)
            self.stream.tagContents('frequency', str(hap_prob[i]))
            # FIXME: check computation of numCopies
            # self.stream.tagContents('numCopies', str(hap_prob[i] * n_u_hap))
            self.stream.closetag('haplotype')
            self.stream.writeln()

        self.stream.closetag('haplotypefreq')
        self.stream.writeln()

        # LD calculations, and only do and output to XML for two locus haplotypes
        if n_loci == 2:
            dprime, Wn, ALD_1_2, ALD_2_1 = _compute_LD(haplotype, hap_prob, compute_ALD=True, debug=self.debug)  

            # output LD to XML
            # FIXME just summary stats for the moment
            self.stream.opentag('linkagediseq')
            self.stream.writeln()
            # hardcode 0 and 1, because we are only ever doing pairwise (for now)
            self.stream.opentag('summary', first="0", second="1")
            self.stream.tagContents('wn', "%g" % Wn)
            self.stream.writeln()
            # FIXME have no chisq test here for the moment
            self.stream.writeln()
            self.stream.tagContents('dprime', "%g" % dprime)
            self.stream.writeln()
            self.stream.tagContents('ALD_1_2', "%g" % ALD_1_2)
            self.stream.writeln()
            self.stream.tagContents('ALD_2_1', "%g" % ALD_2_1)
            self.stream.writeln()
            self.stream.closetag('summary')
            self.stream.writeln()
            self.stream.closetag('linkagediseq')
            self.stream.writeln()
        else:
            dprime, Wn, ALD_1_2, ALD_2_1 = None, None, None, None
        
        self.stream.closetag('group')
        self.stream.writeln()
        
        return converge, lnlike, n_u_hap, n_hap_pairs, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code, haplotype, dprime, Wn, ALD_1_2, ALD_2_1

    def allPairwise(self,
                    weight=None,
                    control=None,
                    numInitCond=10,
                    mode=None):
        """Estimate pairwise statistics for all pairs of loci."""

        # FIXME: sequence data *not* currently supported for haplostats
        locusPairs = getLocusPairs(self.matrix, False)
        if self.debug: print (locusPairs, len(locusPairs))
        for pair in locusPairs:
            self.estHaplotypes(locusKeys=pair,
                               weight=weight,
                               control=control,
                               numInitCond=numInitCond,
                               testMode=self.testMode)
        
    def _haplo_em_fitter(self,
                         n_loci,
                         n_subject,
                         weight,
                         geno_vec,
                         n_alleles,
                         max_haps,
                         max_iter,
                         loci_insert_order,
                         min_posterior,
                         tol,
                         insert_batch_size,
                         random_start,
                         iseed1,
                         iseed2,
                         iseed3,
                         verbose):

        _Haplostats = self._Haplostats

        converge = 0
        min_prior = 0.0
        n_unique = 0
        lnlike = 0.0
        n_u_hap = 0
        n_hap_pairs = 0

        tmp1 = _Haplostats.haplo_em_pin_wrap(n_loci, n_subject, weight, n_alleles,
                                             max_haps, max_iter, loci_insert_order,
                                             min_prior, min_posterior, tol, insert_batch_size,
                                             random_start, iseed1, iseed2, iseed3, verbose, geno_vec)

        # values returned from haplo_em_pin
        status1, converge, lnlike, n_u_hap, n_hap_pairs = tmp1

        tmp2 = _Haplostats.haplo_em_ret_info_wrap(\
            # input parameters
            n_u_hap, n_loci, n_hap_pairs,
            # output parameters: declaring array sizes for ret_val
            n_u_hap,          # hap_prob
            n_u_hap * n_loci, # u_hap
            n_u_hap,          # u_hap_code
            n_hap_pairs,        # subj_id
            n_hap_pairs,        # post
            n_hap_pairs,        # hap1_code
            n_hap_pairs,        # hap2_code
            )

        # values returned from haplo_em_ret_info
        status2, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code = tmp2

        _Haplostats.haplo_free_memory()

        return converge, lnlike, n_u_hap, n_hap_pairs, hap_prob, u_hap, u_hap_code, subj_id, post, hap1_code, hap2_code

        

