#!/usr/bin/env python

"""Module for calculating Hardy-Weinberg statistics.

"""

import string, sys, os, popen2
from Utils import getStreamType, TextOutputStream

class HardyWeinberg:
  """Calculate Hardy-Weinberg statistics.

  Given the observed genotypes for a locus, calculate the expected
  genotype counts based on Hardy Weinberg proportions for individual
  genotype values, and test for fit.

  """

  def __init__(self, locusData, alleleCount, lumpBelow, debug=0):
    """Constructor.

    - locusData and alleleCount to be provided by driver script
      via a call to ParseFile.getLocusData(locus).

    """

    self.locusData = locusData         # ordered tuples of genotypes
    self.lumpBelow = lumpBelow

    self.alleleCounts = alleleCount[0] #just the dictionary of allelename:count
    self.alleleTotal = alleleCount[1]

    self.debug = debug

    self.n = len(self.locusData)
    self.k = len(self.alleleCounts)

    self._generateTables()
    self._calcChisq()

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
#         freq = self.alleleCount[allele] / float(self.alleleTotal)
#         running_freq += freq
#         print allele, 'obs:', self.alleleCount[allele],\
#                       'count:', running_count,\
#                       'freq:', freq,\
#                       'cum:', running_freq
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
    
    # self.alleleTotal = 0

    for genotype in self.locusData:
      """Run through each tuple in the given genotype data and
      create a dictionary of allele counts"""

      # self.alleleTotal += 2
      # if self.alleleCounts.has_key(genotype[0]):
      #   self.alleleCounts[genotype[0]] += 1
      # else:
      #   self.alleleCounts[genotype[0]] = 1
      # if self.alleleCounts.has_key(genotype[1]):
      #   self.alleleCounts[genotype[1]] += 1
      # else:
      #   self.alleleCounts[genotype[1]] = 1

      if genotype[0] not in self.observedAlleles:
        self.observedAlleles.append(genotype[0])
      if genotype[1] not in self.observedAlleles:
        self.observedAlleles.append(genotype[1])

      self.observedGenotypes.append(genotype[0] + ":" + genotype[1])

    frequencyAccumulator = 0.
    for allele in self.alleleCounts.keys():
      """For each entry in the dictionary of allele counts
      generate a corresponding entry in a dictionary of frequencies"""

      freq = self.alleleCounts[allele] / float(self.alleleTotal)
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
      """Generate a list of all possible genotypes

      - sorting the individual genotypes alphabetically"""

      for j in range(i, len(self.observedAlleles)):
          if self.observedAlleles[i] < self.observedAlleles[j]:
            self.possibleGenotypes.append(self.observedAlleles[i] + ":" + self.observedAlleles[j])
          else:
            self.possibleGenotypes.append(self.observedAlleles[j] + ":" + self.observedAlleles[i])

    for genotype in self.possibleGenotypes:
      """Calculate expected genotype counts under HWP

      - Create a dictionary of genotype:frequency key:values"""

      temp = string.split(genotype, ':')
      if temp[0] == temp[1]:         # homozygote, N * pi * pi
        self.expectedGenotypeCounts[genotype] = self.n * \
        self.alleleFrequencies[temp[0]] * self.alleleFrequencies[temp[1]]
      else:                          # heterozygote, 2N * pi * pj
        self.expectedGenotypeCounts[genotype] = 2 * self.n * \
        self.alleleFrequencies[temp[0]] * self.alleleFrequencies[temp[1]]

    total = 0
    for value in self.expectedGenotypeCounts.values():
      """Check that the sum of expected genotype counts approximates N"""

      total += value
    if abs(float(self.n) - total) > float(self.n) / 1000.0:
      print 'AAIIEE!'
      print 'Calculated sum of expected genotype counts is:', total, ', but N is:', self.n
      sys.exit()

    if self.debug:
