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

    def _gentag(self, tagname, attr='', val=''):
        """Internal method for generating tag text.

        *Only use internally*.
        """
        if attr == '':
            return '%s' % tagname
        else:
            return '%s %s="%s"' % (tagname, attr, val)

    def opentag(self, tagname, attr='', val=''):
        """Generate an open XML tag.

        Generate a tag in the form '<tagname attr="val">'.  Note that
        the attribute and values are optional and if omitted produce
        '<tagname>'.  """
        
        self.f.write("<%s>" % self._gentag(tagname, attr, val))

    def emptytag(self, tagname, attr='', val=''):
        """Generate an empty XML tag.

        As per 'opentag()' but without content, i.e.:

        '<tagname attr="val"/>'.
        """
        self.f.write("<%s/>" % self._gentag(tagname, attr, val))
            
    def closetag(self, tagname):
        """Generate a closing XML tag.

        Generate a tag in the form: '</tagname>'. 
        """
        self.f.write('</' + tagname + '>')

    def tagContents(self, tagname, content):
        """Generate open and closing XML tags around contents.

        Generates tags in the form:  '<tagname>content</tagname>'.
        'content' must be a string.
        """
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
      ret.append(key,self.__hash[key])
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
