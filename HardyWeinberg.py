#! /usr/bin/env python

"""Module for calculating Hardy-Weinberg statistics.

"""

class HardyWeinberg:
  """Calculate Hardy-Weinberg statistics.

  Given the observed genotypes for a locus, calculate the expected
  genotype counts based on Hardy Weinberg proportions for individual
  genotype values, and test for fit."""

  def __init__(self, locusData, debug=0):
    """Constructor.

    - locusData to be provided by driver script via a
      call to ParseFile.getLocusData(locus)."""

    self.locusData = locusData
    self.debug = debug

    if self.debug:
      print self.locusData
      for item in self.locusData:
        print item

  def getSampleSize(self):
    return(len(self.locusData))
