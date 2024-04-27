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

import os, sys, types, stat, re, shutil, copy, operator
import numpy as np
from numpy import zeros, take, asarray
GENOTYPE_SEPARATOR = "~"
GENOTYPE_TERMINATOR= "~"
from numpy.lib.user_array import container

class TextOutputStream:
    """Output stream for writing text files.
    """
    def __init__(self, file):
        self.f = file

    def write(self, str):
        self.f.write(str)

    def writeln(self, str='\n'):
        if str == '\n':
            self.f.write('\n')
        else:
            self.f.write(str + '\n')
            
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
            return '%s %s' % (tagname, attr.strip())
        
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
    if key in self.__hash:
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
    return key in self.__hash


  def update(self,dict):
    """
    Updates entries in a dict based on another
    """
    self.__hash.update(dict)


  def count(self,key):
    """
    Finds occurances of a key in a dict (0/1)
    """
    return key in self.__hash


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

class StringMatrix(container):
  """
  StringMatrix is a subclass of NumPy (Numeric Python)
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
      self.array = zeros((self.rowCount, self.colCount*2+self.extraCount), dtype='O')
      self.shape = self.array.shape
      self._typecode = self.array.dtype # Numeric array.typecode()
      self.name = str(self.__class__).split()[0]

  def __repr__(self):
      """Override default representation.

      This is used when the object is 'print'ed, i.e.
      a = StringMatrix(10, [1,2])
     print a"""
      if len(self.array.shape) > 0:
          return (self.__class__.__name__)+repr(self.array)[len("array"):]
      else:
          return (self.__class__.__name__)+"("+repr(self.array)+")"

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
          locusList = ':'.join(self.colList)

      # next write out the allele column headers
      for elem in locusList.split(':'):
          stream.write(elem + '_1' + self.colSep)
          stream.write(elem + '_2' + self.colSep,)
      stream.write('\n')

      # finally the matrix itself
      for row in self.__getitem__(':'.join(self.extraList)+ ':' + \
                                  locusList):
          for elem in row:
              stream.write(elem + self.colSep)
          stream.write('\n')

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
      if type(key) == tuple:
          row,colName= key
          if colName in self.colList:
              col = self.extraCount+self.colList.index(colName)
          else:
              raise KeyError("can't find %s column" % colName)
          return self.array[(row,col)]
      elif type(key) == str:
          colNames = key.split(":")
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

  def getNewStringMatrix(self, key):
      """Create an entirely new StringMatrix using only the columns supplied
      in the keys.

      The format of the keys is identical to __getitem__ except that
      it in this case returns a full StringMatrix instance which
      includes all metadata
      """
      
      if type(key) == str:
          colNames = key.split(":")

          # need both column position and names to reconstruct matrix
          newColPos = [];   newColList = []
          newExtraPos = []; newExtraList = []
          for col in colNames:
              # check first in list of alleles
              if col in self.colList:
                  # get relative location in list
                  relativeLoc = self.colList.index(col)
                  # calculate real locations in array
                  col1 = relativeLoc * 2 + self.extraCount
                  col2 = col1 + 1
                  newColPos.append(col1)
                  newColPos.append(col2)
                  newColList.append(col)
              # now check in non-allele metadata
              elif col in self.extraList:
                  newExtraPos.append(self.extraList.index(col))
                  newExtraList.append(col)
              else:
                  raise KeyError("can't find %s column" % col)

      # build a new matrix using the parameters from the current
      newMatrix = StringMatrix(rowCount=self.rowCount,
                               colList=newColList,
                               extraList=newExtraList,
                               colSep=self.colSep,
                               headerLines=self.headerLines)

      # copy just the columns we requested, both loci cols + extras
      newExtraPos.extend(newColPos)
      newMatrix.array = self.array[:,newExtraPos]
      return newMatrix

  def __setitem__(self, index, value):
      """Override built in.

      This is called when instance is called to assign a value,
      e.g.:

      matrix[3, 'A'] = (entry1, entry2)"""
      if type(index) == tuple:
          row, colName = index
      else:
          raise IndexError("index is not a tuple")
      if type(value) == tuple:
          value1, value2 = value
      elif type(value) == str:
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
          self.array[(row,col1+self.extraCount)] = asarray(value1, dtype=self.dtype)
          self.array[(row,col2+self.extraCount)] = asarray(value2, dtype=self.dtype)

      elif colName in self.extraList:
          col = self.extraList.index(colName)
          self.array[(row,col)] = asarray(value, self.dtype)
      else:
          raise KeyError("can't find %s column" % col)

  def getUniqueAlleles(self, key):
      """
      Return a list of unique integers for given key sorted by allele name using natural sort
      """
      uniqueAlleles = []
      for genotype in self.__getitem__(key):
          for allele in genotype:
              str_allele = str(allele)
              if str_allele not in uniqueAlleles:
                  uniqueAlleles.append(str_allele)
      uniqueAlleles.sort(key=natural_sort_key) # natural sort
      return uniqueAlleles

  def convertToInts(self):
      """
      Convert matrix to integers: needed for haplo-stats
      Note that integers start at 1 for compatibility with haplo-stats module
      FIXME: check whether we need to release memory
      """
      
      # create a new copy
      newMatrix = self.copy()
      for colName in self.colList:
          uniqueAlleles = self.getUniqueAlleles(colName)
          row = 0
          for genotype in self.__getitem__(colName):
              factor_genotype = []
              for allele in genotype:
                  pos = uniqueAlleles.index(str(allele)) + 1
                  factor_genotype.append(pos)
              newMatrix[row, colName] = tuple(factor_genotype)
              row += 1

      return newMatrix

  def countPairs(self):
      """Given a matrix of genotypes (pairs of columns for each
      locus), compute number of possible pairs of haplotypes for each
      subject (the rows of the geno matrix)

      FIXME: this does *not* do any involved handling of missing data
      as per geno.count.pairs from haplo.stats

      FIXME: should these methods eventually be moved to Genotype class?
      """

      # count number of unique alleles at each loci
      n_alleles = {}
      for colName in self.colList:
          n_alleles[colName] = len(self.getUniqueAlleles(colName))

      # count pairs of haplotypes for subjects without any missing alleles
      # FIXME: maybe convert to it's own method as per getUniqueAlleles 
      h1 = self.array[:, 0::2]  # get "_1" allele (odd cols)
      h2 = self.array[:, 1::2]  # get "_2" allele (even cols)
      n_het = np.sum(np.not_equal(h1, h2), 1)  # equivalent of: apply(h1!=h2,1,sum)
      n_het = np.where(n_het == 0, 1, n_het)      # equivalent of: ifelse(n.het==0,1,n.het)
      n_pairs = 2 ** (n_het - 1)   # equivalent of: n.pairs = 2^(n.het-1)

      return n_pairs.tolist()

  def flattenCols(self):
      """Flatten columns into a single list
      FIXME: assumes entries are integers
      """
      flattened_matrix = []

      for col in self.colList:  # FIXME: currently assume we want whole matrix
          # FIXME: possibly refactor extracting column logic with __getitem__
          relativeLoc = self.colList.index(col)
          col1 = relativeLoc * 2 + self.extraCount
          col2 = col1 + 1
          first_col = [int(x) for x in self.array[:,col1]]
          flattened_matrix.extend(first_col)
          second_col = [int(x) for x in self.array[:,col2]]
          flattened_matrix.extend(second_col)

      return flattened_matrix

  def filterOut(self, key, blankDesignator):
      """Returns a filtered matrix.

      When passed a designator, this method will return the rows of
      the matrix that *do not* contain that designator at any rows"""
      def f(x, designator=blankDesignator):
          for value in x:
              if value == designator:
                  return 0
          return 1

      filtered_list = list(filter(f, self.__getitem__(key)))
      return filtered_list[:]

  def getSuperType(self, key):
      """Returns a matrix grouped by columns.

      e.g if matrix is [[A01, A02, B01, B02], [A11, A12, B11, B12]]

      then getSuperType('A:B') will return the matrix with the column
      vector:
      
      [[A01:B01, A02:B02], [A11:B11, A12:B12]]
      """
      li = self.__getitem__(key)

      colName = key.replace(":", "-")
      newMatrix = StringMatrix(rowCount=copy.deepcopy(self.rowCount), \
                               colList=copy.deepcopy([colName]),
                               extraList=copy.deepcopy(self.extraList),
                               colSep=self.colSep,
                               headerLines=self.headerLines)

      pos = 0
      for i in li:
          newMatrix[pos, colName] = (i[0::2].join(":"),
                                     i[1::2].join(":"))
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

def natural_sort_key(s, _nsre=re.compile(r'([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]

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
    os.chmod(filename, stat.S_IFCHR)

    # create as a DOS format file LF -> CRLF
    if sys.platform == 'cygwin':
        convertLineEndings(filename, 2)
        # give it a .txt extension so that lame Windows realizes it's text
        if txt_ext:
            os.rename(filename, filename + '.txt')
            print('%s.txt' %filename)
        else:
            print(filename)
    else:
        print(filename)

def copyfileCustomPlatform(src, dest, txt_ext=0):
    shutil.copyfile(src, dest)
    fixForPlatform(dest, txt_ext=txt_ext)
    print("copying %s to" % src),
    
def copyCustomPlatform(file, dist_dir, txt_ext=0):
    new_filename=os.path.join(dist_dir, os.path.basename(file))
    print("copying %s to" % file)
    shutil.copy(file, dist_dir)
    fixForPlatform(new_filename, txt_ext=txt_ext)

def checkXSLFile(xslFilename,
                 path='',
                 subdir='',
                 abort=False,
                 debug=None,
                 msg=''):
    if debug:
        print("path=%s, subdir=%s, xslFilename=%s xsl path" % (path, subdir, xslFilename))

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
      tempFilename = input("Please enter %s filename [%s]: " % (prompt, filename))

      # if we accept default, still check that file still exists
      if tempFilename == '':
          if os.path.isfile(filename):
              nofile = 0
          else:
              print("File '%s' does not exist" % filename)
      else:
          # if we don't accept default, check that file exists and use
          # the user input as the filename
          if os.path.isfile(tempFilename):
              nofile = 0
              filename = tempFilename
          else:
              # otherwise return an error
              print("File '%s' does not exist" % tempFilename)
      
    return filename


def splitIntoNGroups(alist, n=1):
    """Divides a list up into n parcels (plus whatever is left over)

    This class currently works with Python 2.2, but will eventually
    use iterators, so ultimately will need least Python 2.3!  """
    #from itertools import islice    
    #it = iter(alist)
    
    x = len(alist) // n    # note: don't just drop the last len(alist) % n items
    y = len(alist) % n
    
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

