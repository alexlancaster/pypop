#! /usr/bin/env python
import sys, string

class ParseTSV:
    """Class to parse a standard IHWG datafile."""
    def __init__(self,
                 pop_fields_filename='ihwg-pop-fields.dat',
                 sample_fields_filename='ihwg-sample-fields.dat',
                 debug=0):
        """Constructor for ParseTSV object.  Defaults to filenames:

        ihwg-pop-fields.dat: for valid overall population data fields
        ihwg-sample-fields: for valid sample data fields.

        Also defaults to no debugging.  Set debug=1 in call to constructor
        if debuggin is desired"""
        self.pop_fields_filename=pop_fields_filename
        self.sample_fields_filename=sample_fields_filename
        self.debug = debug

        if self.debug:
            print self.pop_fields_filename

        self.pop_fields = ParseTSV._db_fields_read(self,self.pop_fields_filename)
        self.sample_fields = ParseTSV._db_fields_read(self,self.sample_fields_filename)

        if self.debug:
            # debugging only
            print self.pop_fields
            print self.sample_fields
        
    def _db_fields_read(self, filename):
        """Takes a filename for a database and expects a file with
        database field names separated by newlines

        Returns a tuple of field names.  Use internally only"""
        f = open(filename, 'r')
        data = f.readlines()
        li = []
        for line in data:
            if self.debug:
                print string.rstrip(line)
            li.append(string.rstrip(line))
        return tuple(li)

    def _map_fields(self, line, field_list):
        """Takes a line and a list of valid fields and creates a dictionary
        of positions keyed by valid field names.  Complains if a field
        name is not valid.  Also complains if the correct number of fields
        are not found for the metadata headers.
        
        Returns a 2-tuple:
        
        - a dictionary keyed by field name
        - the total number of  metadata fields.

        Intended to be used internally by class only."""

        # split line
        fields = line.split('\t')

        # check to see if the correct number of fields found
        if len(fields) != len(field_list):
            print "error: found", len(fields), "fields expected", \
                  len(field_list), "fields"
        
        i = 0
        assoc = {}
        for field in fields:

            # strip the field of leading and trailing blanks because
            # column name may inadvertantly contain these due to
            # spreadsheet -> tab-delimited file format idiosyncrasies
        
            field = string.strip(field)

            if (field in field_list) or ("*" + field in field_list):

                # generate the key that matches the one in the
                # data file format
                if "*" + field in field_list:
                    key = "*" + field
                else:
                    key = field
                    
                if assoc.has_key(key):
                    # if key already used (col names are not unique)
                    # append a (2)
                    aug_field = key + "(2)"
                    if aug_field in field_list:  
                        # see if augmented field exists
                        # create a tuple at the same key value
                        assoc[key] = assoc[key], i
                    else:
                        print "error: can't find augmented fieldname", \
                              aug_field
                else:
                    assoc[key] = i
            else:
                print "error: field name `%s' not valid" % field

            i = i + 1

        return assoc, i

    def sample_file_read(self, filename):
        """Takes a filename and reads the file data into an instance variable.
        """
        f = open(filename, 'r')
        self.file_data = f.readlines()

    def map_pop_headers(self):
        """Create the associations between field names and input columns by
        parsing the header information from the top of the file, for the
        population-level data.

        Also validates the file information for the correct number of fields
        are present on each line"""

        # get population header metadata
        pop_header_line = string.rstrip(self.file_data[0])

        # parse it
        self.pop_map, field_count = self._map_fields(pop_header_line, self.pop_fields)

        # debugging only
        if self.debug:
            print "population header line: ", pop_header_line
            print self.pop_map

        # get population data
        pop_data_line = string.rstrip(self.file_data[1])
        # debugging only
        if self.debug:
            print "population data line: ", pop_data_line

        # make sure pop data line matches number expected from metadata
        pop_data_fields = string.split(pop_data_line, '\t')
        if len(pop_data_fields) != field_count:
            print "error: found", len(pop_data_fields),\
                  "fields expected", field_count, "fields"

        # create a dictionary using the metadata field names as key
        # for the population data
        self.pop_data = {}
        for pop_field in self.pop_map.keys():
            self.pop_data[pop_field] = pop_data_fields[self.pop_map[pop_field]]

    def map_sample_headers(self):
        """Create the associations between field names and input columns by
        parsing the header information from the top of the file, for the
        sample data.

        Also validates the file information for the correct number of fields
        are present on each line"""

        # get sample header metadata
        sample_header_line = string.rstrip(self.file_data[2])

        # parse it
        self.sample_map, field_count = self._map_fields(sample_header_line,
                                                        self.sample_fields)
        # debugging only
        if self.debug:
            print "sample header line: ", sample_header_line
            print self.sample_map

        # check file data to see that correct number of fields are
        # present for each sample

        for line_count in range(3, len(self.file_data)):

            # retrieve and strip newline
            line = string.rstrip(self.file_data[line_count])

            # restore the data with the newline stripped
            self.file_data[line_count] = line
            
            fields = string.split(line)
            if field_count != len(fields):
                print "error: incorrect number of fields:", len(fields), \
                      "found, should have:", field_count, \
                      "\noffending line is:\n", line

    def get_pop_data(self):
        """Returns a dictionary of population data keyed by
        types specified in population metadata file"""
        return self.pop_data

    def get_sample_map(self):
        """Returns dictionary containing either a 2-tuple of column
        position or a single column position keyed by field originally
        specified in sample metadata file"""

        return self.sample_map
    
    def get_allele_map(self):
        """Returns dictionary containing 2-tuple of column position keyed by
        allele names originally specified in sample metadata file

        Note that this is simply a _subset_ of that returned by
        get_sample_map()"""

        self.allele_map = {}
        for key in self.sample_map.keys():
            # do we have the allele designator?
            if key[0] == '*':
                self.allele_map[key] = self.sample_map[key]

        return self.allele_map

    def get_file_data(self):
        """Return the raw lines, *without* the header metadata information"""
        return self.file_data[3:]
    
    def gen_sample_output(self, field_list):

        #for field in field_list:
        #print string.strip(field) + '\t',
        for line_count in range(3, len(self.file_data)):
            line = string.strip(self.file_data[line_count])
            element = string.split(line, '\t')
            for field in field_list:
                if self.sample_map.has_key(field):
                    print element[self.sample_map[field]],
                else:
                    print "can't find this field"
                    print "\n"


# this test harness is called if this module is executed standalone
if __name__ == "__main__":

    # create object
    parsefile = ParseTSV()

    # read in IHWG data file from first argument
    parsefile.sample_file_read(sys.argv[1])

    # print the parsed header info
    parsefile.map_headers()

