#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2003-2007. The Regents of the University of California (Regents)
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

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '..'))

import PyPop

######################################################################
# BEGIN: CHECK PATHS and FILEs
######################################################################

# create system-level defaults relative to where python is
# installed, e.g. if python is installed in sys.prefix='/usr'
# we look in /usr/share/pypop, /usr/bin/pypop etc.
# FIXME: this should be removed
datapath = os.path.join(sys.prefix, 'share', 'pypop')
binpath = os.path.join(sys.prefix, 'bin')
altpath = os.path.join(datapath, 'config.ini')

# find our exactly where the current pypop is being run from
pypopbinpath = os.path.dirname(os.path.realpath(sys.argv[0]))

version = PyPop.__version__
pkgname = PyPop.__pkgname__
  
######################################################################
# END: CHECK PATHS and FILEs
######################################################################

######################################################################
# BEGIN: generate message texts
######################################################################

copyright_message = """Copyright (C) 2003-2005 Regents of the University of California
This is free software.  There is NO warranty; not even for
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."""

usage_message = """Usage: pypop [OPTION]... [INPUTFILE]...
Process and run population genetics statistics on one or more INPUTFILEs.
Expects to find a configuration file called 'config.ini' in the
current directory or in %s.

  -l, --use-libxslt    filter XML via XSLT using libxslt (default)
  -s, --use-4suite     filter XML via XSLT using 4Suite
  -x, --xsl=FILE       use XSLT translation file FILE
  -h, --help           show this message
  -c, --config=FILE    select alternative config file
  -d, --debug          enable debugging output (overrides config file setting)
  -i, --interactive    run in interactive mode, prompting user for file names
  -g, --gui            run GUI (currently disabled)
  -o, --outputdir=DIR  put output in directory DIR
  -f, --filelist=FILE  file containing list of files (one per line) to process
                        (mutually exclusive with supplying INPUTFILEs)
      --generate-tsv   generate TSV output files (aka run 'popmeta')
  -V, --version        print version of PyPop
  -m, --testmode       run PyPop in test mode for unit testing
  
  INPUTFILE   input text file""" % altpath

version_message = """pypop %s
%s""" % (version, copyright_message)

interactive_message = """PyPop: Python for Population Genomics (%s)
%s

You may redistribute copies of PyPop under the terms of the
GNU General Public License.  For more information about these
matters, see the file named COPYING.

To accept the default in brackets for each filename, simply press
return for each prompt.
""" % (version, copyright_message)

######################################################################
# END: generate message texts
######################################################################

######################################################################
# BEGIN: parse command line options
######################################################################

from getopt import getopt, GetoptError
from glob import glob
from ConfigParser import ConfigParser
from PyPop.Main import getUserFilenameInput, checkXSLFile

try:
  opts, args =getopt(sys.argv[1:],"mlsigc:hdx:f:o:V", ["testmode", "use-libxslt", "use-4suite", "interactive", "gui", "config=", "help", "debug", "xsl=", "filelist=", "outputdir=", "version", "generate-tsv"])
except GetoptError:
  sys.exit(usage_message)

# default options
use_libxsltmod = 0
use_FourSuite = 0
configFilename = 'config.ini'
specifiedConfigFile = 0
debugFlag = 0
interactiveFlag = 0
guiFlag = 0
xslFilename = None
outputDir = None
fileList = None
generateTSV = 0
testMode = False

# parse options
for o, v in opts:
  if o in ("-l", "--use-libxslt"):
    use_libxsltmod = 1
  elif o in ("-s", "--use-4suite"):
    use_FourSuite = 1
  elif o in ("-c", "--config"):
    configFilename = v
    specifiedConfigFile = 1
  elif o in ("-x", "--xsl"):
    xslFilename = v
  elif o in ("-d", "--debug"):
    debugFlag = 1
  elif o in ("-h", "--help"):
    sys.exit(usage_message)
  elif o in ("-i", "--interactive"):
    interactiveFlag = 1
  elif o in ("-g", "--gui"):
    guiFlag = 1
  elif o in ("--generate-tsv"):
    generateTSV = 1
  elif o in ("-f", "--filelist"):
    if os.path.isfile(v):
      fileList = v
    else:
      sys.exit("'%s' is not a file, please supply a valid file" % v)
  elif o in ("-o", "--outputdir"):
    if os.path.isdir(v):
      outputDir = v
    else:
      sys.exit("'%s' is not a directory, please supply a valid output directory" % v)
  elif o in ("-V", "--version"):
    sys.exit(version_message)
  elif o in ("-m", "--testmode"):
    testMode = True
    
# if neither option is set explicitly, use libxslt python wrappers
if not (use_libxsltmod or use_FourSuite):
  use_libxsltmod = 1

# heuristics for default 'text.xsl' XML -> text file

if xslFilename:
  # first, check the command supplied filename first, return canonical
  # location and abort if it is not found immediately
  xslFilename = checkXSLFile(xslFilename, abort=True, debug=debugFlag)
  xslFilenameDefault = None

