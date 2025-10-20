# This file is part of PyPop

# Copyright (C) 2003-2006.
# The Regents of the University of California (Regents). All Rights Reserved.

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

"""Data structures storing genotype and allele count data."""

import re
import string

from PyPop import logger


class Genotypes:
    """Stores genotypes and caches basic genotype statistics.

    Args:
        matrix (StringMatrix): The ``StringMatrix`` to be converted into a ``Genotype`` instance
        untypedAllele (str): The placeholder for an untyped allele site
        unsequencedSite (bool): The identifier used for an unsequenced site (only used for sequence data)
        allowSemiTyped (int): Whether or not to allow individuals that are typed at only one allele
    """

    def __init__(
        self,
        matrix=None,
        untypedAllele="****",
        unsequencedSite=None,
        allowSemiTyped=0,
    ):
        self.matrix = matrix
        self.untypedAllele = untypedAllele
        self.unsequencedSite = unsequencedSite
        self.allowSemiTyped = allowSemiTyped

        self._genDataStructures()

    def _checkAllele(self, allele1, allele2, unsequencedSites):
        """Check alleles and update counts.

        Args:
           allele1 (str): allele 1
           allele2 (str): allele 2
           unsequencedSites (str): the value representing unsequenced sites
        """
        for phase in [allele1, allele2]:
            if phase not in {self.untypedAllele, self.unsequencedSite}:
                logger.debug("alleleTable: %s", self.alleleTable)
                logger.debug("alleleTable type: %s", type(self.alleleTable))
                logger.debug("phase: %s", phase)
                logger.debug("phase type: %s", type(phase))
                if phase in self.alleleTable:
                    self.alleleTable[phase] += 1
                else:
                    self.alleleTable[phase] = 1
                self.total += 1
            else:
                if self.unsequencedSite == phase:
                    unsequencedSites += 1
                logger.debug(self.unsequencedSite, phase, unsequencedSites)

    def _genDataStructures(self):
        """Generates allele count and map data structures.

        *For internal use only.*
        """
        self.locusKeys = self.matrix.colList

        # then total number of individuals in data file
        self.totalIndivCount = len(self.matrix)

        # total number of loci contained in original file
        self.totalLocusCount = len(self.locusKeys)

        # total loci that contain usable data
        self.totalLociWithData = 0

        self.freqcount = {}
        self.locusTable = {}

        for locus in self.locusKeys:
            logger.debug("locus name: %s", locus)
            logger.debug("column tuple: %s", self.matrix[locus])

            # initialise blank dictionary
            self.alleleTable = {}

            # initialise blank list
            self.locusTable[locus] = []

            self.total = 0
            untypedIndividuals = 0
            unsequencedSites = 0

            # first pass runs a filter of alleles through the
            # anthonynolan data filter/cleaner

            # re-initialise the row count on each iteration of the locus
            rowCount = 0

            subMatrix = self.matrix[locus]

            for line in range(len(subMatrix)):
                logger.debug("%d %s", rowCount, subMatrix[line])
                allele1, allele2 = [str(i) for i in subMatrix[line]]
                logger.debug("... %s %s", allele1, allele2)

                # increment row count
                rowCount += 1

                if self.allowSemiTyped:
                    self._checkAllele(allele1, allele2, unsequencedSites)
                    if self.untypedAllele == allele1:
                        untypedIndividuals += 0.5
                    if self.untypedAllele == allele2:
                        untypedIndividuals += 0.5
                # ensure that *both* alleles are typed
                elif self.untypedAllele not in (allele1, allele2):
                    # check to see if the "allele" isn't a missing sequence site
                    if self.unsequencedSite not in (allele1, allele2):
                        self._checkAllele(allele1, allele2, unsequencedSites)
                    else:
                        if self.unsequencedSite == allele1:
                            unsequencedSites += 1
                        if self.unsequencedSite == allele2:
                            unsequencedSites += 1
                        logger.debug(locus, allele1, allele2, unsequencedSites)
                        continue
                # if either allele is untyped it is we throw out the
                # entire individual and go to the next individual
                else:
                    untypedIndividuals += 1
                    continue

                # save alleles as a tuple, sorted alphabetically
                if allele2 < allele1:
                    self.locusTable[locus].append((allele2, allele1))
                else:
                    self.locusTable[locus].append((allele1, allele2))

                logger.debug("%s %s, %d", allele1, allele2, self.total)

            # assign frequency, counts
            self.freqcount[locus] = (
                self.alleleTable,
                self.total,
                untypedIndividuals,
                unsequencedSites,
            )

            # if all individuals in a locus aren't untyped
            # then count this locus as having usable data
            if untypedIndividuals < self.totalIndivCount:
                self.totalLociWithData += 1

    def getLocusList(self):
        """Get the list of loci.

        Note:
           The returned list filters out all loci that consist of
           individuals that are all untyped.  The order of returned
           list is now fixed for the lifetime of the object.

        Returns:
            list: The list of loci.
        """
        # returns a clone of the locusKeys list, so that this instance
        # variable can't be modified inadvertently
        return self.locusKeys[:]

    def getAlleleCount(self):
        """Allele count statistics for all loci.

        Returns:
            dict: a map of tuples where the key is the locus name.  Each
            tuple is a triple, consisting of a map keyed by alleles
            containing counts, the total count at that locus and the
            number of untyped individuals.
        """
        return self.freqcount

    def getAlleleCountAt(self, locus, lumpValue=0):
        """Get allele count for given locus.

        Args:
           locus (str): locus
           lumpValue (int): the specified amount of lumping (Default: 0)

        Returns:
           tuple: a tuple consisting of a map keyed by alleles
           containing counts, the total count at that locus, and
           number of untyped individuals.
        """
        # need to recalculate values
        if lumpValue != 0:
            alleles, totalAlleles, untyped, unsequenced = self.freqcount[locus]

            lumpedAlleles = {}
            for allele in alleles:
                count = alleles[allele]
                if count <= lumpValue:
                    if "lump" in lumpedAlleles:
                        lumpedAlleles["lump"] += count
                    else:
                        lumpedAlleles["lump"] = count
                else:
                    lumpedAlleles[allele] = count
            return lumpedAlleles, totalAlleles, untyped, unsequenced
        return self.freqcount[locus]

    def serializeSubclassMetadataTo(self, stream):
        """Serialize subclass-specific metadata.

        Specifically, total number of individuals and loci and
        population name.

        Args:
            stream (TextOutputStream): the stream used for output.
        """
        stream.opentag("summaryinfo")
        stream.writeln()
        stream.tagContents("indivcount", f"{self.totalIndivCount}")
        stream.writeln()
        stream.tagContents("allelecount", f"{self.totalIndivCount * 2}")
        stream.writeln()
        stream.tagContents("locuscount", f"{self.totalLocusCount}")
        stream.writeln()
        stream.tagContents("lociWithDataCount", f"{self.totalLociWithData}")
        stream.writeln()
        stream.closetag("summaryinfo")
        stream.writeln()

    def serializeAlleleCountDataAt(self, stream, locus):
        """Serialize locus count data for a specific locus.

        Specifically, total number of individuals and loci and
        population name.

        Args:
            stream (TextOutputStream): the stream used for output
            locus (str): locus
        """
        self.alleleTable, self.total, untypedIndividuals, unsequencedSites = (
            self.freqcount[locus]
        )
        _serializeAlleleCountDataAt(
            stream, self.alleleTable, self.total, untypedIndividuals, unsequencedSites
        )

    def serializeAlleleCountDataTo(self, stream):
        """Serialize allele count data for a specific locus.

        Args:
            stream (TextOutputStream): the stream used for output

        Returns:
            int: always returns ``1``
        """
        stream.opentag("allelecounts")

        for locus in self.freqcount:
            stream.writeln()
            stream.opentag("locus", name=locus)

        stream.writeln()
        stream.closetag("allelecounts")
        return 1

    def getLocusDataAt(self, locus, lumpValue=0):
        """Get the genotyped data for specified locus.

        Note:
            The returned list has filtered out all individuals that
            are untyped at either chromosome. Data is sorted so that
            ``allele1`` < ``allele2``, alphabetically

        Args:
            locus (str): locus to use
            lumpValue (int): the specified amount of lumping (Default: ``0``).

        Returns:
            list: a list genotypes consisting of 2-tuples which
            contain each of the alleles for that individual in the
            list.
        """
        # need to recalculate values
        if lumpValue != 0:
            alleles, _totalAlleles, _untyped, _unsequenced = self.freqcount[locus]

            lumpedAlleles = {}
            listLumped = []
            for allele in alleles:
                count = alleles[allele]
                if count <= lumpValue:
                    listLumped.append(allele)
                    if "lump" in lumpedAlleles:
                        lumpedAlleles["lump"] += count
                    else:
                        lumpedAlleles["lump"] = count
                else:
                    lumpedAlleles[allele] = count

            copyTable = (self.locusTable[locus])[:]
            newTable = []
            for li in copyTable:
                allele1, allele2 = li
                newAllele1 = "lump" if allele1 in listLumped else allele1
                newAllele2 = "lump" if allele2 in listLumped else allele2
                newTable.append((newAllele1, newAllele2))

            return newTable
        # returns a clone of the list, so that this instance variable
        # can't be modified inadvertently
        return (self.locusTable[locus])[:]

    def getLocusData(self):
        """Get the genotyped data for all loci.

        Returns:
           dict: keyed by locus name of lists of 2-tuples as defined
           by :meth:`getLocusDataAt()`

        """
        return self.locusTable

    def getIndividualsData(self):
        """Get data for all individuals.

        Returns:
           StringMatrix: ``StringMatrix`` for all individuals
        """
        # return self.individualsData
        return self.matrix


