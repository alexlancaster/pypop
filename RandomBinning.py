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

from Filter import AnthonyNolanFilter
import Homozygosity

class RandomBinsForHomozygosity:

    def __init__(self,
                 directoryName=None,
                 logFile=None,
                 untypedAllele='****',
                 filename=None,
                 numReplicates=10000,
                 binningReplicates=100,
                 locus=None,
                 debug=0):

        self.untypedAllele = untypedAllele
        self.binningReplicates = binningReplicates
        self.debug = debug
        self.locus = locus

    def randomMethod(self, alleleCountsBefore=None, alleleCountsAfter=None):

        # we don't need the dictionary in this case, just the counts
        alleleCountsBefore = alleleCountsBefore.values()
        alleleCountsAfter = alleleCountsAfter.values()

        print "obsvHomozygosity\tlocus\tmethod"
        
        for i in range(self.binningReplicates):

            alleleCountsRand = copy(alleleCountsBefore)

            while len(alleleCountsRand) > len(alleleCountsAfter):
                bin1 = randrange(0,len(alleleCountsRand),1)
                bin2 = randrange(0,len(alleleCountsRand),1)

                if bin1 != bin2:
                    alleleCountsRand[bin1] += alleleCountsRand[bin2]
                    del alleleCountsRand[bin2]

            homozygosityResults = Homozygosity.getObservedHomozygosityFromAlleleData(alleleCountsRand)
            print homozygosityResults,'\t',self.locus,'\trandom'

        homozygosityResults = Homozygosity.getObservedHomozygosityFromAlleleData(alleleCountsBefore)
        print homozygosityResults,'\t',self.locus,'\tbefore'
        homozygosityResults = Homozygosity.getObservedHomozygosityFromAlleleData(alleleCountsAfter)
        print homozygosityResults,'\t',self.locus,'\tafter'


    def sequenceMethod(self,
                       alleleCountsBefore=None,
                       alleleCountsAfter=None,
                       polyseq=None):

        binningAttempts = 0
        binningAttemptsSuccessful = 0
        
        print "obsvHomozygosity\tlocus\tmethod"
        
        while binningAttemptsSuccessful < self.binningReplicates:

            alleleCountsRand = {}
            for allele in alleleCountsBefore:
                alleleCountsRand[self.locus+"*"+allele] = alleleCountsBefore[allele]

            polyseqSliced = copy(polyseq)

            try:
                del polyseqSliced[self.locus+"*"+self.untypedAllele]
            except:
                if self.debug:
                    print "no untyped allele in polyseq"

            while len(alleleCountsRand) > len(alleleCountsAfter):

                seqLength = len(polyseqSliced.values()[0])
                charToDelete = randrange(0,seqLength,1)
                allelesToBin = []

                if self.debug:
                    print "polyseq",polyseqSliced
                    print "charToDelete",charToDelete
                    print "length of polyseq before",len(polyseqSliced.values()[0])
                    print "alleles before binning",alleleCountsRand

                # deletes the selected character from each sequence
                for allele in polyseqSliced:
                    polyseqSliced[allele] = polyseqSliced[allele][:charToDelete] + polyseqSliced[allele][charToDelete+1:]

                # go thru again to check to see what we have collapsed
                for allele in polyseqSliced:
                    for allele2 in polyseqSliced:
                        if polyseqSliced[allele] == polyseqSliced[allele2] and allele != allele2:
                            if allele not in allelesToBin:
                                allelesToBin.append(allele)
                            if allele2 not in allelesToBin:
                                allelesToBin.append(allele2)

                for allele in allelesToBin[1:]:
                    alleleCountsRand[allelesToBin[0]] += alleleCountsRand[allele]

                for allele in allelesToBin[1:]:
                    del alleleCountsRand[allele]
                    del polyseqSliced[allele]

                if self.debug:
                    print "length of polyseq after",len(polyseqSliced.values()[0])
                    print "allelesToBin",allelesToBin
                    print "alleles after binning",alleleCountsRand
                    print "--------------------"

            binningAttempts += 1
            
            if len(alleleCountsRand) == len(alleleCountsAfter):

                homozygosityResults = Homozygosity.getObservedHomozygosityFromAlleleData(alleleCountsRand.values())
                print homozygosityResults,'\t',self.locus,'\trandom'

                binningAttemptsSuccessful += 1
                if self.debug:
                    print "========================================================="

            elif len(alleleCountsRand) < len(alleleCountsAfter):
                if self.debug:
                    print "=======================OVERSHOT TARGET!=================="
                if binningAttempts > (self.binningReplicates * 10):
                    if self.debug:
                        print "**********OVERSHOT TOO MANY TIMES, EXITING BINNING ***********"
                    break


        homozygosityResults = Homozygosity.getObservedHomozygosityFromAlleleData(alleleCountsBefore.values())
        print homozygosityResults,'\t',self.locus,'\tbefore'
        homozygosityResults = Homozygosity.getObservedHomozygosityFromAlleleData(alleleCountsAfter.values())
        print homozygosityResults,'\t',self.locus,'\tafter'

        print 'had to try %d times to get %d random binnings' % (binningAttempts, binningAttemptsSuccessful)




