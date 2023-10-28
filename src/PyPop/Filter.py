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

"""Module for filtering data files.

   Filters and cleans data before being accepted as input to PyPop
   analysis routines.

."""

import sys, os, string, types, re
from PyPop.Utils import OrderedDict, TextOutputStream, StringMatrix
from copy import deepcopy
from operator import add

class SubclassError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Sub class must implement this method"

class Filter:
    """Abstract base class for Filters
    """
    def __init__(self):
        pass
    def doFiltering(self, matrix=None):
        raise SubclassError()
    def startFirstPass(self, locus):
        raise SubclassError()
    def checkAlleleName(self, alleleName):
        raise SubclassError()
    def addAllele(self, alleleName):
        raise SubclassError()
    def endFirstPass(self):
        raise SubclassError()
    def startFiltering(self):
        raise SubclassError()
    def filterAllele(self, alleleName):
        raise SubclassError()
    def endFiltering(self):
        raise SubclassError()
    def writeToLog(self, logstring=None):
        raise SubclassError()
    def cleanup(self):
        raise SubclassError()
    
class PassThroughFilter(Filter):
    """A filter that doesn't change input data.
    """
    def __init__(self):
        pass
    def doFiltering(self, matrix=None):
        return matrix
    def startFirstPass(self, locus):
        pass
    def checkAlleleName(self, alleleName):
        pass
    def addAllele(self, alleleName):
        pass
    def endFirstPass(self):
        pass
    def startFiltering(self):
        pass
    def filterAllele(self, alleleName):
        return alleleName
    def endFiltering(self):
        pass
    def writeToLog(self, logstring=None):
        pass
    def cleanup(self):
        pass

class AnthonyNolanFilter(Filter):
    """Filters data via anthonynolan's allele call data.

    Allele call data files can be of either txt or msf formats.
    txt files available at http://www.anthonynolan.com
    msf files available at ftp://ftp.ebi.ac.uk/pub/databases/imgt/mhc/hla/
    Use of msf files is required in order to translate allele codes
    into polymorphic sequence data.
    """

    def __init__(self,
                 directoryName=None,
                 alleleFileFormat='msf',
                 preserveAmbiguousFlag=0,
                 preserveUnknownFlag=0,
                 preserveLowresFlag=0,
                 alleleDesignator='*',
                 logFile=None,
                 untypedAllele='****',
                 unsequencedSite = '#',
                 sequenceFileSuffix='_prot',
                 filename=None,
                 numDigits=4,
                 verboseFlag=1,
                 debug=0,
                 sequenceFilterMethod="strict"):
        
        self.directoryName = directoryName
        self.alleleFileFormat=alleleFileFormat
        self.preserveAmbiguousFlag=preserveAmbiguousFlag
        self.preserveUnknownFlag=preserveUnknownFlag
        self.preserveLowresFlag=preserveLowresFlag
        self.numDigits = numDigits
        self.verboseFlag = verboseFlag
        self.debug = debug
        self.alleleDesignator = alleleDesignator
        self.untypedAllele = untypedAllele
        self.unsequencedSite = unsequencedSite
        self.sequenceFilterMethod = sequenceFilterMethod

        if self.unsequencedSite == self.untypedAllele:
            sys.exit("Designator for unsequenced site and untyped allele cannot be the same!")
            
        self.sequenceFileSuffix = sequenceFileSuffix
        self.filename = filename
        self.logFile = logFile

        if self.alleleFileFormat == 'msf':
            patt = re.compile("^ *Name: *([0-9a-zA-Z]+)" + \
                              re.escape(self.alleleDesignator) + \
                              "([0-9a-zA-Z]+)")
            ## These are the names of the loci used in pop files.
            ## These are also the official names specified by NCBI.
            ## MSF files use all of these, except C is Cw.
            ## This exception is handled as a corner case in the code.
            ## In the future the ini file should specify a concordance table.
            loci = ['A', 'C', 'B', 'DRA', 'DRB1', 'DQA1', 'DQB1', 'DPA1', 'DPB1']

        else:
            patt = re.compile("^([0-9a-zA-Z]+)" + \
                              re.escape(self.alleleDesignator) + \
                              "([0-9a-zA-Z]+)")
            loci = ['a', 'b', 'c', 'dqa', 'dqb', 'dra', 'drb', 'dpb', 'dpa']
        
        self.alleleLookupTable = {}
        
        for locus in loci:

            if self.alleleFileFormat == 'msf':
                self._getMSFLinesForLocus(locus)
            else:
                self.lines = (open(os.path.join(directoryName, locus + '_pt.txt'), 'r')).readlines()

            for line in self.lines:
                matchobj = re.search(patt, line)
                if matchobj:
                    name = matchobj.group(1)
                    # CORNER CASE! 'C' locus is called 'Cw' in data files
