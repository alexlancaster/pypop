#!/usr/bin/env python
import os, sys
from getopt import getopt, GetoptError

# don't use libxml/libxslt bindings for the moment, aren't working with
# exslt extensions nor on all platforms.

#import libxml2
#import libxslt

#libxslt.registerAllExtras()
    
## force the libxml2 processor to generate DOM trees compliant with
## the XPath data model.
#libxml2.lineNumbersDefault(1)

## set libxml2 to substitute the entities in the document by default...
#libxml2.substituteEntitiesDefault(1)

def _translate_string_to(xslFilename, inString, outFile):
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
    
def translate_string_to_stdout(xslFilename, inString):
    # save result to stdout "-"
    _translate_string_to(xslFilename, inString, "-")

def translate_string_to_file(xslFilename, inString, outFile):
    _translate_string_to(xslFilename, inString, outFile)

def _translate_file_to(xslFilename, inFile, outFile):
    
    # parse the stylesheet file
    styledoc = libxml2.parseFile(xslFilename)

    # setup the stylesheet instance
    style = libxslt.parseStylesheetDoc(styledoc)

    # parse the inline generated XML file
    doc = libxml2.parseFile(inFile)

    # apply the stylesheet instance to the document instance
    result = style.applyStylesheet(doc, None)
    
    style.saveResultToFilename(outFile, result, 0)

    # free instances
    result.freeDoc()
    style.freeStylesheet()
    doc.freeDoc()

def translate_file_to_stdout(xslFilename, inFile):
    _translate_file_to(xslFilename, inFile, "-")

def translate_file_to_file(xslFilename, inFile, outFile):
    _translate_file_to(xslFilename, inFile, outFile)

usage_message = """Usage: meta.py [OPTION] INPUTFILES...

Processes INPUTFILES and generates 'meta'-analyses.  INPUTFILES are
expected to be the XML output files taken from runs of 'pypop'.

  -m, --meta-xslt=DIR     use specified directory to find XSLT (default: 'xslt')
  -h, --help              show this message
  -d, --dump-meta         dump the meta output file to stdout, ignore xslt file

  INPUTFILES  input XML files""" 

try:
  opts, args =getopt(sys.argv[1:],"m:hd", ["meta-xslt=", "help", "dump-meta"])
except GetoptError:
  sys.exit(usage_message)

metaXSLTDirectory= 'xslt/meta.xsl'
dump_meta = 0

# parse options
for o, v in opts:
  if o in ("-m", "--meta-xslt"):
    metaXSLTDirectory = v
  elif o in ("-h", "--help"):
    sys.exit(usage_message)
  elif o in ("-d", "--dump-meta"):
    dump_meta = 1

# parse arguments
files = args

# generate a metafile XML wrapper

# open doctype
meta_string="<!DOCTYPE meta [\n"
entities = ""
includes = ""

for f in files:
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
    #translate_string_to_file(os.path.join(metaXSLTDirectory, 'sort-by-locus.xsl'), meta_string, 'sorted.xml')
    #translate_file_to_stdout(os.path.join(metaXSLTDirectory, 'meta-to-r.xsl'), 'sorted.xml')
    # have to resort to command-line version because the Python bindings
    # don't understand how to load the exslt extensions in libxslt yet
    # that the meta-to-r.xsl stylesheet uses

    # generate the data file 'sorted-by-locus.xml' of pops sorted by locus
    os.popen("xsltproc %s %s > %s" % (os.path.join(metaXSLTDirectory, 'sort-by-locus.xsl'), 'meta.xml', 'sorted-by-locus.xml'))

    # use 'sorted-by-locus.xml' to generate a list of unique alleles
    # 'allelelist-by-locus.xml' for each locus across all the
    # populations in the set of XML files passed
    os.popen("xsltproc %s %s > %s" % (os.path.join(metaXSLTDirectory, 'allelelist-by-locus.xsl'), 'sorted-by-locus.xml', 'allelelist-by-locus.xml'))

    # finally, using the 'allelelist-by-locus.xml' file implicitly,
    # generate all data output in formats for both R and phylip
    os.popen("xsltproc %s %s" % (os.path.join(metaXSLTDirectory, 'meta-to-r.xsl'), 'meta.xml'))