#       print 'Allele Frequencies:'
#       for allele in self.alleleFrequencies.items():
#         print allele
#       print 'Cumulative frequency:', frequencyAccumulator
#       print 'Total allele count:', self.alleleTotal
#       print '\nGenotype counts:'
#       print 'Possible:'
#       for genotype in self.possibleGenotypes:
#         print genotype
      print 'Observed:'
      for genotype in self.observedGenotypeCounts.items():
        print genotype
      print 'Expected:'
      for genotype in self.expectedGenotypeCounts.items():
        print genotype

################################################################################

  def _calcChisq(self):
    """Calculate the chi-squareds for the common genotypes.

    - create a count of observed and expected lumped together
    for genotypes with an expected value of less than lumpBelow

    - Open a pipe to get the p-value from the system
    using the pval program (should be replaced later)"""

    self.printExpected = [] # list flagging genotypes worth printing
    self.counterA = {}
    self.chisq = {}
    self.chisqPval = {}
    self.commonGenotypeCounter = 0
    self.commonChisqAccumulator = 0.0
    self.rareGenotypeCounter = 0
    self.lumpedObservedGenotypes = 0.0
    self.lumpedExpectedGenotypes = 0.0
    # print 'Calculating Chi Squared'

    for genotype in self.expectedGenotypeCounts.keys():
      if self.expectedGenotypeCounts[genotype] >= self.lumpBelow:

        self.printExpected.append(genotype) # replaces HWprintexpAiAj in specs

        temp = string.split(genotype, ':')
        if self.counterA.has_key(temp[0]):
          self.counterA[temp[0]] += 1
        else:
          self.counterA[temp[0]] = 1
        if self.counterA.has_key(temp[1]):
          self.counterA[temp[1]] += 1
        else:
          self.counterA[temp[1]] = 1

        if self.debug:
          print 'Expected:'
          print genotype, self.expectedGenotypeCounts[genotype]
          if self.observedGenotypeCounts.has_key(genotype):
            print 'Observed:', self.observedGenotypeCounts[genotype]
          else:
            print 'Observed: 0'

        self.commonGenotypeCounter += 1
        if self.observedGenotypeCounts.has_key(genotype):
          observedCount = self.observedGenotypeCounts[genotype]
        else:
          observedCount = 0.0
        # self.commonDfAccumulator = self.commonGenotypeCounter - 1
        self.chisq[genotype] = ((observedCount - \
                          self.expectedGenotypeCounts[genotype]) * \
                          (observedCount - \
                          self.expectedGenotypeCounts[genotype])) /\
                          self.expectedGenotypeCounts[genotype]

        command = "pval 1 %f" % (self.chisq[genotype])
        returnedValue = os.popen(command, 'r').readlines()
        self.chisqPval[genotype] = returnedValue[0][:-1]
        self.commonChisqAccumulator += self.chisq[genotype]

        if self.debug:
          print 'Chi Squared value:'
          print genotype, ':', self.chisq[genotype]
          # print "command %s returned %s" % (command, returnedValue)
          print 'P-value:'
          print genotype, ':', self.chisqPval[genotype]

      else:
        """Expected genotype count for this genotype is less than lumpBelow"""

        # do not append this genotype to the printExpected list
        self.rareGenotypeCounter += 1

        self.lumpedExpectedGenotypes += self.expectedGenotypeCounts[genotype]

        if self.observedGenotypeCounts.has_key(genotype):
          self.lumpedObservedGenotypes += self.observedGenotypeCounts[genotype]


    if self.rareGenotypeCounter > 0:
      """ Calculate the Chi Squared value for the lumped rare genotypes"""
      self.HWChisq = 99.0
      self.HWChisqDf = 99.0
      self.HWChisqPval = 99.0
      self.lumpedChisq = 99.0
      self.lumpedChisqPval = 99.0