class AlleleCounts:
    """Deprecated class to store information in allele count form.

    .. deprecated:: 0.6.0
         this class is now obsolete, the :class:`Genotypes` class
         now holds allele count data as pseudo-genotype matrix.
    """

    def __init__(self, alleleTable=None, locusName=None):
        self.alleleTable = alleleTable
        self.locusName = locusName
        self._genDataStructures()

    def _genDataStructures(self):
        total = 0
        self.freqcount = {}

        for allele in self.alleleTable:
            total += self.alleleTable[allele]

        # store in an iVar for the moment
        self.totalAlleleCount = total

        logger.debug("alleleTable", self.alleleTable)

        # simply reconstruct the 3-tuple as generated in
        # ParseGenotypeFile: alleleTable (a map of counts keyed by
        # allele), total allele count and the number of untyped
        # individuals (in this case, by definition it is zero).
        # then store in the same data structure as ParseGenotypeFile

        # even though we only have a single locus, this will make it
        # easy to generalize later

        self.freqcount[self.locusName] = self.alleleTable, self.totalAlleleCount, 0, 0

    def serializeSubclassMetadataTo(self, stream):
        """Serialize subclass-specific metadata.

        Specifically, total number of alleles and loci.
        """
        stream.opentag("summaryinfo")
        stream.writeln()
        stream.tagContents("allelecount", f"{self.totalAlleleCount}")
        stream.writeln()
        stream.tagContents("locuscount", f"{1}")
        stream.writeln()
        stream.closetag("summaryinfo")
        stream.writeln()

    def serializeAlleleCountDataAt(self, stream, locus):
        # call the class-independent function...

        alleleTable, total, untypedIndividuals, unsequencedSites = self.freqcount[locus]
        _serializeAlleleCountDataAt(
            stream, alleleTable, total, untypedIndividuals, unsequencedSites
        )

    def getAlleleCount(self):
        return self.freqcount[self.locusName]

    def getLocusName(self):
        # the first key is the name of the locus
        return self.locusName


