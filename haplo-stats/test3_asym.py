#!/usr/bin/env python
import numpy
import math
import os
import sys
import itertools as it

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '..'))

from PyPop.Haplo import _compute_LD

#pop locus1 allele1 locus2 allele2 haplo.freq 
#ex1      A      01      B      01        0.3 
#ex1      A      02      B      01        0.0 
#ex1      A      01      B      02        0.0  
#ex1      A      02      B      02        0.5 
#ex1      A      01      B      03        0.0 
#ex1      A      02      B      03        0.2  

# FIXME: these arrays have to be in same order
# this is fragile and probably needs changing in main code
haplos = numpy.array([['A1', 'B1'], ['A2', 'B1'], ['A1', 'B2'], ['A2', 'B2'], ['A1', 'B3'], ['A2', 'B3']],dtype='O')
freqs = numpy.array([0.3, 0.0, 0.0, 0.5, 0.0, 0.2]) 

_compute_LD(haplos, freqs, compute_ALD=True, debug=True)
