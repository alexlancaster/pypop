#! /usr/bin/env python

"""Module for calculating Hardy-Weinberg statistics.

"""

class HardyWeinberg:
  """Calculate Hardy-Weinberg statistics.

  Given the observed genotypes for a locus, calculate the expected
  genotype counts based on Hardy Weinberg proportions for individual
  genotype values, and test for fit.

  """

  def __init__(self, locusData, alleleCount, debug=0):
    """Constructor.

    - locusData to be provided by driver script via a
      call to ParseFile.getLocusData(locus).

    """

    self.locusData = locusData
    self.alleleCount = alleleCount
    self.debug = debug

    if self.debug:
      for genotype in self.locusData:
        print genotype

  def getSampleSize(self):
    """Returns N, the number of records

    """
    return(len(self.locusData))

#  """Assign the number of alleles, two per person."""
#  self.k = 2 * HardyWeinberg.getSampleSize()