else:
  # if not supplied, use heuristics to set a default, heuristics may
  # return a valid path or None (but the value found here is always
  # overriden by options in the .ini file)

  if debugFlag:
    print "pypopbinpath", pypopbinpath
    print "binpath", binpath
    print "datapath", datapath

  from pkg_resources import Requirement, resource_filename, DistributionNotFound

  try:
    mypath = resource_filename(Requirement.parse(pkgname), 'share/pypop')
    xslFilenameDefault = checkXSLFile('text.xsl', mypath, \
                                    abort=False, debug=debugFlag)
  except DistributionNotFound:
    xslFilenameDefault = None

  if xslFilenameDefault == None:
    # otherwise use heuristics for XSLT transformation file 'text.xsl'
    # check child directory 'xslt/' first
    xslFilenameDefault = checkXSLFile('text.xsl', pypopbinpath, \
                                      'xslt', debug=debugFlag)
    # if not found  check sibling directory '../xslt/'
    if xslFilenameDefault == None:
      xslFilenameDefault = checkXSLFile('text.xsl', pypopbinpath, \
                                 '../xslt', debug=debugFlag)

######################################################################
# END: parse command line options
######################################################################

if guiFlag:
  # instantiate PyPop GUI

  if 1:
    sys.exit("GUI support is currently disabled... sorry")
  else:
    #from wxPython.wx import wxPySimpleApp
    #from GUIApp import MainWindow
  
    app = wxPySimpleApp()
    frame = MainWindow(None, -1, "PyPop",
                       datapath = datapath,
                       altpath = altpath,
                       debugFlag = debugFlag)
    app.MainLoop()

else:
  # call as a command-line application

  # start by assuming an empty list of filenames
  fileNames = []

  if interactiveFlag:
    # run in interactive mode, requesting input from user

    # Choices made in previous runs of PyPop will be stored in a file
    # called '.pypoprc', stored the user's home directory
    # (i.e. $HOME/.pypoprc) so that in subsequent invocations of the
    # script it will use the previous choices as defaults.

    # For systems without a concept of a $HOME directory (i.e.
    # Windows), it will look for .pypoprc in the current directory.

    # The '.pypoprc' file will be created if it does not previously
    # exist.  The format of this file is identical to the ConfigParser
    # format (i.e. the .ini file format).
    
    if os.environ['HOME']:
      pypoprcFilename = os.path.join(os.environ['HOME'],'.pypoprc')
    else:
      pypoprcFilename = '.pypoprc'

    pypoprc = ConfigParser()
      
    if os.path.isfile(pypoprcFilename):
      pypoprc.read(pypoprcFilename)
      configFilename = pypoprc.get('Files', 'config')
      fileName = pypoprc.get('Files', 'pop')
    else:
      configFilename = 'config.ini'
      fileName = 'no default'

    print interactive_message
    
    # read user input for both filenames
    configFilename = getUserFilenameInput("config", configFilename)
    fileNames.append(getUserFilenameInput("population", fileName))

    print "PyPop is processing %s ..." % fileNames[0]
    
  else:   
    # non-interactive mode: run in 'batch' mode

    if fileList and len(args) > 0:
      sys.exit("--filelist (-f) option is mutually exclusive with INPUTFILE")
    elif fileList:
      # if we are providing the filelist, don't check number of args
      # use list from file as list to check
      li = [string.strip(f) for f in open(fileList).readlines()]
    elif len(args) > 0:
      # check number of arguments, must be at least one, but can be more
      # use args as list to check
      li = args
    # otherwise bail out with error
    else:
      sys.exit(usage_message)

    # loop through all arguments in , appending to list of files to
    # process, ensuring we expand any Unix-shell globbing-style
    # arguments
    for fileName in li:
      globbedFiles = glob(fileName)
      if len(globbedFiles) == 0:
        # if no files were found for that glob, please exit and warn
        # the user
        sys.exit("Couldn't find file(s): %s" % fileName)
      else:
        fileNames.extend(globbedFiles)

  # parse config file
  from PyPop.Main import Main, getConfigInstance
  config = getConfigInstance(configFilename, altpath, usage_message)

  xmlOutPaths = []
  txtOutPaths = []
  # loop through list of filenames passed, processing each in turn
  for fileName in fileNames:

    # parse out the parts of the filename
    #baseFileName = os.path.basename(fileName)

    application = Main(config=config,
                       debugFlag=debugFlag,
                       fileName=fileName,
                       datapath=datapath,
                       use_libxsltmod=use_libxsltmod,
                       use_FourSuite=use_FourSuite,
                       xslFilename=xslFilename,
                       xslFilenameDefault=xslFilenameDefault,
                       outputDir=outputDir,
                       version=version,
                       testMode=testMode)

    xmlOutPaths.append(application.getXmlOutPath())
    txtOutPaths.append(application.getTxtOutPath())

  if generateTSV:
    from PyPop.Meta import Meta
    
    print "Generating TSV (.dat) files..."
    Meta(popmetabinpath=pypopbinpath,
         datapath=datapath,
         metaXSLTDirectory=None,
         dump_meta=0,
         R_output=1,
         PHYLIP_output=0,
         ihwg_output=1,
         batchsize=len(xmlOutPaths),
         files=xmlOutPaths)

  if interactiveFlag:

    print "PyPop run complete!"
    print "XML output(s) can be found in: ",  xmlOutPaths
    print "Plain text output(s) can be found in: ",  txtOutPaths

    # update .pypoprc file

    if pypoprc.has_section('Files') != 1:
      pypoprc.add_section('Files')
      
    pypoprc.set('Files', 'config', os.path.abspath(configFilename))
    pypoprc.set('Files', 'pop', os.path.abspath(fileNames[0]))
    pypoprc.write(open(pypoprcFilename, 'w'))

