#!/usr/bin/env python
from distutils.core import setup
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

       data_files=[('share/PyPop', ['ws-fields.dat', 'ws-output-fields.dat','ws-pop-fields.dat', 'ws-sample-fields.dat', 'text.xsl', 'config.ini'])]

       )

