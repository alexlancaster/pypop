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

"""Module for calculating homozygosity statistics."""

import math
import os
import string
from functools import reduce
from operator import add
from pathlib import Path

from PyPop.DataTypes import Genotypes, checkIfSequenceData, getLocusPairs, getMetaLocus
from PyPop.Utils import getStreamType


def getObservedHomozygosityFromAlleleData(alleleData):
    sum = 0.0
    sampleCount = reduce(add, alleleData)
    for alleleCount in alleleData:
        freq = float(alleleCount) / float(sampleCount)
        sum += freq * freq

    return sum


class Homozygosity:
    """Calculate homozygosity statistics.

    Given allele count data for a given locus, calculates the observed
    homozygosity and returns the approximate expected homozygosity
    statistics taken from previous simulation runs.
    """

    def __init__(self, alleleData, rootPath=".", debug=0):
        """Constructor for homozygosity statistics.

        Given:

        - 'alleleCountData': tuple consisting of a dictionary of alleles
          with their associated counts and the total number of alleles.

        - 'rootPath': path to the root of the directory where the
          pre-calculated expected homozygosity statistics can be found.

        - 'debug': flag to switch debugging on."""

        self.alleleData = alleleData
        self.numAlleles = len(self.alleleData)
        if self.numAlleles > 0:
            self.sampleCount = reduce(add, self.alleleData)
        else:
            self.sampleCount = 0

        self.rootPath = Path(rootPath)
        self.debug = debug

        self.expectedStatsFlag = self._parseFile()

    def _genPathName(self, sampleCount, numAlleles):
        """Generate path name for homozygosity file.

        If 2n > 2000, use 2000 anyway.

        *Internal use only*"""

        decade, rem = divmod(sampleCount, 10)
        if rem >= 5:
            decade = decade + 1

        twoEn = decade * 10

        # hack because we only have simulated data for 2n <= 2000
        twoEn = min(twoEn, 2000)

        dir = f"2n{twoEn}"
        file = f"{numAlleles}_{twoEn}.out"
        return Path(dir) / file

    def _checkCountRange(self, sampleCount):
        """Check range of total allele count is valid.

        Only check whether sample size is too small

        If sample size is too large, we will use 2000 anyway.

        Returns a boolean.

        *Internal use only"""
        if sampleCount <= 15:
            return 0
        return 1

    def _checkAlleleRange(self, numAlleles):
        """Check range of number of alleles is valid.

        Returns a boolean.

        *Internal use only"""
        if (numAlleles <= 1) or (numAlleles >= 101):
            return 0
        return 1

    def _parseFile(self):
        """Parses the homozygosity file.

        Checks range and existence (well it will eventually) of
        homozygosity data file for given allele count and total allele
        count.

        Returns a boolean.

        *Internal use only*"""

        if self._checkCountRange(self.sampleCount):
            if self._checkAlleleRange(self.numAlleles):
                # generate relative path name
                path = self._genPathName(self.sampleCount, self.numAlleles)

                # open file with full path name created in-line
                with open(self.rootPath / path) as fp:
                    lines = fp.readlines()

                    self.count = int(lines[0].split(":")[1])
                    self.expectedHomozygosity = float(lines[1].split(":")[1])
                    self.varExpectedHomozygosity = float(lines[2].split(":")[1])

                    if self.count > 1999:
                        self.quantile = []
                        # read until we've reached the end of lines or a blank line
                        for i in range(4, len(lines)):
                            # stop reading quantiles if blank encountered
                            if lines[i] == os.linesep:
                                break
                            obsvHomo, pValue = [float(val) for val in lines[i].split()]
                            self.quantile.append((obsvHomo, pValue))

                        if self.debug:
                            print(
                                self.count,
                                self.expectedHomozygosity,
                                self.varExpectedHomozygosity,
                            )
                            print(self.sampleCount, self.numAlleles)

                        return 1

                    if self.debug:
                        print(self.sampleCount, self.numAlleles)
                        print(
                            self.count,
                            self.expectedHomozygosity,
                            self.varExpectedHomozygosity,
                        )
                        print(
                            "Insufficient (",
                            self.count,
                            ") replicates observed for a valid analysis.",
                        )
            elif self.debug:
                print(self.numAlleles, " is out of range of valid k!")
        elif self.debug:
            print(self.sampleCount, " is out of range of valid 2n!")

        return 0

    def getObservedHomozygosity(self):
        """Calculate and return observed homozygosity.

        Available even if expected stats cannot be calculated"""

        sum = 0.0

        # cache floating point value
        sampleCount = float(self.sampleCount)
        self.observedHomozygosity = 0.0

        for alleleCount in self.alleleData:
            freq = float(alleleCount / sampleCount)
            if self.debug:
                print("allelecount = ", alleleCount, " freq = ", freq)
            sum += freq * freq

            self.observedHomozygosity = sum

        return self.observedHomozygosity

    def canGenerateExpectedStats(self):
        """Can expected homozygosity stats be calculated?

        Returns true if expected homozygosity statistics can be
        calculated.  Should be called before attempting to get any
        expected homozygosity statistics."""

        return self.expectedStatsFlag

    def getPValueRange(self):
        """Gets lower and upper bounds for p-value.

        Returns a tuple of (lower, upper) bounds.

        Only meaningful if 'canGenerateExpectedStats()' returns true."""

        upperBound = 999.0
        if self.debug:
            print("quartiles")
            print("homozyg  calcpVal pVal ")
        for val in self.quantile:
            obsvHomo, pVal = val
            if self.debug:
                print(f"{obsvHomo:08f} {pVal:08f}")
            if self.observedHomozygosity > obsvHomo:
                lowerBound = pVal
                return lowerBound, upperBound
            upperBound = pVal

        # if out of range (i.e. off the bottom of the scale)
        # return a zero as the lower bound
        return 0.0, upperBound

    def getCount(self):
        """Number of runs used to calculate statistics.

        Only meaningful if 'canGenerateExpectedStats()' returns true."""
        return self.count

    def getExpectedHomozygosity(self):
        """Gets mean of expected homozygosity.

        This is the estimate of the *expected* homozygosity.

        Only meaningful if 'canGenerateExpectedStats()' returns true."""
        return self.expectedHomozygosity

    def getVarExpectedHomozygosity(self):
        """Gets variance of expected homozygosity.

        This is the estimate of the variance *expected* homozygosity.

        Only meaningful if 'canGenerateExpectedStats()' returns true."""
        return self.varExpectedHomozygosity

    def getNormDevHomozygosity(self):
        """Gets normalized deviate of homozygosity.

        Only meaningful if 'canGenerateExpectedStats()' returns true."""

        sqrtVar = math.sqrt(self.getVarExpectedHomozygosity())
        self.normDevHomozygosity = (
            self.getObservedHomozygosity() - self.getExpectedHomozygosity()
        ) / sqrtVar
        return self.normDevHomozygosity

    def serializeHomozygosityTo(self, stream):
        getStreamType(stream)

        if self.expectedStatsFlag:
            stream.opentag("homozygosity")
            stream.writeln()
            stream.tagContents("observed", f"{self.getObservedHomozygosity():.4f}")
            stream.writeln()
            stream.tagContents("expected", f"{self.getExpectedHomozygosity():.4f}")
            stream.writeln()
            stream.tagContents("normdev", f"{self.getNormDevHomozygosity():.4f}")
            stream.writeln()

            # stream.tagContents('expectedVariance', "%.4f" % self.getVarExpectedHomozygosity())
            # stream.writeln()
            # stream.tagContents('expectedStdErr', "%.4f" % self.getSemExpectedHomozygosity())
            # stream.writeln()
            stream.opentag("pvalue")
            lb, up = self.getPValueRange()
            stream.tagContents("lower", f"{lb:.4f}")
            stream.tagContents("upper", f"{up:.4f}")
            stream.closetag("pvalue")
            stream.writeln()
            stream.closetag("homozygosity")
        elif self.sampleCount == 0:
            stream.emptytag("homozygosity", role="no-data")
        else:
            stream.opentag("homozygosity", role="out-of-range")
            stream.writeln()
            stream.tagContents("observed", f"{self.getObservedHomozygosity():.4f}")
            stream.writeln()
            stream.closetag("homozygosity")

        # always end on a newline
        stream.writeln()


