#! /usr/bin/env python
import sys, string

class AlleleFreq:
    """Class to generate allele frequencies."""
    def __init__(self, locusMap, sampleData,
                 alleleDesignator='*',
                 untypedAllele='****',
                 debug=0):
        """Constructor for AlleleFreq object.

        - *locusMap*: Accepts a map keyed by locus names names holding a
        tuple of column numbers.

        - *sampleData*:  Accepts a list of lines with individual sample data.

        - *alleleDesignator*: The first character of the key which determines
        whether this column contains allele data.  Defaults to `*'
        
        - *untypedAllele*:  The designator for an untyped locus.  Defaults to
        `****'.

        - *debug*: Defaults to no debugging, set debug=1 in call to
        constructor if debugging is desired."""
        
        self.locusMap=locusMap
        self.alleleDesignator=alleleDesignator

        # unpack the tuple of file information
        self.sampleDataLines, self.separator = sampleData
        self.untypedAllele=untypedAllele
        self.debug = debug

    def generateAllelecount(self):
        """Generate and return a map of tuples where the key is the
        locus name.  Each tuple is a double, consisting of a map keyed
        by alleles containing counts and the total count at that locus.
        """
        
        self.freqcount = {}
        for locus in self.locusMap.keys():
            col1, col2 = self.locusMap[locus]
            alleleTable = {}
            total = 0
            for line in self.sampleDataLines:
                fields = string.split(line, self.separator)

                allele1 = fields[col1]
                if self.untypedAllele != allele1:
                    if alleleTable.has_key(allele1):
                        alleleTable[fields[col1]] += 1
                    else:
                        alleleTable[fields[col1]] = 1
                    total += 1
                    
                allele2 = fields[col2]
                if self.untypedAllele != allele2:
                    if alleleTable.has_key(allele2):
                        alleleTable[fields[col2]] += 1
                    else:
                        alleleTable[fields[col2]] = 1
                    total += 1

                if self.debug:
                    print col1, col2, allele1, allele2, total
                self.freqcount[locus] = alleleTable, total

        return self.freqcount

    def printAllelefreq(self):
        """Print out the frequency table for each locus, with totals of
        allele and total counts in parentheses.

        **Note**: This is strictly a quick & dirty function for testing!!!"""
        for locus in self.freqcount.keys():
            print
            print "Locus:", locus
            print "======"
            print
            alleleTable, total = self.freqcount[locus]
            totalFreq = 0
            for allele in alleleTable.keys():
                freq = float(alleleTable[allele])/float(total)
                totalFreq += freq
                print "%s :%0.5f (%d)" % (allele, freq, alleleTable[allele])
            print "Total freq: %s (%d)" % (totalFreq, total)
            
# should have a test harness here!!!