#                    if name == "Cw":
#                        name = "C"
                    allele = matchobj.group(2)

                    if self.alleleLookupTable.has_key(name):
                        if allele not in self.alleleLookupTable[name]:
                            self.alleleLookupTable[name].append(allele)
                    else:
                        self.alleleLookupTable[name] = []
                        self.alleleLookupTable[name].append(allele)

        if self.debug:
            print(self.alleleLookupTable)


    def doFiltering(self, matrix=None):
        """Do filtering on StringMatrix

        Given a StringMatrix, does the filtering on the matrix, and
        returns it for further downstream processing """
        self.matrix = matrix

        for locus in self.matrix.colList:
            if self.debug:
               print("locus name:", locus)

            # first pass runs generates the counts need for final
            # reassignment

            # initialize first pass
            self.startFirstPass(locus)

            # loop through all lines in locus, adding each allele
            for individ in self.matrix[locus]:
                allele1, allele2 = individ
                self.addAllele(allele1)
                self.addAllele(allele2)

            # do final reassignments based on counts
            self.endFirstPass()

            # now we start doing the actual filtering
            self.startFiltering()

            rowCount = 0
            for individ in self.matrix[locus]:

                # get current data out of matrix
                cur_allele1, cur_allele2 = individ

                # put all alleles through filter and regenerate data
                # structures
                allele1 = self.filterAllele(cur_allele1)
                allele2 = self.filterAllele(cur_allele2)

                self.matrix[rowCount,locus] = (allele1, allele2)

                if self.debug:
                    print(rowCount, self.matrix[rowCount,locus])

                # increment row count
                rowCount += 1

            # end filtering for this locus
            self.endFiltering()

        return self.matrix

    def startFirstPass(self, locus):
        self.locus = locus
        self.countTable = {}
        self.translTable = {}

        # open tag for this section
        self.logFile.opentag('firstpass', locus=locus)
        self.logFile.writeln('<![CDATA[')

    def checkAlleleName(self, alleleName):
        """Checks allele name against the database.

        Returns the allele truncated to appropriate number of digits,
        if it can't be found using any of the heuristics, return it as
        an untyped allele (normally four asterisks)
        """

        #alleleInfo = self.filename + ":" + self.locus + ":" + alleleName
        alleleInfo = self.locus + ":" + alleleName

        # default return value is the allele name truncated to
        # numDigits length
        retval = alleleName[:self.numDigits]

        if alleleName in self.alleleLookupTable[self.locus]:
            if self.verboseFlag:
                self.logFile.write("[%s exact match: ]" % alleleInfo)
                    
        else:
            expandedList = []
            extraList = []
            lcdList = []

            for dbAllele in self.alleleLookupTable[self.locus]:
                if dbAllele[:self.numDigits] == alleleName:
                    expandedList.append(dbAllele)
                if alleleName[:self.numDigits] == dbAllele:
                    extraList.append(dbAllele)
                if alleleName[:self.numDigits] == dbAllele[:self.numDigits]:
                    lcdList.append(dbAllele)
            if expandedList != []:
                if self.verboseFlag:
                    self.logFile.write("[%s close exact matches:" % alleleInfo)
                    for li in expandedList:
                        self.logFile.write(" %s" % li)
                    self.logFile.write("]")
            elif extraList != []:
                if self.verboseFlag:
                    self.logFile.write("[%s close matches without trailing zeros:" % alleleInfo)
                    for li in extraList:
                        self.logFile.write(" %s" % li)
                    self.logFile.write("]")
            elif lcdList != []:
                if self.verboseFlag:
                    self.logFile.write("[%s close un-zero-padded matches into:" % alleleInfo)
                    for li in lcdList:
                        self.logFile.write(" %s" % li)
                    self.logFile.write("]")
            elif len(alleleName) < self.numDigits and self.preserveLowresFlag:
                if self.verboseFlag:
                    self.logFile.write("[%s short, low res allele name" % alleleInfo)
                    self.logFile.write("]")
                retval = alleleName
            else:
                if self.preserveUnknownFlag:
                    retval = alleleName
                else:
                    retval = self.untypedAllele
                if self.verboseFlag:
                    if alleleName == self.untypedAllele:
                        self.logFile.write("[%s untyped allele, do nothing]" % alleleInfo)
                    elif len(alleleName) < self.numDigits:
                        self.logFile.write("[%s TOO SHORT must be at least %d digits]" % (alleleInfo, self.numDigits))
                    else:
                        self.logFile.write("[%s NOT FOUND; no close matches!] " % alleleInfo)

        if retval == alleleName:
            self.logFile.writeln(" -> no truncation use: %s" % retval)
        else:
            self.logFile.writeln(" -> truncating to: %s" % retval)

        return retval

    def addAllele(self, alleleName):

        if alleleName not in self.translTable.keys():
            self.translTable[alleleName] = self.checkAlleleName(alleleName)

        filteredAllele = self.translTable[alleleName]

        if self.countTable.has_key(filteredAllele):
            self.countTable[filteredAllele] += 1
        else:
            self.countTable[filteredAllele] = 1

    def endFirstPass(self):

        if self.debug:
            print("translation table:", self.translTable)
            print("count table:", self.countTable)

        translKeys =  self.translTable.keys()

        for allele in translKeys:
            # check to see if we an allele of the form
            # XXX00 (i.e. it ends in zeros)

            alleleInfo = self.locus + ":" + allele
            
            prefix = allele[:-2]
            suffix = allele[-2:]
            if suffix == '00':
                
                self.logFile.write("[%s unresolved allele] " % alleleInfo)
                
                # first check to see if a variant XXX0n exists in the
                # population and choose the one with the highest
                # count
                maxSoFar = 1
                testAllele = None
                for v in [a for a in translKeys if a[:-2] == prefix and a[-2:] != suffix]:
                    count = self.countTable[v]
                    if count > maxSoFar:
                        maxSoFar = count
                        testAllele = v

                if testAllele:
                    self.logFile.writeln(" -> resolved to %s: (highest count %d in pop)" % (testAllele, maxSoFar))
                    self.translTable[allele] = testAllele

                # if none with given prefix are found in population,
                # then check database and find the first one with the
                # lowest number of the form XXX0n
                
                else:
                    for i in xrange(1,9):
                        testAllele = "%s0%d" % (prefix, i)

                        # only check to 4 digits of the allele name
                        # against database i.e. if 03011 and 03012
                        # both exist in the database return the match
                        # 0301 if the original allele-to-match is 0300
                        # and we are checking the first in the 030x
                        # series

                        foundMatch = 0
                        
                        for dbAllele in self.alleleLookupTable[self.locus]:

                            if dbAllele == testAllele:
                                self.logFile.writeln(" -> resolved to %s: (not found in pop, but exact match %s in database)" % (testAllele, dbAllele))
                                self.translTable[allele] = testAllele
                                foundMatch = 1
                                break
                            elif dbAllele[:4] == testAllele:
                                self.logFile.writeln(" -> resolved to %s: (not found in pop, but truncated match %s in database)" % (testAllele, dbAllele))
                                self.translTable[allele] = testAllele
                                foundMatch = 1
                                break

                        # don't check any more alleles if we've found
                        # a match
                        if foundMatch: break

        self.logFile.writeln(']]>')
        self.logFile.closetag('firstpass')
        self.logFile.writeln()
        if self.debug:
            print("after filtering:", self.translTable)

    def startFiltering(self):
        self.logFile.opentag('translateTable', locus=self.locus)
        self.logFile.writeln()
        
    def filterAllele(self, alleleName):

        if self.preserveAmbiguousFlag and len(alleleName.split("/")) > 1:
            transl_collection = []
            for subname in alleleName.split("/"):
                transl = self.checkAlleleName(subname)
                transl_collection += [transl]
                if subname != transl:
                    self.logFile.emptytag('translate', input=subname, output=transl)
                    self.logFile.writeln()
            transl = string.join(transl_collection,"/")
            if alleleName != transl:
                self.logFile.emptytag('translate', input=alleleName, output=transl)
                self.logFile.writeln()
            return transl
                
        else:
            transl = self.translTable[alleleName]
            if alleleName != transl:
                self.logFile.emptytag('translate', input=alleleName, output=transl)
                self.logFile.writeln()
            return transl

    def endFiltering(self):
        self.logFile.closetag('translateTable')
        self.logFile.writeln()

    def writeToLog(self, logstring='\n'):
        self.logFile.writeln(logstring)

    def cleanup(self):
        pass

