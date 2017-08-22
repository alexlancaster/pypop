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

    def test_GetNewStringMatrix(self):

        # create StringMatrix with 3 loci + 1 non-locus keys
        A_matrix = StringMatrix(3, ['A', 'B', 'C'], ['foo'])
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')
        A_matrix[2, 'B'] = ('B3', 'B1')
        A_matrix[0, 'A'] = ('A0', 'A0')
        A_matrix[1, 'A'] = ('A1', 'A2')
        A_matrix[2, 'A'] = ('A0', 'A2')
        A_matrix[0, 'C'] = ('C0', 'C0')
        A_matrix[1, 'C'] = ('C1', 'C2')
        A_matrix[2, 'C'] = ('C2', 'C1')
        A_matrix[0, 'foo'] = "bar"
        A_matrix[1, 'foo'] = "baz"
        A_matrix[2, 'foo'] = "frum"

        # get matrix subset
        B_matrix = A_matrix.getNewStringMatrix("A:C:foo")

        # check new and original matrix columns
        assert A_matrix.colList == ['A', 'B', 'C']
        assert B_matrix.colList == ['A', 'C']

        # check new and original matrix shapes
        # note number of cols is twice number of loci + extra column
        assert A_matrix.shape == (3, 7)
        assert B_matrix.shape == (3, 5)

        assert B_matrix['A'] == [['A0', 'A0'], ['A1', 'A2'], ['A0', 'A2']]
        assert B_matrix['C'] == [['C0', 'C0'], ['C1', 'C2'], ['C2', 'C1']]
        assert B_matrix['foo'] == [['bar'], ['baz'], ['frum']]

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

    def test_CountPairs_Small(self):

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

        pairs = geno.countPairs()
        max_haps =  2*sum(pairs)
        
        assert pairs == [2, 2, 2, 1, 2]
        assert max_haps == 18

    def test_CountPairs_Large(self):

        geno = StringMatrix(45, ['A', 'C', 'B'])
        geno[ 0, 'A'] = ( '101', '201')
        geno[ 1, 'A'] = (  '210', '3012')
        geno[ 2, 'A'] = (  '101', '218')
        geno[ 3, 'A'] = ( '2501', '201')
        geno[ 4, 'A'] = ( '210', '3204')
        geno[ 5, 'A'] = ( '3012', '3204')
        geno[ 6, 'A'] = ( '2501', '3204')
        geno[ 7, 'A'] = ( '6814', '201')
        geno[ 8, 'A'] = ( '201', '201')
        geno[ 9, 'A'] = ( '3204', '101')
        geno[10, 'A'] = ( '6901', '210')
        geno[11, 'A'] = ( '210', '3012')
        geno[12, 'A'] = ( '101', '218')
        geno[13, 'A'] = ( '101', '201')
        geno[14, 'A'] = ( '210', '3012')
        geno[15, 'A'] = ( '101', '218')
        geno[16, 'A'] = ( '101', '218')
        geno[17, 'A'] = ( '2501', '201')
        geno[18, 'A'] = ( '201', '201')
        geno[19, 'A'] = ( '3012', '2501')
        geno[20, 'A'] = ( '218', '6814')
        geno[21, 'A'] = ( '201', '201')
        geno[22, 'A'] = ( '3204', '2501')
        geno[23, 'A'] = ( '218', '218')
        geno[24, 'A'] = ( '3012', '3012')
        geno[25, 'A'] = ( '101', '2501')
        geno[26, 'A'] = ( '101', '210')
        geno[27, 'A'] = ( '210', '3012')
        geno[28, 'A'] = ( '101', '2501')
        geno[29, 'A'] = ( '3204', '6814')
        geno[30, 'A'] = ( '201', '201')
        geno[31, 'A'] = ( '201', '3204')
        geno[32, 'A'] = ( '101', '6901')
        geno[33, 'A'] = ( '210', '210')
        geno[34, 'A'] = ( '3012', '6901')
        geno[35, 'A'] = ( '218', '2501')
        geno[36, 'A'] = ( '101', '2501')
        geno[37, 'A'] = ( '7403', '201')
        geno[38, 'A'] = ( '2501', '3012')
        geno[39, 'A'] = ( '201', '201')
        geno[40, 'A'] = ( '3012', '3012')
        geno[41, 'A'] = ( '3204', '2501')
        geno[42, 'A'] = ( '201', '201')
        geno[43, 'A'] = ( '3012', '3012')
        geno[44, 'A'] = ( '6901', '218')
        geno[ 0, 'C'] = ( '307', '605')
        geno[ 1, 'C'] = ( '712', '102')
        geno[ 2, 'C'] = ( '804', '1202')
        geno[ 3, 'C'] = ( '1507', '307')
        geno[ 4, 'C'] = ( '1801', '102')
        geno[ 5, 'C'] = ( '1507', '605')
        geno[ 6, 'C'] = ( '307', '307')
        geno[ 7, 'C'] = ( '102', '712')
        geno[ 8, 'C'] = ( '1202', '2025')
        geno[ 9, 'C'] = ( '307', '605')
        geno[10, 'C'] = ( '102', '102')
        geno[11, 'C'] = ( '1202', '1202')
        geno[12, 'C'] = ( '307', '307')
        geno[13, 'C'] = ( '102', '102')
        geno[14, 'C'] = ( '1507', '307')
        geno[15, 'C'] = ( '307', '712')
        geno[16, 'C'] = ( '102', '102')
        geno[17, 'C'] = ( '1202', '1507')
        geno[18, 'C'] = ( '307', '307')
        geno[19, 'C'] = ( '102', '102')
        geno[20, 'C'] = ( '307', '307')
        geno[21, 'C'] = ( '1208', '307')
        geno[22, 'C'] = ( '307', '102')
        geno[23, 'C'] = ( '102', '307')
        geno[24, 'C'] = ( '605', '307')
        geno[25, 'C'] = ( '605', '605')
        geno[26, 'C'] = ( '1202', '1507')
        geno[27, 'C'] = ( '307', '307')
        geno[28, 'C'] = ( '102', '102')
        geno[29, 'C'] = ( '605', '1202')
        geno[30, 'C'] = ( '307', '307')
        geno[31, 'C'] = ( '712', '102')
        geno[32, 'C'] = ( '2025', '102')
        geno[33, 'C'] = ( '605', '102')
        geno[34, 'C'] = ( '3021', '605')
        geno[35, 'C'] = ( '605', '605')
        geno[36, 'C'] = ( '501', '408')
        geno[37, 'C'] = ( '605', '307')
        geno[38, 'C'] = ( '712', '3021')
        geno[39, 'C'] = ( '403', '307')
        geno[40, 'C'] = ( '307', '605')
        geno[41, 'C'] = ( '605', '1202')
        geno[42, 'C'] = ( '307', '307')
        geno[43, 'C'] = ( '102', '102')
        geno[44, 'C'] = ( '102', '307')
        geno[ 0, 'B'] = ( '307', '605')
        geno[ 1, 'B'] = ( '712', '102')
        geno[ 2, 'B'] = ( '804', '1202')
        geno[ 3, 'B'] = ( '1507', '307')
        geno[ 4, 'B'] = ( '1801', '102')
        geno[ 5, 'B'] = ( '1507', '605')
        geno[ 6, 'B'] = ( '307', '307')
        geno[ 7, 'B'] = ( '102', '712')
        geno[ 8, 'B'] = ( '1202', '2025')
        geno[ 9, 'B'] = ( '307', '605')
        geno[10, 'B'] = ( '102', '102')
        geno[11, 'B'] = ( '1202', '1202')
        geno[12, 'B'] = ( '307', '307')
        geno[13, 'B'] = ( '102', '102')
        geno[14, 'B'] = ( '1507', '307')
        geno[15, 'B'] = ( '307', '712')
        geno[16, 'B'] = ( '102', '102')
        geno[17, 'B'] = ( '1202', '1507')
        geno[18, 'B'] = ( '307', '307')
        geno[19, 'B'] = ( '102', '102')
        geno[20, 'B'] = ( '307', '307')
        geno[21, 'B'] = ( '1208', '307')
        geno[22, 'B'] = ( '307', '102')
        geno[23, 'B'] = ( '102', '307')
        geno[24, 'B'] = ( '605', '307')
        geno[25, 'B'] = ( '605', '605')
        geno[26, 'B'] = ( '1202', '1507')
        geno[27, 'B'] = ( '307', '307')
        geno[28, 'B'] = ( '102', '102')
        geno[29, 'B'] = ( '605', '1202')
        geno[30, 'B'] = ( '307', '307')
        geno[31, 'B'] = ( '712', '102')
        geno[32, 'B'] = ( '2025', '102')
        geno[33, 'B'] = ( '605', '102')
        geno[34, 'B'] = ( '3021', '605')
        geno[35, 'B'] = ( '605', '605')
        geno[36, 'B'] = ( '501', '408')
        geno[37, 'B'] = ( '605', '307')
        geno[38, 'B'] = ( '712', '3021')
        geno[39, 'B'] = ( '403', '307')
        geno[40, 'B'] = ( '307', '605')
        geno[41, 'B'] = ( '605', '1202')
        geno[42, 'B'] = ( '307', '307')
        geno[43, 'B'] = ( '102', '102')
        geno[44, 'B'] = ( '102', '307')

        pairs = geno.countPairs()
        max_haps = 2*sum(pairs)

        assert pairs == [4, 4, 4, 4, 4, 4, 1, 4, 2, 4, 1, 1, 1, 1, 4, 4, 1, 4, 1, 1, 1, 2, 4, 2, 2, 1, 4, 1, 1, 4, 1, 4, 4, 2, 4, 1, 4, 4, 4, 2, 2, 4, 1, 1, 4]
        assert max_haps == 236
