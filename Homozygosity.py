#!/usr/bin/env python

"""Module for calculating homozygosity statistics.

"""

import string, sys, os

class Homozygosity:
  """Calculate homozygosity statistics.

  """

  def __init__(self, alleleCountData, rootPath=".", debug=0):
    """Constructor."""

    self.alleleData, self.sampleCount = alleleCountData
    self.numAlleles = len(self.alleleData)
    self.rootPath = rootPath
    self.debug = debug

  def _genPathName(self, sampleCount, numAlleles):

    decade, rem = divmod(sampleCount, 10)
    if rem >= 5:
      decade = decade + 1

    twoEn = decade*10

    path = "2n%s%s%s_%s.out" % (twoEn, os.sep, numAlleles, twoEn)
    return path

  def _checkCountRange(self, sampleCount):
    if (sampleCount <= 15) or (sampleCount >= 550):
      return 0
    else:
      return 1

  def _checkAlleleRange(self, numAlleles):
    if (numAlleles <= 1) or (numAlleles >= 41):
      return 0
    else:
      return 1


  def _parseFile(self):

    if self._checkCountRange(self.sampleCount):
      if self._checkAlleleRange(self.numAlleles):

        # generate relative path name
        path = self._genPathName(self.sampleCount, self.numAlleles)

        # open file with full path name created in-line
        lines = open(self.rootPath + os.sep + path, 'r').readlines()

        self.count = int(lines[0].split(':')[1])
        self.mean = float(lines[1].split(':')[1])
        self.var = float(lines[2].split(':')[1])
        self.sem = float(lines[3].split(':')[1])

        self.quantile = []
        for i in range(4, len(lines)):
          obsvHomo, calcP, pValue = [float(val) for val in lines[i].split()]
          self.quantile.append((obsvHomo, calcP, pValue))

        if self.debug:
          print self.count, self.mean, self.var, self.sem
          print self.sampleCount, self.numAlleles
          
        return 1
        
      else:
        print self.numAlleles, " is out of range of valid k!"
    else:
      print self.sampleCount, " is out of range of valid 2n!"

    return 0


  def getObservedHomozygosity(self):
    sum = 0.0

    # cache floating point value
    sampleCount = float(self.sampleCount)

    for allele in self.alleleData.keys():
      freq = float(self.alleleData[allele])/sampleCount
      if self.debug:
        print "allelecount = ", self.alleleData[allele], " freq = ", freq
      sum += freq*freq

    self.observedHomozygosity = 1.0 - sum
    return self.observedHomozygosity

  def getPValue(self):
    for val in self.quantile:
      obsvHomo, calcP, pVal = val
      if self.observedHomozygosity > obsvHomo:
        return pVal
  
  def getCount(self):
    return self.count

  def getMean(self):
    return self.mean

  def getVar(self):
    return self.var

  def getSem(self):
    return self.sem