#       self.lumpedChisq = ((self.lumpedObservedGenotypes - self.lumpedExpectedGenotypes) * \
#                          (self.lumpedObservedGenotypes - self.lumpedExpectedGenotypes) / \
#                          self.lumpedExpectedGenotypes)
# 
#       command = "pval 1 %f" % (self.lumpedChisq)
#       returnedValue = os.popen(command, 'r').readlines()
#       self.lumpedChisqPval = returnedValue[0][:-1]
# 
#       if self.commonGenotypeCounter > 0:
#         self.HWChisq = self.commonChisqAccumulator + self.lumpedChisq
#         self.HWChisqDf = self.commonDfAccumulator + 1
#         command = "pval %f %f" % (self.HWChisqDf, self.HWChisq)
#         returnedValue = os.popen(command, 'r').readlines()
#         self.HWChisqPval = returnedValue[0][:-1]
# 
#       if self.debug:
#         print "Lumped %d for a total of %d observed and %f expected" % (self.rareGenotypeCounter, self.lumpedObservedGenotypes, self.lumpedExpectedGenotypes)
#         print "Chisq: %f, P-Value (dof = 1): %s" % (self.lumpedChisq, self.lumpedChisqPval) # doesn't work if I claim Pval is a float?

    elif self.commonGenotypeCounter > 0:
      self.HWChisq = self.commonChisqAccumulator
      # self.HWChisqDf = self.commonDfAccumulator
      self.HWChisqDf = (float(self.k) * (float(self.k - 1.0))) / 2.0

      command = "pval %d %f" % (self.HWChisqDf, self.commonChisqAccumulator)
      returnValue = os.popen(command, 'r').readlines()

      self.HWChisqPval = float(returnValue[0][:-1])