def _serializeAlleleCountDataAt(
    stream, alleleTable, total, untypedIndividuals, unsequencedSites
):
    """Function to actually do the output."""
    totalFreq = 0
    alleles = list(alleleTable.keys())
    alleles.sort()

    # if all individuals are untyped then suppress itemized output
    if len(alleles) == 0:
        stream.emptytag("allelecounts", role="no-data")
        stream.writeln()
    else:
        # if monomorphic generate a role to indicate this, but
        # still generate the summary output
        if len(alleles) == 1:
            stream.opentag("allelecounts", role="monomorphic")
        else:
            stream.opentag("allelecounts")

        stream.writeln()
        stream.tagContents("untypedindividuals", f"{untypedIndividuals:.1f}")
        stream.writeln()
        stream.tagContents("unsequencedsites", f"{unsequencedSites}")
        stream.writeln()
        stream.tagContents("indivcount", f"{total / 2.0:.1f}")
        stream.writeln()
        stream.tagContents("allelecount", f"{total}")
        stream.writeln()
        stream.tagContents("distinctalleles", f"{len(alleleTable)}")
        stream.writeln()

        for allele in alleles:
            freq = float(alleleTable[allele]) / float(total)
            totalFreq += freq
            strFreq = f"{freq:0.5f} "
            strCount = f"{alleleTable[allele]}"

            stream.opentag("allele", name=allele)
            stream.writeln()
            stream.tagContents("frequency", strFreq)
            stream.tagContents("count", strCount)
            stream.writeln()
            stream.closetag("allele")

            stream.writeln()

        strTotalFreq = f"{totalFreq:0.5f}"
        strTotal = f"{total}"

        stream.tagContents("totalfrequency", strTotalFreq)
        stream.writeln()
        stream.tagContents("totalcount", strTotal)
        stream.closetag("allelecounts")
        stream.writeln()


