#!/usr/bin/env python
import os, sys, libxsltmod
from getopt import getopt, GetoptError

usage_message = """Usage: meta.py [OPTION] INPUTFILES...

Processes INPUTFILES and generates 'meta'-analyses.  INPUTFILES are
expected to be the XML output files taken from runs of 'pypop'.

  -m, --meta-xslt=FILE    use specified XSLT FILE (default: 'xslt/meta.xsl')
  -h, --help              show this message

  INPUTFILES  input XML files""" 

try:
  opts, args =getopt(sys.argv[1:],"m:h", ["meta-xslt=", "help"])
except GetoptError:
  sys.exit(usage_message)

metaXSLTFilename= 'xslt/meta.xsl'

# parse options
for o, v in opts:
  if o in ("-m", "--meta-xslt"):
    metaXSLTFilename = v
  elif o in ("-h", "--help"):
    sys.exit(usage_message)

# parse arguments
files = args

# generate a metafile XML wrapper

# open doctype
meta_string="<!DOCTYPE meta [\n"
entities = ""
includes = ""

for f in files:
    base = os.path.basename(f)
    entities += "<!ENTITY %s SYSTEM \"%s\">\n" % (base, f)
    includes += "&%s;\n" % base

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

def translate_to_stdout(xslFilename, inString):
    
    # do the transformation
    import libxml2
    import libxslt

    # set libxml2 to substitute the entities in the document by default...
    libxml2.substituteEntitiesDefault(1)

    # parse the stylesheet file
    styledoc = libxml2.parseFile(xslFilename)

    # setup the stylesheet instance
    style = libxslt.parseStylesheetDoc(styledoc)

    # parse the inline generated XML file
    doc = libxml2.parseDoc(inString)

    # apply the stylesheet instance to the document instance
    result = style.applyStylesheet(doc, None)
    
    # save result to stdout "-"
    style.saveResultToFilename("-", result, 0)

    # use to dump directly to a string, problem is that it insists on
    # outputting an XML declaration "<?xml ...?>", can't seem to
    # suppress this
    # outString = result.serialize()

    # free instances
    result.freeDoc()
    style.freeStylesheet()
    doc.freeDoc()

    #return outString


output = translate_to_stdout(metaXSLTFilename, meta_string)


