#! /usr/bin/env python

"""Module for parsing data files.

   Includes classes for parsing individuals genotyped at multiple loci
   and classes for parsing literature data which only includes allele
   counts."""

import sys, os, string, types, re

from Utils import getStreamType, StringMatrix, OrderedDict, TextOutputStream

class ParseFile:
    """*Abstract* class for parsing a datafile.

    *Not to be instantiated.*"""
    def __init__(self,
                 filename,
                 validPopFields=None,
                 validSampleFields=None,
                 separator='\t',
                 fieldPairDesignator='_1:_2',
                 debug=0):
        """Constructor for ParseFile object.

        - 'filename': filename for the file to be parsed.

        - 'validPopFields': a string consisting of valid headers (one
           per line) for overall population data (no default)

        - 'validSampleFields': a string consisting of valid headers
           (one per line) for lines of sample data.  (no default)

        - 'separator': separator for adjacent fields (default: a tab
           stop, '\\t').

        - 'fieldPairDesignator': a string which consists of additions
          to the allele `stem' for fields grouped in pairs (allele
          fields) [e.g. for `HLA-A', and `HLA-A(2)', then we use
          ':(2)', for `DQA1_1' and `DQA1_2', then use use '_1:_2', the
          latter case distinguishes both fields from the stem]
          (default: ':(2)')

        - 'debug': Switches debugging on if set to '1' (default: no
          debugging, '0')"""

        self.filename = filename
        self.validPopFields=validPopFields
        self.validSampleFields=validSampleFields
        self.debug = debug
        self.separator = separator
        self.fieldPairDesignator = fieldPairDesignator

        self.popFields = ParseFile._dbFieldsRead(self,self.validPopFields)
        self.sampleFields = ParseFile._dbFieldsRead(self,self.validSampleFields)
        if self.debug:
            # debugging only
            print self.popFields
            print self.sampleFields

        # Reads and parses a given filename.
        
        self._sampleFileRead(self.filename)
        self._mapPopHeaders()
        self._mapSampleHeaders()
        
    def _dbFieldsRead(self, data):
        """Reads the valid key, value pairs.

        Takes a string that is expected to consist of database field
        names separated by newlines.

        Returns a tuple of field names.

        *For internal use only.*"""
        li = []
        for line in string.split(data, os.linesep):
            if self.debug:
                print string.rstrip(line)
            li.append(string.rstrip(line))
        return tuple(li)

    def _mapFields(self, line, fieldList):
        """Creates a list of valid database fields.

        From a separator delimited string, creates a list of valid
        fields and creates a dictionary of positions keyed by valid
        field names.

        - Complains if a field name is not valid.

        - Complains if the correct number of fields are not found for
        the metadata headers.
        
        Returns a 2-tuple:
        
        - a dictionary keyed by field name.

        - the total number of  metadata fields.

        *For internal use only.*"""

        # split line
        fields = line.split(self.separator)

        # check to see if the correct number of fields found
        if len(fields) != len(fieldList):
            print "error: found", len(fields), "fields expected", \
                  len(fieldList), "fields"
        
        i = 0
        assoc = OrderedDict()
        for field in fields:

            # strip the field of leading and trailing blanks because
            # column name may inadvertantly contain these due to
            # spreadsheet -> tab-delimited file format idiosyncrasies
        
            field = string.strip(field)

            # check to see whether field is a valid key, and generate
            # the appropriate identifier, this is done as method call
            # so it can overwritten in subclasses of this abstract
            # class (i.e. the subclass will have 'knowledge' about the
            # nature of fields, but not this abstract class)
            
            isValidKey, key = self.genValidKey(field, fieldList)

            if isValidKey:

                # if key is one of pair already in map, add it to make
                # a tuple at that key e.g. `HLA-A(2)' already exists
                # and inserting `HLA-A', or `DQB1_1' and `DQB1_2' should
                # both be inserted at `DQB1'

                if assoc.has_key(key):
                    assoc[key] = assoc[key], i
                else:
                   assoc[key] = i
                    
            else:
                print "error: field name `%s' not valid" % field

            i = i + 1

        return assoc, i

    def _sampleFileRead(self, filename):
        """Reads filename into object.

        Takes a filename and reads the file data into an instance variable.

        *For internal use only*.
        """
        f = open(filename, 'r')
        self.fileData = f.readlines()

    def _mapPopHeaders(self):

        """Create associations for field names and input columns.
        
        Using the header information from the top of the file, creates
        a dictionary for the population-level data.

        Also validates the file information for the correct number of fields
        are present on each line

        *For internal use only*."""

        # get population header metadata
        popHeaderLine = string.rstrip(self.fileData[0])

        # parse it
        self.popMap, fieldCount = self._mapFields(popHeaderLine, self.popFields)

        # debugging only
        if self.debug:
            print "population header line: ", popHeaderLine
            print self.popMap

        # get population data
        popDataLine = string.rstrip(self.fileData[1])
        # debugging only
        if self.debug:
            print "population data line: ", popDataLine

        # make sure pop data line matches number expected from metadata
        popDataFields = string.split(popDataLine, self.separator)
        if len(popDataFields) != fieldCount:
            print "error: found", len(popDataFields),\
                  "fields expected", fieldCount, "fields"

        # create a dictionary using the metadata field names as key
        # for the population data
        self.popData = OrderedDict()
        for popField in self.popMap.keys():
            self.popData[popField] = popDataFields[self.popMap[popField]]

    def _mapSampleHeaders(self):
        """Create the associations between field names and input columns.

        Using the header information from the top of the file, creates
        associations for the sample data fields.

        Also validates the file information for the correct number of fields
        are present on each line

        *For internal use only*."""

        # get sample header metadata
        sampleHeaderLine = string.rstrip(self.fileData[2])

        # parse it
        self.sampleMap, fieldCount = self._mapFields(sampleHeaderLine,
                                                     self.sampleFields)
        # debugging only
        if self.debug:
            print "sample header line: ", sampleHeaderLine
            print self.sampleMap

        # check file data to see that correct number of fields are
        # present for each sample

        for lineCount in range(3, len(self.fileData)):

            # retrieve and strip newline
            line = string.rstrip(self.fileData[lineCount])

            # restore the data with the newline stripped
            self.fileData[lineCount] = line
            
            fields = string.split(line, self.separator)
            if fieldCount != len(fields):
                print "error: incorrect number of fields:", len(fields), \
                      "found, should have:", fieldCount, \
                      "\noffending line is:\n", line

    def getPopData(self):
        """Returns a dictionary of population data.

        Dictionary is keyed by types specified in population metadata
        file"""
        return self.popData

    def getSampleMap(self):
        """Returns dictionary of sample data.

        Each dictionary position contains either a 2-tuple of column
        position or a single column position keyed by field originally
        specified in sample metadata file"""

        return self.sampleMap
    
    def getFileData(self):
        """Returns file data.

        Returns a 2-tuple `wrapper':

        - raw sample lines, *without*  header metadata.
        
        - the field separator."""
        return self.fileData[3:], self.separator
    
    def genSampleOutput(self, fieldList):
        """Prints the data specified in ordered field list.

        *Use is currently deprecated.*"""

        #for field in fieldList:
        #print string.strip(field) + self.separator,
        for lineCount in range(3, len(self.fileData)):
            line = string.strip(self.fileData[lineCount])
            element = string.split(line, self.separator)
            for field in fieldList:
                if self.sampleMap.has_key(field):
                    print element[self.sampleMap[field]],
                else:
                    print "can't find this field"
                    print "\n"

    def serializeMetadataTo(self, stream):
        type = getStreamType(stream)
        stream.opentag('populationdata')
        stream.writeln()
            
        for summary in self.popData.keys():
            # convert metadata name into a XML tag name
            tagname = string.lower(string.replace(summary,' ','-'))
            stream.tagContents(tagname, self.popData[summary])
            stream.writeln()

        # call subclass-specific metadata serialization
        self.serializeSubclassMetadataTo(stream)
        
        stream.closetag('populationdata')
        stream.writeln()

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

