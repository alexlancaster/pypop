#!/usr/local/bin/python

# Yingssu Tsai
# May 2003

# converts .html file from anthony nolan website, consisting of deleted allele
# names and the replacements

import sys
import re
import string

class deletedAlleles:

  def __init__(self, allelefile):

    self.inFile = allelefile

    self.all = []
    self.alleles = []
    self.replace = {}
    
    f = open(self.inFile)

    
    for line in f.xreadlines():

      match = re.search(r'[A-Zw0-9]+?\*[0-9A-Z]+', line)

      if match:
        replaced = 1
        a = match.group(0)
        self.all.append(a)

      else:
        match = re.search(r'<TD VALIGN=TOP>', line)
        if match:
          self.all.append(' ') 


  def putDictionary(self):
    """puts the information in the dictionary self.replace
    """
    c = 0
    length = len(self.all)
    while c < length:
      allele = self.all[c]
      replaced = self.all[c+1]
      self.replace[allele] = replaced
      c += 2

  
  def removeNone(self):
    """removes the alleles where the replacement allele is ' '
    which means there is no replacement
    """
    for each in self.replace.keys():
      if self.replace[each] == ' ':
        del self.replace[each]

    print self.replace


# testing

anExample = deletedAlleles(sys.argv[1])
anExample.putDictionary()
anExample.removeNone()
