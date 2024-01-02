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
from pathlib import Path
from lxml import etree
from PyPop.Utils import checkXSLFile, splitIntoNGroups

def _translate_string_to(xslFilename, inString, outFile, outputDir=None, params=None):
    # do the transformation
    
    # parse the stylesheet file
    styledoc = etree.parse(xslFilename)

    # setup the stylesheet instance
    style = etree.XSLT(styledoc)

    # parse the inline generated XML file
    doc = etree.fromstring(inString)

    # apply the stylesheet instance to the document instance
    if params:
        result = style(doc, **params)
    else:
        result = style(doc)

    # generate output path
    if outputDir:
        outPath = outputDir / outFile
    else:
        outPath = outFile

    result.write_output(outPath)

    # use to dump directly to a string, problem is that it insists on
    # outputting an XML declaration "<?xml ...?>", can't seem to
    # suppress this
    # outString = result.serialize()

    #return outString
    
def translate_string_to_stdout(xslFilename, inString, outputDir=None, params=None):
    # save result to stdout "-"
    _translate_string_to(xslFilename, inString, "-", outputDir=outputDir, params=params)

def translate_string_to_file(xslFilename, inString, outFile, outputDir=None, params=None):
    _translate_string_to(xslFilename, inString, outFile, outputDir=outputDir, params=params)

def _translate_file_to(xslFilename, inFile, outFile, inputDir=None, outputDir=None, params=None):

    # assuming empty output
    output = None
    
    # parse the stylesheet file
    styledoc = etree.parse(xslFilename)

    # setup the stylesheet instance
    style = etree.XSLT(styledoc)

    try:
        # generate output path
        if inputDir:
            inputPath = inputDir / inFile
        else:
            inputPath = inFile

        # parse the inline generated XML file
        doc = etree.parse(inputPath)

        # apply the stylesheet instance to the document instance
        if params:
            result = style(doc, **params)
        else:
            result = style(doc)

        if outFile == '-': # this is stdout
            text_output = str(result)
            if len(text_output) > 0: # only write something if none-empty
                print(text_output)   # print it to screen
                output = text_output # but also pass it back

        else:
            # generate output path
            if outputDir:
                outPath = outputDir / outFile
            else:
                outPath = outFile
            
            result.write_output(outPath)

        success = True

    except Exception as e:
        print(e.args)
        print("Can't process: %s with stylesheet: %s, skipping" % (inFile, xslFilename))
        success = False

    return success, output

def translate_file_to_stdout(xslFilename, inFile, inputDir=None, params=None):
    retval, stdout = _translate_file_to(xslFilename, inFile, "-", inputDir=inputDir, params=params)
    return retval, stdout

def translate_file_to_file(xslFilename, inFile, outFile, inputDir=None, outputDir=None, params=None):
    retval, output = _translate_file_to(xslFilename, inFile, outFile, inputDir=inputDir, outputDir=outputDir, params=params)
    return retval  # FIXME: don't use the output from a file->file transformation currently


