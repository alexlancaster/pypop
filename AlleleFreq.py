#! /usr/bin/env python
import sys, string

class AlleleFreq:
    """Class to generate allele frequencies."""
    def __init__(self, locus_map, sample_data,
                 allele_designator='*',
                 untyped_allele='****',
                 debug=0):
        """Constructor for AlleleFreq object.

        - locus_map: Accepts a map keyed by locus names names holding a
        tuple of column numbers.

        - sample_data:  Accepts a list of lines with individual sample data.

        - allele_designator: The first character of the key which determines
        whether this column contains allele data.  Defaults to `*'
        
        - untyped_allele:  The designator for an untyped locus.  Defaults to
        `****'.

        - debug:  Defaults to no debugging, set debug=1 in call to constructor
        if debugging is desired."""
        self.locus_map=locus_map
        self.allele_designator=allele_designator
        self.sample_data=sample_data
        self.untyped_allele=untyped_allele
        self.debug = debug

    def generate_allelecount(self):
        """Generate and return a map of tuples where the key is the
        locus name.  Each tuple is a double, consisting of a map keyed
        by alleles containing counts and the total count at that locus.
        """
        
        self.freqcount = {}
        for locus in self.locus_map.keys():
            col1, col2 = self.locus_map[locus]
            allele_table = {}
            total = 0
            for line in self.sample_data:
                fields = string.split(line, '\t')

                allele1 = fields[col1]
                if self.untyped_allele != allele1:
                    if allele_table.has_key(allele1):
                        allele_table[fields[col1]] += 1
                    else:
                        allele_table[fields[col1]] = 1
                    total += 1
                    
                allele2 = fields[col2]
                if self.untyped_allele != allele2:
                    if allele_table.has_key(allele2):
                        allele_table[fields[col2]] += 1
                    else:
                        allele_table[fields[col2]] = 1
                    total += 1

                if self.debug:
                    print col1, col2, allele1, allele2, total
                self.freqcount[locus] = allele_table, total

        return self.freqcount

    def print_allelefreq(self):
        """Print out the frequency table for each locus, with totals of
        allele and total counts in parentheses.

        **Note**: This is strictly a quick & dirty function for testing!!!"""
        for locus in self.freqcount.keys():
            print
            print "Locus:", locus
            print "======"
            print
            allele_table, total = self.freqcount[locus]
            total_freq = 0
            for allele in allele_table.keys():
                freq = float(allele_table[allele])/float(total)
                total_freq += freq
                print "%s :%0.5f (%d)" % (allele, freq, allele_table[allele])
            print "Total freq: %s (%d)" % (total_freq, total)
            
# should have a test harness here!!!

