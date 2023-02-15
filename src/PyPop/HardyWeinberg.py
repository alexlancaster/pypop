#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2003-2006.
# The Regents of the University of California (Regents)
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

"""Module for calculating Hardy-Weinberg statistics.

"""

import sys, os, subprocess, io
from PyPop import _Pvalue
from math import pow, sqrt
from tempfile import TemporaryDirectory
# FIXME: should remove the need for hardcoding a GENOTYPE_SEPARATOR
# this can clash with a character within an allele identifier too easily
from PyPop.Utils import getStreamType, TextOutputStream, GENOTYPE_SEPARATOR
from PyPop.Arlequin import ArlequinExactHWTest

def _chen_statistic (genotype, alleleFreqs, genotypes,  total_gametes):

  total_indivs = total_gametes/2

  allele1, allele2 = genotype.split(GENOTYPE_SEPARATOR)
  p_i = alleleFreqs[allele1]
  p_j = alleleFreqs[allele2]

  # get current genotype frequency
  p_ij = genotypes[genotype]/float(total_indivs)

  # get homozygous genotype frequencies, set to 0.0 if they aren't seen
  try:
    p_ii = genotypes[allele1+GENOTYPE_SEPARATOR+allele1]/float(total_indivs)
  except KeyError:
    p_ii = 0.0
  try:
    p_jj = genotypes[allele2+GENOTYPE_SEPARATOR+allele2]/float(total_indivs)
  except KeyError:
    p_jj = 0.0
    
  if (allele1 != allele2):
    # heterozygote case

    d = p_i*p_j - (0.5)*p_ij
    var = (1.0/float(total_gametes))*(p_i*p_j*((1-p_i)*(1-p_j) + p_i*p_j)
                                      + p_i*p_i*(p_jj - p_j*p_j) 
                                      + p_j*p_j*(p_ii - p_i*p_i))
  else:
    # homozygote case 
    d = p_i*p_i - p_ii
    var = (1.0/float(total_indivs))*(pow(p_i, 4.0)-(2*pow(p_i,3.0))+(p_i*p_i))

  chiSquare = abs(d)*abs(d)/var

  return chiSquare

class HardyWeinberg:
  """Calculate Hardy-Weinberg statistics.

  Given the observed genotypes for a locus, calculate the expected
  genotype counts based on Hardy Weinberg proportions for individual
  genotype values, and test for fit.

  """

  def __init__(self, locusData=None,
               alleleCount=None,
               lumpBelow = 5,
               flagChenTest = 0,
               debug=0):
    """Constructor.

    - locusData and alleleCount to be provided by driver script
      via a call to ParseFile.getLocusData(locus).

    - lumpBelow: treat alleles with frequency less than this as if they
      were in same class  (Default: 5)

    - flagChenTest: if enabled do Chen's chi-square-based "corrected"
      p-value (Default: 0 [False])

    """

    self.locusData = locusData         # ordered tuples of genotypes
    self.lumpBelow = lumpBelow

    self.alleleCounts = alleleCount[0] #just the dictionary of allelename:count
    self.alleleTotal = alleleCount[1]

    self.debug = debug

    self.n = len(self.locusData)
    self.k = len(self.alleleCounts)

    self.flagChenTest = flagChenTest
    
    self._generateTables()
    self._calcChisq()


