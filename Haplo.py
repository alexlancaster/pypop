#! /usr/bin/env python

"""Module for estimating haplotypes.

"""
import sys, string, os, re

class Haplo:
    """*Abstract* base class for haplotype parsing/output.

    Currently a stub class (unimplemented).
    """
    pass

class HaploArlequin(Haplo):
    """Haplotype estimation implemented via Arlequin
    
    Outputs Arlequin format data files and runtime info, also runs and
    parses the resulting Arlequin data so it can be made available
    programatically to rest of Python framework. """
    
    def __init__(self,
                 arpFilename,
                 idCol,
                 prefixCols,
                 suffixCols,
                 windowSize,
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
        
        - untypedAllele:  (defaults to '0')
        
        - arlequinPrefix: prefix for all Arlequin run-time files
        (defaults to 'arl_run').

        - debug: (defaults to 0)
        
        """
        self.arpFilename = arpFilename
        self.idCol = idCol
        self.prefixCols = prefixCols
        self.suffixCols = suffixCols
        self.windowSize = windowSize
        self.arlequinPrefix = arlequinPrefix
        self.untypedAllele = untypedAllele
        self.debug = debug

        if arpFilename[-4:] == '.arp':
            self.arpFilename = arpFilename
            self.arlResPrefix = arpFilename[:-4]
        else:
            sys.exit("Error: Arlequin filename: %s does not have a .arp suffix", arpFilename)

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

    def _outputSample (self, data, startCol, endCol):

        # store output Arlequin-formatted genotypes in an array
        samples = []
        sampleLines = []
        
        # convert columns to locus number
        startLocus = (startCol - self.prefixCols)/2 + 1
        endLocus = (startLocus - 1) + (endCol - startCol)/2

        chunk = xrange(startCol, endCol)
        for line in data:
            words = string.split(line)
            unphase1 = "%10s 1 " % words[self.idCol]
            unphase2 = "%13s" % " "
            for i in chunk:
                allele = words[i]
                # don't output individual if *any* loci is untyped
                if allele == self.untypedAllele:
                    if self.debug:
                        print "untyped allele %s in (%s), (%s)" \
                              % (allele, unphase1, unphase2)
                    break
                if ((i - startCol) % 2): unphase1 = unphase1 + " " + allele
                else: unphase2 = unphase2 + " " + allele
            else:
                # store formatted output samples
                samples.append(unphase1 + os.linesep)
                samples.append(unphase2 + os.linesep)

        # adjust the output count of samples for the `SamplesSize'
        # metadata field

        if len(samples) != 0:
            sampleLines.append("""
            
            SampleName=\"%s pop with %s individuals from locus %d to %d\"
            SampleSize= %s
            SampleData={"""  % (self.arlResPrefix, len(samples)/2, startLocus, endLocus, len(samples)/2))

            sampleLines.append(os.linesep)

            # output previously-stored samples to stream only after
            # calculation of number of samples is made
            for line in samples:
                sampleLines.append(line)
            sampleLines.append("}")
            validSample = 1
        else:
            validSample = 0

        return sampleLines, validSample

    def outputArlequin(self, data):
        """Outputs the specified .arp sample file.
        """
        
        if self.debug:
            print "Counted", len(data), "lines."
        firstLine = data[0]

        # estimate the number of loci from the number of columns
        # and the prefix and suffix columns which can be ignored  
        cols = len(string.split(firstLine))
        colCount = cols - (self.prefixCols + self.suffixCols)

        # sanity check to ensure column number is even (2 alleles for
        # each loci)
        if colCount % 2 != 0:
            sys.exit ("Error: col count (%d) is not even" % colCount)
        else:
            locusCount = (colCount)/2

        if self.debug:
            print "First line", firstLine, "has", cols, "columns and", \
                  locusCount, "allele pairs"

        chunk = xrange(0, locusCount - self.windowSize + 1)

        sampleCount = 0
        totalSamples = []
        
        for locus in chunk:
            start = self.prefixCols + locus*2
            end = start + self.windowSize*2
            sampleLines, validSample = self._outputSample(data, start, end)
            totalSamples.extend(sampleLines)
            sampleCount += validSample

        headerLines = self._outputHeader(sampleCount)

        if self.debug:
            print "sample count", sampleCount
            
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
        
        self._outputArlRunTxt(self.arlequinPrefix + ".txt", self.arpFilename)
        self._outputArlRunArs(self.arlequinPrefix + ".ars")

        # spawn external Arlequin process
        os.system("arlecore.exe")

        # fix permissions on result directory because Arlequin is
        # brain-dead with respect to file permissions on Unix
        os.chmod(self.arlResPrefix + ".res", 0755)

    def genHaplotypes(self):
        """Gets the haplotype estimates back from Arlequin.

        Parses the Arlequin output nonsense to retrieve the haplotype
        estimated data.  Returns a list of the sliding `windows' which
        consists of tuples.

        Each tuple consists of a:

        - dictionary entry (the haplotype-frequency) key-value pairs.

        - population name (original .arp file prefix)

        - sample count (number of samples for that window)

        - start (where the window starts)

        - stop (where the window stops)
        """
        outFile = self.arlResPrefix + ".res" + os.sep + self.arlResPrefix + ".htm"
        dataFound = 0
        headerFound = 0

        haplotypes = []
        
        patt1 = re.compile("== Sample :[\t ]*(\S+) pop with (\d+) individuals from locus (\d+) to (\d+)")
        patt2 = re.compile("    #   Haplotype     Freq.      s.d.")
        patt3 = re.compile("^\s+\d+\s+UNKNOWN(.*)")
        windowRange = range(1, self.windowSize)
        
        for line in open(outFile, 'r').readlines():
            matchobj = re.search(patt1, line)
            if matchobj:
                headerFound = 1
                popName = matchobj.group(1)
                sampleCount = matchobj.group(2)
                start = matchobj.group(3)
                stop = matchobj.group(4)
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
                    haplotypes.append((freqs, popName, sampleCount, start, stop))

            if re.match(patt2, line):
                dataFound = 1

        return haplotypes
