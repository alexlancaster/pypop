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

print metaXSLTFilename

# parse arguments
files = args
#files = sys.argv[1:]

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

#print meta_string

# do the transformation

import libxml2
import libxslt

# parse the stylesheet file
styledoc = libxml2.parseFile(metaXSLTFilename)

# setup the stylesheet instance
style = libxslt.parseStylesheetDoc(styledoc)

# parse the inline generated XML file
doc = libxml2.parseDoc(meta_string)

# apply the stylesheet instance to the document instance
result = style.applyStylesheet(doc, None)

result.debugDumpDocument(None)

# save result to stdout "-"
style.saveResultToFilename("-", result, 0)

# free instances
result.freeDoc()
style.freeStylesheet()
doc.freeDoc()


#output = libxsltmod.translate_to_string('f', 'meta.xsl',
#                                        's', meta_string)

#print output