################################################################################

  def _generateTables(self):
    """Manipulate the given genotype data to generate
    the tables upon which the calculations will be based."""

    self.alleleFrequencies = {}
    self.observedGenotypes = []
    self.observedAlleles = []               # need a uniqed list
    self.observedGenotypeCounts = {}
    self.possibleGenotypes = []
    self.expectedGenotypeCounts = {}
    self.hetsObservedByAllele = {}
    self.hetsExpectedByAllele = {}
    self.hetsChisqByAllele = {}
    self.hetsPvalByAllele = {}
    self.chisqByGenotype = {}
    self.pvalByGenotype = {}
    self.totalHomsObs = 0
    self.totalHetsObs = 0
    self.totalHomsExp = 0.0
    self.totalHetsExp = 0.0
    
    # self.alleleTotal = 0

    if self.flagChenTest:
      self.chenPvalByGenotype = {}

    for allele in self.locusData:
      """Run through each tuple in the given genotype data and
      create dictionaries of observed alleles and genotypes."""

      if allele[0] not in self.observedAlleles:
        self.observedAlleles.append(allele[0])
      if allele[1] not in self.observedAlleles:
        self.observedAlleles.append(allele[1])

      if allele[0] != allele[1]:
        if allele[0] in self.hetsObservedByAllele:
          self.hetsObservedByAllele[allele[0]] += 1
        else:
          self.hetsObservedByAllele[allele[0]] = 1
        if allele[1] in self.hetsObservedByAllele:
          self.hetsObservedByAllele[allele[1]] += 1
        else:
          self.hetsObservedByAllele[allele[1]] = 1

      self.observedGenotypes.append(allele[0] + GENOTYPE_SEPARATOR + allele[1])

    for allele in self.alleleCounts.keys():
      """For each entry in the dictionary of allele counts
      generate a corresponding entry in a dictionary of frequencies"""

      freq = self.alleleCounts[allele] / float(self.alleleTotal)
      self.alleleFrequencies[allele] = freq

    for genotype in self.observedGenotypes:
      """Generate a dictionary of genotype:count key:values

      - and accumulate totals for homozygotes and heterozygotes"""

      if genotype in self.observedGenotypeCounts:
        self.observedGenotypeCounts[genotype] += 1
      else:
        self.observedGenotypeCounts[genotype] = 1

      temp = genotype.split(GENOTYPE_SEPARATOR)
      if temp[0] == temp[1]:
        self.totalHomsObs += 1
      else:
        self.totalHetsObs += 1

    if self.debug:
      print("Total homozygotes observed:", self.totalHomsObs)
      print("Total heterozygotes observed:", self.totalHetsObs)

    for i in range(len(self.observedAlleles)):
      """Generate a list of all possible genotypes

      - sorting the individual genotypes alphabetically"""

      for j in range(i, len(self.observedAlleles)):
          if self.observedAlleles[i] < self.observedAlleles[j]:
            self.possibleGenotypes.append(self.observedAlleles[i] + GENOTYPE_SEPARATOR + self.observedAlleles[j])
          else:
            self.possibleGenotypes.append(self.observedAlleles[j] + GENOTYPE_SEPARATOR + self.observedAlleles[i])

    for genotype in self.possibleGenotypes:
      """Calculate expected genotype counts under HWP

      - Create a dictionary of genotype:frequency key:values

      - accumulate totals for homozygotes and heterozygotes

      - and build table of observed genotypes for each allele"""

      temp = genotype.split(GENOTYPE_SEPARATOR)
      if temp[0] == temp[1]:         # homozygote, N * pi * pi
        self.expectedGenotypeCounts[genotype] = self.n * \
        self.alleleFrequencies[temp[0]] * self.alleleFrequencies[temp[1]]
        self.totalHomsExp += self.expectedGenotypeCounts[genotype]
      else:                          # heterozygote, 2N * pi * pj
        self.expectedGenotypeCounts[genotype] = 2 * self.n * \
        self.alleleFrequencies[temp[0]] * self.alleleFrequencies[temp[1]]
        self.totalHetsExp += self.expectedGenotypeCounts[genotype]

        for allele in self.observedAlleles:
          if allele == temp[0]:
            if allele in self.hetsExpectedByAllele:
              self.hetsExpectedByAllele[allele] += self.expectedGenotypeCounts[genotype]
            else:
              self.hetsExpectedByAllele[allele] = self.expectedGenotypeCounts[genotype]
          elif allele == temp[1]:
            if allele in self.hetsExpectedByAllele:
              self.hetsExpectedByAllele[allele] += self.expectedGenotypeCounts[genotype]
            else:
              self.hetsExpectedByAllele[allele] = self.expectedGenotypeCounts[genotype]

    total = 0
    for value in self.expectedGenotypeCounts.values():
      """Check that the sum of expected genotype counts approximates N"""

      total += value
    if abs(float(self.n) - total) > float(self.n) / 1000.0:
      print('AAIIEE!')
      print('Calculated sum of expected genotype counts is:', total, ', but N is:', self.n)
      sys.exit()

