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

import os, sys
from getopt import getopt, GetoptError

# don't use libxml/libxslt bindings for the moment, aren't working with
# exslt extensions nor on all platforms.

import libxml2
import libxslt

libxslt.registerAllExtras()
    
## force the libxml2 processor to generate DOM trees compliant with
## the XPath data model.
libxml2.lineNumbersDefault(1)

## set libxml2 to substitute the entities in the document by default...
libxml2.substituteEntitiesDefault(1)

def _translate_string_to(xslFilename, inString, outFile, params=None):
    # do the transformation
    
    # parse the stylesheet file
    styledoc = libxml2.parseFile(xslFilename)

    # setup the stylesheet instance
    style = libxslt.parseStylesheetDoc(styledoc)

    # parse the inline generated XML file
    doc = libxml2.parseDoc(inString)

    # apply the stylesheet instance to the document instance
    result = style.applyStylesheet(doc, None)
    
    style.saveResultToFilename(outFile, result, 0)

    # use to dump directly to a string, problem is that it insists on
    # outputting an XML declaration "<?xml ...?>", can't seem to
    # suppress this
    # outString = result.serialize()

    # free instances
    result.freeDoc()
    style.freeStylesheet()
    doc.freeDoc()
    #return outString
    
def translate_string_to_stdout(xslFilename, inString, params=None):
    # save result to stdout "-"
    _translate_string_to(xslFilename, inString, "-", params)

def translate_string_to_file(xslFilename, inString, outFile, params=None):
    _translate_string_to(xslFilename, inString, outFile, params)

def _translate_file_to(xslFilename, inFile, outFile, params=None):
    
    # parse the stylesheet file
    styledoc = libxml2.parseFile(xslFilename)

    # setup the stylesheet instance
    style = libxslt.parseStylesheetDoc(styledoc)

    # parse the inline generated XML file
    doc = libxml2.parseFile(inFile)

    # apply the stylesheet instance to the document instance
    result = style.applyStylesheet(doc, params)
    
    style.saveResultToFilename(outFile, result, 0)

    # free instances
    result.freeDoc()
    style.freeStylesheet()
    doc.freeDoc()

def translate_file_to_stdout(xslFilename, inFile, params=None):
    _translate_file_to(xslFilename, inFile, "-", params)

def translate_file_to_file(xslFilename, inFile, outFile, params=None):
    _translate_file_to(xslFilename, inFile, outFile, params)

datapath = os.path.join(sys.prefix, 'share', 'PyPop')

usage_message = """Usage: popmeta.py [OPTION] INPUTFILES...

Processes INPUTFILES and generates 'meta'-analyses.  INPUTFILES are
expected to be the XML output files taken from runs of 'pypop'.  Will
skip any XML files that are not well-formed XML.

  -m, --meta-xslt=DIR     use specified directory to find XSLT
                            (default: '%s')
  -h, --help              show this message
  -d, --dump-meta         dump the meta output file to stdout, ignore xslt file
      --no-R              don't generate R *.dat files 
      --no-PHYLIP         don't generate PHYLIP *.phy files

  INPUTFILES  input XML files""" % datapath

try:
  opts, args =getopt(sys.argv[1:],"m:hd", ["meta-xslt=", "help", "dump-meta", "no-R", "no-PHYLIP"])
except GetoptError:
  sys.exit(usage_message)

metaXSLTDirectory= datapath
dump_meta = 0
R_output=1
PHYLIP_output=1

# parse options
for o, v in opts:
  if o in ("-m", "--meta-xslt"):
    metaXSLTDirectory = v
  elif o in ("-h", "--help"):
    sys.exit(usage_message)
  elif o in ("-d", "--dump-meta"):
    dump_meta = 1
  elif o=="--no-R":
    R_output = 0
  elif o=="--no-PHYLIP":
    PHYLIP_output = 0

# parse arguments
files = args

# report usage message if no file arguments given
if not(files):
    sys.exit(usage_message)

wellformed_files = []

# check each file for "well-formedness" using xmllint (with '--noout'
# command-line option) in libxslt package, if stderr is anything but
# empty (indicating non-well-formedness), report an error on this
# file, and skip this file in the meta analysis 
for f in files:
    
    #stdin, stdout, stderr  = os.popen3("xmllint --noout %s" % f)
    #lines = stderr.readlines()
    #if len(lines) == 0:
    try:
        libxml2.parseFile(f)
        wellformed_files.append(f)
    except:
        print "%s is not well-formed XML:" % f
        print "  probably a problem with analysis not completing, skipping in meta analysis!"


