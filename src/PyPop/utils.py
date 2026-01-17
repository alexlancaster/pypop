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

"""Module for common utility classes and functions.

Contains convenience classes for output of text and XML
files.
"""

import copy
import operator
import os
import re
import shutil
import stat
import sys
from collections.abc import Sequence
from pathlib import Path

import numpy as np
from numpy import asarray, take, zeros

from PyPop import logger

GENOTYPE_SEPARATOR = "~"
"""
Separator between genotypes

Example:

  In a haplotype
  ``01:01~13:01~04:02``
"""

GENOTYPE_TERMINATOR = "~"
"""
Terminator of genotypes

Example:

  ```02:01:01:01~``
"""


class TextOutputStream:
    """Output stream for writing text files.

    Args:
       file (file): file handle
    """

    def __init__(self, file):
        self.f = file

    def write(self, str):
        """Write to stream.

        Args:
          str (str): string to write
        """
        self.f.write(str)

    def writeln(self, str="\n"):
        """Write a newline to stream.

        Args:
          str (str, optional): defaults to newline
        """
        if str == "\n":
            self.f.write("\n")
        else:
            self.f.write(str + "\n")

    def close(self):
        """Close stream."""
        self.f.close()

    def flush(self):
        """Flush to disk."""
        self.f.flush()


class XMLOutputStream(TextOutputStream):
    """Output stream for writing XML files."""

    def _gentag(self, tagname, **kw):
        """Internal method for generating tag text.

        Strip out non-valid tag character: '?'
        *Only use internally*.
        """
        attr = ""
        tagname = tagname.replace("?", "")
        # loop through keywords turning each into an attr,key pair
        for key, val in kw.items():
            attr = attr + key + "=" + '"' + val + '"' + " "
        if attr == "":
            return f"{tagname}"
        return f"{tagname} {attr.strip()}"

    def opentag(self, tagname, **kw):  # noqa: D417
        """Write an open XML tag to stream.

        Tag attributes passed as optional named keyword arguments.

        Example:
          ``opentag('tagname', role=something, id=else)``

          produces the result:

          ``<tagname role="something" id="else">``

          Attribute and values are optional:

          ``opentag('tagname')``

          Produces:

          ``<tagname>``

        See Also:
           Must be be followed by a :meth:`closetag`.

        Args:
           tagname (str):  name of XML tag

        """
        self.f.write(f"<{self._gentag(tagname, **kw)}>")

    def emptytag(self, tagname, **kw):  # noqa: D417
        """Write an empty XML tag to stream.

        This follows the same syntax as :meth:`opentag` but without
        XML content (but can contain attributes).

        Example:
          ```emptytag('tagname', attr='val')``

          produces:

          ``<tagname attr="val"/>``

        Args:
           tagname (str): name of XML tag
        """
        self.f.write(f"<{self._gentag(tagname, **kw)}/>")

    def closetag(self, tagname):
        """Write a closing XML tag to stream.

        Example:
          ``closetag('tagname')``

          Generate a tag in the form:

          ``</tagname>``

        See Also:
           Must be be preceded by a :meth:`opentag`.

        Args:
           tagname (str): name of XML tag
        """
        self.f.write(f"</{self._gentag(tagname)}>")

    def tagContents(self, tagname, content, **kw):  # noqa: D417
        """Write XML tags around contents to a stream.

        Example:
          ``tagContents('tagname', 'foo bar')``

          produces:

          ``<tagname>foo bar</tagname>```

        Args:
           tagname (str): name of XML tag
           content (str): must only be a string. ``&``, ``<`` and
            ``>`` are converted into valid XML equivalents.

        """
        self.opentag(tagname, **kw)
        content = content.replace("&", "&amp;")
        content = content.replace("<", "&lt;")
        content = content.replace(">", "&gt;")
        self.f.write(content)
        self.closetag(tagname)


