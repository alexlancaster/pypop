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

    for allele in self.locusData:
      """Run through each tuple in the given genotype data and
      create dictionaries of observed alleles and genotypes."""

      if allele[0] not in self.observedAlleles:
        self.observedAlleles.append(allele[0])
      if allele[1] not in self.observedAlleles:
        self.observedAlleles.append(allele[1])

      if allele[0] != allele[1]:
        if self.hetsObservedByAllele.has_key(allele[0]):
          self.hetsObservedByAllele[allele[0]] += 1
        else:
          self.hetsObservedByAllele[allele[0]] = 1
        if self.hetsObservedByAllele.has_key(allele[1]):
          self.hetsObservedByAllele[allele[1]] += 1
        else:
          self.hetsObservedByAllele[allele[1]] = 1

      self.observedGenotypes.append(allele[0] + ":" + allele[1])

    frequencyAccumulator = 0.
    for allele in self.alleleCounts.keys():
      """For each entry in the dictionary of allele counts
      generate a corresponding entry in a dictionary of frequencies"""

      freq = self.alleleCounts[allele] / float(self.alleleTotal)
      frequencyAccumulator += freq
      self.alleleFrequencies[allele] = freq

    for genotype in self.observedGenotypes:
      """Generate a dictionary of genotype:count key:values

      - and accumulate totals for homozygotes and heterozygotes"""

      if self.observedGenotypeCounts.has_key(genotype):
        self.observedGenotypeCounts[genotype] += 1
      else:
        self.observedGenotypeCounts[genotype] = 1

      temp = string.split(genotype, ':')
      if temp[0] == temp[1]:
        self.totalHomsObs += 1
      else:
        self.totalHetsObs += 1

    if self.debug:
      print "Total homozygotes observed:", self.totalHomsObs
      print "Total heterozygotes observed:", self.totalHetsObs

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

      - Create a dictionary of genotype:frequency key:values

      - accumulate totals for homozygotes and heterozygotes

      - and build table of observed genotypes for each allele"""

      temp = string.split(genotype, ':')
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
            if self.hetsExpectedByAllele.has_key(allele):
              self.hetsExpectedByAllele[allele] += self.expectedGenotypeCounts[genotype]
            else:
              self.hetsExpectedByAllele[allele] = self.expectedGenotypeCounts[genotype]
          elif allele == temp[1]:
            if self.hetsExpectedByAllele.has_key(allele):
              self.hetsExpectedByAllele[allele] += self.expectedGenotypeCounts[genotype]
            else:
              self.hetsExpectedByAllele[allele] = self.expectedGenotypeCounts[genotype]

    total = 0
    for value in self.expectedGenotypeCounts.values():
      """Check that the sum of expected genotype counts approximates N"""

      total += value
    if abs(float(self.n) - total) > float(self.n) / 1000.0:
      print 'AAIIEE!'
      print 'Calculated sum of expected genotype counts is:', total, ', but N is:', self.n
      sys.exit()

################################################################################

  def _calcChisq(self):
    """First calculate the chi-squareds for the homozygotes
    and heterozygotes,

    - then calculate the chi-squareds for the common genotypes.

    - create a count of observed and expected lumped together
    for genotypes with an expected value of less than lumpBelow

    - Open a pipe to get the p-value from the system
    using the pval program (should be replaced later)"""

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
    self.flagTooManyParameters = 0
    self.flagTooFewExpected = 0
    self.flagNoCommonGenotypes = 0
    self.flagNoRareGenotypes = 0

    # first all the the homozygotes
    if self.totalHomsExp >= self.lumpBelow:
      squareMe = self.totalHomsObs - self.totalHomsExp
      self.totalChisqHoms = (squareMe * squareMe) / self.totalHomsExp

      command = "pval 1 %f" % (self.totalChisqHoms)
      returnedValue = os.popen(command, 'r').readlines()
      self.chisqHomsPval = float(returnedValue[0][:-1])
      self.flagHoms = 1

    # next all the heterozygotes
    if self.totalHetsExp >= self.lumpBelow:
      squareMe = self.totalHetsObs - self.totalHetsExp
      self.totalChisqHets = (squareMe * squareMe) / self.totalHetsExp

      command = "pval 1 %f" % (self.totalChisqHets)
      returnedValue = os.popen(command, 'r').readlines()
      self.chisqHetsPval = float(returnedValue[0][:-1])
      self.flagHets = 1

    # now the values for heterozygoous genotypes by allele
    for allele in self.observedAlleles:
      if self.hetsExpectedByAllele[allele] >= self.lumpBelow:
        if not self.hetsObservedByAllele.has_key(allele):
          self.hetsObservedByAllele[allele] = 0

        squareMe = self.hetsObservedByAllele[allele] - self.hetsExpectedByAllele[allele]
        self.hetsChisqByAllele[allele] = (squareMe * squareMe) / self.hetsExpectedByAllele[allele]

        command = "pval 1 %f" % (self.hetsChisqByAllele[allele])
        returnedValue = os.popen(command, 'r').readlines()
        self.hetsPvalByAllele[allele] = float(returnedValue[0][:-1])

        if self.debug:
          print 'By Allele:    obs exp   chi        p'
          print '          ', allele, self.hetsObservedByAllele[allele], self.hetsExpectedByAllele[allele], self.hetsChisqByAllele[allele], self.hetsPvalByAllele[allele]

    # the list for all genotypes by genotype
    for genotype in self.expectedGenotypeCounts.keys():
      if self.expectedGenotypeCounts[genotype] >= self.lumpBelow:
        if not self.observedGenotypeCounts.has_key(genotype):
          self.observedGenotypeCounts[genotype] = 0

        squareMe = self.observedGenotypeCounts[genotype] - self.expectedGenotypeCounts[genotype]

        self.chisqByGenotype[genotype] = (squareMe * squareMe) / self.expectedGenotypeCounts[genotype]
        command = "pval 1 %f" % (self.chisqByGenotype[genotype])
        returnedValue = os.popen(command, 'r').readlines()
        self.pvalByGenotype[genotype] = float(returnedValue[0][:-1])

        if self.debug:
          print 'By Genotype:  obs exp   chi        p'
          print '          ', genotype, self.observedGenotypeCounts[genotype], self.expectedGenotypeCounts[genotype], self.chisqByGenotype[genotype], self.pvalByGenotype[genotype]


    # and now the hard stuff
    for genotype in self.expectedGenotypeCounts.keys():
      if self.expectedGenotypeCounts[genotype] >= self.lumpBelow:

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

        squareMe = observedCount - self.expectedGenotypeCounts[genotype]
        self.chisq[genotype] = (squareMe * squareMe) / self.expectedGenotypeCounts[genotype]

        command = "pval 1 %f" % (self.chisq[genotype])
        returnedValue = os.popen(command, 'r').readlines()
        self.chisqPval[genotype] = float(returnedValue[0][:-1])
        self.commonChisqAccumulator += self.chisq[genotype]
        self.commonObservedAccumulator += observedCount
        self.commonExpectedAccumulator += self.expectedGenotypeCounts[genotype]

        if self.debug:
          print 'Chi Squared value:'
          print genotype, ':', self.chisq[genotype]
          # print "command %s returned %s" % (command, returnedValue)
          print 'P-value:'
          print genotype, ':', self.chisqPval[genotype]

      else:
        """Expected genotype count for this genotype is less than lumpBelow"""

        self.rareGenotypeCounter += 1

        self.lumpedExpectedGenotypes += self.expectedGenotypeCounts[genotype]

        if self.observedGenotypeCounts.has_key(genotype):
          self.lumpedObservedGenotypes += self.observedGenotypeCounts[genotype]

    if self.commonGenotypeCounter == 0:
    # no common genotypes, so do no calculations.

      self.flagNoCommonGenotypes = 1

    elif self.rareGenotypeCounter == 0:
    # no rare genotypes, so just do overall grand total

      self.HWChisq = self.commonChisqAccumulator

      self.HWChisqDf = (float(self.k) * (float(self.k - 1.0))) / 2.0
      command = "pval %d %f" % (self.HWChisqDf, self.commonChisqAccumulator)
      returnValue = os.popen(command, 'r').readlines()
      self.HWChisqPval = float(returnValue[0][:-1])

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
        print "self.commonGenotypeCounter - self.counterAllelesCommon = self.commonDf"
        print self.commonGenotypeCounter, "-", self.counterAllelesCommon, "=", self.commonDf

      if self.commonDf >= 1:
      # if the value for degrees of freedom is not zero or negative

        if self.lumpedExpectedGenotypes >= self.lumpBelow:
        # do chisq for the lumped genotypes

          squareMe = self.lumpedObservedGenotypes - self.lumpedExpectedGenotypes
          self.lumpedChisq = (squareMe * squareMe) / self.lumpedExpectedGenotypes

          command = "pval 1 %f" % (self.lumpedChisq)
          returnedValue = os.popen(command, 'r').readlines()
          self.lumpedChisqPval = float(returnedValue[0][:-1])
          self.flagLumps = 1

          if self.debug:
            print "Lumped %d for a total of %d observed and %f expected" % (self.rareGenotypeCounter, self.lumpedObservedGenotypes, self.lumpedExpectedGenotypes)
            print "Chisq: %f, P-Value (dof = 1): %s" % (self.lumpedChisq, self.lumpedChisqPval) # doesn't work if I claim Pval is a float?

        if self.flagLumps == 1:
          self.HWChisq = self.commonChisqAccumulator + self.lumpedChisq
          self.commonObservedAccumulator += self.lumpedObservedGenotypes
          self.commonExpectedAccumulator += self.lumpedExpectedGenotypes
        else:
          self.HWChisq = self.commonChisqAccumulator
          self.flagTooFewExpected = 1

        self.HWChisqDf = self.commonDf
        command = "pval %f %f" % (self.HWChisqDf, self.HWChisq)
        returnedValue = os.popen(command, 'r').readlines()
        self.HWChisqPval = float(returnedValue[0][:-1])
        self.flagCommons = 1

      else:
        self.flagTooManyParameters = 1

################################################################################

  def serializeTo(self, stream):
    type = getStreamType(stream)

    # stream serialization goes here

    stream.opentag('hardyweinberg')
    stream.tagContents("samplesize", "%d" % self.n)
    stream.writeln()
    # don't print out, already printed out in <allelecounts> tag in ParseFile
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
      if self.flagTooFewExpected == 1:
        stream.emptytag('lumped', role='too-few-expected')

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
      stream.tagContents("chisqdf", "%4f" % self.HWChisqDf)
      stream.writeln()
      stream.closetag('common')
      stream.writeln()
    else:
      if self.flagNoCommonGenotypes == 1:
        stream.emptytag('common', role='no-common-genotypes')
      elif self.flagTooManyParameters == 1:
        stream.emptytag('common', role='too-many-parameters')
      stream.writeln()

    stream.closetag('hardyweinberg')

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

        # start tag
        stream.opentag("genotype", row=horiz, col=vert)

        # need to check both permutations of key
        key1 = "%s:%s" % (horiz, vert)
        key2 = "%s:%s" % (vert, horiz)

        # get observed value
        if self.observedGenotypeCounts.has_key(key1):
          obs = self.observedGenotypeCounts[key1]
        elif self.observedGenotypeCounts.has_key(key2):
          obs = self.observedGenotypeCounts[key2]
        else:
          obs = 0

        # get expected value
        if self.expectedGenotypeCounts.has_key(key1):
          exp = self.expectedGenotypeCounts[key1]
        elif self.expectedGenotypeCounts.has_key(key2):
          exp = self.expectedGenotypeCounts[key2]
        else:
          exp = 0.0

        stream.writeln()
        stream.tagContents("observed", "%d" % obs)
        stream.writeln()
        stream.tagContents("expected", "%4f" % exp)
        stream.writeln()

        # get and tag chisq and pvalue (if they exist)
        if self.chisqByGenotype.has_key(key1):
          stream.tagContents("chisq", "%4f" % self.chisqByGenotype[key1])
          stream.writeln()
          stream.tagContents("pvalue", "%4f" % self.pvalByGenotype[key1])
          stream.writeln()
        elif self.chisqByGenotype.has_key(key2):
          stream.tagContents("chisq", "%4f" % self.chisqByGenotype[key2])
          stream.writeln()
          stream.tagContents("pvalue", "%4f" % self.pvalByGenotype[key2])
          stream.writeln()
        else:
          stream.emptytag("chisq", role='not-calculated')
          stream.emptytag("pvalue", role='not-calculated')
          
        stream.closetag("genotype")
        stream.writeln()

    stream.closetag("genotypetable")
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

  - 'maxMatrixSize': maximum size of `flattened' lower-triangular matrix of
     observed alleles (default 250).
  """

  def __init__(self, locusData, alleleCount,
               dememorizationSteps=2000,
               samplingNum=1000,
               samplingSize=1000,
               maxMatrixSize=250,
               **kw):

    self.dememorizationSteps=dememorizationSteps
    self.samplingNum=samplingNum
    self.samplingSize=samplingSize
    self.maxMatrixSize=maxMatrixSize
    
    # call constructor of base class
    HardyWeinberg.__init__(self, locusData, alleleCount, **kw)

               
  def dumpTable(self, locusName, stream):

    if locusName[0] == '*':
      locusName = locusName[1:]

    if self.k < 3:
      stream.emptytag('hardyweinbergGuoThompson', role='too-few-alleles')
      return

    matrixElemCount = (self.k * (self.k + 1)) / 2

    if matrixElemCount < self.maxMatrixSize:
      n = len(self.observedAlleles)

      sortedAlleles = self.observedAlleles
      sortedAlleles.sort()

      if 0:
        hwFilename = locusName + '.hw'
        
        hwStream = TextOutputStream(open(hwFilename, 'w'))

        # generate .hw file
        hwStream.writeln(locusName)
        hwStream.writeln("%d" % n)

      # allele list
      flattenedMatrix = []
    
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
            output = "%2s " % self.observedGenotypeCounts[key1]
          elif self.observedGenotypeCounts.has_key(key2):
            output = "%2s " % self.observedGenotypeCounts[key2]
          else:
            output = "%2s " % "0"

          if 0:
            hwStream.write(output)
          flattenedMatrix.append(int(output))
        if 0:
          hwStream.writeln()

      if 0:
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
        os.remove(xmlFilename)

      # create dummy array
      n = [0]*35
      
      if self.debug:
        print flattenedMatrix
        print n
        print self.k
        print matrixElemCount
        print self.dememorizationSteps, self.samplingNum, self.samplingSize
        print locusName

      # create string "file" buffer
      import cStringIO
      fp = cStringIO.StringIO()

      # import library only when necessary
      import _Gthwe

      _Gthwe.run_data(flattenedMatrix, n, self.k, matrixElemCount,
                      self.dememorizationSteps, self.samplingNum,
                      self.samplingSize, locusName, fp)

      # copy XML output to stream
      stream.write(fp.getvalue())
      fp.close()

    else:
      stream.emptytag('hardyweinbergGuoThompson', role='too-large-matrix')
      
    