################################################################################

  def getChisq(self):
    """ Output routines depend on existence or otherwise of common and
    rare genotypes"""

    # stream serialization has been moved to serializeTo method (below)
    # this code remains here for backward compatibility with 'tdw.py'
    if self.commonGenotypeCounter == 0:
      print "No common genotypes; chi-square cannot be calculated"

    elif self.rareGenotypeCounter == 0:

      print "No rare genotypes with expected less than %d." % self.lumpBelow
      print "HWChisq    :", self.HWChisq
      print "HWChisqDf  :", self.HWChisqDf
      print "HWChisqPval:", self.HWChisqPval
      print "No lumps"

    else:
      print "Sample size     :", self.n
      print "Distinct Alleles:", self.k
      print "Chi Squared     :", self.HWChisq
      print "DoF             :", self.HWChisqDf
      print "HWChisqPval     :", self.HWChisqPval
      print ""
      print "Lumped observed:", self.lumpedObservedGenotypes
      print "Lumped expected:", self.lumpedExpectedGenotypes
      print "Lumped Chisq   :", self.lumpedChisq
      print "Lumped Pval    :", self.lumpedChisqPval

  def serializeTo(self, stream):
    type = getStreamType(stream)

    # stream serialization goes here
    
    if self.commonGenotypeCounter == 0:
      
      if type == 'xml':
        stream.emptytag('hardyweinberg', role='no-common-genotypes')
      else:
        stream.writeln("No common genotypes; chi-square cannot be calculated")

      stream.writeln()
      
    elif self.rareGenotypeCounter == 0:

      if type == 'xml':
        stream.opentag('hardyweinberg', role='no-lumps')
        stream.tagContents("hwchisq", "%4f" % self.HWChisq)
        stream.tagContents("hwchisqdf", "%4f" % self.HWChisqDf)
        stream.tagContents("hwchisqpval", "%4f" % self.HWChisqPval)
        stream.writeln()

        self.serializeXMLTableTo(stream)

        stream.closetag('hardyweinberg')
        
      else:
        stream.writeln("HardyWeinberg statistics:")
        stream.writeln("=========================")
        stream.writeln()
        stream.writeln("No rare genotypes with expected less than %d." % self.lumpBelow)
        stream.writeln("HWChisq    : %.4f " % self.HWChisq)
        stream.writeln("HWChisqDf  : %.4f " % self.HWChisqDf)
        stream.writeln("HWChisqPval: %.4f " % self.HWChisqPval)
        stream.writeln("No lumps")

        self.serializeTextTableTo(stream)

        stream.writeln()
        
    else:

      if type == 'xml':
        stream.opentag('hardyweinberg', role='lumps')
        stream.tagContents("samplesize", "%d" % self.n)
        stream.writeln()
        stream.tagContents("distinctalleles", "%d" % self.k)
        stream.writeln()
        stream.tagContents("chisquared", "%.4f" % self.HWChisq)
        stream.writeln()
        stream.tagContents("degressoffreedom", "%.4f" % self.HWChisqDf)
        stream.writeln()
        stream.tagContents("hwchisqpval", "%.4f" % float(self.HWChisqPval))
        stream.writeln()
        stream.tagContents("lumpedobserved", "%.4f" % self.lumpedObservedGenotypes)
        stream.writeln()
        stream.tagContents("lumpedexpected", "%4f" % self.lumpedExpectedGenotypes)
        stream.writeln()
        stream.tagContents("lumpedChisq", "%4f" % self.lumpedChisq)
        stream.writeln()
        stream.tagContents("lumpedPval", "%4f" % float(self.lumpedChisqPval))
        stream.writeln()

        self.serializeXMLTableTo(stream)

        stream.closetag('hardyweinberg')
        
      else:
        stream.writeln("HardyWeinberg statistics:")
        stream.writeln("=========================")
        stream.writeln("Sample size: %d" % self.n)
        stream.writeln("Distinct Alleles(k):  %d" % self.k)
        stream.writeln("Chi Squared: %.4f" % self.HWChisq)
        stream.writeln("DoF        : %d " % self.HWChisqDf)
        stream.writeln("HWChisqPval: %.4f" % self.HWChisqPval)
        stream.writeln()
        stream.writeln("Lumped observed: %.4f" % self.lumpedObservedGenotypes)
        stream.writeln("Lumped expected: %.4f" % self.lumpedExpectedGenotypes)
        stream.writeln("Lumped Chisq   : %.4f" % self.lumpedChisq)
        stream.writeln("Lumped Pval    : %.4f" % float(self.lumpedChisqPval))
        stream.writeln()

        self.serializeTextTableTo(stream)

      # extra spacer line
      stream.writeln()

  def serializeXMLTableTo(self, stream):

    sortedAlleles = self.observedAlleles[:]
    sortedAlleles.sort()

    stream.opentag("genotypetable")
    stream.writeln()

    for horiz in sortedAlleles:

      for vert in sortedAlleles:
        # ensure that matrix is triangular
        if vert > horiz:
          continue

        # need to check both permutations of key
        key1 = "%s:%s" % (horiz, vert)
        key2 = "%s:%s" % (vert, horiz)

        # get observed value
        if self.observedGenotypeCounts.has_key(key1):
          obs = self.observedGenotypeCounts[key1]
        elif self.observedGenotypeCounts.has_key(key2):
          obs = self.observedGenotypeCounts[key2]
        else:
          obs = "0"

        # get expected value
        if self.expectedGenotypeCounts.has_key(key1):
          exp = self.expectedGenotypeCounts[key1]
        elif self.expectedGenotypeCounts.has_key(key2):
          exp = self.expectedGenotypeCounts[key2]
        else:
          exp = 0.0

        stream.opentag("genotype", row=horiz, col=vert)
        stream.tagContents("observed", "%2s" % obs)
        stream.tagContents("expected", "%.1f" % exp)
        stream.closetag("genotype")
        stream.writeln()

    stream.closetag("genotypetable")
    stream.writeln()

  def serializeTextTableTo(self, stream):

    sortedAlleles = self.observedAlleles
    sortedAlleles.sort()

    # calculate padding width
    width = len(sortedAlleles[0])

    stream.writeln("Genotype table, format of each cell is: obsd/expt:")
    stream.writeln()

    for horiz in sortedAlleles:

      # write each element of allele row header
      stream.write("%*s " % (width, horiz))

      for vert in sortedAlleles:
        # ensure that matrix is triangular
        if vert > horiz:
          continue

        # need to check both permutations of key
        key1 = "%s:%s" % (horiz, vert)
        key2 = "%s:%s" % (vert, horiz)

        # get observed value
        if self.observedGenotypeCounts.has_key(key1):
          obs = self.observedGenotypeCounts[key1]
        elif self.observedGenotypeCounts.has_key(key2):
          obs = self.observedGenotypeCounts[key2]
        else:
          obs = "0"

        # get expected value
        if self.expectedGenotypeCounts.has_key(key1):
          exp = self.expectedGenotypeCounts[key1]
        elif self.expectedGenotypeCounts.has_key(key2):
          exp = self.expectedGenotypeCounts[key2]
        else:
          exp = 0.0
        stream.write("%2s/%.1f " % (obs, exp))
      stream.writeln()

    # indent allele column footer
    stream.write("%5s" % " ")

    # write allele column footer
    for horiz in sortedAlleles:
      stream.write("%6s " % horiz)
    # end of footer line
    stream.writeln()