class StringMatrix(Sequence):
    """Matrix of strings and other metadata from input file to PyPop.

    ``StringMatrix`` is a subclass of
    :class:`collections.abc.Sequence` and represents genotype or
    locus-based data in a row-oriented matrix structure with
    NumPy-style indexing and sequence semantics. Rows correspond to
    individuals, and columns correspond to loci.

    The object supports indexing, assignment, copying, and printing
    using standard Python and NumPy idioms.

    Args:
       rowCount (int): number of rows in matrix
       colList (list): list of locus keys in a specified order
       extraList (list): other non-matrix metadata
       colSep (str): column separator
       headerLines (list): list of lines in the header of original file

    Note:
      * ``len(matrix)`` returns the number of rows.
      * Indexing retrieves data by locus or locus combinations.
      * Assignment updates genotype or metadata values in place.
      * Slicing over rows (e.g., ``matrix[i:j]``) is not currently supported.
      * Deep copying produces a fully independent matrix.

    Examples:
       Create a matrix of two individuals with two loci and assign genotype data:

       >>> matrix = StringMatrix(2, ["A", "B"])
       >>> matrix [0, "A"] = ("A0_1", "A0_2")
       >>> matrix [1, "A"] = ("A1_1", "A1_2")
       >>> matrix [0, "B"] = ("B0_1", "B0_2")
       >>> matrix [1, "B"] = ("B1_1", "B1_2")

       Length of matrix is defined as the number of individuals in the
       matrix:

       >>> len(matrix)
       2

       Retrieve data for a single locus:

       >>> matrix["A"]
       [['A0_1', 'A0_2'], ['A1_1', 'A1_2']]

       String representation:

       >>> print (matrix)
       StringMatrix([['A0_1', 'A0_2', 'B0_1', 'B0_2'],
              ['A1_1', 'A1_2', 'B1_1', 'B1_2']], dtype=object)

       Copying the matrix:

       >>> import copy
       >>> m2 = copy.deepcopy(matrix)
       >>> m2 is matrix
       False

    """

    def __init__(
        self, rowCount=None, colList=None, extraList=None, colSep="\t", headerLines=None
    ):
        # colList is a mutable type so we freeze the list of locus
        # keys in the original order in file by making a *clone* of
        # the list of keys.

        # the order of loci in the array will correspond to the
        # original file order, and we don't want this tampered with by
        # the `callee' function (i.e. effectively override the Python
        # 'pass by reference' default and 'pass by value').

        self.colList = colList[:]

        self.colCount = len(self.colList)
        self.rowCount = rowCount

        if extraList:
            self.extraList = extraList[:]
            self.extraCount = len(self.extraList)
        else:
            self.extraList = None
            self.extraCount = 0

        self.colSep = colSep
        self.headerLines = headerLines

        # initialising the internal NumPy array
        self.array = zeros(
            (self.rowCount, self.colCount * 2 + self.extraCount), dtype="O"
        )
        self.dtype = self.array.dtype
        self.shape = self.array.shape
        self._typecode = self.array.dtype
        self.name = str(self.__class__).split()[0]

    def __repr__(self):
        """Override default representation.

        Returns:
           str: new string representation
        """
        if len(self.array.shape) > 0:
            return (self.__class__.__name__) + repr(self.array)[len("array") :]
        return (self.__class__.__name__) + "(" + repr(self.array) + ")"

    def __len__(self):
        """Get number of rows (individuals) in the matrix.

        This allows ``StringMatrix`` instances to be used with
        `len()`, iteration, and other Python sequence protocols.

        Returns:
           int: number of rows in the matrix

        """
        return self.array.shape[0]

    def __deepcopy__(self, memo):
        """Create a deepcopy for ``copy.deepcopy``.

        This simply calls ``self.copy()`` to allow
        ``copy.deepcopy(matrixInstance)`` to work out of the box.

        Args:
           memo (dict): opaque object

        Returns:
          StringMatrix: copy of the matrix

        """
        return self.copy()

    def __getslice__(self, i, j):
        """Get slice (overrides built-in).

        Warning:
          Currently not supported for :class:`StringMatrix`

        """
        msg = "slices not currently supported"
        raise Exception(msg)  # noqa: TRY002

    def __getitem__(self, key):
        """Get the item at given key (overrides built-in numpy).

        Args:
          key (str): locus key

        Returns:
           list: a list (a single column vector if only one position
           specified), or list of lists: (a set of column vectors if
           several positions specified) of tuples for ``key``

        Raises:
           KeyError: if key is not found, or of wrong type

        """
        if type(key) is tuple:
            row, colName = key
            if colName in self.colList:
                col = self.extraCount + self.colList.index(colName)
            else:
                msg = f"can't find {colName} column"
                raise KeyError(msg)
            return self.array[(row, col)]
        if type(key) is str:
            colNames = key.split(":")
            li = []
            for col in colNames:
                # check first in list of alleles
                if col in self.colList:
                    # get relative location in list
                    relativeLoc = self.colList.index(col)
                    # calculate real locations in array
                    col1 = relativeLoc * 2 + self.extraCount
                    col2 = col1 + 1
                    li.append(col1)
                    li.append(col2)
                # now check in non-allele metadata
                elif (self.extraList is not None) and (col in self.extraList):
                    li.append(self.extraList.index(col))
                else:
                    msg = f"can't find {col} column"
                    raise KeyError(msg)

            if len(colNames) == 1:
                # return simply the pair of columns at that location as
                # a list
                return take(self.array, tuple(li[0:2]), 1).tolist()
            # return the matrix consisting of column vectors
            # of the designated keys
            return take(self.array, tuple(li), 1).tolist()
        msg = "keys must be a string or tuple"
        raise KeyError(msg)

    def __setitem__(self, index, value):
        """Set the value at an index (override built in).

        Args:
           index (tuple): index into matrix
           value (tuple|str): can set using a tuple of strings, or a
            single string (for metadata)

        Raises:
           IndexError: if ``index`` is not a tuple
           ValueError: if ``value`` is not a tuple or string
           KeyError: if the ``index`` can't be found

        """
        if type(index) is tuple:
            row, colName = index
        else:
            msg = "index is not a tuple"
            raise IndexError(msg)
        if type(value) is tuple:
            value1, value2 = value
        elif type(value) is str:
            # don't need to do anything
            pass
        else:
            msg = "value being assigned is not a tuple"
            raise ValueError(msg)

        if colName in self.colList:
            # find the location in order in the array
            col = self.colList.index(colName)
            # calculate the offsets to the actual array location
            col1 = col * 2
            col2 = col1 + 1
            # store each element in turn
            self.array[(row, col1 + self.extraCount)] = (
                value1 if type(value1) is str else asarray(value1, dtype=self.dtype)
            )
            self.array[(row, col2 + self.extraCount)] = (
                value2 if type(value2) is str else asarray(value2, dtype=self.dtype)
            )

        elif colName in self.extraList:
            col = self.extraList.index(colName)
            self.array[(row, col)] = (
                value if type(value) is str else asarray(value, self.dtype)
            )
        else:
            msg = f"can't find {col} column"
            raise KeyError(msg)

    def dump(self, locus=None, stream=sys.stdout):
        """Write file to a stream in original format.

        Args:
           locus (str, optional): write just specified locus, if
            omitted, default to all loci
           stream (TextOutputStream|XMLOutputStream|stdout): output stream

        """
        # first write out header, if there is one
        if self.headerLines:
            for line in self.headerLines:
                (stream.write(line),)

        # next write out the non-allele column headers, if there are some
        if self.extraList:
            for elem in self.extraList:
                stream.write(elem + self.colSep)

        locusList = locus if locus else ":".join(self.colList)

        # next write out the allele column headers
        for elem in locusList.split(":"):
            stream.write(elem + "_1" + self.colSep)
            stream.write(
                elem + "_2" + self.colSep,
            )
        stream.write("\n")

        # finally the matrix itself

        # prepend extra fields if they exist
        all_cols = (
            ":".join(self.extraList) + ":" + locusList if self.extraList else locusList
        )

        for row in self.__getitem__(all_cols):
            for elem in row:
                stream.write(str(elem) + self.colSep)  # convert element to str
            stream.write("\n")

    def copy(self):
        """Make a (deep) copy.

        Return:
            StringMatrix: a deep copy of the current object
        """
        # FIXME: currently this goes via the constructor, not sure if
        # there is a better way of doing this

        thecopy = StringMatrix(
            copy.deepcopy(self.rowCount),
            copy.deepcopy(self.colList),
            copy.deepcopy(self.extraList),
            self.colSep,
            self.headerLines,
        )
        thecopy.array = self.array.copy()
        return thecopy

    def getNewStringMatrix(self, key):
        """Create new StringMatrix containing specified loci.

        Note:
          The format of the keys is identical to :meth:`__getitem__`
          except that it returns a full ``StringMatrix`` instance
          which includes all metadata

        Args:
           key (str): a string representing the loci, using the
            ``locus1:locus2`` format

        Returns:
           StringMatrix: full instance

        Raises:
           KeyError: if locus can not be found.

        """
        if type(key) is str:
            colNames = key.split(":")

            # need both column position and names to reconstruct matrix
            newColPos = []
            newColList = []
            newExtraPos = []
            newExtraList = []
            for col in colNames:
                # check first in list of alleles
                if col in self.colList:
                    # get relative location in list
                    relativeLoc = self.colList.index(col)
                    # calculate real locations in array
                    col1 = relativeLoc * 2 + self.extraCount
                    col2 = col1 + 1
                    newColPos.append(col1)
                    newColPos.append(col2)
                    newColList.append(col)
                # now check in non-allele metadata
                elif col in self.extraList:
                    newExtraPos.append(self.extraList.index(col))
                    newExtraList.append(col)
                else:
                    msg = f"can't find {col} column"
                    raise KeyError(msg)

        # build a new matrix using the parameters from the current
        newMatrix = StringMatrix(
            rowCount=self.rowCount,
            colList=newColList,
            extraList=newExtraList,
            colSep=self.colSep,
            headerLines=self.headerLines,
        )

        # copy just the columns we requested, both loci cols + extras
        newExtraPos.extend(newColPos)
        newMatrix.array = self.array[:, newExtraPos]
        return newMatrix

    def getUniqueAlleles(self, key):
        """Get naturally sorted list of unique alleles.

        Args:
           key (str): loci to get

        Returns:
           list: list of unique integers sorted by allele name using
           natural sort

        """
        uniqueAlleles = []
        for genotype in self.__getitem__(key):
            for allele in genotype:
                str_allele = str(allele)
                if str_allele not in uniqueAlleles:
                    uniqueAlleles.append(str_allele)
        uniqueAlleles.sort(key=natural_sort_key)  # natural sort
        return uniqueAlleles

    def convertToInts(self):
        """Convert the matrix to integers.

        Note:
          This function is used by the :class:`PyPop.haplo.Haplostats`
          class.  Note that integers start at 1 for compatibility with
          haplo-stats module

        Returns:
          StringMatrix: matrix where the original allele names are now
          represented by integers

        """
        # FIXME: check whether we need to release memory
        # create a new copy
        newMatrix = self.copy()
        for colName in self.colList:
            uniqueAlleles = self.getUniqueAlleles(colName)
            for row, genotype in enumerate(self.__getitem__(colName)):
                factor_genotype = []
                for allele in genotype:
                    pos = uniqueAlleles.index(str(allele)) + 1
                    factor_genotype.append(pos)
                newMatrix[row, colName] = tuple(factor_genotype)

        return newMatrix

    def countPairs(self):
        """Count all possible pairs of haplotypes for each matrix row.

        Warning:
          This does *not* do any involved handling of missing data as
          per ``geno.count.pairs`` from R ``haplo.stats`` module.

        Returns:
          list: each element is the number of pairs in row order

        """
        # FIXME: should these methods eventually be moved to the
        # :class:`PyPop.ParseFile.Genotype` class?

        # count number of unique alleles at each loci
        n_alleles = {}
        for colName in self.colList:
            n_alleles[colName] = len(self.getUniqueAlleles(colName))

        # count pairs of haplotypes for subjects without any missing alleles
        # FIXME: maybe convert to it's own method as per getUniqueAlleles
        h1 = self.array[:, 0::2]  # get "_1" allele (odd cols)
        h2 = self.array[:, 1::2]  # get "_2" allele (even cols)
        n_het = np.sum(np.not_equal(h1, h2), 1)  # equivalent of: apply(h1!=h2,1,sum)
        n_het = np.where(
            n_het == 0, 1, n_het
        )  # equivalent of: ifelse(n.het==0,1,n.het)
        n_pairs = 2 ** (n_het - 1)  # equivalent of: n.pairs = 2^(n.het-1)

        return n_pairs.tolist()

    def flattenCols(self):
        """Flatten columns into a single list.

        Important:
           Currently assumes entries are integers.

        Returns:
           list: all alleles, the two genotype columns concatenated
           for each locus

        """
        flattened_matrix = []

        for col in self.colList:  # FIXME: currently assume we want whole matrix
            # FIXME: possibly refactor extracting column logic with __getitem__
            relativeLoc = self.colList.index(col)
            col1 = relativeLoc * 2 + self.extraCount
            col2 = col1 + 1
            first_col = [int(x) for x in self.array[:, col1]]
            flattened_matrix.extend(first_col)
            second_col = [int(x) for x in self.array[:, col2]]
            flattened_matrix.extend(second_col)

        return flattened_matrix

    def filterOut(self, key, blankDesignator):
        """Get matrix rows filtered by a designator.

        Args:
           key (str): locus to filter
           blankDesignator (str): string to exclude

        Returns:
           list: the rows of the matrix that *do not* contain
           ``blankDesignator`` at any rows

        """

        def f(x, designator=blankDesignator):
            for value in x:
                if value == designator:
                    return 0
            return 1

        filtered_list = list(filter(f, self.__getitem__(key)))
        return filtered_list[:]

    def getSuperType(self, key):
        """Get a matrix grouped by specified key.

        Example:
          Return a new matrix with the column vector with the alleles
          for each genotype concatenated like so:

          >>> matrix = StringMatrix(2, ["A", "B"])
          >>> matrix[0, "A"] = ("A01", "A02")
          >>> matrix[1, "A"] = ("A11", "A12")
          >>> matrix[0, "B"] = ("B01", "B02")
          >>> matrix[1, "B"] = ("B11", "B12")
          >>> print(matrix)
          StringMatrix([['A01', 'A02', 'B01', 'B02'],
                 ['A11', 'A12', 'B11', 'B12']], dtype=object)
          >>> matrix.getSuperType("A:B")
          StringMatrix([['A01:B01', 'A02:B02'],
                 ['A11:B11', 'A12:B12']], dtype=object)

        Args:
           key (str): loci to group

        Returns:
           StringMatrix: a new matrix with the columns concatenated

        """
        li = self.__getitem__(key)

        colName = key.replace(":", "-")
        newMatrix = StringMatrix(
            rowCount=copy.deepcopy(self.rowCount),
            colList=copy.deepcopy([colName]),
            extraList=copy.deepcopy(self.extraList),
            colSep=self.colSep,
            headerLines=self.headerLines,
        )

        for pos, i in enumerate(li):
            # newMatrix[pos, colName] = (i[0::2].join(":"), i[1::2].join(":"))
            newMatrix[pos, colName] = (":".join(i[0::2]), ":".join(i[1::2]))

        return newMatrix


