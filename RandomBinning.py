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
from copy import deepcopy
from random import randrange

from Filter import AnthonyNolanFilter


class RandomAlleleBinning:

    def __init__(self,
                 directoryName=None,
                 logFile=None,
                 untypedAllele='****',
                 filename=None,
                 binningDigits=4,
                 debug=0):
        self.binningDigits = binningDigits
        self.untypedAllele = untypedAllele
        self.debug = debug
    
    def generateRandomBins(self, alleleCountsBefore=None, alleleCountsAfter=None, binningReplicates=100):

        # we don't need the dictionary in this case, just the counts
        alleleCountsBefore = alleleCountsBefore.values()
        alleleCountsAfter = alleleCountsAfter.values()
        
        randomBins = []
        
        for i in range(binningReplicates):

            alleleCountsRand = deepcopy(alleleCountsBefore)

            while len(alleleCountsRand) > len(alleleCountsAfter):
                bin1 = randrange(0,len(alleleCountsRand),1)
                bin2 = randrange(0,len(alleleCountsRand),1)

                if bin1 != bin2:
                    alleleCountsRand[bin1] += alleleCountsRand[bin2]
                    del alleleCountsRand[bin2]

            randomBins.append(alleleCountsRand)

        return randomBins


    def generateRandomBinsFromSequence(self, alleleCountsBefore=None, alleleCountsAfter=None, binningReplicates=100, polyseq=None, locus=None):

        randomBins = []
        
        for i in range(binningReplicates):

            alleleCountsRand = {}
            for allele in alleleCountsBefore:
                alleleCountsRand[locus+"*"+allele] = alleleCountsBefore[allele]

            polyseqSliced = deepcopy(polyseq)

            try:
                del polyseqSliced[locus+"*"+self.untypedAllele]
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

            randomBins.append(alleleCountsRand.values())

            if self.debug:
                if len(alleleCountsRand) == len(alleleCountsAfter):
                    print "========================================================="
                elif len(alleleCountsRand) < len(alleleCountsAfter):
                    print "=======================OVERSHOT TARGET!=================="
                else:
                    sys.exit("this shouldn't happen")


        return randomBins


