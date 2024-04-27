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

"""Python population genetics statistics.
"""

import string
from copy import copy
from random import randrange

from PyPop.Filter import AnthonyNolanFilter
from PyPop.Homozygosity import getObservedHomozygosityFromAlleleData, HomozygosityEWSlatkinExact

class RandomBinsForHomozygosity:

    def __init__(self,
                 directoryName=None,
                 logFile=None,
                 untypedAllele='****',
                 filename=None,
                 numReplicates=10000,
                 binningReplicates=100,
                 locus=None,
                 xmlfile=None,
                 debug=0,
                 randomResultsFileName=None):

        self.untypedAllele = untypedAllele
        self.binningReplicates = binningReplicates
        self.numReplicates = numReplicates
        self.debug = debug
        self.locus = locus
        self.filename = filename.split(".")[-2]
        self.filename = self.filename.split("/")[-1]
        self.xmlStream = xmlfile
        self.debug = debug
        self.logFile = logFile
        self.alleleCountDict = {}
        self.randomResultsFile = open(randomResultsFileName, "w")
        self.randomResultsFile.write("\t".join("filename locus method theta prob_ewens prob_homozygosity mean_homozygosity obsv_homozygosity var_homozygosity normDevHomozygosity".split()) + "\n" )
        
    def _dumpResults(self, alleleCountsBefore=None, alleleCountsAfter=None, randMethod=None):

        # append the before and after allele counts to the dictionary
        # so we can look up all of the stats en masse
        self.alleleCountDict[tuple(alleleCountsBefore)] = "before"
        self.alleleCountDict[tuple(alleleCountsAfter)] = "after"
        
        if self.debug:
            print('alleleCountsBefore', alleleCountsBefore)
            print('alleleCountsAfter', alleleCountsAfter)
            print('alleleCountDict', self.alleleCountDict)

        hzExactObj = HomozygosityEWSlatkinExact(numReplicates=self.numReplicates, debug=self.debug)
        stats = hzExactObj.returnBulkHomozygosityStats(self.alleleCountDict, binningMethod=self.binningMethod)

        for s in stats:
            for m in range(stats[s]):
                s = list(map(str, s))
                self.randomResultsFile.write("\t".join([self.filename, self.locus] + s) + "\n")

        self.randomResultsFile.close()

    def _updateCountDict(self, alleleCounts=None):

        alleleCounts.sort()
        alleleCounts = tuple(alleleCounts)

        if self.debug:
            print(alleleCounts)
            
        if alleleCounts in self.alleleCountDict.keys():
            self.alleleCountDict[alleleCounts] += 1
        else:
            self.alleleCountDict[alleleCounts] = 1
        

    def randomMethod(self, alleleCountsBefore=None, alleleCountsAfter=None):

        self.binningMethod = "random"

        # we don't need the dictionary in this case, just the counts
        alleleCountsBefore = alleleCountsBefore.values()
        alleleCountsAfter = alleleCountsAfter.values()

        for i in range(self.binningReplicates):
            alleleCountsRand = copy(list(alleleCountsBefore))

            while len(alleleCountsRand) > len(alleleCountsAfter):
                bin1 = randrange(0,len(alleleCountsRand),1)
                bin2 = randrange(0,len(alleleCountsRand),1)

                if bin1 != bin2:
                    alleleCountsRand[bin1] += alleleCountsRand[bin2]
                    del alleleCountsRand[bin2]

            self._updateCountDict(alleleCountsRand)

        self._dumpResults(alleleCountsBefore, alleleCountsAfter)


    def sequenceMethod(self,
                       alleleCountsBefore=None,
                       alleleCountsAfter=None,
                       polyseq=None,
                       polyseqpos=None):


        self.binningMethod = "sequence"

        binningAttempts = 0
        binningAttemptsSuccessful = 0
        polyseqpos = polyseqpos[self.locus]
        
        deleteHistory = {}
        deleteHistoryAll = {}
        collapseHistory = {}
        weightedCollapseHistory = {}
        for pos in polyseqpos:
            deleteHistory[pos] = 0
            deleteHistoryAll[pos] = 0
            collapseHistory[pos] = 0
            weightedCollapseHistory[pos] = 0

        while binningAttemptsSuccessful < self.binningReplicates:

            alleleCountsRand = {}
            for allele in alleleCountsBefore:
                alleleCountsRand[self.locus+"*"+allele] = alleleCountsBefore[allele]

            polyseqSliced = copy(polyseq)
            polyseqposDeletes = copy(polyseqpos)
            deleteHistorySaved = copy(deleteHistory)
            collapseHistorySaved = copy(collapseHistory)
            weightedCollapseHistorySaved = copy(weightedCollapseHistory)

            try:
                del polyseqSliced[self.locus+"*"+self.untypedAllele]
            except:
                if self.debug:
                    print("no untyped allele in polyseq")

            while len(alleleCountsRand) > len(alleleCountsAfter):

                seqLength = len(polyseqSliced.values()[0])
                posToDelete = randrange(0,seqLength,1)
                absolutePosToDelete = polyseqposDeletes[posToDelete]
                deleteHistory[absolutePosToDelete] += 1
                deleteHistoryAll[absolutePosToDelete] += 1
                allelesToBin = []

                if self.debug:
                    print("polyseq",polyseqSliced)
                    print("posToDelete",posToDelete)
                    print("length of polyseq before",seqLength)
                    print("alleles before binning",alleleCountsRand)

                # deletes the selected character from each sequence
                for allele in polyseqSliced:
                    polyseqSliced[allele] = polyseqSliced[allele][:posToDelete] + polyseqSliced[allele][posToDelete+1:] 
                del polyseqposDeletes[posToDelete]

                # go thru again to check to see what we have collapsed
                for allele in polyseqSliced:
                    for allele2 in polyseqSliced:
                        if polyseqSliced[allele] == polyseqSliced[allele2] and allele != allele2:
                            if allele not in allelesToBin:
                                allelesToBin.append(allele)
                            if allele2 not in allelesToBin:
                                allelesToBin.append(allele2)

                # go thru again and tally up the allele counts from
                # the collapse-ees into the collapse-er (which is the
                # first one, arbitrarily)
                for allele in allelesToBin[1:]:
                    alleleCountsRand[allelesToBin[0]] += alleleCountsRand[allele]

                # to thru again and tally up the statistics
                for allele in allelesToBin:
                    collapseHistory[absolutePosToDelete] += 1
                    weightedCollapseHistory[absolutePosToDelete] += alleleCountsRand[allele]

                # go thru one more time to delete the collapse-ees
                for allele in allelesToBin[1:]:
                    del alleleCountsRand[allele]
                    del polyseqSliced[allele]

                if self.debug:
                    print("length of polyseq after",len(polyseqSliced.values()[0]))
                    print("allelesToBin",allelesToBin)
                    print("alleles after binning",alleleCountsRand)
                    print("--------------------")

            binningAttempts += 1

            if len(alleleCountsRand) == len(alleleCountsAfter):
                binningAttemptsSuccessful += 1
                self._updateCountDict(alleleCountsRand.values())

            elif len(alleleCountsRand) < len(alleleCountsAfter):
                if self.debug:
                    print("=======================OVERSHOT TARGET!==================")
                # restore counters to pre-overshoot counts
                deleteHistory = copy(deleteHistorySaved)
                collapseHistory = copy(collapseHistorySaved)
                weightedCollapseHistory = copy(weightedCollapseHistorySaved)
                
            if binningAttempts > (self.binningReplicates * 100):
                print("FilterLog: Locus %s: While attempting %d replicates of sequence-based random binning, overshot target too many times; exiting binning with only %d successful replicates." % (self.locus, self.binningReplicates, binningAttemptsSuccessful))
                self.logFile.writeln("Locus %s: While attempting %d replicates of sequence-based random binning, overshot target too many times; exiting binning with only %d successful replicates." % (self.locus, self.binningReplicates, binningAttemptsSuccessful) )
                break


        self._dumpResults(alleleCountsBefore.values(), alleleCountsAfter.values())

        # THIS GOES IN FILTER LOG FILE
        self.logFile.writeln('Tried %d times to get %d random binnings.' % (binningAttempts, binningAttemptsSuccessful))
        self.logFile.writeln('locus\tposition\ttimesDeleted\ttimesDeletedAll\tcollapses\tcollapsesWeighted')
        for pos in polyseqpos:
            self.logFile.writeln('\t'.join([self.locus, str(pos),
                                            str(deleteHistory[pos]/float(binningAttemptsSuccessful)),
                                            str(deleteHistoryAll[pos]/float(binningAttemptsSuccessful)),
                                            str(collapseHistory[pos]/float(binningAttemptsSuccessful)),
                                            str(weightedCollapseHistory[pos]/float(binningAttemptsSuccessful))]))

    