class Group:
    """Group list or sequence into non-overlapping chunks.

    Example:
      >>> for pair in Group('aabbccddee', 2):
      ...    print(pair)  # doctest: +NORMALIZE_WHITESPACE
      ...
      aa
      bb
      cc
      dd
      ee

      >>> a = Group('aabbccddee', 2)
      >>> a[0]
      'aa'
      >>> a[3]
      'dd'

    Args:
        li (str|list): string or list
        size (int): size of grouping

    """

    def __init__(self, li, size):
        self.size = size
        self.li = li

    def __getitem__(self, group):
        """Get the item by position.

        Args:
           group (int): get the item by position

        Returns:
           str|list: the value at that position

        Raises:
           IndexError: if ``group`` is out of bounds
        """
        idx = group * self.size
        if idx > len(self.li):
            msg = "Out of range"
            raise IndexError(msg)
        return self.li[idx : idx + self.size]


### global FUNCTIONS start here


def critical_exit(message, *args):  # noqa: D417
    """Log a CRITICAL message and exit with status 1.

    .. versionadded:: 1.4.0

    Args:
        message (str): Logging format string.
    """
    logger.critical(message, *args, stacklevel=2)
    sys.exit(1)


def getStreamType(stream):
    """Get the type of stream.

    Args:
      stream (TextOutputStream|XMLOutputStream): stream to check

    Returns:
      string: either ``xml`` or ``text``.
    """
    return "xml" if isinstance(stream, XMLOutputStream) == 1 else "text"


