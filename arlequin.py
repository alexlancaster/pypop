#! /usr/bin/env python

import sys
from Haplo import HaploArlequin

inputFilename = sys.argv[1]
arpFilename = sys.argv[2]

haploParse = HaploArlequin(idCol = 1,
                           arpFilename = arpFilename,
                           prefixCols = 6,
                           suffixCols = 1,
                           windowSize = 3,
                           debug=1)

f = open(inputFilename, 'r')
data = f.readlines()
f.close()

haploParse.outputArlequin(data)
haploParse.runArlequin()
