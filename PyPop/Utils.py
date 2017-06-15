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

"""Module for common utility classes and functions.

   Contains convenience classes for output of text and XML
   files.
"""

import os, sys, string, types, re, shutil, copy, operator
import Numeric
from Numeric import zeros, take, asarray, PyObject
from UserArray import UserArray

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

    def flush(self):
        self.f.flush()

class XMLOutputStream(TextOutputStream):
    """Output stream for writing XML files.
    """

    def _gentag(self, tagname, **kw):
        """Internal method for generating tag text.

        Strip out non-valid tag character: '?'
        *Only use internally*.
        """
        attr=''
        tagname = tagname.replace('?', '')
        # loop through keywords turning each into an attr,key pair
        for i in kw.keys():
            attr = attr + i + "=" + "\"" + kw[i] + "\"" + " "
        if attr == '':
            return '%s' % tagname
        else:
            return '%s %s' % (tagname, string.strip(attr))
        
    def opentag(self, tagname, **kw):
        """Generate an open XML tag.

        Generate an open XML tag.  Attributes are passed in the form
        of optional named arguments, e.g. opentag('tagname',
        role=something, id=else) will produce the result '<tagname
        role="something" id="else"> Note that the attribute and values
        are optional and if omitted produce '<tagname>'.  """
        
        self.f.write("<%s>" % self._gentag(tagname, **kw))
        
    def emptytag(self, tagname, **kw):
        """Generate an empty XML tag.

        As per 'opentag()' but without content, i.e.:

        '<tagname attr="val"/>'.
        """
        self.f.write("<%s/>" % self._gentag(tagname, **kw))
            
    def closetag(self, tagname):
        """Generate a closing XML tag.

        Generate a tag in the form: '</tagname>'. 
        """
        self.f.write('</%s>' % self._gentag(tagname))

    def tagContents(self, tagname, content, **kw):
        """Generate open and closing XML tags around contents.

        Generates tags in the form: '<tagname>content</tagname>'.
        'content' must be a string.  Convert '&' and '<' and '>' into
        valid XML equivalents.

        """
        self.opentag(tagname, **kw)
        content = content.replace("&", "&amp;")
        content = content.replace("<", "&lt;")
        content = content.replace(">", "&gt;")
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

class OrderedDict:
  """
  Allows dict to have _ORDERED_ pairs
  """

  __version__ = '1.1'

  def __init__(self,hash=[]):
    """
    Creates an ordered dict
    """
    self.__hash = {}
    self.KEYS = []

    while hash:
      k, v, hash = hash[0], hash[1], hash[2:]
      self.__hash[k] = v
      self.KEYS.append(k)


  def __addval__(self,key,value):
    """
    Internal function to add/change key-value pair (at end)
    """
    try:
      i = self.KEYS.index(key)
    except:
      self.__hash[key] = value
      self.KEYS.append(key)
    else:
      self.__hash[key] = value


  def __setitem__(self,i,hash):
    """
    Adds key-value pairs (existing keys not moved)
    """
    if type(i) == type(Index()):
      del self.__hash[self.KEYS[i.i]]
      if len(hash) != 1:
        self.KEYS[i.i], hash = hash[0], hash[1:]
      self.__hash[self.KEYS[i.i]] = hash[0]
    else:
      self.__addval__(i,hash)


  def __getitem__(self,key):
    """
    Returns value of given key
    """
    if type(key) == type(Index()):
      key = self.KEYS[key.i]
      return [key,self.__hash[key]]
    return self.__hash[key]


  def __len__(self):
    """
    Returns the number of pairs in the dict
    """
    return len(self.KEYS)


  def index(self,key):
    """
    Returns position of key in dict
    """
    return self.KEYS.index(key)


  def keys(self):
    """
    Returns list of keys in dict
    """
    return self.KEYS


  def values(self):
    """
    Returns list of values in dict
    """
    ret = []
    for key in self.KEYS:
      ret.append(self.__hash[key])
    return ret


  def items(self):
    """
    Returns list of tuples of keys and values
    """
    ret = []
    for key in self.KEYS:
      ret.append((key,self.__hash[key]))
    return ret


  def insert(self,i,key,value):
    """
    Inserts a key-value pair at a given index
    """
    InsertError = "Duplicate key entry"
    if self.__hash.has_key(key):
      raise InsertError
    else:
      self.KEYS.insert(i,key)
      self.__hash[key] = value


  def remove(self,i):
    """
    Removes a key-value pair from the dict
    """
    del self.__hash[i]
    self.KEYS.remove(i)


  def __delitem__(self,i):
    """
    Removes a key-value pair from the dict
    """
    if type(i) != type(Index()):
      i = Index(self.KEYS.index(i))
    del self.__hash[self.KEYS[i.i]]
    del self.KEYS[i.i]
      

  def reverse(self):
    """
    Reverses the order of the key-value pairs
    """
    self.KEYS.reverse()


  def sort(self,cmp=0):
    """
    Sorts the dict (allows for sort algorithm)
    """
    if cmp:
      self.KEYS.sort(cmp)
    else:
      self.KEYS.sort()


  def clear(self):
    """
    Clears all the entries in the dict
    """
    self.__hash = {}
    self.KEYS = []


  def copy(self):
    """
    Makes copy of dict, also of OrderdDict class
    """
    hash = OrderedDict()
    hash.KEYS = self.KEYS[:]
    hash.__hash = self.__hash.copy()
    return hash


  def get(self,key):
    """
    Returns the value of a key
    """
    return self.__hash[key]


  def has_key(self,key):
    """
    Looks for existance of key in dict
    """
    return self.__hash.has_key(key)


  def update(self,dict):
    """
    Updates entries in a dict based on another
    """
    self.__hash.update(dict)


  def count(self,key):
    """
    Finds occurances of a key in a dict (0/1)
    """
    return self.__hash.has_key(key)


  def __getslice__(self,i,j):
    """
    Returns an OrderedDict of key-value pairs from a dict
    """
    ret = []
    for x in range(i,j):
      ret.append(self.KEYS[x])
      ret.append(self.__hash[self.KEYS[x]])
    return OrderedDict(ret)


  def __setslice__(self,i,j,hash):
    """
    Sets a slice of elements from the dict
    """
    hash = list(hash)
    for x in range(i,j):
      k, v, hash = hash[0], hash[1], hash[2:]
      self.__setitem__(Index(x),[k,v])


