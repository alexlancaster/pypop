#!/usr/bin/env python
from distutils.core import setup, Extension
from distutils.file_util import copy_file

import sys, os, string

# distutils doesn't currently have an explicit way of setting CFLAGS,
# it takes CFLAGS from the environment variable of the same name, so
# we set the environment to emulate that.
os.environ['CFLAGS'] = '-funroll-loops'

# if and only if we are making a source distribution, then regenerate
# ChangeLog
if sys.argv[1] == 'sdist':
    # first check to see if we are distributing from CVS
    if os.path.isdir("CVS"):
        # if yes, generate a "ChangeLog"
        print "creating ChangeLog from CVS entries"
        os.system("rcs2log -u \"single:Richard Single:single@allele5.biol.berkeley.edu\" -u \"mpn:Mark Nelson:mpn@alleleb.biol.berkeley.edu\" -u \"alex:Alex Lancaster:alexl@socrates.berkeley.edu\" -u \"diogo:Diogo Meyer:diogo@allele5.biol.berkeley.edu\" > ChangeLog")
        if os.path.isfile('VERSION') == 0:
            sys.exit("before distributing, please create a VERSION file!")

# get version from the file VERSION
if os.path.isfile('VERSION'):
  f = open('VERSION')
  version = string.strip(f.readline())
# check if it's a development version (i.e. in CVS tree, use this)
elif os.path.isfile('DEVEL_VERSION'):
  version = 'DEVEL_VERSION'
else:
  sys.exit("Could not find VERSION file!  Exiting...")

def Ensure_Scripts(scripts):
    """Strips '.py' from installed scripts.

    This is a hack and needs work.
    """
    for script in scripts:
        suffix = script[-3:]
        prefix = script[:-3]
        if suffix == '.py':
            #if sys.argv[1] == 'install':
            copy_file(script,prefix,preserve_mode=0)
            scripts[scripts.index(script)] = prefix
    return scripts

# data files to install
data_file_paths = ['config.ini', 'VERSION']
# xslt files are in a subdirectory
xslt_files = ['xslt' + os.sep + i + '.xsl' for i in ['text', 'html', 'lib', 'common', 'meta', 'summary', 'sort-by-locus']]
data_file_paths.extend(xslt_files)

setup (name = "PyPop",
       version = version,
       description = "Population genetics statistics",
       url = "http://allele5.biol.berkeley.edu",
       maintainer = "Alex Lancaster",
       maintainer_email = "alexl@socrates.berkeley.edu",

       extra_path = 'PyPop',

       py_modules = ["Arlequin", "HardyWeinberg", "Utils",
                     "Haplo", "Homozygosity",  "ParseFile", "Filter"],
       scripts= Ensure_Scripts(['pypop.py']),

       data_files=[('share/PyPop', data_file_paths)],

# compile SWIG module
       
       ext_modules=[Extension("_Emhaplofreqmodule",
                              ["emhaplofreq/emhaplofreq_wrap.i",
                               "emhaplofreq/emhaplofreq.c"],
                              include_dirs=["emhaplofreq"],
                              define_macros=[('fprintf', 'pyfprintf'),
                                             ('DEBUG', '0'),
                                             ('EXTERNAL_MODE', '1'),
                                             ('XML_OUTPUT', '1')]
                              ),

                    Extension("_Gthwemodule",
                              [ "gthwe/gthwe_wrap.i",
                                "gthwe/hwe.c",
                                "gthwe/cal_const.c",
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
                              include_dirs=["gthwe"],
                              define_macros=[('fprintf', 'pyfprintf'),
                                             ('XML_OUTPUT', '1'),
                                             ('SUPPRESS_ALLELE_TABLE', '1'),
                                             ('MAX_ALLELE', '35'),
                                             ('LENGTH',
                                              'MAX_ALLELE*(MAX_ALLELE+1)/2')
                                             ]
                              )
                    ]
       )