class HomozygosityEWSlatkinExact(Homozygosity):
    def __init__(self, alleleData=None, numReplicates=10000, debug=0):
        self.alleleData = alleleData

        self.numReplicates = numReplicates
        self.debug = debug

    def doCalcs(self, alleleData):
        self.alleleData = alleleData
        self.numAlleles = len(self.alleleData)
        if self.numAlleles > 0:
            self.sampleCount = reduce(add, self.alleleData)
        else:
            self.sampleCount = 0

        if self.sampleCount > 0:
            from PyPop import _EWSlatkinExact

            self.EW = _EWSlatkinExact

            # create the correct array that module expect,
            # by pre- and appending zeroes to the list
            if self.debug:
                print(list(self.alleleData))
                print(type(self.alleleData))

            li = [0, *list(self.alleleData), 0]

            if self.debug:
                print(
                    "args to slatkin exact test:",
                    li,
                    self.numAlleles,
                    self.sampleCount,
                    self.numReplicates,
                )

            self.EW.main_proc(li, self.numAlleles, self.sampleCount, self.numReplicates)

            self.theta = self.EW.get_theta()
            self.prob_ewens = self.EW.get_prob_ewens()
            self.prob_homozygosity = self.EW.get_prob_homozygosity()
            self.mean_homozygosity = self.EW.get_mean_homozygosity()
            self.obsv_homozygosity = self.getObservedHomozygosity()
            self.var_homozygosity = self.EW.get_var_homozygosity()

    def getHomozygosity(self):
        return (
            self.theta,
            self.prob_ewens,
            self.prob_homozygosity,
            self.mean_homozygosity,
            self.obsv_homozygosity,
            self.var_homozygosity,
        )

    def serializeHomozygosityTo(self, stream):
        self.doCalcs(self.alleleData)

        if self.getObservedHomozygosity() >= 1.0:
            stream.emptytag("homozygosityEWSlatkinExact", role="monomorphic")
        elif self.sampleCount > 0:
            stream.opentag("homozygosityEWSlatkinExact")
            stream.writeln()

            stream.tagContents("theta", f"{self.theta:.4f}")
            stream.writeln()

            stream.tagContents("probEwens", f"{self.prob_ewens:.4f}")
            stream.writeln()

            stream.tagContents("probHomozygosity", f"{self.prob_homozygosity:.4f}")
            stream.writeln()

            stream.tagContents("meanHomozygosity", f"{self.mean_homozygosity:.4f}")
            stream.writeln()

            stream.tagContents("observedHomozygosity", f"{self.obsv_homozygosity:.4f}")
            stream.writeln()

            stream.tagContents("varHomozygosity", f"{self.var_homozygosity:.4f}")
            stream.writeln()

            # calculate normalized deviate of homozygosity (F_nd)
            sqrtVar = math.sqrt(math.fabs(self.EW.get_var_homozygosity()))

            try:
                normDevHomozygosity = (
                    self.getObservedHomozygosity() - self.EW.get_mean_homozygosity()
                ) / sqrtVar
                normDevStr = f"{normDevHomozygosity:.4f}"
            except Exception:
                normDevStr = "****"
            stream.tagContents("normDevHomozygosity", normDevStr)

            stream.writeln()

            stream.closetag("homozygosityEWSlatkinExact")

        else:
            stream.emptytag("homozygosityEWSlatkinExact", role="no-data")

        # always end on a newline
        stream.writeln()

    def returnBulkHomozygosityStats(self, alleleCountDict=None, binningMethod=None):
        # this function is written to work with the RandomBinning module

        resultsDict = {}

        for i in alleleCountDict:
            if alleleCountDict[i] == "before" or alleleCountDict[i] == "after":
                resultType = alleleCountDict[i]
                multiplier = 1
            else:
                resultType = binningMethod
                multiplier = alleleCountDict[i]

            self.alleleData = list(i)
            self.doCalcs(self.alleleData)
            # calculate normalized deviate of homozygosity (F_nd)
            sqrtVar = math.sqrt(math.fabs(self.EW.get_var_homozygosity()))
            normDevHomozygosity = (
                self.getObservedHomozygosity() - self.EW.get_mean_homozygosity()
            ) / sqrtVar

            # package the results
            resultsDict[
                (
                    resultType,
                    self.theta,
                    self.prob_ewens,
                    self.prob_homozygosity,
                    self.mean_homozygosity,
                    self.obsv_homozygosity,
                    self.var_homozygosity,
                    normDevHomozygosity,
                )
            ] = multiplier

        return resultsDict


