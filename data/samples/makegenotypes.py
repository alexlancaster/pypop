#!/usr/bin/env python
import sys, string

f=file(sys.argv[1])
#type=sys.argv[2]

alleles=string.split(f.readline())
matrixSize=len(alleles)

genotypes = {}

# works for upper-triangular matrix
for i in range(0,matrixSize):
    counts=string.split(f.readline())
    #print counts
    for count in range(0,len(counts)):
        name="%s:%s" % (alleles[i], alleles[i+count])
        genotypes[name] = int(counts[count])
  

# output .pop file

#print genotypes

for genotype in genotypes.keys():
    for count in range(0, genotypes[genotype]):
        pair = string.split(genotype, ':')
        print "%s\t%s" % (pair[0], pair[1])


#a = [[1236],
#     [120,3],
#     [18,0,0],
#     [982,55,7,249],
#     [32,1,0,12,0],
#     [2582,132,20,1162,29,1312],
#     [6,0,0,4,0,4,0],
#     [2,0,0,0,0,0,0,0],
#     [115,5,2,53,1,149,0,0,4]]

# matrixSize = len(a)

# for i in range(0,matrixSize):
#     for j in range(0,i+1):
#         #print i,j
#         #print a[i][j]
#         for g in range(0,a[i][j]):
#             print "A%d\tA%d" % (i+1,j+1)
