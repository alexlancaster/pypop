#! /usr/bin/env python

"""Module for parsing data files.

   Includes classes for parsing individuals genotyped at multiple loci
   and classes for parsing literature data which only includes allele
   counts."""

import sys, os, string

from Utils import getStreamType

class ParseFile:
    """*Abstract* class for parsing a datafile.

    *Not to be instantiated.*"""
    def __init__(self,
                 filename,
                 validPopFields=None,
                 validSampleFields=None,
                 separator='\t',
                 fieldPairDesignator='(2)',
                 debug=0):
        """Constructor for ParseFile object.

        - 'filename': filename for the file to be parsed.

        - 'validPopFields': a string consisting of valid headers (one
           per line) for overall population data (no default)

        - 'validSampleFields': a string consisting of valid headers
           (one per line) for lines of sample data.  (no default)

        - 'separator': separator for adjacent fields (default: a tab
           stop, '\\t').

        - 'fieldPairDesignator': designates the pair indicator if a
          fields are grouped in pairs [e.g. HLA-A, and HLA-A(B)]
          (default: '(2)')

        - 'debug': Switches debugging on if set to '1' (default: no
          debugging, '0')"""
        
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
        
        self._sampleFileRead(filename)
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
        assoc = {}
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

                augField = key + self.fieldPairDesignator
                unAugField = key[:-len(self.fieldPairDesignator)]
                if assoc.has_key(key):
                    # if key already used (col names are not unique)
                    # append the fieldPairDesignator
                    if augField in fieldList:  
                        # see if augmented field exists
                        # create a tuple at the same key value
                        assoc[key] = assoc[key], i
                    else:
                        print "error: can't find augmented fieldname", \
                              augField

                # if key is one of pair with the augmented already in
                # map, add it to make a tuple at that key
                # e.g. HLA-A(2) already exists and inserting HLA-A
                elif assoc.has_key(augField):
                    if augField in fieldList:
                        assoc[augField] = assoc[augField], i

                # likewise if key is one of pair with the unaugmented
                # already in map
                # e.g. HLA-A already exists and inserting HLA-A(2)
                elif assoc.has_key(unAugField):
                    if unAugField in fieldList:  
                        assoc[unAugField] = assoc[unAugField], i
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
        self.popData = {}
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
            
            fields = string.split(line)
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
        if type == 'xml':
            stream.opentag('populationdata')
            stream.writeln()
            
        for summary in self.popData.keys():
            if type == 'xml':
                # convert metadata name into a XML tag name
                tagname = string.lower(string.replace(summary,' ',''))
                stream.tagContents(tagname, self.popData[summary])
                stream.writeln()
            else:
                stream.writeln("%20s: %s" % (summary, self.popData[summary]))

        # call subclass-specific metadata serialization
        self.serializeSubclassMetadataTo(stream)
        
        if type == 'xml':
            stream.closetag('populationdata')
            stream.writeln()

