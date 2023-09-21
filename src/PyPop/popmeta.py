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

def main(argv=sys.argv):

  from PyPop import copyright_message, __version__ as version
  from PyPop.Meta import Meta
  from PyPop.CommandLineInterface import get_popmeta_cli

  datapath = os.path.join(sys.prefix, 'share', 'PyPop')

  parser = get_popmeta_cli(version=version, copyright_message=copyright_message)
  args = parser.parse_args(argv[1:])

  # find our exactly where the current executable is being run from
  popmetabinpath = os.path.dirname(os.path.realpath(sys.argv[0]))

  metaXSLTDirectory = args.xsldir
  dump_meta = args.output_meta
  TSV_output = args.generate_tsv
  prefixTSV = args.prefix_tsv
  PHYLIP_output = args.enable_phylip
  ihwg_output = args.enable_ihwg
  batchsize = args.batchsize
  outputDir = args.outputdir

  if PHYLIP_output:
    batchsize = 1   #  set batch size to 1

  if outputDir:
      if not outputDir.is_dir():
        sys.exit("'%s' is not a directory, please supply a valid output directory" % outputDir)

  # parse arguments
  xml_files = args.xmlfiles

  Meta(popmetabinpath=popmetabinpath,
       datapath=datapath,
       metaXSLTDirectory=metaXSLTDirectory,
       dump_meta=dump_meta,
       TSV_output=TSV_output,
       prefixTSV=prefixTSV,
       PHYLIP_output=PHYLIP_output,
       ihwg_output=ihwg_output,
       batchsize=batchsize,
       outputDir=outputDir,
       xml_files=xml_files)

if __name__ == "__main__":

  DIR = os.path.abspath(os.path.dirname(__file__))
  sys.path.insert(0, os.path.join(DIR, '..'))

  main()