################################################################################

  def _calcChisq(self):
    """First calculate the chi-squareds for the homozygotes
    and heterozygotes,

    - then calculate the chi-squareds for the common genotypes.

    - create a count of observed and expected lumped together for
      genotypes with an expected value of less than lumpBelow

    - Chi-square p-values are calculated with the _Pvalue extension
      module called as an inline Python function, but is C code
      compiled as a loadable shared library.  This code is based on
      R's implementation of the chi-square test which is released
      under the GNU GPL and as such, is redistributable with our
      code, removing the need for an external program"""

    self.counterA = {}
    self.chisq = {}
    self.chisqPval = {}
    self.commonGenotypeCounter = 0
    self.commonChisqAccumulator = 0.0
    self.commonObservedAccumulator = 0
    self.commonExpectedAccumulator = 0.0
    self.rareGenotypeCounter = 0
    self.lumpedObservedGenotypes = 0.0
    self.lumpedExpectedGenotypes = 0.0
    self.flagHets = 0
    self.flagHoms = 0
    self.flagCommons = 0
    self.flagLumps = 0
    self.flagCommonPlusLumped = 0
    self.flagTooManyParameters = 0
    self.flagTooFewExpected = 0
    self.flagNoCommonGenotypes = 0
    self.flagNoRareGenotypes = 0

    # first all the the homozygotes
    if self.totalHomsExp >= self.lumpBelow:
      squareMe = self.totalHomsObs - self.totalHomsExp
      self.totalChisqHoms = (squareMe * squareMe) / self.totalHomsExp

      self.chisqHomsPval = _Pvalue.pval(self.totalChisqHoms, 1)
      self.flagHoms = 1

    # next all the heterozygotes
    if self.totalHetsExp >= self.lumpBelow:
      squareMe = self.totalHetsObs - self.totalHetsExp
      self.totalChisqHets = (squareMe * squareMe) / self.totalHetsExp

      self.chisqHetsPval = _Pvalue.pval(self.totalChisqHets, 1)
      self.flagHets = 1

    # now the values for heterozygoous genotypes by allele
    for allele in self.observedAlleles:
      if self.hetsExpectedByAllele:
        if self.hetsExpectedByAllele[allele] >= self.lumpBelow:
          if not (allele in self.hetsObservedByAllele):
            self.hetsObservedByAllele[allele] = 0

          squareMe = self.hetsObservedByAllele[allele] - self.hetsExpectedByAllele[allele]
          self.hetsChisqByAllele[allele] = (squareMe * squareMe) / self.hetsExpectedByAllele[allele]

          self.hetsPvalByAllele[allele] = _Pvalue.pval(self.hetsChisqByAllele[allele], 1)

          if self.debug:
            print('By Allele:    obs exp   chi        p')
            print('          ', allele, self.hetsObservedByAllele[allele], self.hetsExpectedByAllele[allele], self.hetsChisqByAllele[allele], self.hetsPvalByAllele[allele])

    # do Chen's statistic
    if self.flagChenTest:
      for genotype in self.observedGenotypeCounts.keys():
        chenChiSquare = _chen_statistic(genotype, self.alleleFrequencies,
                            self.observedGenotypeCounts, self.alleleTotal)
        self.chenPvalByGenotype[genotype] = _Pvalue.pval(chenChiSquare,1)

    # the list for all genotypes by genotype
    for genotype in self.expectedGenotypeCounts.keys():

      if self.expectedGenotypeCounts[genotype] >= self.lumpBelow:
        if not (genotype in self.observedGenotypeCounts):
          self.observedGenotypeCounts[genotype] = 0

        squareMe = self.observedGenotypeCounts[genotype] - self.expectedGenotypeCounts[genotype]

        self.chisqByGenotype[genotype] = (squareMe * squareMe) / self.expectedGenotypeCounts[genotype]
        self.pvalByGenotype[genotype] = _Pvalue.pval(self.chisqByGenotype[genotype],1)
        
        if self.debug:
          print('By Genotype:  obs exp   chi        p')
          print('          ', genotype, self.observedGenotypeCounts[genotype], self.expectedGenotypeCounts[genotype], self.chisqByGenotype[genotype], self.pvalByGenotype[genotype])


    # and now the hard stuff
    for genotype in self.expectedGenotypeCounts.keys():
      if self.expectedGenotypeCounts[genotype] >= self.lumpBelow:

        # Count the common genotypes in categories by allele.
        # Used to determine DoF for common genotypes later.
        temp = genotype.split(GENOTYPE_SEPARATOR)
        if temp[0] in self.counterA:
          self.counterA[temp[0]] += 1
        else:
          self.counterA[temp[0]] = 1
        if temp[1] in self.counterA:
          self.counterA[temp[1]] += 1
        else:
          self.counterA[temp[1]] = 1

        if self.debug:
          print('Expected:')
          print(genotype, self.expectedGenotypeCounts[genotype])
          if genotype in self.observedGenotypeCounts:
            print('Observed:', self.observedGenotypeCounts[genotype])
          else:
            print('Observed: 0')

        # calculate the contribution of each genotype to it
        # and tot up the cumulative chi-square 
        self.commonGenotypeCounter += 1
        if genotype in self.observedGenotypeCounts:
          observedCount = self.observedGenotypeCounts[genotype]
        else:
          observedCount = 0.0

        squareMe = observedCount - self.expectedGenotypeCounts[genotype]
        self.chisq[genotype] = (squareMe * squareMe) / self.expectedGenotypeCounts[genotype]

        self.chisqPval[genotype] = _Pvalue.pval(self.chisq[genotype], 1)
        
        self.commonChisqAccumulator += self.chisq[genotype]
        self.commonObservedAccumulator += observedCount
        self.commonExpectedAccumulator += self.expectedGenotypeCounts[genotype]

        if self.debug:
          print('Chi Squared value:')
          print(genotype, ':', self.chisq[genotype])
          # print("command %s returned %s" % (command, returnedValue)
          print('P-value:')
          print(genotype, ':', self.chisqPval[genotype])

      else:
        """Expected genotype count for this genotype is less than lumpBelow"""

        self.rareGenotypeCounter += 1

        self.lumpedExpectedGenotypes += self.expectedGenotypeCounts[genotype]

        if genotype in self.observedGenotypeCounts:
          self.lumpedObservedGenotypes += self.observedGenotypeCounts[genotype]
    # End of loop for genotype in self.expectedGenotypeCounts.keys():

    if self.commonGenotypeCounter == 0:
    # no common genotypes, so do no calculations.

      self.flagNoCommonGenotypes = 1

    elif self.rareGenotypeCounter == 0:
    # no rare genotypes, so just do overall grand total

      self.HWChisq = self.commonChisqAccumulator

      self.HWChisqDf = (float(self.k) * (float(self.k - 1.0))) / 2.0
      self.HWChisqPval = _Pvalue.pval(self.commonChisqAccumulator, self.HWChisqDf)

      self.flagCommons = 1
      self.flagNoRareGenotypes = 1

    elif self.rareGenotypeCounter > 0:
      """ Calculate the Chi Squared value for the lumped rare genotypes"""

      # first calculate the degrees of freedom for the common genotypes
      self.counterAllelesCommon = 0

      for allele in self.counterA.keys():
        if self.counterA[allele] > 0:
          self.counterAllelesCommon += 1

      # if all alleles present in common genotypes, then there are
      # k - 1 independent allele frequency estimates.
      if self.counterAllelesCommon == self.k:
        self.counterAllelesCommon -= 1

      self.commonDf = self.commonGenotypeCounter - self.counterAllelesCommon

      if self.debug:
        print("self.commonGenotypeCounter - self.counterAllelesCommon = self.commonDf")
        print(self.commonGenotypeCounter, "-", self.counterAllelesCommon, "=", self.commonDf)

      if self.commonDf >= 1:
      # if the value for degrees of freedom is not zero or negative

        if self.lumpedExpectedGenotypes >= self.lumpBelow:
        # do chisq for the lumped genotypes

          squareMe = self.lumpedObservedGenotypes - self.lumpedExpectedGenotypes
          self.lumpedChisq = (squareMe * squareMe) / self.lumpedExpectedGenotypes

          self.lumpedChisqPval = _Pvalue.pval(self.lumpedChisq, 1)
            
          self.flagLumps = 1

          if self.debug:
            print("Lumped %d for a total of %d observed and %f expected" % (self.rareGenotypeCounter, self.lumpedObservedGenotypes, self.lumpedExpectedGenotypes))
            print("Chisq: %f, P-Value (dof = 1): %s" % (self.lumpedChisq, self.lumpedChisqPval)) # doesn't work if I claim Pval is a float?

        else:
          self.flagTooFewExpected = 1

        # Do commons by themselves first
        self.HWChisq = self.commonChisqAccumulator
        self.HWChisqDf = self.commonDf
        self.HWChisqPval = _Pvalue.pval(self.HWChisq, self.HWChisqDf)
        self.flagCommons = 1

        if self.flagLumps == 1:
        # Do common plus lumped
          self.commonPlusLumpedChisq = self.commonChisqAccumulator + self.lumpedChisq
          self.commonPlusLumpedObserved = self.commonObservedAccumulator + self.lumpedObservedGenotypes
          self.commonPlusLumpedExpected = self.commonExpectedAccumulator + self.lumpedExpectedGenotypes
          self.commonPlusLumpedChisqDf = self.commonDf
          self.commonPlusLumpedChisqPval = _Pvalue.pval(self.commonPlusLumpedChisq, self.commonPlusLumpedChisqDf)
          
          self.flagCommonPlusLumped = 1

      else:
        self.flagTooManyParameters = 1