# FIXME: regex should be passed as a parameter
def checkIfSequenceData(matrix):
    """Heuristic check to determine whether we are analysing sequence.

    Note:
       The regex matches loci of the form ``A_32`` or ``A_-32``

    Args:
        matrix (StringMatrix): matrix to check

    Returns:
        int: if sequence, return ``1``, otherwise ``0``
    """
    locus = matrix.colList[0]
    return 1 if re.search("[a-zA-Z0-9]+_[-]?[0-9]+", locus) else 0


def getMetaLocus(locus, isSequenceData):
    """Get the overall locus that this sequence belongs to.

    Args:
        locus (str): Locus of interest.
        isSequenceData (bool): whether this locus is sequence data

    Returns:
        str: The locus name, or ``None`` if not sequence data.
    """
    if isSequenceData:
        metaLocus = string.split(string.split(locus, ":")[0], "_")[0]
    else:
        metaLocus = None
    return metaLocus


def getLocusPairs(matrix, sequenceData):
    """Get locus pairs for a given matrix.

    :param matrix: matrix
    :type matrix: StringMatrix
    :param sequenceData: is this sequence data?
    :type sequenceData: bool
    :return: Returns a list of all pairs of loci from a given ``StringMatrix``.
    :rtype: list
    """
    loci = matrix.colList

    li = []
    for i in loci:
        lociCopy = loci[:]
        indexRemoved = loci.index(i)
        del lociCopy[indexRemoved]
        for j in lociCopy:
            if ((i + ":" + j) in li) or ((j + ":" + i) in li):
                pass
            # if we are running sequence data restrict pairs
            # to pairs within *within* the same gene locus
            elif sequenceData:
                genelocus_i = string.split(i, "_")[0]
                genelocus_j = string.split(j, "_")[0]
                # only append if gene is *within* the same locus
                if genelocus_i == genelocus_j:
                    li.append(i + ":" + j)
            else:
                li.append(i + ":" + j)
    return li


def getLumpedDataLevels(genotypeData, locus, lumpLevels):
    """Get lumped data for a specific locus.

    Args:
       genotypeData (Genotypes): genotype data to query
       locus (str): the locus
       lumpLevels (list): a list of integers representing lumping levels

    Returns:
       dict: a dictionary of tuples:
         - locusData: keyed by locus
         - alleleCount:
    """
    lumpData = {}
    for level in lumpLevels:
        lumpData[level] = (
            genotypeData.getLocusDataAt(locus, lumpValue=level),
            genotypeData.getAlleleCountAt(locus, lumpValue=level),
        )
    return lumpData
