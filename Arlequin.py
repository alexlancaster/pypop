#! /usr/bin/env python

"""Module for exposing Arlequin functionality in Python.

"""
import sys, string, os, re, shutil

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
            print "_outputSample:chunk:", chunk
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
                if ((chunk.index(i) + 1) % 2): unphase1 = unphase1 + " " + allele
                else: unphase2 = unphase2 + " " + allele
            else:
                # store formatted output samples
                samples.append(unphase1 + os.linesep)
                samples.append(unphase2 + os.linesep)

        # adjust the output count of samples for the `SamplesSize'
        # metadata field

        if len(samples) != 0:
            sampleLines.append("""
            
            SampleName=\"%s pop with %s individuals from loci %s\"
            SampleSize= %s
            SampleData={"""  % (self.arlResPrefix, len(samples)/2, str(slice), len(samples)/2))

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
            print "Counted", len(data), "lines."
        firstLine = data[0]

        # calculate the number of loci from the number of columns
        # and the prefix and suffix columns which can be ignored  
        cols = len(string.split(firstLine))
        colCount = cols - (self.prefixCols + self.suffixCols)

        # sanity check to ensure column number is even (2 alleles for
        # each loci)
        if colCount % 2 != 0:
            sys.exit ("Error: col count (%d) is not even" % colCount)
        else:
            locusCount = (colCount)/2

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
            print "First line", firstLine, "has", cols, "columns and", \
                  locusCount, "allele pairs"
            print "Map order:", self.mapOrder

        # if windowSize is set to zero, the default to using
        # locusCount as windowSize

        if self.windowSize == 0:
            self.windowSize = locusCount

        #chunk = xrange(0, locusCount - self.windowSize + 1)
        chunk = xrange(0, len(self.mapOrder) - self.windowSize + 1)

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
                print locus, colChunk, locusSlice

            # generate the sample
            sampleLines, validSample = self._outputSample(data,
                                                          colChunk,
                                                          locusSlice)
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
        os.chmod(self.arlResPrefix + ".res", 0755)

# this is called if this module is executed standalone
if __name__ == "__main__":

    usage_message = """Usage: Arlequin.py [OPTION] INPUTFILE ARPFILE ARSFILE
Process a tab-delimited INPUTFILE of alleles to produce an data files
(including ARPFILE), using parameters from ARSFILE for the Arlequin population
genetics program.

 -i, --idcol=NUM       column number of identifier (first column is zero)
 -c, --cols=POS1,POS2  number of leading columns (POS1) before start and end
                        (POS2) of allele data (including IDCOL)
 -k, --sort=POS1,..    specify order of loci if different from column order
                        in file (must not repeat a locus)
 -w, --windowsize=NUM  number of loci involved in window size 
                        (note that this is twice the number of allele columns)
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
         getopt(sys.argv[1:],"i:c:k:w:u:xhd",\
                ["idcol=", "cols=", "sort=", "windowsize=", "untyped=", "execute", "help","debug"])
    except GetoptError:
        sys.exit(usage_message)

    # default options
    idCol = 0
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
        elif o in ("-c", "--cols"):
            prefixCols, suffixCols = map(int, string.split(v, ','))
        elif o in ("-k", "--sort"):
            mapOrder = map(int, string.split(v, ','))
            print mapOrder
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
    batch.outputArlequin(open(inputFilename, 'r').readlines())
    batch.outputRunFiles()

    # run Arlequin if asked
    if executeFlag:
        batch.runArlequin()