################################################################################

  def serializeTo(self, stream, allelelump=0):
    type = getStreamType(stream)

    # stream serialization goes here

    stream.opentag('hardyweinberg', allelelump=("%d" % allelelump))
    stream.writeln()
    stream.tagContents("samplesize", "%d" % self.n)
    stream.writeln()
    # don't print(out, already printed out in <allelecounts> tag in ParseFile
    # stream.tagContents("distinctalleles", "%d" % self.k)
    # stream.writeln()
    stream.tagContents("lumpBelow", "%d" % self.lumpBelow)
    stream.writeln()

    self.serializeXMLTableTo(stream)

    if self.flagHoms == 1:
      stream.opentag('homozygotes')
      stream.writeln()
      stream.tagContents("observed", "%d" % self.totalHomsObs)
      stream.writeln()
      stream.tagContents("expected", "%4f" % self.totalHomsExp)
      stream.writeln()
      stream.tagContents("chisq", "%4f" % self.totalChisqHoms)
      stream.writeln()
      stream.tagContents("pvalue", "%4f" % self.chisqHomsPval)
      stream.writeln()
      stream.tagContents("chisqdf", "1")
      stream.writeln()
      stream.closetag('homozygotes')
      stream.writeln()

    if self.flagHets == 1:
      stream.opentag('heterozygotes')
      stream.writeln()
      stream.tagContents("observed", "%d" % self.totalHetsObs)
      stream.writeln()
      stream.tagContents("expected", "%4f" % self.totalHetsExp)
      stream.writeln()
      stream.tagContents("chisq", "%4f" % self.totalChisqHets)
      stream.writeln()
      stream.tagContents("pvalue", "%4f" % self.chisqHetsPval)
      stream.writeln()
      stream.tagContents("chisqdf", "1")
      stream.writeln()
      stream.closetag('heterozygotes')
      stream.writeln()

    # loop for heterozygotes by allele
    stream.opentag('heterozygotesByAllele')
    stream.writeln()
    for allele in self.hetsChisqByAllele.keys():
      stream.opentag('allele', name=allele)
      stream.writeln()
      stream.tagContents("observed", "%d" % self.hetsObservedByAllele[allele])
      stream.writeln()
      stream.tagContents("expected", "%4f" % self.hetsExpectedByAllele[allele])
      stream.writeln()
      stream.tagContents("chisq", "%4f" % self.hetsChisqByAllele[allele])
      stream.writeln()
      stream.tagContents("pvalue", "%4f" % self.hetsPvalByAllele[allele])
      stream.writeln()
      stream.closetag('allele')
      stream.writeln()

    stream.closetag('heterozygotesByAllele')
    stream.writeln()

    if self.flagLumps == 1:
      stream.opentag('lumped')
      stream.writeln()
      stream.tagContents("observed", "%d" % self.lumpedObservedGenotypes)
      stream.writeln()
      stream.tagContents("expected", "%4f" % self.lumpedExpectedGenotypes)
      stream.writeln()
      stream.tagContents("chisq", "%4f" % self.lumpedChisq)
      stream.writeln()
      stream.tagContents("pvalue", "%4f" % self.lumpedChisqPval)
      stream.writeln()
      stream.tagContents("chisqdf", "1")
      stream.writeln()
      stream.closetag('lumped')
      stream.writeln()
    else:
      if self.flagNoRareGenotypes == 1:
        stream.emptytag('lumped', role='no-rare-genotypes')
      elif self.flagTooFewExpected == 1:
        stream.emptytag('lumped', role='too-few-expected')
      else:
        stream.emptytag('lumped', role='not-calculated')

    if self.flagCommons == 1:
      stream.opentag('common')
      stream.writeln()
      stream.tagContents("observed", "%d" % self.commonObservedAccumulator)
      stream.writeln()
      stream.tagContents("expected", "%4f" % self.commonExpectedAccumulator)
      stream.writeln()
      stream.tagContents("chisq", "%4f" % self.HWChisq)
      stream.writeln()
      stream.tagContents("pvalue", "%4f" % self.HWChisqPval)
      stream.writeln()
      stream.tagContents("chisqdf", "%d" % int(self.HWChisqDf))
      stream.writeln()
      stream.closetag('common')
      stream.writeln()
    else:
      if self.flagNoCommonGenotypes == 1:
        stream.emptytag('common', role='no-common-genotypes')
      elif self.flagTooManyParameters == 1:
        stream.emptytag('common', role='too-many-parameters')
      else:
        stream.emptytag('common', role='not-calculated')
      stream.writeln()

    if self.flagCommonPlusLumped == 1:
      stream.opentag('commonpluslumped')
      stream.writeln()
      stream.tagContents("observed", "%d" % self.commonPlusLumpedObserved)
      stream.writeln()
      stream.tagContents("expected", "%4f" % self.commonPlusLumpedExpected)
      stream.writeln()
      stream.tagContents("chisq", "%4f" % self.commonPlusLumpedChisq)
      stream.writeln()
      stream.tagContents("pvalue", "%4f" % self.commonPlusLumpedChisqPval)
      stream.writeln()
      stream.tagContents("chisqdf", "%d" % int(self.commonPlusLumpedChisqDf))
      stream.writeln()
      stream.closetag('commonpluslumped')
      stream.writeln()
    else:
      stream.emptytag('commonpluslumped', role='not-calculated')
      stream.writeln()

    stream.closetag('hardyweinberg')

    # extra spacer line
    stream.writeln()

  def serializeXMLTableTo(self, stream):

    sortedAlleles = self.observedAlleles[:]
    sortedAlleles.sort()

    stream.opentag("genotypetable")
    stream.writeln()

    genotypeId = 0

    for horiz in sortedAlleles:

      for vert in sortedAlleles:
        # ensure that matrix is triangular
        if vert > horiz:
          continue

        # start tag
        stream.opentag("genotype", row=horiz, id=("%d" % genotypeId), col=vert)

        # increment id
        genotypeId += 1

        # need to check both permutations of key
        key1 = "%s%s%s" % (horiz, GENOTYPE_SEPARATOR, vert)
        key2 = "%s%s%s" % (vert, GENOTYPE_SEPARATOR, horiz)

        # get observed value
        if key1 in self.observedGenotypeCounts:
          obs = self.observedGenotypeCounts[key1]
        elif key2 in self.observedGenotypeCounts:
          obs = self.observedGenotypeCounts[key2]
        else:
          obs = 0

        # get expected value
        if key1 in self.expectedGenotypeCounts:
          exp = self.expectedGenotypeCounts[key1]
        elif key2 in self.expectedGenotypeCounts:
          exp = self.expectedGenotypeCounts[key2]
        else:
          exp = 0.0

        stream.writeln()
        stream.tagContents("observed", "%d" % obs)
        stream.writeln()
        stream.tagContents("expected", "%4f" % exp)
        stream.writeln()

        # get and tag chisq and pvalue (if they exist)
        if key1 in self.chisqByGenotype:
          stream.tagContents("chisq", "%4f" % self.chisqByGenotype[key1])
          stream.writeln()
          stream.tagContents("pvalue", "%4f" % self.pvalByGenotype[key1])
        elif key2 in self.chisqByGenotype:
          stream.tagContents("chisq", "%4f" % self.chisqByGenotype[key2])
          stream.writeln()
          stream.tagContents("pvalue", "%4f" % self.pvalByGenotype[key2])
        else:
          stream.emptytag("chisq", role='not-calculated')
          stream.writeln()
          stream.emptytag("pvalue", role='not-calculated')
        stream.writeln()

        if self.flagChenTest:
          if key1 in self.chenPvalByGenotype:
            stream.tagContents("chenPvalue", "%4f" % \
                             self.chenPvalByGenotype[key1])
          elif key2 in self.chenPvalByGenotype:
            stream.tagContents("chenPvalue", "%4f" % \
                               self.chenPvalByGenotype[key2])
          else:
            stream.emptytag("chenPvalue", role='not-calculated')
          stream.writeln()

          
        stream.closetag("genotype")
        stream.writeln()

    stream.closetag("genotypetable")
    stream.writeln()