################# translation methods begin here
    def makeSeqDictionaries(self, matrix=None, locus=None):
        
        self.matrix = matrix

        # polyseq is a dictionary, keyed on 'locus*allele', of all
        # allele sequences, containing ONLY the polymorphic positions.
        # polyseqpos is a dictionary, keyed on 'locus', of the
        # positions of the polymorphic residues which you find in
        # polyseq.
        
        self.polyseqpos = {}
        self.polyseq = {}

        # if method was called without a single locus specified, we
        # should find the sequences for ALL loci
        if locus == None:
            locusList = self.matrix.colList
        else:
            locusList = [locus]

        for locus in locusList:

            if self.debug:
               print("------> beginning sequence translation of locus: %s <------" % locus)

            # self.sequences is a dictionary, keyed on allele, used to
            # temporarily store full sequences
            self.sequences = {}

            self._getMSFLinesForLocus(locus)

            # read the expected length of the alignment, as told by the msf file header
            for line in self.lines:
                match = re.search('MSF: [0-9]+',line)
                if match:
                    break
            try:
                self.length = int(string.split(match.group())[1])
            except:
                # FIXME:  How do we want to handle a non-existent MSF header alignment length
                raise RuntimeError('could not find the alignment length from msf file %s.' % self.filename)

            # see where the header of the MSF file ends (demarcated by // )
            self.msfHead = 0
            for line in self.lines:
                if string.find(line,'//') != -1:
                    break
                else:
                    self.msfHead += 1

            rowCount = 0
            for individ in self.matrix[locus]:
                for allele in individ:

                    # if the allele hasn't been keyed yet, we'll have to get a sequence
                    if not self.sequences.has_key(allele):

                        # FIXME: this code is specific to HLA data
                        # find "null alleles" (ending in "N")
                        # it makes a null allele
                        if allele[-1:] == 'N':
                            ## FIXME: should we treat null alleles as 'unsequenced' or
                            ## as an 'untyped' allele?, according to discussion with
                            ## Steve Mack on 2006-04-03 best to have as 'untyped'
                            self.sequences[allele] = '*' * self.length

                        # get the sequence if we can...
                        elif allele in self.alleleLookupTable[locus]:
                            self.sequences[allele] = self._getSequenceFromLines(locus, allele)

                        # ...otherwise, try to find a good close match
                        else:
                            if allele == self.untypedAllele:
                                self.sequences[allele] = '*' * self.length

                            # FIXME: this code is specific to HLA data
                            # deal with 5 digit allele codes and try again
                            elif len(allele) == 5 and allele.isdigit():
                                allele6digits = allele[:4] + '0' + allele[4:5]
                                if self.debug:
                                    print('%s NOT found in msf file (probably because it is five digits), trying %s' % (allele, allele6digits))
                                if allele6digits in self.alleleLookupTable[locus]:
                                    self.sequences[allele] = self._getSequenceFromLines(locus, allele6digits)
                                else:
                                    self.sequences[allele] = self._getConsensusFromLines(locus, allele6digits)
                            ## FIXME: HLA-specific
                            ## also test for 7 digits
                            elif len(allele) == 7 and allele.isdigit():
                                allele8digits = allele[:4] + '0' + allele[4:6]
                                if self.debug:
                                    print('%s NOT found in msf file (probably because it is seven digits), trying %s' % (allele, allele8digits))
                                if allele8digits in self.alleleLookupTable[locus]:
                                    self.sequences[allele] = self._getSequenceFromLines(locus, allele8digits)
                                else:
                                    self.sequences[allele] = self._getConsensusFromLines(locus, allele8digits)

                            else:
                                self.sequences[allele] = self._getConsensusFromLines(locus, allele)

            if self.debug:
                print('full sequence for locus', locus, self.sequences)

            # Make the self.unsequenedSite (normally '#') the standard null placeholder
            for allele in self.sequences:
                ##self.sequences[allele] = string.replace(self.sequences[allele],'.','*')
                self.sequences[allele] = string.replace(self.sequences[allele],'.',self.unsequencedSite)
                ##self.sequences[allele] = string.replace(self.sequences[allele],'X','*')
                self.sequences[allele] = string.replace(self.sequences[allele],'X',self.unsequencedSite)
                
            # pre-populates the polyseq dictionary with empty strings,
            # so we can then build the polymorphic sequences
            # letter-by-letter.  keyed on 'locus*allele'
            for allele in self.sequences:
                self.polyseq[locus + '*' + allele] = ''

            # also initialize (with an empty list) polyseqpos
            # dictionary entry for this locus so we can append to it
            # later.  a note about positions: if you are using msf
            # files, the position will be relative to the official
            # IMGT/HLA sequence alignments (see
            # http://www.ebi.ac.uk/imgt/hla/nomen_pt2.html )
            self.polyseqpos[locus] = []

            # checks each position of each allele, counts the number
            # of unique characters (excepting . X and * characters)
            for pos in range(self.length):
                uniqueCounter = {}
                for allele in self.sequences:
                    letter = self.sequences[allele][pos]
                    ## FIXME: seems unnecessary to check '.' and 'X' because we have already
                    ## made them self.unsequencedSite above, check!!
                    if letter != '.' and letter != 'X' and letter != '*' and letter != self.unsequencedSite:
                        uniqueCounter[letter] = 1
                uniqueCount = len(uniqueCounter)

                # if it is a polymorphic position, we loop thru again
                # and add it to polyseq and add its position to
                # polyseqpos (actually we add the position plus one
                # because that is how humans count.)
                if uniqueCount > 1:
                    for allele in self.sequences:
                        self.polyseq[locus + '*' + allele] += self.sequences[allele][pos]
                    self.polyseqpos[locus].append(pos+1)

            # this block was used to output *complete* sequences for a pop file
            # (with all the positions, not just the polymorphic residues.)
            if len(self.polyseqpos[locus]) > 1:
                self.logFile.opentag('sequence',locus=locus)
                self.logFile.writeln()

                # this will give you the complete sequence of each individual
                for individ in self.matrix[locus]:
                    for allele in individ:
                        alleleString = "> " + allele
                        self.logFile.writeln(alleleString)
                        self.logFile.writeln(self.sequences[allele])
                # this will give you the complete sequence for each unique allele in the pop
                for allele in self.sequences:
                    alleleString = "> " + allele
                    self.logFile.writeln(alleleString)
                    self.logFile.writeln(self.sequences[allele])

                self.logFile.closetag('sequence')
                self.logFile.writeln()



        if self.debug:
            print(self.polyseq)
            print(self.polyseqpos)

        return self.polyseq, self.polyseqpos

    def translateMatrix(self, matrix=None):

        self.matrix = matrix
        self.polyseq, self.polyseqpos = self.makeSeqDictionaries(self.matrix)

        # log to the -filter.xml file
        self.logFile.opentag('sequence-summary')
        self.logFile.writeln()
        self.logFile.writeln('Sequence consensus method: %s' % self.sequenceFilterMethod)

        for locus in self.matrix.colList:
            alleleTally = {}
            for individ in self.matrix[locus]:
                for allele in individ:
                    if allele in alleleTally:
                        alleleTally[allele] += 1
                    else:
                        alleleTally[allele] = 1

            self.logFile.writeln('-------------------------')
            self.logFile.writeln('locus: %s' % locus)

            # makes the position numbers into a block of monospace, vertically oriented numbers
            if len(self.polyseqpos[locus]) > 0:
                positionString = {}
                longestPosition = len(str(max(self.polyseqpos[locus])))
                for positionDigit in xrange(longestPosition,0,-1):
                    positionString[positionDigit] = ''
                    for position in self.polyseqpos[locus]:
                        if len(str(position)) >= positionDigit:
                            positionString[positionDigit] += str(position)[-positionDigit]
                        else:
                            positionString[positionDigit] += ' '
                for line in xrange(len(positionString.keys()),0,-1):
                    self.logFile.writeln('\t\t' + positionString[line])

            li = alleleTally.keys()
            li.sort()
            for allele in li:
                self.logFile.writeln(allele + '\t' + str(alleleTally[allele]) + '\t' + self.polyseq[locus + '*' + allele])
            self.logFile.writeln()
            self.logFile.writeln('Total chromosomes: %d' % reduce(add,alleleTally.values()))

            for position in xrange(len(self.polyseqpos[locus])):
                positionTally = {}
                for allele in li:
                    letter = self.polyseq[locus + '*' + allele][position]
                    if letter in positionTally:
                        positionTally[letter] += alleleTally[allele]
                    else:
                        positionTally[letter] = alleleTally[allele]

                positionReportString = "Position: " + str(self.polyseqpos[locus][position])
                letters = positionTally.keys()
                letters.sort()
                for letter in letters:
                    positionReportString += "\t" + letter + " " + str(positionTally[letter])
                self.logFile.writeln(positionReportString)

            self.logFile.writeln()

        self.logFile.closetag('sequence-summary')


        # creating the new data matrix
        # colList is the new list of columns, like A_33, A_47, etc...
        colList = []
        for locus in self.matrix.colList:
            for pos in self.polyseqpos[locus]:
                colList.append(locus + '_' + self._genOffsets(locus, pos))

        rowCount = len(self.matrix[locus])

        if self.debug:
            print(rowCount)
            print(colList)
        
        seqMatrix = StringMatrix(rowCount, colList)

        for locus in self.matrix.colList:
            individCount = 0
            for individ in self.matrix[locus]:

                name1 = locus + '*' + individ[0]
                name2 = locus + '*' + individ[1]

                posCount = 0

                for pos in self.polyseqpos[locus]:

                    letter1 = self.polyseq[name1][posCount]
                    letter2 = self.polyseq[name2][posCount]

                    if letter1 == '*':
                        letter1 = self.untypedAllele
                    if letter2 == '*':
                        letter2 = self.untypedAllele
                    
                    ##if letter1 == '.' or letter1 == 'X' or letter1 == '*':
                        ##letter1 = self.untypedAllele
                    ##    letter1 = self.unsequencedSite
                    ##if letter2 == '.' or letter2 == 'X' or letter2 == '*':
                        ##letter2 = self.untypedAllele
                    ##    letter2 = self.unsequencedSite

                    seqMatrix[individCount,locus + '_' + \
                              self._genOffsets(locus, pos)] = (letter1,letter2)

                    posCount += 1
                    
                individCount += 1

        if self.debug:
            print(seqMatrix)

        return seqMatrix

    def _genOffsets(self, locus, pos):

        ## FIXME: this code is specific to HLA data
        offsets = {'A': 24, 'B':24, 'C':24,  'DQA1': 23, 'DRB1': 29,
                   'DQB1': 32, 'DPA1':31, 'DPB1': 29}

        if offsets.has_key(locus):
            str_pos = str(pos-offsets[locus])
        else:
            str_pos = str(pos)

        return str_pos

    def _getMSFLinesForLocus(self, locus):

        # FIXME: this code is specific to hla data
        # CORNER CASE! 'C' locus is called 'Cw' in data files
