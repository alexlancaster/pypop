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

"""Module for parsing data files.

   Includes classes for parsing individuals genotyped at multiple loci
   and classes for parsing literature data which only includes allele
   counts."""

import sys, os, string, types, re, operator

from PyPop.Utils import getStreamType, StringMatrix, OrderedDict, TextOutputStream

class ParseFile:
    """*Abstract* class for parsing a datafile.

    *Not to be instantiated.*"""
    def __init__(self,
                 filename,
                 validPopFields=None,
                 validSampleFields=None,
                 separator='\t',
                 fieldPairDesignator='_1:_2',
                 alleleDesignator='*',
                 popNameDesignator='+',
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

        - 'alleleDesignator': The first character of the key which
        determines whether this column contains allele data.  Defaults to
        '*'

        - 'popNameDesignator': The first character of the key which
        determines whether this column contains the population name.
        Defaults to '+'

        - 'debug': Switches debugging on if set to '1' (default: no
          debugging, '0')"""

        self.filename = filename
        self.validPopFields=validPopFields
        self.validSampleFields=validSampleFields
        self.debug = debug
        self.separator = separator
        self.fieldPairDesignator = fieldPairDesignator
        self.alleleDesignator=alleleDesignator
        self.popNameDesignator = popNameDesignator

        # assume no population or sample data, until supplied
        self.popData = None
        self.sampleMap = None
    
        # Reads and parses a given filename.

        self._sampleFileRead(self.filename)


        if self.validPopFields == None:
            # skip parsing of metadata header
            self.sampleFirstLine = 1
        else:
            # parse metadata header
            self.sampleFirstLine = 3

            # gets the .ini file information for metadata
            self.popFields = ParseFile._dbFieldsRead(self, self.validPopFields)
            if self.debug:
                # debugging only
                print("validPopFields:", self.validPopFields)
                print("popFields:", self.popFields)

            # parse the metadata
            self._mapPopHeaders()


        # gets the .ini file information for samples
        self.sampleFields = ParseFile._dbFieldsRead(self, self.validSampleFields)
        if self.debug:
            print(self.sampleFields)

        # always parse the samples, they must always exist!
        self._mapSampleHeaders()

    def _dbFieldsRead(self, data):
        """Reads the valid key, value pairs.

        Takes a string that is expected to consist of database field
        names separated by newlines.

        Returns a tuple of field names.

        *For internal use only.*"""
        li = []
        for line in data.split():
            if self.debug:
                print(line.rstrip())
            li.append(line.rstrip())
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
        if len(fields) != len(fieldList) and self.debug:
            print("warning: found", len(fields), "fields expected",
                  len(fieldList), "fields")
        
        i = 0
        assoc = OrderedDict()
        for field in fields:

            # strip the field of leading and trailing blanks because
            # column name may inadvertantly contain these due to
            # spreadsheet -> tab-delimited file format idiosyncrasies
        
            field = field.strip()

            # check to see whether field is a valid key, and generate
            # the appropriate identifier, this is done as method call
            # so it can overwritten in subclasses of this abstract
            # class (i.e. the subclass will have 'knowledge' about the
            # nature of fields, but not this abstract class)
            
            # If an asterisk character is given as the first item in
            # the valid fields list, then accept any field name (ie,
            # locus name) as valid.  This makes sense only in the
            # allelecount file context.
            if fieldList[0] == "*":
                isValidKey, key = (1, field)
            else:
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
                    
            elif self.debug:
                print("warning: field name `%s' not valid" % field)

            i = i + 1

        return assoc, i

    def _sampleFileRead(self, filename):
        """Reads filename into object.

        Takes a filename and reads the file data into an instance variable.

        *For internal use only*.
        """
        with open(filename, 'r') as f:
            self.fileData = f.readlines()

    def _mapPopHeaders(self):

        """Create associations for field names and input columns.
        
        Using the header information from the top of the file, creates
        a dictionary for the population-level data.

        Also validates the file information for the correct number of fields
        are present on each line

        *For internal use only*."""

        # get population header metadata
        popHeaderLine = self.fileData[0].rstrip()

        # parse it
        self.popMap, fieldCount = self._mapFields(popHeaderLine, self.popFields)

        # debugging only
        if self.debug:
            print("population header line: ", popHeaderLine)
            print(self.popMap)

        # get population data
        popDataLine = self.fileData[1].rstrip()
        # debugging only
        if self.debug:
            print("population data line: ", popDataLine)

        # make sure pop data line matches number expected from metadata
        popDataFields = popDataLine.split(self.separator)
        if len(popDataFields) != fieldCount:
            print("error: found", len(popDataFields),
                  "fields expected", fieldCount, "fields")

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
        sampleHeaderLine = self.fileData[self.sampleFirstLine-1].rstrip()

        # parse it
        self.sampleMap, fieldCount = self._mapFields(sampleHeaderLine,
                                                     self.sampleFields)
        # debugging only
        if self.debug:
            print("sample header line: ", sampleHeaderLine)
            print(self.sampleMap)

        # check file data to see that correct number of fields are
        # present for each sample

        for lineCount in range(self.sampleFirstLine, len(self.fileData)):

            # retrieve and strip newline
            line = self.fileData[lineCount].rstrip()

            # restore the data with the newline stripped
            self.fileData[lineCount] = line
            
            fields = line.split(self.separator)
            if fieldCount != len(fields):
                print("error: incorrect number of fields:", len(fields),
                      "found, should have:", fieldCount,
                      "\noffending line is:\n", line)


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
        return self.fileData[self.sampleFirstLine:], self.separator
    
    def genSampleOutput(self, fieldList):
        """Prints the data specified in ordered field list.

        *Use is currently deprecated.*"""

        #for field in fieldList:
        #print string.strip(field) + self.separator,
        for lineCount in range(self.sampleFirstLine, len(self.fileData)):
            line = self.fileData[lineCount].strip()
            element = line.split(self.separator)
            for field in fieldList:
                if self.sampleMap.has_key(field):
                    print(element[self.sampleMap[field]]),
                else:
                    print("can't find this field\n")

    def serializeMetadataTo(self, stream):
        type = getStreamType(stream)

        stream.opentag('populationdata')
        stream.writeln()

        if self.popData:

            for summary in self.popData.keys():
                # convert metadata name into a XML tag name
                tagname = summary.replace(' ','-').lower()
                stream.tagContents(tagname, self.popData[summary])
                stream.writeln()

        # call subclass-specific metadata serialization
        self.serializeSubclassMetadataTo(stream)
            
        stream.closetag('populationdata')
        stream.writeln()

class ParseGenotypeFile(ParseFile):
    """Class to parse standard datafile in genotype form."""
    
    def __init__(self,
                 filename,
                 untypedAllele='****',
                 **kw):
        """Constructor for ParseGenotypeFile.

        - 'filename': filename for the file to be parsed.
        
        In addition to the arguments for the base class, this class
        accepts the following additional keywords:

        - 'untypedAllele': The designator for an untyped locus.  Defaults
        to '****'.
        """
        self.untypedAllele=untypedAllele
        
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

        # assume there is no population column
        
        popNameCol = None

        # create a map that only contains non-allele fields
        self.nonAlleleMap = OrderedDict()

        self.alleleMap = OrderedDict()
        for key in self.sampleMap.keys():

            # do we have the allele designator?
            if key[0] == self.alleleDesignator:
                # remove allele designator, only necessary
                # for initial splitting out of locus keys from
                # other fields, and also make uppercase
                locusKey = key[len(self.alleleDesignator):].upper()
                self.alleleMap[locusKey] = self.sampleMap[key]
            elif key[0] == self.popNameDesignator:
                popNameCol = self.sampleMap[key]
                self.nonAlleleMap[key[1:]] = self.sampleMap[key]
            else:
                self.nonAlleleMap[key] = self.sampleMap[key]

        if popNameCol == None:
            self.popName = None
        else:
            # save population name
            self.popName = self.fileData[self.sampleFirstLine].split(self.separator)[popNameCol]


    def _genDataStructures(self):
        """Generates matrix only
        
        *For internal use only.*"""        

        # generate alleleMap and population field name
        self._genInternalMaps()

        sampleDataLines, separator = self.getFileData()

        if self.debug:
            print('sampleMap keys:', self.sampleMap.keys())
            print('sampleMap values:', self.sampleMap.values())
            print('first line of data', sampleDataLines[0])


        # then total number of individuals in data file
        self.totalIndivCount = len(sampleDataLines)

        # total number of loci contained in original file
        self.totalLocusCount = len(self.alleleMap)

        # freeze the list of locusKeys in a particular order
        self.locusKeys = self.alleleMap.keys()

        # freeze list of non-allel data
        self.extraKeys = self.nonAlleleMap.keys()

        # create an empty-list of lists to store all the row data
        #self.individualsList = [[] for line in range(0, self.totalIndivCount)]
        self.matrix = StringMatrix(self.totalIndivCount,
                                   self.locusKeys,
                                   self.extraKeys,
                                   self.separator,
                                   self.fileData[:self.sampleFirstLine-1])

        rowCount = 0
        # store all the non-allele meta-data
        for line in sampleDataLines:
            fields = line.split(self.separator)
            for key in self.nonAlleleMap.keys():
                self.matrix[rowCount, key] = fields[self.nonAlleleMap[key]]

            rowCount += 1

        if self.debug:
            print("before filling matrix with allele data")
            print(self.matrix)

        for locus in self.locusKeys:
            if self.debug:
               print("locus name:", locus)
               print("column tuple:", self.alleleMap[locus])

            col1, col2 = self.alleleMap[locus]

            # re-initialise the row count on each iteration of the locus
            rowCount = 0
            for line in sampleDataLines:
                fields = line.split(self.separator)

                # create data structures

                allele1 = fields[col1].strip()
                allele2 = fields[col2].strip()

                # underlying NumPy array data type won't allow storage
                # of any sequence-type object (e.g. list or tuple) but
                # we can workaround this by overriding the __setitem__
                # method of the UserArray wrapper class used for
                # subtyping and storing tuple internally as two
                # separate columns in the underlying array.

                self.matrix[rowCount,locus] = (allele1, allele2)
                
                if self.debug:
                    print(rowCount, self.matrix[rowCount,locus])

                # increment row count
                rowCount += 1

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

            li = self.fieldPairDesignator.split(":")

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
            print("validKey: %d, key: %s" % (isValidKey, key))
            
        return isValidKey, key

    def getMatrix(self):
        """Returns the genotype data.

        Returns the genotype data in a 'StringMatrix' NumPy array.
        """
        return self.matrix

    def serializeSubclassMetadataTo(self, stream):
        """Serialize subclass-specific metadata."""

        if self.popName:
            # if present in input , print population name
            stream.tagContents('popname', self.popName)
            stream.writeln()


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

        self.alleleTable = {}
        totalAlleles = 0
        for line in sampleDataLines:
            allele, count = line.split(separator)
            # convert to integer
            count = int(count)
            # check to see if key already exists
            if self.alleleTable.has_key(allele):
                # if it does, increment the count
                self.alleleTable[allele] += count
            else:
                # otherwise assign the count
                self.alleleTable[allele] = count

            # increment total alleles found
            totalAlleles += count

        if self.debug:
            print('alleleTable', self.alleleTable)
            print('sampleMap keys:', self.sampleMap.keys())
            print('sampleMap values:', self.sampleMap.values())
            
        self.locusName = self.sampleMap.keys()[0]

        # turn this into a pseudo-genotype data matrix

        # calculate the total number of individuals to create
        if operator.mod(totalAlleles, 2):
            # if odd create an extra individual with one untyped
            # allele to pad out the alleles
            self.totalIndivCount = totalAlleles / 2 + 1
        else:
            self.totalIndivCount = totalAlleles / 2

        self.locusList = [self.locusName]

        # create an empty-list of lists to store all the row data
        self.matrix = StringMatrix(self.totalIndivCount,
                                   self.locusList,
                                   self.separator)

        # loop through alleles creating pseudo-genotypes
        rowCount = 0
        alleleCount = 0
        for alleleName in self.alleleTable.keys():
            for allele in range(0, self.alleleTable[alleleName]):
                # odd position (end of individual)
                if operator.mod(alleleCount, 2):
                    genotype = (lastAlleleName, alleleName)
                    self.matrix[rowCount, self.locusName] = genotype
                    rowCount += 1
                # even position (start of individual, remember first allele)  
                else:
                    lastAlleleName = alleleName
                alleleCount += 1
        if rowCount == (self.totalIndivCount - 1):
            self.matrix[rowCount, self.locusName] = (lastAlleleName, '****')

        if self.debug:
            print("generated pseudo-genotype matrix:")
            print(self.matrix)

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
            listOfValidLoci = name.split(":")

            # check to see if the locus is one of the valid ones
            if (field in listOfValidLoci):
                isValidKey = 1
            else:
                isValidKey = 0

        return isValidKey, field

    def serializeSubclassMetadataTo(self, stream):
        # nothing special is required here, so pass
        pass
    
    def getAlleleTable(self):
        return self.alleleTable

    def getLocusName(self):
        # the first key is the name of the locus
        return self.locusName

    def getMatrix(self):
        """Returns the genotype data.

        Returns the genotype data in a 'StringMatrix' NumPy array.
        """
        return self.matrix

# this test harness is called if this module is executed standalone
if __name__ == "__main__":

    print("dummy test harness, currently a no-op")
    #parsefile = ParseGenotypeFile(sys.argv[1], debug=1)


