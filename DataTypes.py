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

"""Module for storing genotype and allele count data."""

import sys, os, string, types, re

from Utils import getStreamType, StringMatrix, OrderedDict, TextOutputStream

def _serializeAlleleCountDataAt(stream, alleleTable,
                                total, untypedIndividuals):

    """Function to actually do the output"""

    totalFreq = 0
    alleles = alleleTable.keys()
    alleles.sort()

    # if all individuals are untyped then supress itemized output
    if len(alleles) == 0:
        stream.emptytag('allelecounts', role='no-data')
        stream.writeln()
    else:
        # if monomorphic generate a role to indicate this, but
        # still generate the summary output
        if len(alleles) == 1:
            stream.opentag('allelecounts', role='monomorphic')
        else:
            stream.opentag('allelecounts')

        stream.writeln()
        stream.tagContents('untypedindividuals', \
                           "%d" % untypedIndividuals)
        stream.writeln()
        stream.tagContents('indivcount', \
                           "%d" % (total/2))
        stream.writeln()
        stream.tagContents('allelecount', \
                           "%d" % total)
        stream.writeln()
        stream.tagContents('distinctalleles', \
                           "%d" % len(alleleTable))
        stream.writeln()

        for allele in alleles:
            freq = float(alleleTable[allele])/float(total)
            totalFreq += freq
            strFreq = "%0.5f " % freq
            strCount = ("%d" % alleleTable[allele])

            stream.opentag('allele', name=allele)
            stream.writeln()
            stream.tagContents('frequency', strFreq)
            stream.tagContents('count', strCount)
            stream.writeln()
            stream.closetag('allele')

            stream.writeln()

        strTotalFreq = "%0.5f" % totalFreq
        strTotal = "%d" % total

        stream.tagContents('totalfrequency', strTotalFreq)
        stream.writeln()
        stream.tagContents('totalcount', strTotal)
        stream.closetag("allelecounts")
        stream.writeln()


