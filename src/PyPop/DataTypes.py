#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2003-2006.
# The Regents of the University of California (Regents). All Rights Reserved.

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

from PyPop.Utils import getStreamType, StringMatrix, OrderedDict, TextOutputStream

def _serializeAlleleCountDataAt(stream, alleleTable,
                                total, untypedIndividuals,
                                unsequencedSites):

    """Function to actually do the output"""

    totalFreq = 0
    alleles = list(alleleTable.keys())
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
                           "%.1f" % untypedIndividuals)
        stream.writeln()
        stream.tagContents('unsequencedsites', \
                           "%d" % unsequencedSites)
        stream.writeln()
        stream.tagContents('indivcount', \
                           "%.1f" % (total/2.0))
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
    """Base class that stores and caches basic genotype statistics.
    """
    def __init__(self,
                 matrix=None,
                 untypedAllele='****',
                 unsequencedSite=None,
                 allowSemiTyped=0,
                 debug=0):
        self.matrix = matrix
        self.untypedAllele = untypedAllele
        self.unsequencedSite = unsequencedSite
        self.allowSemiTyped = allowSemiTyped
        self.debug = debug
        
        self._genDataStructures()

    def _checkAllele(self, allele1, allele2, unsequencedSites):
        for phase in [allele1, allele2]:
            if (self.untypedAllele != phase and self.unsequencedSite != phase):
                if self.debug:
                    print("alleleTable:", self.alleleTable)
                    print("alleleTable type:", type(self.alleleTable))
                    print("phase:", phase)
                    print("phase type:", type(phase))
                if phase in self.alleleTable:
                    self.alleleTable[phase] += 1
                else:
                    self.alleleTable[phase] = 1
                self.total += 1
            else:
                if (self.unsequencedSite == phase):
                    unsequencedSites += 1
                if self.debug:
                    print(self.unsequencedSite, phase, unsequencedSites)

        
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
               print("locus name: %s" %locus)
               print("column tuple: %s" %self.matrix[locus])

            # initialise blank dictionary
            self.alleleTable = {}

            # initialise blank list
            self.locusTable[locus] = []
      
            self.total = 0
            untypedIndividuals = 0
            unsequencedSites = 0

            # first pass runs a filter of alleles through the
            # anthonynolan data filter/cleaner

            # re-initialise the row count on each iteration of the locus
            rowCount = 0

            subMatrix = self.matrix[locus]

            for line in range(0, len(subMatrix)):

                if self.debug:
                    print(rowCount, subMatrix[line]),

                allele1, allele2 = [str(i) for i in subMatrix[line]]

                if self.debug:
                    print(allele1, allele2)
                
                # increment row count
                rowCount += 1

                if self.allowSemiTyped:
                    self._checkAllele(allele1, allele2, unsequencedSites)
                    if (self.untypedAllele == allele1):
                        untypedIndividuals += 0.5
                    if (self.untypedAllele == allele2):
                        untypedIndividuals += 0.5
                else:
                    # ensure that *both* alleles are typed
                    if (self.untypedAllele != allele1) and \
                           (self.untypedAllele != allele2):
                        # check to see if the "allele" isn't a missing sequence site
                        if (self.unsequencedSite != allele1) and \
                           (self.unsequencedSite != allele2):
                            self._checkAllele(allele1, allele2, unsequencedSites)
                        else:
                            if self.unsequencedSite == allele1:
                                unsequencedSites += 1
                            if self.unsequencedSite == allele2:
                                unsequencedSites += 1
                            if self.debug:
                                print(locus, allele1, allele2, unsequencedSites)
                            continue
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
                    print(allele1, allele2, self.total)

            # assign frequency, counts
            self.freqcount[locus] = self.alleleTable, self.total, untypedIndividuals, unsequencedSites

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

    def getAlleleCountAt(self, locus, lumpValue=0):
        """Return allele count for given locus.

        - 'lumpValue': the specified amount of lumping (Default: 0)        

        Given a locus name, return a tuple: consisting of a map keyed
        by alleles containing counts, the total count at that
        locus, and number of untyped individuals.  """

        # need to recalculate values
        if (lumpValue != 0):

            alleles, totalAlleles, untyped, unsequenced = self.freqcount[locus]

            lumpedAlleles = {}
            for allele in alleles.keys():
                count = alleles[allele]
                if count <= lumpValue:
                    if 'lump' in lumpedAlleles:
                        lumpedAlleles['lump'] += count
                    else:
                        lumpedAlleles['lump'] = count
                else:
                    lumpedAlleles[allele] = count
            lumpedTuple = lumpedAlleles, totalAlleles, untyped, unsequenced
            ## print lumpedTuple
            
            return lumpedTuple
        else:
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
        
        self.alleleTable, self.total, untypedIndividuals, unsequencedSites = self.freqcount[locus]
        _serializeAlleleCountDataAt(stream, self.alleleTable,
                                    self.total, untypedIndividuals,
                                    unsequencedSites)

    def serializeAlleleCountDataTo(self, stream):
        type = getStreamType(stream)
        
        stream.opentag('allelecounts')
            
        for locus in self.freqcount.keys():
            stream.writeln()
            stream.opentag('locus', name=locus)
                    
        stream.writeln()
        stream.closetag('allelecounts')
        return 1

    def getLocusDataAt(self, locus, lumpValue=0):
        """Returns the genotyped data for specified locus.  

        Given a 'locus', return a list genotypes consisting of
        2-tuples which contain each of the alleles for that individual
        in the list.

        - 'lumpValue': the specified amount of lumping (Default: 0)

        **Note:** *this list has filtered out all individuals that are
        untyped at either chromosome.*

        **Note 2:** data is sorted so that allele1 < allele2,
        alphabetically """

        # need to recalculate values
        if (lumpValue != 0):

            alleles, totalAlleles, untyped, unsequenced = self.freqcount[locus]

            lumpedAlleles = {}
            listLumped = []
            for allele in alleles.keys():
                count = alleles[allele]
                if count <= lumpValue:
                    listLumped.append(allele)
                    if 'lump' in lumpedAlleles:
                        lumpedAlleles['lump'] += count
                    else:
                        lumpedAlleles['lump'] = count
                else:
                    lumpedAlleles[allele] = count
            ##print listLumped
            copyTable = (self.locusTable[locus])[:]
            newTable = []
            for li in copyTable:
                allele1, allele2 = li
                if allele1 in listLumped:
                    newAllele1 = 'lump'
                else:
                    newAllele1 = allele1
                if allele2 in listLumped:
                    newAllele2 = 'lump'
                else:
                    newAllele2 = allele2
                newTable.append((newAllele1, newAllele2))
                    
            ##print copyTable
            ##print newTable
            
            return newTable
        else:
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

