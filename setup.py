#!/usr/bin/env python
from distutils.core import setup, Extension
import os
# check to see if we are distributing from CVS
if os.path.isdir("CVS"):
    # if yes, generate a "ChangeLog"
    print "creating ChangeLog from CVS entries"
    os.system("rcs2log > ChangeLog")
    
setup (name = "PyPop",
       version = "0.1",
       description = "Population genetics statistics",
       url = "http://allele5.biol.berkeley.edu",
       maintainer = "Alex Lancaster",
       maintainer_email = "alexl@socrates.berkeley.edu",

       extra_path = 'PyPop',

       py_modules = ["Arlequin", "HardyWeinberg", "Utils",
                     "Haplo", "Homozygosity",  "ParseFile" ],
       scripts= ['pypop.py'],

       data_files=[('share/PyPop', ['ws-fields.dat', 'ws-output-fields.dat','ws-pop-fields.dat', 'ws-sample-fields.dat', 'text.xsl', 'config.ini'])],

# compile SWIG module
       
       ext_modules=[Extension("_Emhaplofreqmodule",
                              ["emhaplofreq/emhaplofreq_wrap.i",
                               "emhaplofreq/emhaplofreq.c"],
                              include_dirs=["emhaplofreq"]),

                    Extension("Gthwe", ["gthwe/cal_const.c",
                              "gthwe/cal_n.c", "gthwe/cal_prob.c",
                              "gthwe/check_file.c",
                              "gthwe/do_switch.c", 
                              "gthwe/new_rand.c",
                              "gthwe/ln_p_value.c",
                              "gthwe/to_calculate_log.c",
                              "gthwe/print_data.c",
                              "gthwe/random_choose.c",
                              "gthwe/read_data.c",
                              "gthwe/select_index.c",
                              "gthwe/stamp_time.c",
                              "gthwe/test_switch.c"],
                              include_dirs=["gthwe"])
                    ]
       )