class HardyWeinbergGuoThompson(HardyWeinberg):
  """Wrapper class for 'gthwe'

  A wrapper for the Guo & Thompson program 'gthwe'. 

  - 'locusData', 'alleleCount':  As per base class.
  
  In addition to the arguments for the base class, this class
  accepts the following additional keywords:

  - 'runMCMCTest': If enabled run the Monte Carlo-Markov chain (MCMC)
    version of the test (what is normally referred to as "Guo &
    Thompson")
  
  - 'runPlainMCTest': If enabled run a plain Monte Carlo/randomization
    without the Markov-chain version of the test (this is also
    described in the original "Guo & Thompson" Biometrics paper, but
    was not in their original program)


  - 'dememorizationSteps': number of `dememorization' initial steps
    for random number generator (default 2000).

  - 'samplingNum': the number of chunks for random number generator
    (default 1000).

  - 'samplingSize': size of each chunk (default 1000).

  - 'maxMatrixSize': maximum size of `flattened' lower-triangular matrix of
     observed alleles (default 250).

  - 'monteCarloSteps': number of steps for the plain Monte Carlo
     randomization test (without Markov-chain)
     """

  def __init__(self,
               locusData=None,
               alleleCount=None,
               runMCMCTest=0,
               runPlainMCTest=0,
               dememorizationSteps=2000,
               samplingNum=1000,
               samplingSize=1000,
               maxMatrixSize=250,
               monteCarloSteps=1000000, # samplingNum*samplingSize (consistency)
               testing=False,
               **kw):

    self.runMCMCTest=runMCMCTest
    self.runPlainMCTest=runPlainMCTest
    self.dememorizationSteps=dememorizationSteps
    self.samplingNum=samplingNum
    self.samplingSize=samplingSize
    self.maxMatrixSize=maxMatrixSize
    self.monteCarloSteps=monteCarloSteps
    if testing:
      self.testing = 1
    else:
      self.testing = 0

    # call constructor of base class
    HardyWeinberg.__init__(self,
                           locusData=locusData,
                           alleleCount=alleleCount,
                           **kw)

  def generateFlattenedMatrix(self):

    self.sortedAlleles = self.observedAlleles
    self.sortedAlleles.sort()

    if self.debug:
      print ("sortedAlleles: ", self.sortedAlleles)
      print ("observedGenotypeCounts: ", self.observedGenotypeCounts)

    # allele list
    self.flattenedMatrix = []
    self.flattenedMatrixNames = []
    self.totalGametes = 0

    # FIXME: The order in which this flattenedMatrix is generated is
    # very important, because it must match *exactly* the order in
    # which is emitted by the XML <hardyweinberg><genotypetable>.
    # currently the order *does* match, because allele list is
    # sorted before running test (check this!).  If it didn't, the
    # individual pvalues genotypes output order in the gthwe module
    # wouldn't match the genotypes in the XML, making it impossible
    # to match the emitted pvalues with their genotype label (I
    # can't think of any other solution to this other than passing
    # in the labels for the genotypes which would be very
    # cumbersome).
    for horiz in self.sortedAlleles:
      # print("%2s" % horiz),
      for vert in self.sortedAlleles:
        # ensure that matrix is triangular
        if vert > horiz:
          continue

        # need to check both permutations of key
        key1 = "%s%s%s" % (horiz, GENOTYPE_SEPARATOR, vert)
        key2 = "%s%s%s" % (vert, GENOTYPE_SEPARATOR, horiz)
        if key1 in self.observedGenotypeCounts:
          output = "%2s " % self.observedGenotypeCounts[key1]
        elif key2 in self.observedGenotypeCounts:
          output = "%2s " % self.observedGenotypeCounts[key2]
        else:
          output = "%2s " % "0"

        self.flattenedMatrix.append(int(output))
        self.flattenedMatrixNames.append(key2)
        self.totalGametes += int(output)
               
  def dumpTable(self, locusName, stream, allelelump=0):

    if locusName[0] == '*':
      locusName = locusName[1:]

    if self.k < 2:
      stream.emptytag('hardyweinbergGuoThompson', role='too-few-alleles')
      return

    matrixElemCount = (self.k * (self.k + 1)) / 2

    # generate a flattened matrix
    self.generateFlattenedMatrix()

    # create dummy array with length of the number of alleles
    n = [0]*(self.k)

    if self.debug:
      print("flattenedMatrix:", self.flattenedMatrix)
      print("flattenedMatrixNames:", self.flattenedMatrixNames)
      print("len(flattenedMatrix):", len(self.flattenedMatrix))
      print("n: ", n)
      print("k: ", self.k)
      print("totalGametes", self.totalGametes)
      print("sampling{steps,num, size}: ", self.dememorizationSteps, self.samplingNum, self.samplingSize)
      print("locusName: ", locusName)
      print("allelelump: ", allelelump)

      # flush stdout before running the G&T step
      sys.stdout.flush()

    # import library only when necessary
    from PyPop import _Gthwe

    if self.runMCMCTest:

      stream.opentag('hardyweinbergGuoThompson',
                      allelelump=("%d" % allelelump))

      self.serializeXMLTableTo(stream)

      with TemporaryDirectory() as tmp:
        # generates temporary directory and filename, and cleans-up after block ends
        xml_tmp_filename=os.path.join(tmp, 'gthwe.out.xml')

        _Gthwe.run_data(self.flattenedMatrix, n, self.k, self.totalGametes,
                        self.dememorizationSteps, self.samplingNum,
                        self.samplingSize, locusName, xml_tmp_filename, 0, self.testing)

        # read the generated contents of the temporary XML file
        fp = open(xml_tmp_filename)
        # copy XML output to stream
        stream.write(fp.read())
        fp.close()

      stream.closetag('hardyweinbergGuoThompson')
      stream.writeln()


    if self.runPlainMCTest:
      stream.opentag('hardyweinbergGuoThompson',
                      type='monte-carlo',
                      allelelump=("%d" % allelelump))
      self.serializeXMLTableTo(stream)

      
      with TemporaryDirectory() as tmp:
        # generates temporary directory and filename, and cleans-up after block ends
        xml_tmp_filename=os.path.join(tmp, 'gthwe.out.xml')

        _Gthwe.run_randomization(self.flattenedMatrix, n, self.k,
                                 self.totalGametes, self.monteCarloSteps,
                                 xml_tmp_filename, 0, self.testing)

        # read the generated contents of the temporary XML file
        fp = open(xml_tmp_filename)
        # copy XML output to stream
        stream.write(fp.read())
        fp.close()
        
      stream.closetag('hardyweinbergGuoThompson')
      stream.writeln()



