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

"""Computing homozygosity statistics on genotype or allele counts."""

import math
import os
import string
from functools import reduce
from operator import add
from pathlib import Path

# import C module
from PyPop import _EWSlatkinExact, logger
from PyPop.datatypes import Genotypes, checkIfSequenceData, getLocusPairs, getMetaLocus
from PyPop.utils import getStreamType


class Homozygosity:
    """Calculate homozygosity statistics.

    Given allele count data for a given locus, calculates the observed
    homozygosity and returns the approximate expected homozygosity
    statistics taken from previous simulation runs.

    Args:
       alleleData (list): list of allele counts
       rootPath (str): path to the root of the directory where the
         pre-calculated expected homozygosity statistics can be found.
    """

    def __init__(self, alleleData, rootPath="."):
        self.alleleData = alleleData
        self.numAlleles = len(self.alleleData)
        if self.numAlleles > 0:
            self.sampleCount = reduce(add, self.alleleData)
        else:
            self.sampleCount = 0

        self.rootPath = Path(rootPath)
        self.expectedStatsFlag = self._parseFile()

    def _genPathName(self, sampleCount, numAlleles):
        """Generate path name for homozygosity file.

        If 2n > 2000, use 2000 anyway.

        Args:
           sampleCount (int): number of samples
           numAlleles (int): number of alleles

        Returns:
           pathlib.Path: path to file
        """
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

        Only check whether sample size is too small If sample size is
        too large, we will use 2000 anyway.

        Args:
           sampleCount (int): number of samples

        Returns:
           int: ``0`` if less than 15, otherwise, ``1``
        """
        if sampleCount <= 15:
            return 0
        return 1

    def _checkAlleleRange(self, numAlleles):
        """Check range of number of alleles is valid.

        Args:
           numAlleles (int): number of samples

        Returns:
           int: ``0`` if out of range, otherwise, ``1``
        """
        if (numAlleles <= 1) or (numAlleles >= 101):
            return 0
        return 1

    def _parseFile(self):
        """Parses the homozygosity file.

        Checks range and existence (well it will eventually) of
        homozygosity data file for given allele count and total allele
        count.

        Returns:
           int: ``1`` if in range, ``0`` if out of range
        """
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

                        logger.debug(
                            "%d %g %g",
                            self.count,
                            self.expectedHomozygosity,
                            self.varExpectedHomozygosity,
                        )
                        logger.debug("%d %d", self.sampleCount, self.numAlleles)

                        return 1

                    logger.debug("%d %d", self.sampleCount, self.numAlleles)
                    logger.debug(
                        "%d %g %g",
                        self.count,
                        self.expectedHomozygosity,
                        self.varExpectedHomozygosity,
                    )
                    logger.warning(
                        "Insufficient (%d) replicates observed for a valid analysis.",
                        self.count,
                    )
            logger.debug("%d is out of range of valid k!", self.numAlleles)
        logger.debug("%d is out of range of valid 2n!", self.sampleCount)

        return 0

    def getObservedHomozygosity(self):
        """Calculate and return observed homozygosity.

        Available even if expected stats cannot be calculated.

        Returns:
          float: observed homozygosity
        """
        sum = 0.0

        # cache floating point value
        sampleCount = float(self.sampleCount)
        self.observedHomozygosity = 0.0

        for alleleCount in self.alleleData:
            freq = float(alleleCount / sampleCount)
            logger.debug("allelecount = %d freq = %g", alleleCount, freq)
            sum += freq * freq

            self.observedHomozygosity = sum

        return self.observedHomozygosity

    def canGenerateExpectedStats(self):
        """Can expected homozygosity stats be calculated?

        Returns ``1`` if expected homozygosity statistics can be
        calculated.  Should be called before attempting to get any
        expected homozygosity statistics.

        Returns:
           int: ``1`` if can be calculated, otherwise ``0``
        """
        return self.expectedStatsFlag

    def getPValueRange(self):
        """Gets lower and upper bounds for p-value.

        Only meaningful if :meth:`canGenerateExpectedStats` returns true.

        Returns:
          tuple:  (``lower``, ``upper``) bounds.
        """
        upperBound = 999.0
        logger.debug("quartiles")
        logger.debug("homozyg  calcpVal pVal ")
        for val in self.quantile:
            obsvHomo, pVal = val
            logger.debug(f"{obsvHomo:08f} {pVal:08f}")
            if self.observedHomozygosity > obsvHomo:
                lowerBound = pVal
                return lowerBound, upperBound
            upperBound = pVal

        # if out of range (i.e. off the bottom of the scale)
        # return a zero as the lower bound
        return 0.0, upperBound

    def getCount(self):
        """Number of runs used to calculate statistics.

        Only meaningful if :meth:`canGenerateExpectedStats` returns ``1``.

        Returns:
          int: number of runs
        """
        return self.count

    def getExpectedHomozygosity(self):
        """Gets mean of expected homozygosity.

        This is the estimate of the *expected* homozygosity.  Only
        meaningful if :meth:`canGenerateExpectedStats` returns true.

        Returns:
           float: mean of expected homozygosity
        """
        return self.expectedHomozygosity

    def getVarExpectedHomozygosity(self):
        """Gets variance of expected homozygosity.

        This is the estimate of the variance *expected* homozygosity.
        Only meaningful if :meth:`canGenerateExpectedStats` returns true.

        Returns:
           float: variance of expected homozygosity
        """
        return self.varExpectedHomozygosity

    def getNormDevHomozygosity(self):
        """Gets normalized deviate of homozygosity.

        Only meaningful if :meth:`canGenerateExpectedStats` returns true.

        Returns:
           float: normalized deviate of homozygosity
        """
        sqrtVar = math.sqrt(self.getVarExpectedHomozygosity())
        self.normDevHomozygosity = (
            self.getObservedHomozygosity() - self.getExpectedHomozygosity()
        ) / sqrtVar
        return self.normDevHomozygosity

    def serializeHomozygosityTo(self, stream):
        """Serialize homozygosity to a stream.

        Args:
           stream (XMLOutputStream): stream to save to
        """
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
    """Compute homozygosity using the Ewens-Watterson-Slatkin "exact test".

    Args:
       alleleData (list): list of allele counts
       numReplicates (int): number or replicates for simulation.
    """

    def __init__(self, alleleData=None, numReplicates=10000):
        self.alleleData = alleleData
        self.numReplicates = numReplicates

    def doCalcs(self, alleleData):
        """Run the computations.

        Args:
           alleleData (list): list of allele counts
        """
        self.alleleData = alleleData
        self.numAlleles = len(self.alleleData)
        if self.numAlleles > 0:
            self.sampleCount = reduce(add, self.alleleData)
        else:
            self.sampleCount = 0

        if self.sampleCount > 0:
            self.EW = _EWSlatkinExact

            # create the correct array that module expect,
            # by pre- and appending zeroes to the list
            logger.debug("%s", list(self.alleleData))
            logger.debug("%s", type(self.alleleData))

            li = [0, *list(self.alleleData), 0]

            logger.debug(
                "args to slatkin exact test: %s %d %d %d",
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
        """Get the homozygosity statistics.

        Returns:
           tuple: tuple consisting of:
             - theta
             - prob_ewens
             - prob_homozygosity
             - mean_homozygosity
             - obsv_homozygosity
             - var_homozygosity
        """
        return (
            self.theta,
            self.prob_ewens,
            self.prob_homozygosity,
            self.mean_homozygosity,
            self.obsv_homozygosity,
            self.var_homozygosity,
        )

    def serializeHomozygosityTo(self, stream):
        """Serialize homozygosity to a stream.

        Args:
           stream (XMLOutputStream): stream to save to
        """
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
        """Get bulk homozygosity statistics for multiple allele counts.

        This function is designed to work with the
        :mod:`PyPop.RandomBinning` submodule.

        Args:
           alleleCountDict (dict): dictionary of lists of allele counts
           binningMethod (str): record the binning method used

        Returns:
           dict: dictionary of statistics

        """
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
    """Compute pairwise homozygosity using the Ewens-Watterson-Slatkin.

    Args:
       matrix (StringMatrix): matrix with multiple loci columns for pairwise comparison
       numReplicates (int, optional): number or replicates for simulation.
       untypedAllele (str, optional): untyped allele
    """

    def __init__(self, matrix=None, numReplicates=10000, untypedAllele="****"):
        self.matrix = matrix
        self.numReplicates = numReplicates
        self.untypedAllele = untypedAllele
        self.sequenceData = checkIfSequenceData(self.matrix)
        self.pairs = getLocusPairs(self.matrix, self.sequenceData)

    def serializeTo(self, stream):
        """Serialize to a stream.

        Args:
           stream (XMLOutputStream): stream to save to
        """
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
                countData.values(),
                numReplicates=self.numReplicates,
            )

            hz.serializeHomozygosityTo(stream)
            stream.closetag("group")
            stream.writeln()

        stream.closetag("homozygosityEWSlatkinExactPairwise")
        stream.writeln()


def getObservedHomozygosityFromAlleleData(alleleData):
    """Get homozygosity from allele data.

    Args:
       alleleData (list): list of allele counts

    Returns:
       float: observed homozygosity
    """
    sum = 0.0
    sampleCount = reduce(add, alleleData)
    for alleleCount in alleleData:
        freq = float(alleleCount) / float(sampleCount)
        sum += freq * freq

    return sum