def glob_with_pathlib(pattern):
    """Use globbing with ``pathlib``.

    Args:
       pattern (str): globbing pattern

    Returns:
       list: of pathlib globs
    """
    path = Path(pattern).resolve()
    return list(path.parent.glob(path.name))


def natural_sort_key(s, _nsre=re.compile(r"([0-9]+)")):
    """Generate a key for natural (human-friendly) sorting.

    This function splits a string into text and number components so that
    numbers are compared by value instead of lexicographically. It is
    intended for use as the ``key`` function in :meth:`list.sort` or
    :func:`sorted`.

    Example:
      >>> items = ["item2", "item10", "item1"]
      >>> sorted(items, key=natural_sort_key)
      ['item1', 'item2', 'item10']

    Args:
        s (str): The string to split into text and number components.
        _nsre (Pattern): Precompiled regular expression used internally
            to split the string into digit and non-digit chunks. This is
            not intended to be overridden in normal use.

    Returns:
        list: A list of strings and integers to be used as a sort key.
    """
    return [
        int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)
    ]


def unique_elements(li):
    """Gets the unique elements in a list.

    Args:
      li (list): a list

    Returns:
      list: unique elements
    """
    d = {}
    length = len(li)
    map(operator.setitem, length * [d], li, length * [None])
    return d.keys()


