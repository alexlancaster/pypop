#! /usr/bin/env python
import sys, string

class ParseTSV:
    """Class to parse a standard IHWG datafile."""
    def __init__(self,
                 pop_fields_filename='ihwg-pop-fields.dat',
                 sample_fields_filename='ihwg-sample-fields.dat'):
        """Constructor for ParseTSV object.  Defaults to filenames:

        ihwg-pop-fields.dat: for valid overall population data fields
        ihwg-sample-fields: for valid sample data fields"""
        self.pop_fields_filename=pop_fields_filename
        self.sample_fields_filename=sample_fields_filename

        print self.pop_fields_filename

        self.pop_fields = ParseTSV.db_fields_read(self,self.pop_fields_filename)
        self.sample_fields = ParseTSV.db_fields_read(self,self.sample_fields_filename)
        self.debug = 1
        if self.debug:
            # debugging only
            print self.pop_fields
            print self.sample_fields
        
    def db_fields_read(self, filename):
        """Takes a filename for a database and expects a file with
        database field names separated by newlines

        Returns a tuple of field names."""
        f = open(filename, 'r')
        data = f.readlines()
        li = []
        for line in data:
            print string.rstrip(line)
            li.append(string.rstrip(line))
        return tuple(li)

    def sample_file_read(self, filename):
        """Takes a filename and reads the file data into an instance variable
        """
        f = open(filename, 'r')
        self.file_data = f.readlines()

    def map_fields(self, line, field_list):
        """Takes a line and a list of valid fields and creates a dictionary
        of positions keyed by valid field names.  Complains if a field
        name is not valid.
        
        Returns a dictionary keyed by field name."""
        fields = line.split('\t')
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
                        assoc[aug_field] = i
                    else:
                        print "error: can't find augmented fieldname", \
                              aug_field
                else:
                    assoc[key] = i
            else:
                print "error: field name `%s' not valid" % field

            i = i + 1
            
        return assoc

    def map_headers(self):
        """Create the associations between field names and input columns by
        parsing the header information from the top of the file."""
        first_line = string.rstrip(self.file_data[0])
        self.pop_map = self.map_fields(first_line, self.pop_fields)
        # debugging only
        if self.debug:
            print "first line: ", first_line
            print self.pop_map 

        second_line = string.rstrip(self.file_data[1])

        # debugging only
        if self.debug:
            print "second line: ", second_line

        third_line = string.rstrip(self.file_data[2])

        self.sample_map = self.map_fields(third_line, self.sample_fields)
        # debugging only
        if self.debug:
            print "third line: ", third_line
            print self.sample_map

    def gen_sample_output(self, field_list):

        #for field in field_list:
        #    print string.strip(field) + '\t',
            
        for line_count in range(3, len(self.file_data)):
            line = string.strip(self.file_data[line_count])
            el = string.split(line, '\t')
            for field in field_list:
                if self.sample_map.has_key(field):
                    print el[self.sample_map[field]],
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

