#!/usr/bin/env python

"""Module for calculating Hardy-Weinberg statistics.

"""

import string

class HardyWeinberg:
  """Calculate Hardy-Weinberg statistics.

  Given the observed genotypes for a locus, calculate the expected
  genotype counts based on Hardy Weinberg proportions for individual
  genotype values, and test for fit.

  """

  def __init__(self, locusData, alleleCount, debug=0):
    """Constructor.

    - locusData and alleleCount to be provided by driver script
      via a call to ParseFile.getLocusData(locus).

    """

    self.locusData = locusData

#     we can't use the alleleCount data at the moment
#     because ParseFile.getAlleleCountAt() returns unclean data
#     self.alleleCount = alleleCount[0] #just the dictionary of allelename:count
#     self.alleleTotal = alleleCount[1]

    self.debug = debug

    self.n = len(self.locusData)
    self.k = 2 * self.n

    self._generateTables()

#     if self.debug:
#       self.counter = 0
#       for genotype in self.locusData:
#         self.counter += 1
#         print genotype
#       print "Population:", self.n
#       print "Alleles:", self.k
#       print 'Given:', self.alleleTotal
#       print'Counter:', self.counter
#       print self.alleleCount
#       running_count = 0
#       running_freq = 0.0
#       for allele in self.alleleCount.keys():
#         running_count += self.alleleCount[allele]
#         #freq = self.alleleCount[allele] / float(self.k)
#         freq = self.alleleCount[allele] / float(self.alleleTotal)
#         running_freq += freq
#         print allele, 'obs:', self.alleleCount[allele],\
#                       'count:', running_count,\
#                       'freq:', freq,\
#                       'cum:', running_freq

  def _generateTables(self):
    """Manipulate the given genotype data to generate
    the tables upon which the calculations will be based."""

    self.alleleCounts = {}
    self.alleleFrequencies = {}
    self.observedGenotypes = []
    self.observedAlleles = []               # need a uniqed list
    self.observedGenotypeCounts = {}
    self.possibleGenotypes = []
    self.expectedGenotypeCounts = {}
    
    self.alleleTotal = 0

    for genotype in self.locusData:
      """Run through each tuple in the given genotype data and
      create a dictionary of allele counts"""
      self.alleleTotal += 2
      if self.alleleCounts.has_key(genotype[0]):
        self.alleleCounts[genotype[0]] += 1
      else:
        self.alleleCounts[genotype[0]] = 1
      if self.alleleCounts.has_key(genotype[1]):
        self.alleleCounts[genotype[1]] += 1
      else:
        self.alleleCounts[genotype[1]] = 1

      if genotype[0] not in self.observedAlleles:
        self.observedAlleles.append(genotype[0])
      if genotype[1] not in self.observedAlleles:
        self.observedAlleles.append(genotype[1])

      self.observedGenotypes.append(genotype[0] + ":" + genotype[1])

    frequencyAccumulator = 0.
    for allele in self.alleleCounts.keys():
      """For each entry in the dictionary of allele counts
      generate a corresponding entry in a dictionary of frequencies"""
      freq = self.alleleCounts[allele] / float(self.k)
      frequencyAccumulator += freq
      self.alleleFrequencies[allele] = freq

    for genotype in self.observedGenotypes:
      """Generate a dictionary of genotype:count key:values"""
      # maybe this should be a copy of possibleGenotypes with zeroes where
      # there are no observations???
      if self.observedGenotypeCounts.has_key(genotype):
        self.observedGenotypeCounts[genotype] += 1
      else:
        self.observedGenotypeCounts[genotype] = 1

    for i in range(len(self.observedAlleles)):
      """Generate a list of all possible genotypes"""
      self.possibleGenotypes.append(self.observedAlleles[i] + ":" + self.observedAlleles[i])   # the homozygotes
      for j in range(i + 1, len(self.observedAlleles)):
        if j < len(self.observedAlleles):
          self.possibleGenotypes.append(self.observedAlleles[i] + ":" + self.observedAlleles[j])

#--mpn-- is working here
    for genotype in self.possibleGenotypes:
      """Calculate expected genotype counts under HWP"""
      temp = string.split(genotype, ':')
      if temp[0] == temp[1]:         # homozygote, N * pi * pi
        self.expectedGenotypeCounts[genotype] = self.n * self.alleleFrequencies[temp[0]] * self.alleleFrequencies[temp[1]]
      else:                          # heterozygote, 2N * pi * pj
        self.expectedGenotypeCounts[genotype] = 2 * self.n * self.alleleFrequencies[temp[0]] * self.alleleFrequencies[temp[1]]


    if self.debug:
      print 'Allele Frequencies:'
      for allele in self.alleleFrequencies.items():
        print allele
      print 'Cumulative frequency:', frequencyAccumulator
      print 'Total allele count:', self.alleleTotal
      print '\nGenotype counts:'
      print 'Observed:'
      for genotype in self.observedGenotypeCounts.items():
        print genotype
      print 'Expected:'
      for genotype in self.expectedGenotypeCounts.items():
        print genotype

