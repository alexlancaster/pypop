#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2003. The Regents of the University of California (Regents)
# All Rights Reserved.

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

"""Python population genetics statistics.
"""

import sys, os, string, time

datapath = os.path.join(sys.prefix, 'share', 'PyPop')
altpath = os.path.join(datapath, 'config.ini')

usage_message = """Usage: pypop [OPTION] INPUTFILE
Process and run population genetics statistics on an INPUTFILE.
Expects to find a configuration file called 'config.ini' in the
current directory or in %s.

  -l, --use-libxslt    filter XML via XSLT using libxslt (default)
  -s, --use-4suite     filter XML via XSLT using 4Suite
  -h, --help           show this message
  -c, --config=FILE    select alternative config file
  -d, --debug          enable debugging output (overrides config file setting)
  -g, --gui            run GUI (warning *very* experimental)
  
  INPUTFILE   input text file""" % altpath

from getopt import getopt, GetoptError

try:
  opts, args =getopt(sys.argv[1:],"lsgc:hd", ["use-libxslt", "use-4suite", "gui", "config=", "help", "debug"])
except GetoptError:
  sys.exit(usage_message)

# default options
use_libxsltmod = 0
use_FourSuite = 0
configFilename = 'config.ini'
specifiedConfigFile = 0
debugFlag = 0
guiFlag =0

# parse options
for o, v in opts:
  if o in ("-l", "--use-libxslt"):
    use_libxsltmod = 1
  elif o in ("-s", "--use-4suite"):
    use_FourSuite = 1
  elif o in ("-c", "--config"):
    configFilename = v
    specifiedConfigFile = 1
  elif o in ("-d", "--debug"):
    debugFlag = 1
  elif o in ("-h", "--help"):
    sys.exit(usage_message)
  elif o in ("-g", "--gui"):
    guiFlag = 1

# if neither option is set explicitly, use libxslt python wrappers
if not (use_libxsltmod or use_FourSuite):
  use_libxsltmod = 1

if guiFlag:
  # instantiate PyPop GUI

  from wxPython.wx import wxPySimpleApp
  from GUIApp import MainWindow
  
  app = wxPySimpleApp()
  frame = MainWindow(None, -1, "PyPop",
                     datapath = datapath,
                     altpath = altpath,
                     debugFlag = debugFlag)
  app.MainLoop()

else:
  # call as a command-line application
  
  # check number of arguments
  if len(args) != 1:
    sys.exit(usage_message)

  # parse arguments
  fileName = args[0]

  # parse out the parts of the filename
  baseFileName = os.path.basename(fileName)
  prefixFileName = string.split(baseFileName, ".")[0]

  from Main import Main, getConfigInstance

  config = getConfigInstance(configFilename, altpath, usage_message)

  application = Main(config=config,
                     debugFlag=debugFlag,
                     fileName=fileName,
                     datapath=datapath,
                     use_libxsltmod=use_libxsltmod,
                     use_FourSuite=use_FourSuite)