#        if locus == 'C':
#            locus = 'Cw'

        # FIXME:  make the file name configurable
        self.filename = locus + self.sequenceFileSuffix + '.msf'
        
        self.lines = open(os.path.join(self.directoryName, self.filename), 'r').readlines()



    def _getSequenceFromLines(self, locus=None, allele=None):

        # FIXME: this code is specific to hla data
        # CORNER CASE! 'C' locus is called 'Cw' in data files
#        if locus == 'C':
#            locus = 'Cw'

        name = locus + self.alleleDesignator + allele

        regexp = re.compile('.*' + re.escape(name) + ' .*')
        seq = ''
        for line in self.lines[self.msfHead:]:
            if string.find(line,name + ' ') != -1:
                match = re.search(regexp,line)
                seq = seq + string.join(string.split(match.group())[1:],'')

        # check length of seq against what we expected from the msf header
        if len(seq) < self.length:
            # pad with X's if the length is too short 
            if self.debug:
                print('%s is found, PADDED with %d Xs so it equals alignment length (%d).' % (allele,self.length-len(seq),self.length))
            seq += 'X'*(self.length-len(seq))

        elif len(seq) > self.length:
            # truncate if length is too long (FIXME: this should at least raise a warning)
            if self.debug:
                print('%s is found, TRUNCATED by %d so it equals alignment length (%d).' % (allele,len(seq)-self.length,self.length))
            seq = seq[:self.length-len(seq)]

        else:
            if self.debug:
                print('%s is found, length okay.' % (allele))

        return seq


    def _getConsensusFromLines(self, locus=None, allele=None):
        
        # dictionary to store all the good matches we come up with.
        # this will be used to make the consensus
        closestMatches = {}

        # we split the allele on the slash to deal with ambiguous typing
        for alleleSplit in allele.split('/'):
            # we pad 5-digit alleles with a fifth position zero (FIXME:
            # this is HLA specific!)
            if len(alleleSplit) == 5 and alleleSplit.isdigit():
                alleleSplit = alleleSplit[:4] + '0' + alleleSplit[4:5]
                
            # if the allele is 4 dig, ending in 00, we can safely chop
            # this off, as it won't be found in the seq dict
            if len(alleleSplit) == 4 and alleleSplit[2:4] == '00':
                alleleSplit = alleleSplit[:2]

            for potentialMatch in self.alleleLookupTable[locus]:
                for pos in range(len(potentialMatch)):
                    ## make sure that potential match is not a null allele
                    ## FIXME: HLA specific
                    if (alleleSplit == potentialMatch[:-pos] or alleleSplit == potentialMatch) and potentialMatch[-1:] != 'N':
                        closestMatches[potentialMatch] = self._getSequenceFromLines(locus, potentialMatch)

        seq = ''
        
        if len(closestMatches) == 0:
            if self.debug:
                print('%s NOT found in the msf file, no close matches found.' % allele)
            seq = '*' * self.length

        elif len(closestMatches) == 1:
            if self.debug:
                print('%s NOT found in the msf file, %s is only close match, so using that.' % (allele,closestMatches.keys()[0]))
            seq = closestMatches.values()[0]

        else:
            for pos in range(len(closestMatches.values()[0])):

                # checks each position of each allele, counts the number
                # of unique characters (excepting . X and * characters)
                uniqueCounter = {}

                for potentialMatch in closestMatches:
                    letter = closestMatches[potentialMatch][pos]

                    ## greedy method is to treat unsequencedSite as
                    ## ignored, thus allowing a consensus letter (if
                    ## same letter is otherwise present in 1 or more
                    ## other seqs)
                    if self.sequenceFilterMethod == 'greedy':
                        if letter != '.' and letter != 'X' and letter != '*' and letter != self.unsequencedSite:
                            uniqueCounter[letter] = 1
                            letterOfTheLaw = letter
                        else:
                            pass

                    ## default behavior (below) is to treat
                    ## unsequencedSite as a unique allele to make sure
                    ## that those sites don't get treated as having a
                    ## consensus sequence if only one of the sequences
                    ## in the the set of matches is typed
                    elif letter != '*':
                        uniqueCounter[letter] = 1
                        letterOfTheLaw = letter

                if self.debug:
                    print(uniqueCounter)
                uniqueCount = len(uniqueCounter)

                if uniqueCount == 1:
                    seq += letterOfTheLaw
                else:
                    seq += self.unsequencedSite

            if self.debug:
                print(seq)
                print('%s NOT found in the msf file, so we use a consensus of ' % allele, closestMatches.keys())

        return seq


