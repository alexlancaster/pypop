#! /usr/bin/env python
import sys, string
# this is file generates a parsed output of the input file

def ihwg_db_fields_read(filename):
    f = open(filename, 'r')
    data = f.readlines()
    li = []
    for line in data:
        print string.rstrip(line)
        li.append(string.rstrip(line))
    return tuple(li)

def ihwg_sample_file_read(filename):
    f = open(filename, 'r')
    data = f.readlines()
    return data

ihwg_pop_fields = ihwg_db_fields_read('ihwg-pop-fields.dat')
ihwg_sample_fields = ihwg_db_fields_read('ihwg-sample-fields.dat')

print ihwg_pop_fields
print ihwg_sample_fields

contents = ihwg_sample_file_read(sys.argv[1])

print "first line: ", string.rstrip(contents[0])
words = (string.rstrip(contents[0])).split('\t')
for word in words:
    print word
    
print

print "second line: ", string.rstrip(contents[1])
print "third line: ", string.rstrip(contents[2])