class ParseGenotypeFile(ParseFile):
    """Class to parse standard datafile in genotype form."""
    
    def __init__(self,
                 filename,
                 alleleDesignator='*',
                 untypedAllele='****',
                 popNameDesignator='+',
                 filter=None,
                 **kw):
        """Constructor for ParseGenotypeFile.

        - 'filename': filename for the file to be parsed.
        
        In addition to the arguments for the base class, this class
        accepts the following additional keywords:

        - 'alleleDesignator': The first character of the key which
        determines whether this column contains allele data.  Defaults to
        '*'

        - 'popNameDesignator': The first character of the key which
        determines whether this column contains the population name.
        Defaults to '+'

        - 'filter': Instance of filter for alleles (e.g. anthonynolan)
        
        - 'untypedAllele': The designator for an untyped locus.  Defaults
        to '****'.
        """
        self.alleleDesignator=alleleDesignator
        self.untypedAllele=untypedAllele
        self.popNameDesignator = popNameDesignator
        self.filter = filter
        
        ParseFile.__init__(self, filename, **kw)

        self._genDataStructures()

    def _genInternalMaps(self):
        """Returns dictionary containing 2-tuple of column position.

        It is keyed by locus names originally specified in sample
        metadata file, the locus names (keys) are made uppercase and
        don't contain the allele designator.

        Note that this is simply a transformed _subset_ of that
        returned by **getSampleMap()**

        *For internal use only.*"""

        self.alleleMap = OrderedDict()
        for key in self.sampleMap.keys():

            # do we have the allele designator?
            if key[0] == self.alleleDesignator:
                # remove allele designator, only necessary
                # for initial splitting out of locus keys from
                # other fields, and also make uppercase
                locusKey = string.upper(key[len(self.alleleDesignator):])
                self.alleleMap[locusKey] = self.sampleMap[key]
            elif key[0] == self.popNameDesignator:
                self.popNameCol = self.sampleMap[key]

        return self.alleleMap


    def _genDataStructures(self):
        """Generates allele count and map data structures.
        
        *For internal use only.*"""        

        sampleDataLines, separator = self.getFileData()

        # generate alleleMap and population field name
        self._genInternalMaps()

        if self.debug:
            print 'sampleMap keys:', self.sampleMap.keys()
            print 'sampleMap values:', self.sampleMap.values()
            print 'popNameCol', self.popNameCol
            print 'first line of data', sampleDataLines[0]

        # first get popName
        self.popName = string.split(sampleDataLines[0], separator)[self.popNameCol]

        # then total number of individuals in data file
        self.totalIndivCount = len(sampleDataLines)

        # total number of loci contained in original file
        self.totalLocusCount = len(self.alleleMap)

        # total loci that contain usable data
        self.totalLociWithData = 0
        
        self.freqcount = {}
        self.locusTable = {}

        # freeze the list of locusKeys in a particular order
        self.locusKeys = self.alleleMap.keys()

        # create an empty-list of lists to store all the row data
        #self.individualsList = [[] for line in range(0, self.totalIndivCount)]
        self.matrix = StringMatrix(self.totalIndivCount, self.locusKeys)

        self.filter.writeToLog()
        self.filter.writeToLog("|| %s : filter results ||" % self.filename)
        self.filter.writeToLog()
        
        for locus in self.locusKeys:
	    if self.debug:
	       print "locus name:", locus
	       print "column tuple:", self.alleleMap[locus]
            col1, col2 = self.alleleMap[locus]

            # initialise blank dictionary
            alleleTable = {}

            # initialise blank list
            self.locusTable[locus] = []
            
            total = 0
            untypedIndividuals = 0

            # first pass runs a filter of alleles through the
            # anthonynolan data filter/cleaner

            # initialize the filter
            self.filter.startFirstPass(locus)

            # loop through all lines in locus
            for line in sampleDataLines:
                fields = string.split(line, separator)
                allele1 = string.strip(fields[col1])
                allele2 = string.strip(fields[col2])
                self.filter.addAllele(allele1)
                self.filter.addAllele(allele2)

            # do final reassignments based on counts
            self.filter.endFirstPass()

            # re-initialise the row count on each iteration of the locus
            rowCount = 0
            for line in sampleDataLines:
                fields = string.split(line, separator)

                # put all alleles through filter before doing
                # data structures
                allele1 = self.filter.filterAllele(string.strip(fields[col1]))
                allele2 = self.filter.filterAllele(string.strip(fields[col2]))
                    
                # extend the list by the allele pair
                #self.individualsList[rowCount].extend([allele1 + ':',
                #                                       allele2 + ':'])

                # underlying NumPy array data type won't allow storage
                # of any sequence-type object (e.g. list or tuple) but
                # we can workaround this by overriding the __setitem__
                # method of the UserArray wrapper class used for
                # subtyping and storing tuple internally as two
                # separate columns in the underlying array.

                self.matrix[rowCount,locus] = (allele1, allele2)
                
                if self.debug:
                    print rowCount, self.matrix[rowCount,locus]

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
                    print col1, col2, allele1, allele2, total
                    
            self.freqcount[locus] = alleleTable, total, untypedIndividuals

            # if all individuals in a locus aren't untyped
            # then count this locus as having usable data
            if untypedIndividuals < self.totalIndivCount:
                self.totalLociWithData += 1                

        # close log file for filter
        #self.filter.logFile.close()

    def _checkAlleles(self):
        pass

    def genValidKey(self, field, fieldList):
        """Check and validate key.

        - 'field':  string with field name.

        - 'fieldList':  a dictionary of valid fields.
        
        Check to see whether 'field' is a valid key, and generate the
        appropriate 'key'.  Returns a 2-tuple consisting of
        'isValidKey' boolean and the 'key'.

        *Note: this is explicitly done in the subclass of the abstract
        'ParseFile' class (i.e. since this subclass should have
        `knowledge' about the nature of fields, but the abstract
        class should not have)*"""

        if (field in fieldList) or \
           (self.alleleDesignator + field in fieldList):
            isValidKey = 1
        else:
            if self.popNameDesignator + field in fieldList:
                isValidKey = 1
            else:
                isValidKey = 0

        # generate the key that matches the one in the data file
        # format

        # if this is an `allele'-type field
        if self.alleleDesignator + field in fieldList:

            li = string.split(self.fieldPairDesignator,":")

            # if pair identifiers are both the same length and
            # non-zero (e.g. '_1' and '_2', then we can assume that
            # the underlying `stem' should be the field name with the
            # pair identifer stripped off, otherwise simply use the
            # field name
            
            if (len(li[0]) == len(li[1])) and (len(li[0]) != 0):
                key = self.alleleDesignator + field[:-len(li[0])]
            else:
                key = self.alleleDesignator + field

        else:
            # this is the population field name
            if self.popNameDesignator + field in fieldList:
                key = self.popNameDesignator + field
            else:
                # this is a regular (non-`allele' type field)
                key = field

        if self.debug:
            print "validKey: %d, key: %s" % (isValidKey, key)
            
        return isValidKey, key

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

        stream.tagContents('popname', self.popName)
        stream.writeln()
        stream.opentag('totals')
        stream.writeln()
        stream.tagContents('indivcount', "%d" % self.totalIndivCount)
        stream.writeln()
        stream.tagContents('allelecount', "%d" % (self.totalIndivCount*2))
        stream.writeln()
        stream.tagContents('locuscount', "%d" % self.totalLocusCount)
        stream.writeln()
        stream.tagContents('lociWithDataCount', "%d" % self.totalLociWithData)
        stream.writeln()
        stream.closetag('totals')
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

