#! /usr/bin/env python

"""Module for filtering data files.

   Filters and cleans data before being accepted as input to PyPop
   analysis routines.

."""

import sys, os, string, types, re, exceptions
from Utils import OrderedDict, TextOutputStream

class SubclassError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Sub class must implement this method"

class Filter:
    def __init__(self):
        pass
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
    def __init__(self):
        pass
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

    Data sets found at "anthonynolan":http://www.anthonynolan.com
    """
    def __init__(self,
                 directoryName='/home/alex/ihwg/src/data/anthonynolan/HIG-seq-pep-text/',
                 logFile=None,
                 untypedAllele='****',
                 filename=None,
                 numDigits=4,
                 verboseFlag=1,
                 debug=0):

        self.directoryName = directoryName
        self.numDigits = numDigits
        self.verboseFlag = verboseFlag
        self.debug = debug
        self.untypedAllele = untypedAllele
        self.filename = filename
        self.logFile = logFile

        # start log file
        self.logFile.opentag('filterlog', filename=self.filename)
        self.logFile.writeln()

        patt = re.compile("^([0-9a-zA-Z]+)\*([0-9a-zA-Z]+)")
        
        self.alleleLookupTable = {}
        loci = ['a', 'b', 'c', 'dqa', 'dqb', 'dra', 'drb', 'dpb', 'dpa']
        
        for locus in loci:
            if self.debug:
                print locus
            lines = (open(os.path.join(directoryName, locus + '_pt.txt'), 'r')).readlines()

            for line in lines:
                matchobj = re.search(patt, line)
                if matchobj:
                    name = matchobj.group(1)
                    # corner case!!
                    # 'C' locus is called 'Cw' in data files
                    if name == "Cw":
                        name = "C"
                    allele = matchobj.group(2)
                    if self.debug:
                        print name, allele
                    if self.alleleLookupTable.has_key(name):
                        if allele not in self.alleleLookupTable[name]:
                            self.alleleLookupTable[name].append(allele)
                    else:
                        self.alleleLookupTable[name] = []
                        self.alleleLookupTable[name].append(allele)

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
            else:
                #retval = self.untypedAllele
                retval = alleleName
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
            print "translation table:", self.translTable
            print "count table:", self.countTable

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
            print "after filtering:", self.translTable

    def startFiltering(self):
        self.logFile.opentag('translateTable', locus=self.locus)
        self.logFile.writeln()
        
    def filterAllele(self, alleleName):
        transl = self.translTable[alleleName]
        if alleleName != transl:
            self.logFile.emptytag('translate', input=alleleName, output=transl)
            self.logFile.writeln()
        return transl

    def endFiltering(self):
        self.logFile.closetag('translateTable')
        self.logFile.writeln()

    def writeToLog(self, logstring=os.linesep):
        self.logFile.writeln(logstring)

    def cleanup(self):
        # end tag for XML
        self.logFile.closetag('filterlog')
        # close log file
        self.logFile.close()


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
                print allele, "translates to", filteredAllele, "and has count", self.countTable[filteredAllele]

            # if below the threshold, make allele 'lump
            if self.countTable[filteredAllele] <= self.lumpThreshold:
                self.translTable[allele] = 'lump'


        



            
