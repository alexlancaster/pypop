#! /usr/bin/env python
import sys, string

class ParseFile:
    """Class to parse a standard IHWG datafile."""
    def __init__(self,
                 popFieldsFilename='ihwg-pop-fields.dat',
                 sampleFieldsFilename='ihwg-sample-fields.dat',
                 separator='\t',
                 debug=0):
        """Constructor for ParseFile object.

        - *popFieldsFieldname*: valid headers for overall population
           data  (default: `ihwg-pop-fields.dat')

        - *sampleFieldsFilename: valid headers for lines of sample
        data.  (default: `ihwg-sample-fields')

        - *separator*: separator for adjacent fields (default: a tab
           stop, '\t').

        - *debug*: Switches debugging on if set to `1' (default: no
           debugging, '0')"""
        self.popFieldsFilename=popFieldsFilename
        self.sampleFieldsFilename=sampleFieldsFilename
        self.debug = debug
        self.separator = separator

        if self.debug:
            print self.popFieldsFilename

        self.popFields = ParseFile._dbFieldsRead(self,self.popFieldsFilename)
        self.sampleFields = ParseFile._dbFieldsRead(self,self.sampleFieldsFilename)

        if self.debug:
            # debugging only
            print self.popFields
            print self.sampleFields
        
    def _dbFieldsRead(self, filename):
        """Takes a filename for a database and expects a file with
        database field names separated by newlines.

        Returns a tuple of field names.  Use internally only."""
        f = open(filename, 'r')
        data = f.readlines()
        li = []
        for line in data:
            if self.debug:
                print string.rstrip(line)
            li.append(string.rstrip(line))
        return tuple(li)

    def _mapFields(self, line, fieldList):
        """Takes a line and a list of valid fields and creates a dictionary
        of positions keyed by valid field names.

        - Complains if a field name is not valid.

        - Complains if the correct number of fields are not found for
        the metadata headers.
        
        Returns a 2-tuple:
        
        - a dictionary keyed by field name.

        - the total number of  metadata fields.

        Intended to be used internally by class only."""

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

            if (field in fieldList) or ("*" + field in fieldList):

                # generate the key that matches the one in the
                # data file format
                if "*" + field in fieldList:
                    key = "*" + field
                else:
                    key = field
                    
                if assoc.has_key(key):
                    # if key already used (col names are not unique)
                    # append a (2)
                    augField = key + "(2)"
                    if augField in fieldList:  
                        # see if augmented field exists
                        # create a tuple at the same key value
                        assoc[key] = assoc[key], i
                    else:
                        print "error: can't find augmented fieldname", \
                              augField
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

    def parseFile(self, filename):
        """Read and parse given filename.

        This method must be called before any accessor "get*" methods
        can be called."""
        
        self._sampleFileRead(filename)
        self._mapPopHeaders()
        self._mapSampleHeaders()

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
    
    def getAlleleMap(self):
        """Returns dictionary containing 2-tuple of column position.

        It is keyed by allele names originally specified in sample
        metadata file

        Note that this is simply a _subset_ of that returned by
        **getSampleMap()**"""

        self.alleleMap = {}
        for key in self.sampleMap.keys():
            # do we have the allele designator?
            if key[0] == '*':
                self.alleleMap[key] = self.sampleMap[key]

        return self.alleleMap

    def getFileData(self):
        """Returns file data.

        Returns a 2-tuple 'wrapper':

        - raw sample lines, *without*  header metadata.
        
        - the field separator."""
        return self.fileData[3:], self.separator
    
    def genSampleOutput(self, fieldList):

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


# this test harness is called if this module is executed standalone
if __name__ == "__main__":

    # create object
    parsefile = ParseFile()

    # read in IHWG data file from first argument
    parsefile.sampleFileRead(sys.argv[1])

    # print the parsed header info
    parsefile.mapHeaders()

