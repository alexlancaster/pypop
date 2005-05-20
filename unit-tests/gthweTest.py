#!/usr/bin/env python
import sys
import _Gthwe
f = sys.stdout
#f = open('out.gthwe', 'w')
a = [0, 3, 1 ,5, 18, 1, 3, 7, 5, 2]
n = [0]*35
step = 2000
group = 1000
size = 1000
_Gthwe.run_data(a,n,4,45,step,group,size,'LocusName',f)
_Gthwe.run_data(a,n,4,45,step,group,size,'LocusName',f)
_Gthwe.run_data(a,n,4,45,step,group,size,'LocusName',f)
#f.close()