def appendTo2dList(aList, appendStr=":"):
    """Append a string to each element in a list.

    Args:
      aList (list): list to append to
      appendStr (str): string to append

    Returns:
       list: a list with string appended to each element

    """
    return [[f"{cell}{appendStr}" for cell in row] for row in aList]


def convertLineEndings(file, mode):
    """Convert line endings based on platform.

    Args:
        file (str): file name to convert
        mode (int): Conversion mode, one of

          - ``1`` Unix to Mac
          - ``2`` Unix to DOS

    """
    if mode == 1:
        if Path(file).is_dir():
            critical_exit("%s Directory!", file)
        with open(file) as fp:
            data = fp.read()
            if "\0" in data:
                critical_exit("%s Binary!", file)
            newdata = re.sub("\r?\n", "\r", data)
        if newdata != data:
            with open(file, "w") as f:
                f.write(newdata)
    elif mode == 2:
        if Path(file).is_dir():
            critical_exit("%s Directory!", file)
        with open(file) as fp:
            data = fp.read()
            if "\0" in data:
                critical_exit("%s Binary!", file)
            newdata = re.sub("\r(?!\n)|(?<!\r)\n", "\r\n", data)
        if newdata != data:
            with open(file, "w") as f:
                f.write(newdata)


def fixForPlatform(filename, txt_ext=0):
    """Fix for some Windws/MS-DOS platforms.

    Args:
       filename (str): path to file
       txt_ext (int, optional): if enabled (``1``) add a ``.txt`` extension

    """
    # make file read-writeable by everybody
    Path(filename).chmod(stat.S_IFCHR)

    # create as a DOS format file LF -> CRLF
    if sys.platform == "cygwin":
        convertLineEndings(filename, 2)
        # give it a .txt extension so that lame Windows realizes it's text
        if txt_ext:
            Path(filename).rename(filename + ".txt")
            print(f"{filename}.txt")
        else:
            print(filename)
    else:
        print(filename)


