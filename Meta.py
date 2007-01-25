#!/usr/bin/env python

# This file is part of PyPop
# $Id$

# Copyright (C) 2005.
# The Regents of the University of California (Regents)
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

"""Module for collecting multiple population outputs.

"""
import os, sys
from getopt import getopt, GetoptError
from Utils import checkXSLFile, splitIntoNGroups

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
    result = style.applyStylesheet(doc, params)
    
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

    try:
        # parse the inline generated XML file
        doc = libxml2.parseFile(inFile)

        # apply the stylesheet instance to the document instance
        result = style.applyStylesheet(doc, params)
    
        style.saveResultToFilename(outFile, result, 0)

        success = 1
    
    
        # free instances
        result.freeDoc()
        style.freeStylesheet()
        doc.freeDoc()

    except:
        print "Can't parse: %s, skipping" % inFile
        success = 0

    return success


def translate_file_to_stdout(xslFilename, inFile, params=None):
    retval = _translate_file_to(xslFilename, inFile, "-", params)
    return retval

def translate_file_to_file(xslFilename, inFile, outFile, params=None):
    retval = _translate_file_to(xslFilename, inFile, outFile, params)
    return retval


class Meta:
    """Aggregates output from multiple population runs.

    """
    def __init__(self,
                 popmetabinpath = None,
                 datapath = None,
                 metaXSLTDirectory = None,
                 dump_meta = 0,
                 R_output = 1,
                 PHYLIP_output = 0,
                 ihwg_output = 1,
                 batchsize = 0,
                 files = None):
        """Transform a specified list of XML output files to *.dat
        tab-separated values (TSV) form.

        Defaults:
        # output R tables by default
        R_output=1

        # don't output PHYLIP by default
        PHYLIP_output=0

        # by default, enable the 13th IHWG format headers
        ihwg_output = 1

        # by default process separately (batchsize=0)
        batchsize = 0
        """

        # heuristics to find default location of 'xslt/' subdirectory, if it is
        # not supplied by the command-line option

        if not(metaXSLTDirectory):
            if checkXSLFile('meta-to-r.xsl', popmetabinpath, 'xslt'):
                metaXSLTDirectory = os.path.join(popmetabinpath, 'xslt')
            elif checkXSLFile('meta-to-r.xsl', popmetabinpath, os.path.join('..', 'xslt')):
                metaXSLTDirectory = os.path.join(popmetabinpath, '..', 'xslt')
            else:
                metaXSLTDirectory= datapath

        if (batchsize > 1) and PHYLIP_output:
            sys.exit("processing in batches and enabling PHYLIP are mutually exclusive options\n" + usage_message)

        # create XSLT parameters
        if ihwg_output:
            xslt_params = {"ihwg-fmt": "1"}
        else:
            xslt_params = {"ihwg-fmt": "0"}

        # parse arguments
        #files = args

        # report usage message if no file arguments given
        #if not(files):
        #    sys.exit(usage_message)

        wellformed_files = []

        # check each file for "well-formedness" using libxml2.parseFile()
        # libxml2 package, if not well-formed report an error on this file,
        # and skip this file in the meta analysis
        for f in files:
            try:
                doc = libxml2.parseFile(f)
                wellformed_files.append(f)
                doc.freeDoc()
            except:
                print "%s is not well-formed XML:" % f
                print "  probably a problem with analysis not completing, skipping in meta analysis!"

        if batchsize:
            fileBatchList = splitIntoNGroups(wellformed_files, n=batchsize)
        else:
            fileBatchList = splitIntoNGroups(wellformed_files, \
                                             n=len(wellformed_files))

        datfiles= ['1-locus-allele.dat', '1-locus-genotype.dat',
                   '1-locus-summary.dat', '1-locus-pairwise-fnd.dat',
                   '1-locus-hardyweinberg.dat',
                   '2-locus-haplo.dat', '2-locus-summary.dat',
                   '3-locus-summary.dat', '3-locus-haplo.dat',
                   '4-locus-summary.dat', '4-locus-haplo.dat',]

        for fileBatch in range(len(fileBatchList)):

            # generate a metafile XML wrapper

            # open doctype
            meta_string="<!DOCTYPE meta [\n"
            entities = ""
            includes = ""

            # loop through and create the meta.xml file *only* for the well-formed
            # XML files

            for f in fileBatchList[fileBatch]:
                base = os.path.basename(f)
                ent = "ENT" + base.replace(' ', '-')
                entities += "<!ENTITY %s SYSTEM \"%s\">\n" % (ent, f.replace(' ', '%20'))
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

                if R_output:
                    # generate all data output in formats for R
                    success = translate_file_to_stdout(os.path.join(metaXSLTDirectory, 'meta-to-r.xsl'), 'meta.xml', xslt_params)

                if PHYLIP_output:
                    # using the '{allele,haplo}list-by-{locus,group}.xml' files implicitly:
                    success = translate_string_to_file(os.path.join(metaXSLTDirectory, 'sort-by-locus.xsl'), meta_string, 'sorted-by-locus.xml')

                    # use 'sorted-by-locus.xml' to generate a list of unique alleles
                    # 'allelelist-by-locus.xml' for each locus across all the
                    # populations in the set of XML files passed
                    success = translate_file_to_file(os.path.join(metaXSLTDirectory, 'allelelist-by-locus.xsl'), 'sorted-by-locus.xml', 'allelelist-by-locus.xml')

                    # similarly, generate a unique list of haplotypes
                    # 'haplolist-by-locus.xml'
                    success = translate_file_to_file(os.path.join(metaXSLTDirectory, 'haplolist-by-group.xsl'), 'meta.xml', 'haplolist-by-group.xml')

                    # generate Phylip allele data

                    # generate individual locus files (don't use loci parameter)
                    success = translate_file_to_stdout(os.path.join(metaXSLTDirectory, 'phylip-allele.xsl'), 'sorted-by-locus.xml')

                    # generate locus group files
                    for locus in ['A:B','C:B','DRB1:DQB1','A:B:DRB1','DRB1:DPB1','A:DPA1']:
                        success = translate_file_to_stdout(os.path.join(metaXSLTDirectory, 'phylip-allele.xsl'), 'sorted-by-locus.xml', params={'loci': '"' + locus + '"'})

                    # generate Phylip haplotype data
                    for haplo in ['A:B','C:B','DRB1:DQB1','A:B:DRB1','DRB1:DPB1','A:DPA1']:
                        success = translate_file_to_stdout(os.path.join(metaXSLTDirectory, 'phylip-haplo.xsl'), 'meta.xml', params={'loci': '"' + haplo + '"'})

                # after processing, move files if necessary
                if len(fileBatchList) > 1:
                    for dat in datfiles:
                        # print "moving", dat, "to %s.%d" % (dat, fileBatch)
                        if success:
                            os.rename(dat, "%s.%d" % (dat, fileBatch))
                        else:
                            print "problem with generating %s in batch %d" \
                                  % (dat, fileBatch)

        # at end of entire processing, need to cat files together
        # this is a bit hacky
        if len(fileBatchList) > 1:
            for dat in datfiles:
                # create final file to concatenate to
                outdat = file(dat, 'w')
                # now concatenate them
                for i in range(len(fileBatchList)):
                    # write temp file to outdat
                    catFilename = "%s.%d" % (dat, i)
                    catFile = file(catFilename)
                    # drop the first line, iff we are past first file
                    if i > 0:
                        catFile.readline() # skip this line
                        #catFile.next() <- this only works in Python 2.3 or better
                    for line in catFile:
                        outdat.write(line)
                    # then remove it
                    catFile.close()
                    os.remove(catFilename)
                # finally, close the ultimate output file
                outdat.close()

