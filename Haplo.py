#! /usr/bin/env python

"""Module for estimating haplotypes.

"""
import sys, string, os

class Haplo:
    """*Abstract* base class for haplotype parsing/output.

    Currently a stub class (unimplemented).
    """
    pass

class HaploArlequin(Haplo):
    """Outputs Arlequin format data files and runtime info.

    """
    def __init__(self,
                 arpFilename,
                 idCol,
                 prefixCols,
                 suffixCols,
                 windowSize,
                 untypedAllele = '0',
                 arlequinPrefix = "arl_run",
                 debug=0):

        self.arpFilename = arpFilename
        self.idCol = idCol
        self.prefixCols = prefixCols
        self.suffixCols = suffixCols
        self.windowSize = windowSize
        self.arlequinPrefix = arlequinPrefix
        self.untypedAllele = untypedAllele
        self.debug = debug

    def _outputHeader(self, sampleCount):

        self.arpFile.write("""[Profile]
        
        Title=\"Arlequin sample run\"
        NbSamples=%d

             GenotypicData=1
             GameticPhase=0
             DataType=STANDARD
             LocusSeparator=WHITESPACE
             MissingData='%s'
             RecessiveData=0                         
             RecessiveAllele=\"null\" """ % (sampleCount, self.untypedAllele))

        self.arpFile.write("""[Data]

        [[Samples]]""")


    def _outputSample (self, data, startCol, endCol):

        self.arpFile.write("""
    
        SampleName=\"The %s population with %s individuals from %d col to %d col\"
        SampleSize= %s
        SampleData={"""  % ("??", len(data), startCol, endCol, len(data)))

        self.arpFile.write(os.linesep)
        
        chunk = xrange(startCol, endCol)
        for line in data:
            words = string.split(line)
            unphase1 = "%10s 1 " % words[self.idCol]
            unphase2 = "%13s" % " "
            for i in chunk:
                if (i % 2): unphase1 = unphase1 + " " + words[i]
                else: unphase2 = unphase2 + " " + words[i]
            self.arpFile.write(unphase1 + os.linesep)
            self.arpFile.write(unphase2 + os.linesep)

        self.arpFile.write("}")

    def outputArlequin(self, data):

        # open specified arp
        self.arpFile = open(self.arpFilename, 'w')
        
        if self.debug:
            print "Counted", len(data), "lines."
        firstLine = data[0]
        cols = len(string.split(firstLine))
        locusCount = (cols - (self.prefixCols + self.suffixCols))/2

        if self.debug:
            print "First line", firstLine, "has", cols, "columns and", \
                  locusCount, "allele pairs"

        chunk = xrange(0, locusCount - self.windowSize + 1)
        
        self._outputHeader(len(chunk))
        
        for locus in chunk:
            start = self.prefixCols + locus*2
            end = start + self.windowSize*2
            self._outputSample(data, start, end)

        # close .arp file
        self.arpFile.close()

    def _outputArlRunTxt(self, txtFilename, arpFilename):
        file = open(txtFilename, 'w')
        file.write("""%s
use_assoc_settings
%s%s%s
0
0
end""" % (os.getcwd(), os.getcwd(), os.sep, arpFilename))

    def _outputArlRunArs(self, arsFilename):
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
ComputeAllAllelesEM=1
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
        self._outputArlRunTxt(self.arlequinPrefix + ".txt", self.arpFilename)
        self._outputArlRunArs(self.arlequinPrefix + ".ars")

        # spawn external Arlequin process
        os.system("arlecore.exe")

        # fix permissions on result directory because Arlequin is
        # brain-dead with respect to file permissions on Unix
        os.chmod(self.arlequinPrefix + ".res", 0755)
    
#print string.join([words[x] for x in chunk if (x % 2) == 0])
#print string.join([words[x] for x in chunk if (x % 2) != 0])