class ParseAlleleCountFile(ParseFile):
    """Class to parse datafile in allele count form.

    Currently  only handles one locus per population, in format:

    <metadata-line1>
    <metadata-line2>
    DQA1 count
    0102 20
    0103 33
    ...
    
    *Currently a prototype implementation*."""
    def __init__(self,
                 filename,
                 **kw):
        ParseFile.__init__(self, filename, **kw)
        self._genDataStructures()

    def _genDataStructures(self):
        sampleDataLines, separator = self.getFileData()

        total = 0
        self.freqcount = {}

        self.alleleTable = {}
        
        for line in sampleDataLines:
            allele, count = string.split(line, separator)
            # store as an integer
            self.alleleTable[allele] = int(count)
            total += int(count)

        # store in an iVar for the moment
        self.totalAlleleCount = total
        
        if self.debug:
            print 'alleleTable', self.alleleTable
            print 'sampleMap keys:', self.sampleMap.keys()
            print 'sampleMap values:', self.sampleMap.values()
            
        # simply reconstruct the 3-tuple as generated in
        # ParseGenotypeFile: alleleTable (a map of counts keyed by
        # allele), total allele count and the number of untyped
        # individuals (in this case, by definition it is zero).
        # then store in the same data structure as ParseGenotypeFile

        # use the locus name as key
        self.locusName = self.sampleMap.keys()[0]
        
        # even though we only have a single locus, this will make it
        # easy to generalize later

        self.freqcount[self.locusName] = \
                                  self.alleleTable, self.totalAlleleCount, 0


    def genValidKey(self, field, fieldList):
        """Checks to  see validity of a field.

        Given a 'field', this is checked against the 'fieldList' and a
        tuple of a boolean (key is valid) and a a key is returned.

        The first element in the 'fieldList' which is a locus name,
        can match one of many loci (delimited by colons ':').  E.g. it
        may look like:

        'DQA1:DRA:DQB1'

        If the field in the input file match *any* of these keys,
        return the field and a valid match.
        """
        if (field in fieldList):
            isValidKey = 1
        else:
            # get the locus name, always the first in the list
            name = fieldList[0]

            # turn this into a list, splitting on the colon
            # delimiter
            listOfValidLoci = string.split(name, ":")

            # check to see if the locus is one of the valid ones
            if (field in listOfValidLoci):
                isValidKey = 1
            else:
                isValidKey = 0

        return isValidKey, field

    def serializeSubclassMetadataTo(self, stream):
        """Serialize subclass-specific metadata.

        Specifically, total number of alleles and loci.
         """

        stream.opentag('totals')
        stream.writeln()
        stream.tagContents('allelecount', "%d" % self.totalAlleleCount)
        stream.writeln()
        stream.tagContents('locuscount', "%d" % 1)
        stream.writeln()
        stream.closetag('totals')
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

# this test harness is called if this module is executed standalone
if __name__ == "__main__":

    # read in IHWG data file from first argument
    parsefile = ParseGenotypeFile(sys.argv[1], debug=1)