class BinningFilter:
    """Filters data through rules defined in one file for each locus.

    """

    def __init__(self,
                 customBinningDict=None,
                 logFile=None,
                 untypedAllele='****',
                 filename=None,
                 binningDigits=4,
                 debug=0):
        self.binningDigits = binningDigits
        self.untypedAllele = untypedAllele
        self.customBinningDict = customBinningDict
        self.logFile = logFile
    
    def doDigitBinning(self,matrix=None):

        self.logFile.opentag('DigitBinningFilter')
        self.logFile.writeln('<![CDATA[')
        
        allele = ['','']
        for locus in matrix.colList:
            individCount = 0
            for individ in matrix[locus]:
                for i in range(2):
                    allele[i] = str(individ[i])  # FIXME: matrix type is `ndarray`
                    if allele[i] != self.untypedAllele and len(allele[i]) > self.binningDigits:
                        self.logFile.write("DigitBinning: " + locus + "* " + allele[i])
                        allele[i] = allele[i][:self.binningDigits]
                        self.logFile.writeln(" is being truncated to " + allele[i])
                        
                matrix[individCount,locus] = (allele[0],allele[1])
                individCount += 1

        self.logFile.writeln(']]>')
        self.logFile.closetag('CustomBinningFilter')
        self.logFile.writeln()
                
        return matrix

        
    def doCustomBinning(self, matrix=None):

        self.logFile.opentag('CustomBinningFilter')
        self.logFile.writeln('<![CDATA[')

        # go through each cell of the matrix and make necessary substitutions
        allele = ['','']
        for locus in matrix.colList:
            individCount = 0

            if locus.lower() in self.customBinningDict.keys():
            
                for individ in matrix[locus]:
                    for i in range(2):
                        individ[i] = str(individ[i])  # FIXME: matrix type is `ndarray` needs to be string for len() and other string operations
                        if len(individ[i].split("/")) > 1:
                            allele_collection = []
                            for subname in individ[i].split("/"):
                                allele_collection += [self.lookupCustomBinning(testAllele=subname, locus=locus)]

                            allele[i] = string.join(list(set(allele_collection)),"/")

                        else:
                            allele[i] = self.lookupCustomBinning(testAllele=individ[i], locus=locus)

                    
                    matrix[individCount,locus] = (allele[0],allele[1])
                    individCount += 1
                         
            else:
               self.logFile.writeln("Skipping CustomBinning filter for locus " + locus + " because no rules found.")

        self.logFile.writeln(']]>')
        self.logFile.closetag('CustomBinningFilter')
        self.logFile.writeln()
          
        return matrix

    def lookupCustomBinning(self, testAllele, locus):

        exactMatches = []
        closeMatches = {}

        # see if allele exists in the binning rules (exact or close)
        for ruleSet in self.customBinningDict[locus.lower()]:
            ruleSetSplit = ruleSet.strip('!').split('/')

            # check for exact match(es)
            if testAllele in ruleSetSplit:
                if ruleSet[0] == '!' and testAllele in ruleSetSplit[1:]:
                    exactMatches.append(ruleSetSplit[0])
                elif ruleSet[0] != '!':
                    exactMatches.append(ruleSet)

            # check for close match(es)
            if len(testAllele) > 2:
                ruleCounter = 0
                matchTracker = {}
                for potentialMatch in ruleSetSplit:
                    for digitSlice in range(len(testAllele)-2):
                        if testAllele[:-digitSlice-1] == potentialMatch:
                            if ruleSet[0] == '!':
                                closeMatches[ruleSetSplit[0]] = digitSlice+1
                            else:
                                closeMatches[ruleSet] = digitSlice+1

        if exactMatches != []:
            self.logFile.writeln("Exact rule match: " + locus + "* " + testAllele + " is being replaced by " + exactMatches[0])
            if len(exactMatches) > 1:
                print("WARNING: other exact matches found: " + locus + "* " + testAllele + exactMatches)
            return(exactMatches[0])

        elif len(closeMatches) > 0:
            bestScore = 1000
            for match in closeMatches:
                if closeMatches[match] < bestScore:
                    bestScore = closeMatches[match]
                    finalMatch = match
            self.logFile.writeln("Close rule match: " + locus + "* " + testAllele + " is being replaced by " + finalMatch)
            if len(closeMatches) > 1:
                print("WARNING: other close matches found: " + locus + "* " + testAllele + closeMatches)
            return(finalMatch)

        else:
            #self.logFile.writeln("No match found for: " + locus + "* " + testAllele + "!!!!!!!!")
            return(testAllele)

                        
 
class AlleleCountAnthonyNolanFilter(AnthonyNolanFilter):
    """Filters data with an allelecount less than a threshold.

    """
    def __init__(self,
                 lumpThreshold=None,
                 **kw):

        self.lumpThreshold = lumpThreshold
        AnthonyNolanFilter.__init__(self, **kw)

    def endFirstPass(self):

        """Do regular AnthonyNolanFilter then translate alleles with
        count < lumpThreshold to 'lump'

        """

        AnthonyNolanFilter.endFirstPass(self)

        # now, translate alleles with count < lumpThreshold to "lump"

        translKeys = self.translTable.keys()
        
        for allele in translKeys:

            filteredAllele = self.translTable[allele]

            if self.debug:
                print(allele, "translates to", filteredAllele, "and has count", self.countTable[filteredAllele])

            # if below the threshold, make allele 'lump
            if self.countTable[filteredAllele] <= self.lumpThreshold:
                self.translTable[allele] = 'lump'


        

