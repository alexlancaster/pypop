#! /usr/bin/env python

import sys
from Haplo import HaploArlequin

f = open(sys.argv[1], 'r')
data = f.readlines()

haploParse = HaploArlequin(idCol = 1,
                           prefixCols = 6,
                           suffixCols = 1,
                           windowSize = 3,
                           debug=1)

haploParse.outputArlequin(data)
