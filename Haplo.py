#! /usr/bin/env python

"""Module for estimating haplotypes.

"""

import sys, string


class Haplo:
    """*Abstract* base class for haplotype parsing/output.

    Currently a stub class (unimplemented).
    """
    pass

class HaploArlequin(Haplo):
    """Outputs Arlequin format data files and runtime info.

    """
    def __init__(self,
                 idCol,
                 prefixCols,
                 suffixCols,
                 windowSize,
                 debug=0):
        
        self.idCol = idCol
        self.prefixCols = prefixCols
        self.suffixCols = suffixCols
        self.windowSize = windowSize
        self.debug = debug

    def outputHeader(self):

        print """[Data]

        [[Samples]]"""


    def outputSample (self, data, startCol, endCol):

        print """
    
        SampleName=\"The %s population with %s individuals from %d col to %d col\"
        SampleSize= %s
        SampleData={"""  % ("??", len(data), startCol, endCol, len(data))
    
        chunk = xrange(startCol, endCol)
        for line in data:
            words = string.split(line)
            unphase1 = "%10s 1 " % words[self.idCol]
            unphase2 = "%13s" % " "
            for i in chunk:
                if (i % 2): unphase1 = unphase1 + " " + words[i]
                else: unphase2 = unphase2 + " " + words[i]
            print unphase1
            print unphase2

        print "}"

    def outputArlequin(self, data):

        if self.debug:
            print "Counted", len(data), "lines."
        firstLine = data[0]
        cols = len(string.split(firstLine))
        locusCount = (cols - (self.prefixCols + self.suffixCols))/2

        if self.debug:
            print "First line", firstLine, "has", cols, "columns and", \
                  locusCount, "allele pairs"

        self.outputHeader()

        for locus in xrange(0, locusCount - self.windowSize + 1):
            start = self.prefixCols + locus*2
            end = start + self.windowSize*2
            self.outputSample(data, start, end)


#print string.join([words[x] for x in chunk if (x % 2) == 0])
#print string.join([words[x] for x in chunk if (x % 2) != 0])