def copyfileCustomPlatform(src, dest, txt_ext=0):
    """Copy file to file with fixes.

    Args:
       src (str): source file
       dest (str): source file
       txt_ext (int, optional): if enabled (``1``) add a ``.txt`` extension

    """
    shutil.copyfile(src, dest)
    fixForPlatform(dest, txt_ext=txt_ext)
    (print(f"copying {src} to"),)


def copyCustomPlatform(file, dist_dir, txt_ext=0):
    """Copy file to directory with fixes.

    Args:
       file (str): source file
       dist_dir (str): source directory
       txt_ext (int, optional): if enabled (``1``) add a ``.txt`` extension

    """
    new_filename = Path(dist_dir) / Path(file).name
    print(f"copying {file} to")
    shutil.copy(file, dist_dir)
    fixForPlatform(new_filename, txt_ext=txt_ext)


def checkXSLFile(xslFilename, path="", subdir="", abort=False, msg=""):
    """Check XSL filename and return full path.

    Args:
       xslFilename (str): name of the XSL file
       path (str): root path to check
       subdir (str): subdirectory under ``path`` to check
       abort (bool): if enabled (``True``) file isn't found, exit with
        an error.  Default is ``False``
       msg (str): output message on abort

    Returns:
       str: checked and validaated path

    """
    logger.debug(
        "path=%s, subdir=%s, xslFilename=%s xsl path", path, subdir, xslFilename
    )

    # generate a full path to check
    checkPath = os.path.realpath(Path(path) / subdir / xslFilename)
    if Path(checkPath).is_file():
        return checkPath
    if abort:
        critical_exit("Can't find XSL: %s %s", checkPath, msg)
    else:
        logger.warning("Can't find XSL: %s %s", checkPath, msg)
    return None