class HardyWeinbergGuoThompson(HardyWeinberg):
  """Wrapper class for 'gthwe'

  Currently a hacked-up placeholder class for a wrapper for the Guo &
  Thompson program 'gthwe'.  Need more work before being production!

  - 'locusData', 'alleleCount':  As per base class.
  
  In addition to the arguments for the base class, this class
  accepts the following additional keywords:
  
  - 'dememorizationSteps': number of `dememorization' initial steps
    for random number generator (default 2000).

  - 'samplingNum': the number of chunks for random number generator
    (default 1000).

  - 'samplingSize': size of each chunk (default 1000).
  """

  def __init__(self, locusData, alleleCount,
               dememorizationSteps=2000,
               samplingNum=1000,
               samplingSize=1000,
               **kw):

    self.dememorizationSteps=dememorizationSteps
    self.samplingNum=samplingNum
    self.samplingSize=samplingSize

    # call constructor of base class
    HardyWeinberg.__init__(self, locusData, alleleCount, **kw)

               
  def dumpTable(self, locusName, stream):

    if locusName[0] == '*':
      locusName = locusName[1:]

    hwFilename = locusName + '.hw'
    hwlFilename = locusName + '.hwl'
        
    hwStream = TextOutputStream(open(hwFilename, 'w'))
    hwlStream = TextOutputStream(open(hwlFilename, 'w'))
    
    n = len(self.observedAlleles)

    # generate .hwl file
    hwlStream.writeln(locusName)
    sortedAlleles = self.observedAlleles
    sortedAlleles.sort()

    for allele in sortedAlleles:
      hwlStream.writeln(allele)

    # close the .hwl file
    hwlStream.close()
      
    # generate .hw file
    hwStream.writeln(locusName)
    hwStream.writeln("%d" % n)

    for horiz in sortedAlleles:
      # print "%2s" % horiz,
      for vert in sortedAlleles:
        # ensure that matrix is triangular
        if vert > horiz:
          continue

        # need to check both permutations of key
        key1 = "%s:%s" % (horiz, vert)
        key2 = "%s:%s" % (vert, horiz)
        if self.observedGenotypeCounts.has_key(key1):
          hwStream.write("%2s " % self.observedGenotypeCounts[key1])
        elif self.observedGenotypeCounts.has_key(key2):
          hwStream.write("%2s " % self.observedGenotypeCounts[key2])
        else:
          hwStream.write("%2s " % "0")
      hwStream.writeln()

    # set parameters
    hwStream.writeln("%d %d %d" % (self.dememorizationSteps,
                                   self.samplingNum,
                                   self.samplingSize))
    
    # close the .hw file
    hwStream.close()

    xmlFilename = locusName + '.xml'

    # execute program, capture stdin, stout and stderr
    commandStr = "gthwe %s %s" % (hwFilename, xmlFilename)
    fin, fout, ferr = os.popen3(commandStr, 't', 2000000)

    # check stderr first
    for line in ferr.readlines():
      if line.startswith("***Error"):
        print "too few alleles"
   
    print "stdout:", fout.readlines()
    print "stderr:", ferr.readlines()

    if self.debug:
      print open(xmlFilename, 'r').readlines()

    # copy the resultant output to XML stream
    for line in open(xmlFilename, 'r').readlines():
      stream.write(line)

    # remove temporary files
    os.remove(hwFilename)
    os.remove(hwlFilename)
    os.remove(xmlFilename)