class HomozygosityEWSlatkinExactPairwise:
    def __init__(self, matrix=None, numReplicates=10000, untypedAllele="****", debug=0):
        self.matrix = matrix
        self.numReplicates = numReplicates
        self.debug = debug
        self.untypedAllele = untypedAllele
        self.sequenceData = checkIfSequenceData(self.matrix)
        self.pairs = getLocusPairs(self.matrix, self.sequenceData)

    def serializeTo(self, stream):
        stream.opentag("homozygosityEWSlatkinExactPairwise")
        stream.writeln()

        for pair in self.pairs:
            metaLocus = getMetaLocus(pair, self.sequenceData)

            stream.opentag("group", locus=pair, metalocus=metaLocus)
            stream.writeln()
            subMat = self.matrix.getSuperType(pair)
            ##print(subMat
            ##print(subMat.colList

            # StringMatrix can't use a colon (":") as part of an allele
            # identifier, so replace them with dash ("-")
            colName = string.replace(pair, ":", "-")

            # generate allele frequency counts via Genotypes class
            g = Genotypes(matrix=subMat, untypedAllele=self.untypedAllele)

            # get allele count data
            countData = g.getAlleleCountAt(colName)[0]

            # only pass in count frequencies
            hz = HomozygosityEWSlatkinExact(
                countData.values(), numReplicates=self.numReplicates, debug=self.debug
            )

            hz.serializeHomozygosityTo(stream)
            stream.closetag("group")
            stream.writeln()

        stream.closetag("homozygosityEWSlatkinExactPairwise")
        stream.writeln()