def getUserFilenameInput(prompt, filename):
    """Get user filename input.

    Read user input for a filename, check its existence, continue
    requesting input until a valid filename is entered.

    Args:
       prompt (str): description of file
       filename (str): default filename

    Returns:
       str: name of file eventually selected
    """
    nofile = 1
    while nofile:
        tempFilename = input(f"Please enter {prompt} filename [{filename}]: ")

        # if we accept default, still check that file still exists
        if tempFilename == "":
            if Path(filename).is_file():
                nofile = 0
            else:
                print(f"File '{filename}' does not exist")
        # if we don't accept default, check that file exists and use
        # the user input as the filename
        elif Path(tempFilename).is_file():
            nofile = 0
            filename = tempFilename
        else:
            # otherwise return an error
            print(f"File '{tempFilename}' does not exist")

    return filename


def splitIntoNGroups(alist, n=1):
    """Divides a list up into n parcels (plus whatever is left over).

    Example:
       >>> a = ['A', 'B', 'C', 'D', 'E']
       >>> splitIntoNGroups(a, 2)
       [['A', 'B'], ['C', 'D'], ['E']]

    Args:
       alist (list): list to divide up
       n (int): parcel size

    Returns:
       list: list of lists

    """
    # FIXME: This class should be ported to use Python 3 iterators
    # from itertools import islice
    # it = iter(alist)

    x = len(alist) // n  # note: don't just drop the last len(alist) % n items
    y = len(alist) % n

    # initialize an empty list
    retval = []

    # only create list if divisor is non-zero
    if x:
        retval = [alist[i * x : ((i + 1) * x)] for i in range(n)]
        # retval = [ list(islice(it, x)) for i in range(n) ]

    # if modulus is non-zero make sure to add the extra part of list
    if y:
        extra = alist[-y:]
        # extra = list(islice(it, y))
        retval.append(extra)

    return retval
