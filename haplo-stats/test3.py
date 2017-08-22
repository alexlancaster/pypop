#!/usr/bin/env python
import numpy
import math
import os.path
import sys
import itertools as it

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '..'))

from PyPop.Haplo import _compute_LD

# FIXME: these arrays have to be in same order
# this is fragile and probably needs changing in main code
haplos = numpy.array([['A1', 'B1'], ['A2', 'B1'], ['A1', 'B2'], ['A2', 'B2']],dtype='O')
freqs = numpy.array([0.3, 0.1, 0.1, 0.5]) 

_compute_LD(haplos, freqs, compute_ALD=True, debug=True)
