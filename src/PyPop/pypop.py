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

import sys, os, time
from glob import glob
from configparser import ConfigParser
from pathlib import Path

def main(argv=sys.argv):

    from PyPop import platform_info
    from PyPop.CommandLineInterface import get_pypop_cli
    from PyPop import copyright_message, __version__ as version
    from PyPop.Main import Main, getConfigInstance, getUserFilenameInput, checkXSLFile
    from PyPop.Meta import Meta

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


    ######################################################################
    # END: CHECK PATHS and FILEs
    ######################################################################

    ######################################################################
    # BEGIN: generate message texts
    ######################################################################

    interactive_message = """PyPop: Python for Population Genomics (%s)
%s
%s

You may redistribute copies of PyPop under the terms of the
GNU General Public License.  For more information about these
matters, see the file named COPYING.
    """ % (version, platform_info, copyright_message)

    ######################################################################
    # END: generate message texts
    ######################################################################

    ######################################################################
    # BEGIN: parse command line options
    ######################################################################

    parser = get_pypop_cli(version=version, copyright_message=copyright_message)
    args = parser.parse_args(argv[1:])

    # IHWG and PHYLIP output only make sense if '-t' also supplied
    if (args.enable_ihwg or args.enable_phylip or args.prefix_tsv) and (not args.enable_tsv):
        parser.error('--enable-iwhg, --enable-phylip or --prefix_tsv can only be used if --generate-tsv also supplied')

    if args.outputdir:
        if not args.outputdir.is_dir():
          parser.error("'%s' is not a directory, please supply a valid output directory" % args.outputdir)

    configFilename = args.config
    xslFilename = args.xsl
    debugFlag = args.debug
    interactiveFlag = args.interactive
    generateTSV = args.enable_tsv
    prefixTSV = args.prefix_tsv
    testMode = args.testmode
    fileList = args.filelist
    outputDir = args.outputdir
    popFilenames = args.popfiles      
    ihwg_output = args.enable_ihwg
    PHYLIP_output = args.enable_phylip

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
        print("pypopbinpath", pypopbinpath)
        print("binpath", binpath)
        print("datapath", datapath)


      try:
        from importlib.resources import files
        mypath = files('PyPop.xslt')
      except (ModuleNotFoundError, ImportError):  # fallback to using backport if not found
        from importlib_resources import files
        mypath = files('PyPop.xslt').joinpath('')

      xslFilenameDefault = checkXSLFile('text.xsl', mypath, \
                                        abort=False, debug=debugFlag)

      if xslFilenameDefault == None:
        # otherwise use heuristics for XSLT transformation file 'text.xsl'
        # check child directory 'xslt/' first
        xslFilenameDefault = checkXSLFile('text.xsl', pypopbinpath, \
                                          'xslt', debug=debugFlag)
        # if not found  check sibling directory '../PyPop/xslt/'
        if xslFilenameDefault == None:
          xslFilenameDefault = checkXSLFile('text.xsl', pypopbinpath, \
                                            '../PyPop/xslt', debug=debugFlag)

    ######################################################################
    # END: parse command line options
    ######################################################################

    # call as a command-line application

    # start by assuming an empty list of filenames
    fileNames = []

    if interactiveFlag:
      # run in interactive mode, requesting input from user

      # Choices made in previous runs of PyPop will be stored in a file
      # called '.pypoprc', stored the user's home directory
      # (i.e. $HOME/.pypoprc) so that in subsequent invocations of the
      # script it will use the previous choices as defaults.

      # The '.pypoprc' file will be created if it does not previously
      # exist.  The format of this file is identical to the ConfigParser
      # format (i.e. the .ini file format).

      pypoprcFilename = Path.home() / '.pypoprc'
        
      pypoprc = ConfigParser()

      if os.path.isfile(pypoprcFilename):
        pypoprc.read(pypoprcFilename)
        configFilename = pypoprc.get('Files', 'config')
        fileName = pypoprc.get('Files', 'pop')
      else:
        configFilename = 'Choose your .ini file (no default)'
        fileName = 'Choose your .pop file (no default)'          

      print(interactive_message)

      from tkinter import Tk
      from tkinter.filedialog import askopenfilename
      from _tkinter import TclError

      # read user input for both filenames
      try:
          Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

          print("""Select both an '.ini' configuration file and a '.pop' file via the
system file dialog.""")

          
          configFilename = askopenfilename(title="Please select a PyPop configuration file",
                                           initialfile=str(Path(configFilename).name),
                                           initialdir=str(Path(configFilename).parent),
                                           filetypes=[(".ini files", "*.ini"), ("All Files", "*.*")])

          fileNames.append(askopenfilename(title="Please select a population (.pop) file",
                                           initialfile=str(Path(fileName).name),
                                           initialdir=str(Path(fileName).parent),
                                           filetypes=[(".pop files", "*.pop"), ("All Files", "*.*")]))

      except TclError:  # if GUI failed, fallback to command-line

          print("""To accept the default in brackets for each filename, simply press
return for each prompt.""")

          configFilename = getUserFilenameInput("config", configFilename)
          fileNames.append(getUserFilenameInput("population", fileName))
      
      print("PyPop is processing %s ..." % fileNames[0])

    else:   
      # non-interactive mode: run in 'batch' mode

      if fileList:
        # if we are providing the filelist
        # use list from file as list to check
        #li = [f.strip('\n') for f in open(fileList).readlines()]
        li = [f.strip('\n') for f in fileList.readlines()]
        fileList.close() # make sure we close it
      elif popFilenames:
        # check number of arguments, must be at least one, but can be more
        # use args as list to check
        li = popFilenames
      # otherwise bail out with error
      else:
        sys.exit("ERROR: neither a list of files, nor a file containing a list was provided")
          
      # loop through all arguments in li, appending to list of files to
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
    config = getConfigInstance(configFilename, altpath)

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
                         xslFilename=xslFilename,
                         xslFilenameDefault=xslFilenameDefault,
                         outputDir=outputDir,
                         version=version,
                         testMode=testMode)

      xmlOutPaths.append(application.getXmlOutPath())
      txtOutPaths.append(application.getTxtOutPath())

    if generateTSV:

      if PHYLIP_output:
        # if we're doing PHYLIP output, need to process all XML at once
        batchsize = 1
      else:
        # otherwise we can do them one-by-one
        batchsize = len(xmlOutPaths)

      print("Generating TSV (.dat) files...")
      Meta(popmetabinpath=pypopbinpath,
           datapath=datapath,
           metaXSLTDirectory=None,
           dump_meta=False,
           TSV_output=True,
           prefixTSV=prefixTSV,
           PHYLIP_output=PHYLIP_output,
           ihwg_output=ihwg_output,
           batchsize=batchsize,
           outputDir=outputDir,
           xml_files=xmlOutPaths)

    if interactiveFlag:

      print("PyPop run complete!")
      print("XML output(s) can be found in: ",  xmlOutPaths)
      print("Plain text output(s) can be found in: ",  txtOutPaths)

      # update .pypoprc file

      if pypoprc.has_section('Files') != 1:
        pypoprc.add_section('Files')

      pypoprc.set('Files', 'config', os.path.abspath(configFilename))
      pypoprc.set('Files', 'pop', os.path.abspath(fileNames[0]))
      pypoprc.write(open(pypoprcFilename, 'w'))

def main_interactive(argv=sys.argv):
    argv.append("-i")
    main(argv)
    input("Press Enter to exit...")
      
if __name__ == "__main__":

    DIR = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(DIR, '..'))
    sys.path.insert(0, os.path.join(DIR, '../src'))

    main()