class Genotypes:

    def __init__(self,
                 matrix=None,
                 untypedAllele='****',
                 debug=0):
        self.matrix = matrix
        self.untypedAllele = untypedAllele
        self.debug = debug
        
        self._genDataStructures()
        
    def _genDataStructures(self):
        """Generates allele count and map data structures.
        
        *For internal use only.*"""        

        self.locusKeys = self.matrix.colList

        # then total number of individuals in data file
        self.totalIndivCount = len(self.matrix)

        # total number of loci contained in original file
        self.totalLocusCount = len(self.locusKeys)

        # total loci that contain usable data
        self.totalLociWithData = 0
        
        self.freqcount = {}
        self.locusTable = {}

        for locus in self.locusKeys:
            if self.debug:
               print "locus name:", locus
               print "column tuple:", self.matrix[locus]

            # initialise blank dictionary
            alleleTable = {}

            # initialise blank list
            self.locusTable[locus] = []
      
            total = 0
            untypedIndividuals = 0

            # first pass runs a filter of alleles through the
            # anthonynolan data filter/cleaner

            # re-initialise the row count on each iteration of the locus
            rowCount = 0

            subMatrix = self.matrix[locus]

            for line in range(0, len(subMatrix)):

                if self.debug:
                    print rowCount, subMatrix[line],

                allele1, allele2 = subMatrix[line]

                if self.debug:
                    print allele1, allele2
                
                # increment row count
                rowCount += 1

                # ensure that *both* alleles are typed 
                if (self.untypedAllele != allele1) and \
                   (self.untypedAllele != allele2):
                    if alleleTable.has_key(allele1):
                        alleleTable[allele1] += 1
                    else:
                        alleleTable[allele1] = 1
                    total += 1

                    if alleleTable.has_key(allele2):
                        alleleTable[allele2] += 1
                    else:
                        alleleTable[allele2] = 1
                    total += 1
                # if either allele is untyped it is we throw out the
                # entire individual and go to the next individual
                else:
                    untypedIndividuals += 1
                    continue

                # save alleles as a tuple, sorted alphabetically
                if allele2 < allele1:
                  self.locusTable[locus].append((allele2, allele1))
                else:
                  self.locusTable[locus].append((allele1, allele2))

                if self.debug:
                    print allele1, allele2, total

            # assign frequency, counts
            self.freqcount[locus] = alleleTable, total, untypedIndividuals

            # if all individuals in a locus aren't untyped
            # then count this locus as having usable data
            if untypedIndividuals < self.totalIndivCount:
                self.totalLociWithData += 1                

    def getLocusList(self):
        """Returns the list of loci.

        *Note: this list has filtered out all loci that consist
        of individuals that are all untyped.*

        *Note 2: the order of this list is now fixed for the lifetime
          of the object.*
        """

        # returns a clone of the locusKeys list, so that this instance
        # variable can't be modified inadvertantly
        return self.locusKeys[:]

    def getAlleleCount(self):
        """Return allele count statistics for all loci.
        
        Return a map of tuples where the key is the locus name.  Each
        tuple is a triple, consisting of a map keyed by alleles
        containing counts, the total count at that locus and the
        number of untyped individuals.  """
        
        return self.freqcount

    def getAlleleCountAt(self, locus):
        """Return allele count for given locus.
        
        Given a locus name, return a tuple: consisting of a map keyed
        by alleles containing counts, the total count at that
        locus, and number of untyped individuals.  """
        
        return self.freqcount[locus]

    def serializeSubclassMetadataTo(self, stream):
        """Serialize subclass-specific metadata.

        Specifically, total number of individuals and loci and
        population name.  """

        stream.opentag('summaryinfo')
        stream.writeln()
        stream.tagContents('indivcount', "%d" % self.totalIndivCount)
        stream.writeln()
        stream.tagContents('allelecount', "%d" % (self.totalIndivCount*2))
        stream.writeln()
        stream.tagContents('locuscount', "%d" % self.totalLocusCount)
        stream.writeln()
        stream.tagContents('lociWithDataCount', "%d" % self.totalLociWithData)
        stream.writeln()
        stream.closetag('summaryinfo')
        stream.writeln()

    def serializeAlleleCountDataAt(self, stream, locus):
        """ """
        
        alleleTable, total, untypedIndividuals = self.freqcount[locus]
        _serializeAlleleCountDataAt(stream, alleleTable,
                                    total, untypedIndividuals)

    def serializeAlleleCountDataTo(self, stream):
        type = getStreamType(stream)
        
        stream.opentag('allelecounts')
            
        for locus in self.freqcount.keys():
            stream.writeln()
            stream.opentag('locus', name=locus)
                    
        stream.writeln()
        stream.closetag('allelecounts')
        return 1

    def getLocusDataAt(self, locus):
        """Returns the genotyped data for specified locus.

        Given a 'locus', return a list genotypes consisting of
        2-tuples which contain each of the alleles for that individual
        in the list.

        **Note:** *this list has filtered out all individuals that are
        untyped at either chromosome.*

        **Note 2:** data is sorted so that allele1 < allele2,
        alphabetically """

        # returns a clone of the list, so that this instance variable
        # can't be modified inadvertantly
        return (self.locusTable[locus])[:]
    
    def getLocusData(self):
        """Returns the genotyped data for all loci.

        Returns a dictionary keyed by locus name of lists of 2-tuples
        as defined by 'getLocusDataAt()'
        """
        return self.locusTable

    def getIndividualsData(self):
        """Returns the individual data.

        Returns a 'StringMatrix'.
        """
        #return self.individualsData
        return self.matrix

class AlleleCounts:
    """Class to store information in allele count form."""
    
    def __init__(self,
                 alleleTable=None,
                 locusName=None,
                 debug=0):
        self.alleleTable = alleleTable
        self.locusName = locusName
        self.debug = debug
        self._genDataStructures()
        
    def _genDataStructures(self):
        total = 0
        self.freqcount = {}

        for allele in self.alleleTable.keys():
            total += self.alleleTable[allele] 

        # store in an iVar for the moment
        self.totalAlleleCount = total
        
        if self.debug:
            print 'alleleTable', self.alleleTable

        # simply reconstruct the 3-tuple as generated in
        # ParseGenotypeFile: alleleTable (a map of counts keyed by
        # allele), total allele count and the number of untyped
        # individuals (in this case, by definition it is zero).
        # then store in the same data structure as ParseGenotypeFile

        # even though we only have a single locus, this will make it
        # easy to generalize later

        self.freqcount[self.locusName] = \
                                  self.alleleTable, self.totalAlleleCount, 0


    def serializeSubclassMetadataTo(self, stream):
        """Serialize subclass-specific metadata.

        Specifically, total number of alleles and loci.
         """

        stream.opentag('summaryinfo')
        stream.writeln()
        stream.tagContents('allelecount', "%d" % self.totalAlleleCount)
        stream.writeln()
        stream.tagContents('locuscount', "%d" % 1)
        stream.writeln()
        stream.closetag('summaryinfo')
        stream.writeln()

    def serializeAlleleCountDataAt(self, stream, locus):

        # call the class-independent function...
        
        alleleTable, total, untypedIndividuals = self.freqcount[locus]
        _serializeAlleleCountDataAt(stream, alleleTable,
                                    total, untypedIndividuals)

    def getAlleleCount(self):
        return self.freqcount[self.locusName]

    def getLocusName(self):
        # the first key is the name of the locus
        return self.locusName
