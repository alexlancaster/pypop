#!/usr/bin/env python
import os, sys, libxsltmod

files = sys.argv[1:]

# generate a metafile XML wrapper
meta_string="<meta>"
for f in files:
    meta_string += "<filename>%s</filename>" % f
meta_string += "</meta>"

print meta_string

# do the transformation
output = libxsltmod.translate_to_string('f', 'meta.xsl',
                                        's', meta_string)

print output
