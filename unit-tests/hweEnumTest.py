#!/usr/bin/env python
import sys
import _HweEnum
matrix=[0,3,1,5,18,1,3,7,5,2]
_HweEnum.run_external(matrix,4)
print _HweEnum.get_p_value()
print _HweEnum.get_pr_observed()
print _HweEnum.get_diff_statistic_pvalue()
print _HweEnum.get_chen_statistic_pvalue()