class Index:
  """
  Returns an Index object for OrderedDict
  """

  def __init__(self,i=0):
    """
    Creates an Index object for use with OrderedDict
    """
    self.i = i

class StringMatrix(UserArray):
  """
  StringMatrix is a subclass of the Numeric Python (NumPy)
  UserArray class, and uses NumPy to store the data in an efficient
  array format, rather than internal Python lists.
  """

  def __init__(self,
               rowCount=None,
               colList=None,
               extraList=None,
               colSep='\t',
               headerLines=None):
      """Constructor for StringMatrix.

      colList is a mutable type so we freeze the list of locus keys in
      the original order in file by making a *clone* of the list of
      keys.

      the order of loci in the array will correspond to the original
      file order, and we don't want this tampered with by the `callee'
      function (i.e. effectively override the Python 'pass by
      reference' default and 'pass by value')."""
      
      self.colList = colList[:]
      
      self.colCount = len(self.colList)
      self.rowCount = rowCount

      if extraList:
          self.extraList = extraList[:]
          self.extraCount = len(self.extraList)
      else:
          self.extraList = None
          self.extraCount = 0

      self.colSep = colSep
      self.headerLines = headerLines

      # initialising the internal NumPy array
      self.array = zeros((self.rowCount, self.colCount*2+self.extraCount), PyObject)
      self.shape = self.array.shape
      self._typecode = self.array.typecode()
      self.name = string.split(str(self.__class__))[0]

  def __repr__(self):
      """Override default representation.

      This is used when the object is 'print'ed, i.e.
      a = StringMatrix(10, [1,2])
     print a"""
      if len(self.array.shape) > 0:
          return (self.__class__.__name__)[6:12]+repr(self.array)[len("array"):]
      else:
          return (self.__class__.__name__)[6:12]+"("+repr(self.array)+")"

  def dump(self, locus=None, stream=sys.stdout):
      # write out file in original format
      # first write out header, if there is one
      if self.headerLines:
          for line in self.headerLines:
              stream.write(line),

      # next write out the non-allele column headers, if there are some
      if self.extraList:
          for elem in self.extraList:
              stream.write(elem + self.colSep)

      if locus:
          locusList = locus
      else:
          locusList = string.join(self.colList,':')

      # next write out the allele column headers
      for elem in string.split(locusList, ':'):
          stream.write(elem + '_1' + self.colSep)
          stream.write(elem + '_2' + self.colSep,)
      stream.write(os.linesep)

      # finally the matrix itself
      for row in self.__getitem__(string.join(self.extraList,':')+ ':' + \
                                  locusList):
          for elem in row:
              stream.write(elem + self.colSep)
          stream.write(os.linesep)

  def copy(self):
      """Make a (deep) copy of the StringMatrix

      Currently this goes via the constructor, not sure if
      there is a better way of doing this"""
      thecopy = StringMatrix(copy.deepcopy(self.rowCount), \
                             copy.deepcopy(self.colList),
                             copy.deepcopy(self.extraList),
                             self.colSep,
                             self.headerLines)
      thecopy.array = self.array.copy()
      return thecopy

  def __deepcopy__(self, memo):
      """Create a deepcopy for copy.deepcopy

      This simply calls self.copy() to allow
      copy.deepcopy(matrixInstance) to Do The Right Thing"""
      return self.copy()
      
  def __getslice__(self, i, j):
      raise Exception("slices not currently supported")
      #return self._rc(self.array[i:j])

  def __getitem__(self, key):
      """Override built in.

      This is called when instance is called to retrieve a position
      e.g.:

      li = matrix['A']

      returns a list (a single column vector if only one position
      specified), or list of lists: (a set of column vectors if
      several positions specified) of tuples for that position"""
      if type(key) == types.TupleType:
          row,colName= key
          if colName in self.colList:
              col = self.extraCount+self.colList.index(colName)
          else:
              raise KeyError("can't find %s column" % colName)
          return self.array[(row,col)]
      elif type(key) == types.StringType:
          colNames = string.split(key, ":")
          li = []
          for col in colNames:
              # check first in list of alleles
              if col in self.colList:
                  # get relative location in list
                  relativeLoc = self.colList.index(col)
                  # calculate real locations in array
                  col1 = relativeLoc * 2 + self.extraCount
                  col2 = col1 + 1
                  li.append(col1)
                  li.append(col2)
              # now check in non-allele metadata
              elif col in self.extraList:
                  li.append(self.extraList.index(col))
              else:
                  raise KeyError("can't find %s column" % col)

          if len(colNames) == 1:
              # return simply the pair of columns at that location as
              # a list
              return take(self.array, tuple(li[0:2]), 1).tolist()
          else:
              # return the matrix consisting of column vectors
              # of the designated keys
              return take(self.array, tuple(li), 1).tolist()
      else:
          raise KeyError("keys must be a string or tuple")

  def __setitem__(self, index, value):
      """Override built in.

      This is called when instance is called to assign a value,
      e.g.:

      matrix[3, 'A'] = (entry1, entry2)"""
      if type(index) == types.TupleType:
          row, colName = index
      else:
          raise IndexError("index is not a tuple")
      if type(value) == types.TupleType:
          value1, value2 = value
      elif type(value) == types.StringType:
          value = value
      else:
          raise ValueError("value being assigned is not a tuple")

      if colName in self.colList:
          # find the location in order in the array
          col = self.colList.index(colName)
          # calculate the offsets to the actual array location
          col1 = col * 2
          col2 = col1 + 1
          # store each element in turn
          self.array[(row,col1+self.extraCount)] = asarray(value1,self._typecode)
          self.array[(row,col2+self.extraCount)] = asarray(value2,self._typecode)

      elif colName in self.extraList:
          col = self.extraList.index(colName)
          self.array[(row,col)] = asarray(value,self._typecode)
      else:
          raise KeyError("can't find %s column" % col)

  def filterOut(self, key, blankDesignator):
      """Returns a filtered matrix.

      When passed a designator, this method will return the rows of
      the matrix that *do not* contain that designator at any rows"""
      def f(x, designator=blankDesignator):
          for value in x:
              if value == designator:
                  return 0
          return 1

      return (filter(f, self.__getitem__(key)))[:]

  def getSuperType(self, key):
      """Returns a matrix grouped by columns.

      e.g if matrix is [[A01, A02, B01, B02], [A11, A12, B11, B12]]

      then getSuperType('A:B') will return the matrix with the column
      vector:
      
      [[A01:B01, A02:B02], [A11:B11, A12:B12]]
      """
      li = self.__getitem__(key)

      colName = string.replace(key, ":", "-")
      newMatrix = StringMatrix(rowCount=copy.deepcopy(self.rowCount), \
                               colList=copy.deepcopy([colName]),
                               extraList=copy.deepcopy(self.extraList),
                               colSep=self.colSep,
                               headerLines=self.headerLines)

      pos = 0
      for i in li:
          newMatrix[pos, colName] = (string.join(i[0::2], ":"),
                                     string.join(i[1::2],":"))
          pos += 1

      return newMatrix
      
      