def checkIfSequenceData(matrix):

    # FIXME: hack to determine whether we are analysing sequence
    # we use a regex to match anything in the form A_32 or A_-32
    # this should be passed as a parameter
    locus = matrix.colList[0]
    if re.search("[a-zA-Z0-9]+_[-]?[0-9]+", locus):
        sequenceData = 1
    else:
        sequenceData = 0

    return sequenceData

def getMetaLocus(locus, isSequenceData):

    if isSequenceData:
        metaLocus = string.split(string.split(locus, ':')[0],'_')[0]
    else:
        metaLocus = None

    return metaLocus

def getLocusPairs(matrix, sequenceData):
    """
    Returns a list of all pairs of loci from a given StringMatrix
    """
        
    loci = matrix.colList
        
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
    return li

def getLumpedDataLevels(genotypeData, locus, lumpLevels):
    """Returns a dictionary of tuples with alleleCount and locusData
    lumped by different levels specified as a list of integers."""

    lumpData = {}
    for level in lumpLevels:
        lumpData[level] = (genotypeData.getLocusDataAt(locus,
                                                     lumpValue=level),
                           genotypeData.getAlleleCountAt(locus,
                                                         lumpValue=level))
    return lumpData



class AlleleCounts:
    """WARNING: this class is now obsolete, the Genotypes class
    now holds allele count data as pseudo-genotype matrix.
    
    Class to store information in allele count form."""
    
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
            print('alleleTable', self.alleleTable)

        # simply reconstruct the 3-tuple as generated in
        # ParseGenotypeFile: alleleTable (a map of counts keyed by
        # allele), total allele count and the number of untyped
        # individuals (in this case, by definition it is zero).
        # then store in the same data structure as ParseGenotypeFile

        # even though we only have a single locus, this will make it
        # easy to generalize later

        self.freqcount[self.locusName] = \
                                  self.alleleTable, self.totalAlleleCount, 0, 0


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
        
        alleleTable, total, untypedIndividuals, unsequencedSites = self.freqcount[locus]
        _serializeAlleleCountDataAt(stream, alleleTable,
                                    total, untypedIndividuals, unsequencedSites)

    def getAlleleCount(self):
        return self.freqcount[self.locusName]

    def getLocusName(self):
        # the first key is the name of the locus
        return self.locusName
