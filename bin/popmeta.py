#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2003, 2004. The Regents of the University of California
# (Regents) All Rights Reserved.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

# IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT,
# INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING
# LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS
# DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.

# REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING
# DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED "AS
# IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT,
# UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

import os, sys
from getopt import getopt, GetoptError

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '..'))

from PyPop.Meta import Meta

datapath = os.path.join(sys.prefix, 'share', 'PyPop')

usage_message = """Usage: popmeta.py [OPTION] INPUTFILES...

Processes INPUTFILES and generates 'meta'-analyses.  INPUTFILES are
expected to be the XML output files taken from runs of 'pypop'.  Will
skip any XML files that are not well-formed XML.

  -m, --meta-xslt=DIR     use specified directory to find XSLT
                           (default: '%s')
  -h, --help              show this message
  -d, --dump-meta         dump the meta output file to stdout, ignore xslt file
      --disable-R         disable generation of R *.dat file
      --enable-PHYLIP     enable generation of PHYLIP *.phy files
      --disable-ihwg      disable 13th workshop populationdata default headers,
                           take as-is
  -b, --batchsize=FACTOR  process in batches of size total/FACTOR rather than
                           all at once [mutually exclusive with --enable-PHYLIP]
  INPUTFILES  input XML files""" % datapath

try:
  opts, args =getopt(sys.argv[1:],"m:hdb:", ["meta-xslt=", "help", "dump-meta", "disable-R", "enable-PHYLIP", "disable-ihwg", "batchsize"])
except GetoptError:
  sys.exit(usage_message)

# find our exactly where the current executable is being run from
popmetabinpath = os.path.dirname(os.path.realpath(sys.argv[0]))

# set to empty, either user will specify a path or the system default
# will be used
metaXSLTDirectory = None

# output R tables by default
R_output=1

# don't output PHYLIP by default
PHYLIP_output=0

# by default, enable the 13th IHWG format headers
ihwg_output = 1

# by default process each file separately (batchsize=0)
batchsize = 0

# by default don't print out XML
dump_meta = 0

# parse options
for o, v in opts:
  if o in ("-m", "--meta-xslt"):
    metaXSLTDirectory = v
  elif o in ("-h", "--help"):
    sys.exit(usage_message)
  elif o in ("-d", "--dump-meta"):
    dump_meta = 1
  elif o=="--disable-R":
    R_output = 0
  elif o=="--enable-PHYLIP":
    PHYLIP_output = 1
  elif o=="--disable-ihwg":
    ihwg_output = 0
  elif o in("-b", "--batchsize"):
    batchsize = int(v)

if PHYLIP_output:
  # if set and not of size 1, exit
  if (batchsize > 1):
    sys.exit("processing in batches and enabling PHYLIP are mutually exclusive options\n" + usage_message)
  # otherwise set batch size to 1
  else:
    batchsize = 1

# parse arguments
files = args

# report usage message if no file arguments given
if not(files):
    sys.exit(usage_message)

Meta(popmetabinpath=popmetabinpath,
     datapath=datapath,
     metaXSLTDirectory=metaXSLTDirectory,
     dump_meta=dump_meta,
     R_output=R_output,
     PHYLIP_output=PHYLIP_output,
     ihwg_output=ihwg_output,
     batchsize=batchsize,
     files=files)