class Meta:
    """Aggregates output from multiple population runs.

    """
    def __init__(self,
                 popmetabinpath = None,
                 datapath = None,
                 metaXSLTDirectory = None,
                 dump_meta = False,
                 TSV_output = True,
                 prefixTSV = None,
                 PHYLIP_output = False,
                 ihwg_output = False,
                 batchsize = 0,
                 outputDir = None,
                 xml_files = None):
        """Transform a specified list of XML output files to *.tsv
        tab-separated values (TSV) form.

        Defaults:
        # output .tsv tables by default (can be used by R)
        TSV_output=True

        # don't output PHYLIP by default
        PHYLIP_output=False

        # by default, don't enable the 13th IHWG format headers
        ihwg_output = False

        # by default process separately (batchsize=0)
        batchsize = 0
        """

        # set default parser to resolve the SYSTEM file entities, now
        # that the lxml > 5.0.0 default is to disable resolution.  but
        # disallow network access
        etree.set_default_parser(etree.XMLParser(resolve_entities=True, no_network=True))
        
        # the name of the XSLT file for transformation
        meta_to_tsv_xsl = 'meta-to-tsv.xsl'
        
        # heuristics to find default location of 'xslt/' subdirectory, if it is
        # not supplied by the command-line option

        if not(metaXSLTDirectory):

            try:
                from importlib.resources import files
                introspection_path = files('PyPop.xslt')
            except (ModuleNotFoundError, ImportError):  # fallback to using backport if not found
                from importlib_resources import files
                introspection_path = files('PyPop.xslt').joinpath('')

            if checkXSLFile(meta_to_tsv_xsl, introspection_path):  # first check installed path
                metaXSLTDirectory = introspection_path
            elif checkXSLFile(meta_to_tsv_xsl, popmetabinpath, 'xslt'):  # next, heuristics
                metaXSLTDirectory = os.path.join(popmetabinpath, 'xslt')
            elif checkXSLFile(meta_to_tsv_xsl, popmetabinpath, os.path.join('..', 'PyPop/xslt')):
                metaXSLTDirectory = os.path.join(popmetabinpath, '..', 'PyPop/xslt')
            else:
                metaXSLTDirectory= datapath

        if (batchsize > 1) and PHYLIP_output:
            sys.exit("processing in batches and enabling PHYLIP are mutually exclusive options\n")

        # create XSLT parameters
        if ihwg_output:
            xslt_params = {"ihwg-fmt": "1"}
        else:
            xslt_params = {"ihwg-fmt": "0"}

        # pass in subdirectory if it's given
        if outputDir:
            xslt_params['outputDir'] = "'" + str(outputDir) + "/'" # make sure to include slash
        else:
            xslt_params['outputDir'] = "'./'" # otherwise chose current directory

        # use a prefix for all TSV if given
        if prefixTSV:
            xslt_params['prefixTSV'] = "'" + prefixTSV + "-'" # make sure to include dash
        else:
            xslt_params['prefixTSV'] = "''" # otherwise use empty string
            
        # FIXME
        # report error if no file arguments given

        wellformed_files = []

        # check each file for "well-formedness" using etree.parse()
        # if not well-formed report an error on this file,
        # and skip this file in the meta analysis
        for xml_file in xml_files:
            try:
                doc = etree.parse(xml_file)
                wellformed_files.append(xml_file)
            except:
                print("%s is not well-formed XML:" % f)
                print("  probably a problem with analysis not completing, skipping in meta analysis!")

        if batchsize:
            fileBatchList = splitIntoNGroups(wellformed_files, n=batchsize)
        else:
            fileBatchList = splitIntoNGroups(wellformed_files, \
                                             n=len(wellformed_files))

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
                uri = Path(os.path.abspath(f)).as_uri()
                ent = "ENT" + base.replace(' ', '-')
                entities += "<!ENTITY %s SYSTEM \"%s\">\n" % (ent, uri)
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
                print(meta_string)
            else:
                if outputDir:
                    meta_xml_path = outputDir / 'meta.xml'
                else:
                    meta_xml_path = 'meta.xml'
                
                f = open(meta_xml_path, 'w')
                f.write(meta_string)
                f.close()

                if TSV_output:
                    # generate all data output in formats for programs that read TSV files
                    # stdout records the files generated by the XML -> TSV transformation
                    success, stdout = translate_file_to_stdout(os.path.join(metaXSLTDirectory, meta_to_tsv_xsl), "meta.xml", inputDir=outputDir, params=xslt_params)
                    # transform stdout into a list of tsv files
                    tsv_files = stdout.strip().split("\n")
                    

                if PHYLIP_output:
                    # using the '{allele,haplo}list-by-{locus,group}.xml' files implicitly:
                    success = translate_string_to_file(os.path.join(metaXSLTDirectory, 'sort-by-locus.xsl'), meta_string, 'sorted-by-locus.xml', outputDir=outputDir)

                    # use 'sorted-by-locus.xml' to generate a list of unique alleles
                    # 'allelelist-by-locus.xml' for each locus across all the
                    # populations in the set of XML files passed
                    success = translate_file_to_file(os.path.join(metaXSLTDirectory, 'allelelist-by-locus.xsl'),
                                                     'sorted-by-locus.xml', 'allelelist-by-locus.xml', inputDir=outputDir, outputDir=outputDir)

                    # similarly, generate a unique list of haplotypes
                    # 'haplolist-by-locus.xml'
                    success = translate_file_to_file(os.path.join(metaXSLTDirectory, 'haplolist-by-group.xsl'), "meta.xml", 'haplolist-by-group.xml',
                                                     inputDir=outputDir, outputDir=outputDir)

                    # generate Phylip allele data

                    # generate individual locus files (don't use loci parameter)
                    success, stdout = translate_file_to_stdout(os.path.join(metaXSLTDirectory, 'phylip-allele.xsl'), 'sorted-by-locus.xml',
                                                       inputDir=outputDir, params={'outputDir': xslt_params['outputDir']})

                    # generate locus group files
                    for locus in ['A:B','C:B','DRB1:DQB1','A:B:DRB1','DRB1:DPB1','A:DPA1']:
                        success, stdout = translate_file_to_stdout(os.path.join(metaXSLTDirectory, 'phylip-allele.xsl'), 'sorted-by-locus.xml',
                                                           inputDir=outputDir, params={'loci': '"' + locus + '"', 'outputDir': xslt_params['outputDir']})

                    # generate Phylip haplotype data
                    for haplo in ['A:B','C:B','DRB1:DQB1','A:B:DRB1','DRB1:DPB1','A:DPA1']:
                        success, stdout = translate_file_to_stdout(os.path.join(metaXSLTDirectory, 'phylip-haplo.xsl'), "meta.xml",
                                                           inputDir=outputDir, params={'loci': '"' + haplo + '"', 'outputDir': xslt_params['outputDir']})

                # after processing, move files if necessary
                if len(fileBatchList) > 1:
                    for dat in tsv_files:
                        if success:
                            if os.path.exists(dat):
                                #print("renaming:", dat, "to:", "%s.%d" % (dat, fileBatch))
                                os.rename(dat, "%s.%d" % (dat, fileBatch))
                            else:
                                print("%s in batch %d doesn't exist - skipping"
                                  % (dat, fileBatch))
                        else:
                            print("problem with generating %s in batch %d"
                                  % (dat, fileBatch))

        # at end of entire processing, need to cat files together
        # this is a bit hacky
        if len(fileBatchList) > 1:
            for dat in tsv_files:
                # create final file to concatenate to
                outdat = open(dat, 'w')
                # now concatenate them
                for i in range(len(fileBatchList)):
                    # write temp file to outdat
                    catFilename = "%s.%d" % (dat, i)
                    if not(os.path.exists(catFilename)):  # if the file is not generated, we skip
                        continue
                    catFile = open(catFilename)
                    # drop the first line, iff we are past first file
                    for linenum, line in enumerate(catFile):
                        if i > 0:
                            if linenum > 0:
                                outdat.write(line)
                        else:
                            outdat.write(line)
                    # then remove it
                    catFile.close()
                    os.remove(catFilename)
                # close the ultimate output file
                outdat.close()
                # if the file is empty, we remove it
                if os.path.getsize(dat) == 0:
                    os.remove(dat)

