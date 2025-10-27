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

"""Generating randomized sets allele counts for statistical analyses."""

from copy import copy
from random import randrange

from PyPop import logger
from PyPop.homozygosity import (
    HomozygosityEWSlatkinExact,
)


class RandomBinsForHomozygosity:
    """Generate randomized sets of bins for homozygosity analysis.

    Args:
        logFile (str): output log file
        untypedAllele (str, optional): untyped allele (default ``****``)
        filename (str): input filename
        numReplicates (int, optional): replicates (default ``10000``)
        binningReplicates (int, optional): replicates for binning (default ``100``)
        locus (str): locus name
        xmlfile (XMLOutputStream, optional): output stream
        randomResultsFileName (str): output file for the randomized results
    """

    def __init__(
        self,
        logFile=None,
        untypedAllele="****",
        filename=None,
        numReplicates=10000,
        binningReplicates=100,
        locus=None,
        xmlfile=None,
        randomResultsFileName=None,
    ):
        self.untypedAllele = untypedAllele
        self.binningReplicates = binningReplicates
        self.numReplicates = numReplicates
        self.locus = locus
        self.filename = filename.split(".")[-2]
        self.filename = self.filename.split("/")[-1]
        self.xmlStream = xmlfile
        self.logFile = logFile
        self.alleleCountDict = {}
        # FIXME: don't require context manager, skip run SIM115
        self.randomResultsFile = open(randomResultsFileName, "w")  # noqa: SIM115
        self.randomResultsFile.write(
            "\t".join(
                [
                    "filename",
                    "locus",
                    "method",
                    "theta",
                    "prob_ewens",
                    "prob_homozygosity",
                    "mean_homozygosity",
                    "obsv_homozygosity",
                    "var_homozygosity",
                    "normDevHomozygosity",
                ]
            )
            + "\n"
        )

    def _dumpResults(
        self,
        alleleCountsBefore=None,
        alleleCountsAfter=None,
    ):
        """Dump results to file.

        Args:
           alleleCountsBefore (list): allele counts before binning
           alleleCountsAfter (list): allele counts after binning
        """
        # append the before and after allele counts to the dictionary
        # so we can look up all of the stats en masse
        self.alleleCountDict[tuple(alleleCountsBefore)] = "before"
        self.alleleCountDict[tuple(alleleCountsAfter)] = "after"

        logger.debug("alleleCountsBefore %s", alleleCountsBefore)
        logger.debug("alleleCountsAfter %s", alleleCountsAfter)
        logger.debug("alleleCountDict %s", self.alleleCountDict)

        hzExactObj = HomozygosityEWSlatkinExact(
            numReplicates=self.numReplicates,
        )
        stats = hzExactObj.returnBulkHomozygosityStats(
            self.alleleCountDict, binningMethod=self.binningMethod
        )

        for s in stats:
            for _m in range(stats[s]):
                s_mapped = list(map(str, s))
                self.randomResultsFile.write(
                    "\t".join([self.filename, self.locus, *s_mapped]) + "\n"
                )

        self.randomResultsFile.close()

    def _updateCountDict(self, alleleCounts=None):
        """Update counts.

        Args:
           alleleCounts (list): allele count list
        """
        alleleCounts.sort()
        alleleCounts = tuple(alleleCounts)

        logger.debug(alleleCounts)

        if alleleCounts in self.alleleCountDict:
            self.alleleCountDict[alleleCounts] += 1
        else:
            self.alleleCountDict[alleleCounts] = 1

    def randomMethod(self, alleleCountsBefore=None, alleleCountsAfter=None):
        """Do binning replicates with random-based method.

        Args:
           alleleCountsBefore (list): allele counts before binning
           alleleCountsAfter (list): allele counts after binning

        """
        self.binningMethod = "random"

        # we don't need the dictionary in this case, just the counts
        alleleCountsBefore = alleleCountsBefore.values()
        alleleCountsAfter = alleleCountsAfter.values()

        for _i in range(self.binningReplicates):
            alleleCountsRand = copy(list(alleleCountsBefore))

            while len(alleleCountsRand) > len(alleleCountsAfter):
                bin1 = randrange(0, len(alleleCountsRand), 1)
                bin2 = randrange(0, len(alleleCountsRand), 1)

                if bin1 != bin2:
                    alleleCountsRand[bin1] += alleleCountsRand[bin2]
                    del alleleCountsRand[bin2]

            self._updateCountDict(alleleCountsRand)

        self._dumpResults(alleleCountsBefore, alleleCountsAfter)

    def sequenceMethod(
        self,
        alleleCountsBefore=None,
        alleleCountsAfter=None,
        polyseq=None,
        polyseqpos=None,
    ):
        """Do binning replicates with sequence-based method.

        Args:
           alleleCountsBefore (list): allele counts before binning
           alleleCountsAfter (list): allele counts after binning
           polyseq (dict): Keyed on ``locus*allele`` of all allele
            sequences, containing **ONLY** the polymorphic positions.
           polyseqpos (dict): Keyed on ``locus`` of the positions of
            the polymorphic residues which you find in ``polyseq``.
        """
        self.binningMethod = "sequence"

        binningAttempts = 0
        binningAttemptsSuccessful = 0
        polyseqpos = polyseqpos[self.locus]

        deleteHistory = {}
        deleteHistoryAll = {}
        collapseHistory = {}
        weightedCollapseHistory = {}
        for pos in polyseqpos:
            deleteHistory[pos] = 0
            deleteHistoryAll[pos] = 0
            collapseHistory[pos] = 0
            weightedCollapseHistory[pos] = 0

        while binningAttemptsSuccessful < self.binningReplicates:
            alleleCountsRand = {}
            for allele in alleleCountsBefore:
                alleleCountsRand[self.locus + "*" + allele] = alleleCountsBefore[allele]

            polyseqSliced = copy(polyseq)
            polyseqposDeletes = copy(polyseqpos)
            deleteHistorySaved = copy(deleteHistory)
            collapseHistorySaved = copy(collapseHistory)
            weightedCollapseHistorySaved = copy(weightedCollapseHistory)

            try:
                del polyseqSliced[self.locus + "*" + self.untypedAllele]
            except Exception:
                logger.debug("no untyped allele in polyseq")

            while len(alleleCountsRand) > len(alleleCountsAfter):
                seqLength = len(polyseqSliced.values()[0])
                posToDelete = randrange(0, seqLength, 1)
                absolutePosToDelete = polyseqposDeletes[posToDelete]
                deleteHistory[absolutePosToDelete] += 1
                deleteHistoryAll[absolutePosToDelete] += 1
                allelesToBin = []

                logger.debug("polyseq %s", polyseqSliced)
                logger.debug("posToDelete %s", posToDelete)
                logger.debug("length of polyseq before %s", seqLength)
                logger.debug("alleles before binning %s", alleleCountsRand)

                # deletes the selected character from each sequence
                for allele in polyseqSliced:
                    polyseqSliced[allele] = (
                        polyseqSliced[allele][:posToDelete]
                        + polyseqSliced[allele][posToDelete + 1 :]
                    )
                del polyseqposDeletes[posToDelete]

                # go thru again to check to see what we have collapsed
                for allele in polyseqSliced:
                    for allele2 in polyseqSliced:
                        if (
                            polyseqSliced[allele] == polyseqSliced[allele2]
                            and allele != allele2
                        ):
                            if allele not in allelesToBin:
                                allelesToBin.append(allele)
                            if allele2 not in allelesToBin:
                                allelesToBin.append(allele2)

                # go thru again and tally up the allele counts from
                # the collapse-ees into the collapse-er (which is the
                # first one, arbitrarily)
                for allele in allelesToBin[1:]:
                    alleleCountsRand[allelesToBin[0]] += alleleCountsRand[allele]

                # to thru again and tally up the statistics
                for allele in allelesToBin:
                    collapseHistory[absolutePosToDelete] += 1
                    weightedCollapseHistory[absolutePosToDelete] += alleleCountsRand[
                        allele
                    ]

                # go thru one more time to delete the collapse-ees
                for allele in allelesToBin[1:]:
                    del alleleCountsRand[allele]
                    del polyseqSliced[allele]

                logger.debug(
                    "length of polyseq after %d", len(polyseqSliced.values()[0])
                )
                logger.debug("allelesToBin %s", allelesToBin)
                logger.debug("alleles after binning %s", alleleCountsRand)
                logger.debug("--------------------")

            binningAttempts += 1

            if len(alleleCountsRand) == len(alleleCountsAfter):
                binningAttemptsSuccessful += 1
                self._updateCountDict(alleleCountsRand.values())

            elif len(alleleCountsRand) < len(alleleCountsAfter):
                logger.debug(
                    "=======================OVERSHOT TARGET!=================="
                )
                # restore counters to pre-overshoot counts
                deleteHistory = copy(deleteHistorySaved)
                collapseHistory = copy(collapseHistorySaved)
                weightedCollapseHistory = copy(weightedCollapseHistorySaved)

            if binningAttempts > (self.binningReplicates * 100):
                print(
                    f"FilterLog: Locus {self.locus}: While attempting {self.binningReplicates} replicates of sequence-based random binning, overshot target too many times; exiting binning with only {binningAttemptsSuccessful} successful replicates."
                )
                self.logFile.writeln(
                    f"Locus {self.locus}: While attempting {self.binningReplicates} replicates of sequence-based random binning, overshot target too many times; exiting binning with only {binningAttemptsSuccessful} successful replicates."
                )
                break

        self._dumpResults(alleleCountsBefore.values(), alleleCountsAfter.values())

        # THIS GOES IN FILTER LOG FILE
        self.logFile.writeln(
            f"Tried {binningAttempts} times to get {binningAttemptsSuccessful} random binnings."
        )
        self.logFile.writeln(
            "locus\tposition\ttimesDeleted\ttimesDeletedAll\tcollapses\tcollapsesWeighted"
        )
        for pos in polyseqpos:
            self.logFile.writeln(
                "\t".join(
                    [
                        self.locus,
                        str(pos),
                        str(deleteHistory[pos] / float(binningAttemptsSuccessful)),
                        str(deleteHistoryAll[pos] / float(binningAttemptsSuccessful)),
                        str(collapseHistory[pos] / float(binningAttemptsSuccessful)),
                        str(
                            weightedCollapseHistory[pos]
                            / float(binningAttemptsSuccessful)
                        ),
                    ]
                )
            )