class ParseGenotypeFile(ParseFile):
    """Class to parse standard datafile in genotype form.  Tweaked."""
    
    def __init__(self,
                 filename,
                 alleleDesignator='*',
                 untypedAllele='****',
                 **kw):
        """Constructor for ParseGenotypeFile.

        - 'filename': filename for the file to be parsed.
        
        In addition to the arguments for the base class, this class
        accepts the following additional keywords:

        - 'alleleDesignator': The first character of the key which
        determines whether this column contains allele data.  Defaults to
        '*'
        
        - 'untypedAllele': The designator for an untyped locus.  Defaults
        to '****'.
        """
        self.alleleDesignator=alleleDesignator
        self.untypedAllele=untypedAllele

        ParseFile.__init__(self, filename, **kw)
        self._genDataStructures()

    def _getAlleleColPos(self):
        """Returns dictionary containing 2-tuple of column position.

        It is keyed by allele names originally specified in sample
        metadata file

        Note that this is simply a _subset_ of that returned by
        **getSampleMap()**

        *For internal use only.*"""

        self.alleleMap = {}
        for key in self.sampleMap.keys():
            # do we have the allele designator?
            if key[0] == self.alleleDesignator:
                self.alleleMap[key] = self.sampleMap[key]

        return self.alleleMap

    def _genDataStructures(self):
        """Generates allele count and map data structures.
        
        *For internal use only.*"""        

        sampleDataLines, separator = self.getFileData()
        self._getAlleleColPos()


        self.totalIndivCount = len(sampleDataLines)
        self.totalLocusCount = len(self.alleleMap)
        
        self.freqcount = {}
        self.locusTable = {}

        # create an empty-list of lists to store all the row data
        self.individualsList = [[] for line in range(0, self.totalIndivCount)]

        # freeze the list of locusKeys in a particular order
        self.locusKeys = self.alleleMap.keys()
        
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

            # re-initialise the row count on each iteration of the locus
            rowCount = 0
            for line in sampleDataLines:
                fields = string.split(line, separator)

                allele1 = fields[col1]
                allele2 = fields[col2]

                if self.debug:
                    print rowCount, self.individualsList[rowCount]

                # extend the list by the allele pair
                self.individualsList[rowCount].extend([allele1 + ':',
                                                       allele2 + ':'])

                # increment row count
                rowCount += 1

                # ensure that *both* alleles are typed 
                if (self.untypedAllele != allele1) and \
                   (self.untypedAllele != allele2):
                    if alleleTable.has_key(allele1):
                        alleleTable[fields[col1]] += 1
                    else:
                        alleleTable[fields[col1]] = 1
                    total += 1

                    if alleleTable.has_key(allele2):
                        alleleTable[fields[col2]] += 1
                    else:
                        alleleTable[fields[col2]] = 1
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
            self.individualsData = self.individualsList, self.locusKeys

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
            isValidKey = 0

        # generate the key that matches the one in the
        # data file format
        if self.alleleDesignator + field in fieldList:
            key = self.alleleDesignator + field
        else:
            key = field

        return isValidKey, key

    def getLocusList(self):
        """Returns the list of loci.

        *Note: this list has filtered out all loci that consist
        of individuals that are all untyped.*

        *Note 2: the order of this list is now fixed for the lifetime
          of the object.*
        """
        
        return self.locusKeys

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

        Specifically, total number of individuals and loci.
         """
        type = getStreamType(stream)

        if type == 'xml':
            stream.opentag('totals')
            stream.writeln()
            stream.tagContents('indivcount', "%d" % self.totalIndivCount)
            stream.writeln()
            stream.tagContents('allelecount', "%d" % (self.totalIndivCount*2))
            stream.writeln()
            stream.tagContents('locuscount', "%d" % self.totalLocusCount)
            stream.writeln()
            stream.closetag('totals')
            stream.writeln()
        else:
            stream.writeln("%20s: %d" % \
                           ("Sample Size (n)", self.totalIndivCount))
            stream.writeln("%20s: %d" % \
                           ("Allele Count (2n)", self.totalIndivCount*2))
            stream.writeln("%20s: %d" % \
                           ("Total Loci", self.totalLocusCount))
	
    def serializeAlleleCountDataAt(self, stream, locus):
        """ """
        type = getStreamType(stream)
        
        alleleTable, total, untypedIndividuals = self.freqcount[locus]

        totalFreq = 0
        alleles = alleleTable.keys()
        alleles.sort()

        # if all individuals are untyped then supress itemized output
        if len(alleles) == 0:
            if type == 'xml':
                stream.emptytag('allelecounts', 'class', 'no-data')
                stream.writeln()
            else:
                stream.writeln("No allele data; no allele counts generated")
        else:

            if type == 'xml':
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
            else:
                stream.writeln("Individuals w/ missing data: %d" \
                               % untypedIndividuals)
                stream.writeln("Sample Size (n): %d" % (total/2))
                stream.writeln("Allele Count (2n): %d" % total)

                # print header of freq table
                stream.writeln("%4s: %-8s (%s)" % ("Name", "Freq", "Count"))

            for allele in alleles:
                freq = float(alleleTable[allele])/float(total)
                totalFreq += freq
                strFreq = "%0.5f " % freq
                strCount = ("%d" % alleleTable[allele])

                if type == 'xml':
                    stream.opentag('allele', 'name', allele)
                    stream.writeln()
                    stream.tagContents('frequency', strFreq)
                    stream.tagContents('count', strCount)
                    stream.writeln()
                    stream.closetag('allele')
                else:
                    stream.write("%s: %s (%s)" % (allele, strFreq, strCount))

                stream.writeln()

            strTotalFreq = "%0.5f" % totalFreq
            strTotal = "%d" % total

            if type == 'xml':
                stream.tagContents('totalfrequency', strTotalFreq)
                stream.writeln()
                stream.tagContents('totalcount', strTotal)
                stream.closetag("allelecounts")
            else:
                stream.writeln("Total frequency: %s (%s)"
                             % (strTotalFreq, strTotal))
            stream.writeln()

    def serializeAlleleCountDataTo(self, stream):
        type = getStreamType(stream)
        
        if type == 'xml':
            stream.opentag('allelecounts')
        else:
            stream.writeln("Allele counts")
            
        for locus in self.freqcount.keys():
            stream.writeln()
            if type == 'xml':
                stream.opentag('locus', 'name', locus)
            else:
                stream.write("Locus = %s" % locus)
                stream.writeln()
                self.serializeAlleleCountDataAt(stream, locus)
                stream.closetag('locus')
                    
        stream.writeln()
        
        if type == 'xml':
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

        return self.locusTable[locus]
    
    def getLocusData(self):
        """Returns the genotyped data for all loci.

        Returns a dictionary keyed by locus name of lists of 2-tuples
        as defined by 'getLocusDataAt()'
        """
        return self.locusTable

    def getIndividualsData(self):
        """Returns the individual data.

        Returns a 2-tuple consisting of:

        - a list of individuals (the original `rows' of data in the
          input file) each of which consists of an ordered list of
          allele strings.

        - an ordered list of keys (the locus names)
        """
        return self.individualsData

class ParseAlleleCountFile(ParseFile):
    """Class to parse datafile in allele count form.

    *Currently unimplemented*."""
    pass

# this test harness is called if this module is executed standalone
if __name__ == "__main__":

    # read in IHWG data file from first argument
    parsefile = ParseGenotypeFile(sys.argv[1], debug=1)


