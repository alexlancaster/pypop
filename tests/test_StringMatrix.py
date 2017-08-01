import base
import subprocess
import hashlib
import unittest
import pytest
from PyPop.Utils import StringMatrix, appendTo2dList

def new_matrix():
    return StringMatrix(3, ['A', 'B', 'C'])

class StringMatrixTest(unittest.TestCase):
    def test_new(self):
        # check everything is zero upon first assignment
        A_matrix = new_matrix()
        assert A_matrix['A'] == [[0, 0], [0, 0], [0, 0]]
        assert A_matrix['B'] == [[0, 0], [0, 0], [0, 0]]
        assert A_matrix['C'] == [[0, 0], [0, 0], [0, 0]]

    def test_assign(self):
        # test assignment
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')
        assert A_matrix['A'] == [[0, 0], [0, 0], [0, 0]]
        assert A_matrix['B'] == [['B0', 'B0'], ['B1', 'B1'], [0, 0]]
        assert A_matrix['C'] == [[0, 0], [0, 0], [0, 0]]

    def test_copy(self):
        # check copies are independent
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')

        B_matrix = A_matrix.copy()
        B_matrix[0,'A'] = ('A0', 'A0')
        B_matrix[1,'A'] = ('A1', 'A2')

        # B should be changed
        assert B_matrix['A'] == [['A0', 'A0'], ['A1', 'A2'], [0, 0]]
        assert B_matrix['B'] == [['B0', 'B0'], ['B1', 'B1'], [0, 0]]
        assert B_matrix['C'] == [[0, 0], [0, 0], [0, 0]]
    
        # A should be unchanged and have nothing the A column
        assert A_matrix['A'] == [[0, 0], [0, 0], [0, 0]]
        assert A_matrix['B'] == [['B0', 'B0'], ['B1', 'B1'], [0, 0]]
        assert A_matrix['C'] == [[0, 0], [0, 0], [0, 0]]

    def test_submatrix_one_locus(self):
        # test subMatrix, get all data at locus 'A'
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')
        A_matrix[0, 'A'] = ('A0', 'A0')
        A_matrix[1, 'A'] = ('A1', 'A2')
        assert A_matrix['A'] == [['A0', 'A0'], ['A1', 'A2'], [0, 0]]

    def test_submatrix_two_locus(self):
        # test subMatrix, get all data for b at locus 'A:B'
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')
        A_matrix[0, 'A'] = ('A0', 'A0')
        A_matrix[1, 'A'] = ('A1', 'A2')
        assert A_matrix['A:B'] == [['A0', 'A0', 'B0', 'B0'], ['A1', 'A2', 'B1', 'B1'], [0, 0, 0, 0]]

    def test_filterout(self):
        # filterOut all rows that contain 'B1'
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')
        A_matrix[0, 'A'] = ('A0', 'A0')
        A_matrix[1, 'A'] = ('A1', 'A2')
        B_list = A_matrix.filterOut('A:B:C', 'B1') # do the filter
        assert B_list == [['A0', 'A0', 'B0', 'B0', 0, 0], [0, 0, 0, 0, 0, 0]]

    def test_append(self):
        # append a string to each allele
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')
        A_matrix[0, 'A'] = ('A0', 'A0')
        A_matrix[1, 'A'] = ('A1', 'A2')

        assert appendTo2dList(A_matrix['A:B:C'], appendStr=':') == [['A0:', 'A0:', 'B0:', 'B0:', '0:', '0:'], ['A1:', 'A2:', 'B1:', 'B1:', '0:', '0:'], ['0:', '0:', '0:', '0:', '0:', '0:']]

        assert A_matrix['A'] == [['A0', 'A0'], ['A1', 'A2'], [0, 0]]
        assert A_matrix['B'] == [['B0', 'B0'], ['B1', 'B1'], [0, 0]]
        assert A_matrix['C'] == [[0, 0], [0, 0], [0, 0]]

    def test_GetUniqueAlleles(self):
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')
        A_matrix[0, 'A'] = ('A0', 'A0')
        A_matrix[1, 'A'] = ('A1', 'A2')

        # remember that some columns have no data, so '0' is also an element!
        assert A_matrix.getUniqueAlleles('A') == ['0', 'A0', 'A1', 'A2']
        assert A_matrix.getUniqueAlleles('B') == ['0', 'B0', 'B1']
        assert A_matrix.getUniqueAlleles('C') == ['0']

    def test_ConvertToInts(self):
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')
        A_matrix[0, 'A'] = ('A0', 'A0')
        A_matrix[1, 'A'] = ('A1', 'A2')

        B_matrix = A_matrix.convertToInts()

        # check that original matrix remains unchanged
        assert A_matrix['A'] == [['A0', 'A0'], ['A1', 'A2'], [0, 0]]
        assert A_matrix['B'] == [['B0', 'B0'], ['B1', 'B1'], [0, 0]]
        assert A_matrix['C'] == [[0, 0], [0, 0], [0, 0]]

        # check new matrix
        assert B_matrix['A'] == [[2, 2], [3, 4], [1, 1]]
        assert B_matrix['B'] == [[2, 2], [3, 3], [1, 1]]
        assert B_matrix['C'] == [[1, 1], [1, 1], [1, 1]]


    def test_ConvertToInt_FlattenCols(self):
        geno = StringMatrix(5, ["DRB", "B"])
        geno[0, 'DRB'] = ('4', '11')
        geno[1, 'DRB'] = ('2', '7')
        geno[2, 'DRB'] = ('1', '13')
        geno[3, 'DRB'] = ('7', '7')
        geno[4, 'DRB'] = ('8', '11')
        geno[0, 'B'] = ('62', '61')
        geno[1, 'B'] = ('7', '44')
        geno[2, 'B'] = ('27', '62')
        geno[3, 'B'] = ('7', '44')
        geno[4, 'B'] = ('51', '55')

        new_geno = geno.convertToInts()
        flattened_list = new_geno.flattenCols()

        assert flattened_list == [3, 2, 1, 4, 5, 6, 4, 7, 4, 6, 7, 1, 2, 1, 4, 6, 3, 7, 3, 5]