class HardyWeinbergEnumeration(HardyWeinbergGuoThompson):
  """Uses Hazael Maldonado Torres' exact enumeration test

  - 'doOverall': if set to true ('1'), then do overall p-value test
                 default is false ('0')
  """
  def __init__(self,
               locusData=None,
               alleleCount=None,
               doOverall=0,
               **kw):
    from PyPop import _HweEnum

    self.HweEnumProcess = _HweEnum
    
    HardyWeinbergGuoThompson.__init__(self,
                                      locusData=locusData,
                                      alleleCount=alleleCount,
                                      **kw)
    self.doOverall = doOverall
    self.generateFlattenedMatrix()

    self.HweEnumProcess.run_external(self.flattenedMatrix,
                                     self.k,
                                     self.doOverall)

    if self.doOverall:
      self.exactPValue = self.HweEnumProcess.get_p_value()
      self.observedPValue = self.HweEnumProcess.get_pr_observed()
      self.diffPvals =  self.HweEnumProcess.get_diff_statistic_pvalue()
      self.chenPvals =  self.HweEnumProcess.get_chen_statistic_pvalue()
    else:
      self.diffPvals =  self.HweEnumProcess.get_diff_statistic_pvalue_ext()
      self.chenPvals =  self.HweEnumProcess.get_chen_statistic_pvalue_ext()
      
    
  def serializeTo(self, stream, allelelump=0):
    stream.opentag('hardyweinbergEnumeration',
                   allelelump=("%d" % allelelump))

    self.serializeXMLTableTo(stream)
    
    stream.writeln()
    if self.doOverall:
      stream.tagContents("pvalue", "%f" % self.exactPValue, type="overall")
    else:
      stream.emptytag("pvalue", type="overall", role="not-calculated")
    stream.writeln()
    if self.doOverall:
      stream.tagContents("pvalue", "%f" % self.observedPValue, type="observed")
    else:
      stream.emptytag("pvalue", type="observed", role="not-calculated")
    stream.writeln()

    if self.doOverall:
      method="full"
    else:
      method="three-by-three"
      
    for i in range(0, self.k):
      for j in range(0, i+1):

        if self.debug:
          print("genotype count: %4d" % self.flattenedMatrix[(i*(i+1)/2)+j],
                "diff pval: %.4f" % self.diffPvals[(i*(i+1)/2)+j],
                "chen pval: %.4f" % self.chenPvals[(i*(i+1)/2)+j])

        stream.tagContents ("pvalue", "%f" % self.diffPvals[(i*(i+1)/2)+j],
                            type='genotype', statistic='diff_statistic',
                            row=("%d" % i), col=("%d" % j), method=method)

        stream.tagContents ("pvalue", "%f" % self.chenPvals[(i*(i+1)/2)+j],
                            type='genotype', statistic='chen_statistic',
                            row=("%d" % i), col=("%d" % j), method=method)

        stream.writeln()
    stream.closetag('hardyweinbergEnumeration')
    self.HweEnumProcess.cleanup()
    
