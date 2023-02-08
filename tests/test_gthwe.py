#!/usr/bin/env python
import base
import sys
from PyPop import _Gthwe
import pytest

@pytest.mark.skip(reason="test is currently incomplete and doesn't run on all platforms")
def test_gthwe():
    f = open('out.gthwe', 'w')
    a = [0, 3, 1 ,5, 18, 1, 3, 7, 5, 2]
    n = [0]*35
    step = 2000
    group = 1000
    size = 1000
    _Gthwe.run_data(a,n,4,45,step,group,size,'LocusName',f, 0)
    f.close()

    # FIXME, incomplete: need to add an assert function