# generate a metafile XML wrapper

# open doctype
meta_string="<!DOCTYPE meta [\n"
entities = ""
includes = ""

# loop through and create the meta.xml file *only* for the well-formed
# XML files
for f in wellformed_files:
    base = os.path.basename(f)
    ent = "ENT" + base
    entities += "<!ENTITY %s SYSTEM \"%s\">\n" % (ent, f)
    includes += "&%s;\n" % ent

# put entities after doctype
meta_string += entities

# close doctype
meta_string += "]>\n"

# open tag
meta_string += "<meta>\n"

# include content
meta_string += includes

# close tag
meta_string += "</meta>"

if dump_meta == 1:
    print meta_string
else:
    f = open('meta.xml', 'w')
    f.write(meta_string)
    f.close()
    translate_string_to_file(os.path.join(metaXSLTDirectory, 'sort-by-locus.xsl'), meta_string, 'sorted-by-locus.xml')
    #translate_file_to_stdout(os.path.join(metaXSLTDirectory, 'meta-to-r.xsl'), 'sorted.xml')
    # have to resort to command-line version because the Python bindings
    # don't understand how to load the exslt extensions in libxslt yet
    # that the meta-to-r.xsl stylesheet uses

    # generate the data file 'sorted-by-locus.xml' of pops sorted by locus
    #os.popen("xsltproc %s %s > %s" % (os.path.join(metaXSLTDirectory, 'sort-by-locus.xsl'), 'meta.xml', 'sorted-by-locus.xml'))

    # using the '{allele,haplo}list-by-{locus,group}.xml' files implicitly:

    if R_output:
        # generate all data output in formats for R
        translate_file_to_stdout(os.path.join(metaXSLTDirectory, 'meta-to-r.xsl'), 'meta.xml')
        #os.popen("xsltproc %s %s 2> log.out" % (os.path.join(metaXSLTDirectory, 'meta-to-r.xsl'), 'meta.xml'))

    if PHYLIP_output:
        # use 'sorted-by-locus.xml' to generate a list of unique alleles
        # 'allelelist-by-locus.xml' for each locus across all the
        # populations in the set of XML files passed
        translate_file_to_file(os.path.join(metaXSLTDirectory, 'allelelist-by-locus.xsl'), 'sorted-by-locus.xml', 'allelelist-by-locus.xml')
        #os.popen("xsltproc %s %s > %s" % (os.path.join(metaXSLTDirectory, 'allelelist-by-locus.xsl'), 'sorted-by-locus.xml', 'allelelist-by-locus.xml'))

        # similarly, generate a unique list of haplotypes
        # 'haplolist-by-locus.xml'
        translate_file_to_file(os.path.join(metaXSLTDirectory, 'haplolist-by-group.xsl'), 'meta.xml', 'haplolist-by-group.xml')
        #os.popen("xsltproc %s %s > %s" % (os.path.join(metaXSLTDirectory, 'haplolist-by-group.xsl'), 'meta.xml', 'haplolist-by-group.xml'))

        # generate Phylip allele data

        # generate individual locus files (don't use loci parameter)
        translate_file_to_stdout(os.path.join(metaXSLTDirectory, 'phylip-allele.xsl'), 'sorted-by-locus.xml')
        #os.popen("xsltproc %s %s" % (os.path.join(metaXSLTDirectory, 'phylip-allele.xsl'), 'sorted-by-locus.xml'))

        # generate locus group files
        for locus in ['A:B','C:B','DRB1:DQB1','A:B:DRB1','DRB1:DPB1','A:DPA1']:
            translate_file_to_stdout(os.path.join(metaXSLTDirectory, 'phylip-allele.xsl'), 'sorted-by-locus.xml', params={'loci': '"' + locus + '"'})
            #os.popen("xsltproc --stringparam loci %s %s %s" % (locus, os.path.join(metaXSLTDirectory, 'phylip-allele.xsl'), 'sorted-by-locus.xml'))

        # generate Phylip haplotype data
        for haplo in ['A:B','C:B','DRB1:DQB1','A:B:DRB1','DRB1:DPB1','A:DPA1']:
            translate_file_to_stdout(os.path.join(metaXSLTDirectory, 'phylip-haplo.xsl'), 'sorted-by-locus.xml', params={'loci': '"' + haplo + '"'})
            #os.popen("xsltproc --stringparam loci %s %s %s" % (haplo, os.path.join(metaXSLTDirectory, 'phylip-haplo.xsl'), 'meta.xml'))