class HardyWeinbergGuoThompsonArlequin:
  """Wrapper class for 'Arlequin'.

  This class extracts the Hardy-Weinberg (HW) statistics using the
  Arlequin implementation of the HW exact test, by the following:

  1. creates a subdirectory 'arlequinRuns' in which all the Arlequin
     specific files are generated;

  2. then the specified arlequin executable is run, generating the
     Arlequin output HTML files (*.htm);

  3. the Arlequin output is then parsed for the relevant statistics;

  4. lastly, the 'arlequinRuns' directory is removed.

  Since the directory name 'arlequinRuns' is currently hardcoded, this
  has the consequence that this class cannot be invoked concurrently.

  Parameters:

  - 'markovChainStepsHW': Number of steps to use in Markov chain
  (default: 100000).

  - 'markovChainDememorisationStepsHW': "Burn-in" time for Markov
  chain (default: 1000).

  """
  def __init__(self,
               matrix=None,
               locusName=None,
               arlequinExec='arlecore.exe',
               markovChainStepsHW = 100000,
               markovChainDememorisationStepsHW = 1000,
               untypedAllele='****',
               debug=None):

    self.matrix = matrix
    self.locusName = locusName
    self.debug = debug
    self.arlequinExec = arlequinExec
    self.markovChainStepsHW = markovChainStepsHW
    self.markovChainDememorisationStepsHW = markovChainDememorisationStepsHW

    self.untypedAllele = untypedAllele
    self.noDataFlag = 0
    
    # if no data, don't run analysis
    if len(self.matrix.filterOut(self.locusName, self.untypedAllele)) > 0:

      arlequin = ArlequinExactHWTest(matrix = self.matrix,
                                     lociList = [self.locusName],
                                     arlequinExec = self.arlequinExec,
                                     markovChainStepsHW = \
                                     self.markovChainStepsHW,
                                     markovChainDememorisationStepsHW = \
                                     self.markovChainDememorisationStepsHW,
                                     untypedAllele = self.untypedAllele,
                                     debug=self.debug)
      
      self.output = arlequin.getHWExactTest()
      arlequin.cleanup()
      
    else:
      self.noDataFlag = 1

  def serializeTo(self, stream):

    if self.noDataFlag:
      stream.emptytag('hardyweinbergGuoThompsonArlequin', role='no-data')
      stream.writeln()

    else:
      if self.debug:
        print(self.output)

      # if this is monomorphic locus, can't do HW exact testwith
      # Arlequin, return an empty tag with role='monomorphic'
      
      if self.output['1'] == 'monomorphic':
        stream.emptytag('hardyweinbergGuoThompsonArlequin', role='monomorphic')
        stream.writeln()

      else:
        
        # only one locus done at a time from output
        genos, obsHet, expHet, pvalue, stddev, steps = self.output['1']

        # generate output section
        stream.opentag('hardyweinbergGuoThompsonArlequin')
        stream.writeln()
        stream.tagContents('obs-hetero', "%4f" % obsHet)
        stream.writeln()
        stream.tagContents('exp-hetero', "%4f" % expHet)
        stream.writeln()
        stream.tagContents('pvalue', "%4f" % pvalue)
        stream.writeln()
        stream.tagContents('stddev', "%4f" % stddev)
        stream.writeln()
        stream.tagContents('steps', "%d" % steps)
        stream.writeln()
        stream.closetag('hardyweinbergGuoThompsonArlequin')
        stream.writeln()
      
    