class Group:
  # group a list or sequence by a given size
  # example usage:
  # for pair in Group('aabbccddee',2):
  #   do something with pair.
  
  def __init__(self, l, size):
    self.size=size
    self.l = l

  def __getitem__(self, group):
    idx = group * self.size
    if idx > len(self.l): 
      raise IndexError("Out of range")
    return self.l[idx:idx+self.size]

### global FUNCTIONS start here


def unique_elements(l):
    """Gets the unique elements in a list"""
    d = {}
    length = len(l)
    map(operator.setitem, length * [d], l, length * [None])
    return d.keys ()

def appendTo2dList(aList, appendStr=':'):

    return [["%s%s" % (cell, appendStr) \
             for cell in row] for row in aList]

def convertLineEndings(file, mode):
    # 1 - Unix to Mac, 2 - Unix to DOS
    if mode == 1:
        if os.path.isdir(file):
            sys.exit(file + "Directory!")
        data = open(file, "r").read()
        if '\0' in data:
            sys.exit(file + "Binary!")
        newdata = re.sub("\r?\n", "\r", data)
        if newdata != data:
            f = open(file, "w")
            f.write(newdata)
            f.close()
    elif mode == 2:
        if os.path.isdir(file):
            sys.exit(file + "Directory!")
        data = open(file, "r").read()
        if '\0' in data:
            sys.exit(file + "Binary!")
        newdata = re.sub("\r(?!\n)|(?<!\r)\n", "\r\n", data)
        if newdata != data:
            f = open(file, "w")
            f.write(newdata)
            f.close()

