#!/usr/bin/env python
import os, sys, libxsltmod

files = sys.argv[1:]

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
output = libxsltmod.translate_to_string('f', 'meta.xsl',
                                        's', meta_string)

print output
