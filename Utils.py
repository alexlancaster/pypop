#! /usr/bin/env python

"""Module for common utility classes and functions.

   Contains convenience classes for output of text and XML
   files.
"""

import os, string

class TextOutputStream:
    """Output stream for writing text files.
    """
    def __init__(self, file):
        self.f = file

    def write(self, str):
        self.f.write(str)

    def writeln(self, str=os.linesep):
        if str == os.linesep:
            self.f.write(os.linesep)
        else:
            self.f.write(str + os.linesep)
            
    def close(self):
        self.f.close()

class XMLOutputStream(TextOutputStream):
    """Output stream for writing XML files.
    """

    def opentag(self, tagname, attr='', val=''):
        if attr == '':
            self.f.write('<%s>' % (tagname))
        else:
            self.f.write('<%s %s="%s">' % (tagname, attr, val))
            
    def closetag(self, tagname):
        self.f.write('</' + tagname + '>')

    def tagContents(self, tagname, content):
        self.opentag(tagname)
        self.f.write(content)
        self.closetag(tagname)

def getStreamType(stream):
    """Return the type of stream.

       Returns either 'xml' or 'text'.
    """
    if isinstance(stream, XMLOutputStream) == 1:
        type = 'xml'
    else:
        type = 'text'
    return type