def fixForPlatform(filename, txt_ext=0):
    # make file read-writeable by everybody
    os.chmod(filename, 0666)

    # create as a DOS format file LF -> CRLF
    if sys.platform == 'cygwin':
        convertLineEndings(filename, 2)
        # give it a .txt extension so that lame Windows realizes it's text
        if txt_ext:
            os.rename(filename, filename + '.txt')
            print filename + '.txt'
        else:
            print filename
    else:
        print filename

def copyfileCustomPlatform(src, dest, txt_ext=0):
    shutil.copyfile(src, dest)
    fixForPlatform(dest, txt_ext=txt_ext)
    print "copying %s to" % src,
    
def copyCustomPlatform(file, dist_dir, txt_ext=0):
    new_filename=os.path.join(dist_dir, os.path.basename(file))
    print "copying %s to" % file, 
    shutil.copy(file, dist_dir)
    fixForPlatform(new_filename, txt_ext=txt_ext)

def checkXSLFile(xslFilename,
                 path='',
                 subdir='',
                 abort=None,
                 debug=None,
                 msg=''):
    if debug:
        print "path=%s, subdir=%s, xslFilename=%s xsl path" % (path, subdir, xslFilename)

    # generate a full path to check
    checkPath = os.path.realpath(os.path.join(path, subdir, xslFilename))
    if os.path.isfile(checkPath):
        return checkPath
    else:
        if abort:
            sys.exit("Can't find XSL: %s %s" % (checkPath, msg))
        else:
            return None

def getUserFilenameInput(prompt, filename):
    """Read user input for a filename, check its existence, continue
    requesting input until a valid filename is entered."""

    nofile = 1
    while nofile:
      tempFilename = raw_input("Please enter %s filename [%s]: " % (prompt, filename))

      # if we accept default, still check that file still exists
      if tempFilename == '':
          if os.path.isfile(filename):
              nofile = 0
          else:
              print "File '%s' does not exist" % filename
      else:
          # if we don't accept default, check that file exists and use
          # the user input as the filename
          if os.path.isfile(tempFilename):
              nofile = 0
              filename = tempFilename
          else:
              # otherwise return an error
              print "File '%s' does not exist" % tempFilename
      
    return filename


def splitIntoNGroups(alist, n=1):
    """Divides a list up into n parcels (plus whatever is left over)

    This class currently works with Python 2.2, but will eventually
    use iterators, so ultimately will need least Python 2.3!  """
    #from itertools import islice    
    #it = iter(alist)
    
    x = len(alist)/n    # note: don't just drop the last len(alist) % n items
    y = len(alist)%n
    
    # initialize an empty list
    retval = []

    # only create list if divisor is non-zero
    if x:
        retval = [ alist[i*x:((i+1)*x)] for i in range(n) ]
        #retval = [ list(islice(it, x)) for i in range(n) ]

    # if modulus is non-zero make sure to add the extra part of list
    if y:
        extra = alist[-y:]
        #extra = list(islice(it, y))
        retval.append(extra)

    return retval

# if __name__ == "__main__":
#     # test classes
#     import copy

#     # test StringMatrix class
#     a = StringMatrix(3, ['A', 'B', 'C'])

#     print "original matrix is all zeroes: "
#     print a

#     a[0, 'B'] = ('B0', 'B0')
#     a[1, 'B'] = ('B1', 'B1')
#     print "modified matrix: "
#     print a

#     #b = copy.deepcopy(a)
#     b = a.copy()
    
#     b[0,'A'] = ('A0', 'A0')
#     b[1,'A'] = ('A1', 'A2')

#     print "b should be changed:"
#     print b
    
#     print "a should be unchanged and have nothing the A column:"
#     print a

#     print "test subMatrix, get all data for b at locus 'A':"
#     print b['A']

#     print "test subMatrix, get all data for b at locus 'A:B':"
#     print b['A:B']

#     print "now filterOut B1 elements from b to create c:"
#     c = b.filterOut('A:B:C', 'B1')
#     print c
    
#     print "test appending to a subMatrix c: "
#     print appendTo2dList(c, appendStr=':')

#     print "b should be unchanged by this:"
#     print b
