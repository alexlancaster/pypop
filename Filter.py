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
    def filterAllele(self, alleleName):
        raise SubclassError()
    def writeToLog(self, logstring=None):
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
    def filterAllele(self, alleleName):
        return alleleName
    def writeToLog(self, logstring=None):
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

    def checkAlleleName(self, alleleName):
        """Checks allele name against the database.

        Returns the allele truncated to appropriate number of digits,
        if it can't be found using any of the heuristics, return it as
        an untyped allele (normally four asterisks)
        """

        alleleInfo = self.filename + ":" + self.locus + ":" + alleleName
        
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
                        if testAllele in self.alleleLookupTable[self.locus]:
                            self.logFile.writeln(" -> resolved to %s: (not found in pop, but in database)" % testAllele)
                            self.translTable[allele] = testAllele
                            break
                
        if self.debug:
            print "after filtering:", self.translTable
        
        
    def filterAllele(self, alleleName):
        transl = self.translTable[alleleName]
        if alleleName != transl:
            self.logFile.writeln("<<%s to %s>>" % (alleleName, transl))
        return transl

    def writeToLog(self, logstring=os.linesep):
        self.logFile.writeln(logstring)

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


        



            
