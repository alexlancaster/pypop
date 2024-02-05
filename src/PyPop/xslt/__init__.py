#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2024
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

"""
Python XSLT extensions for handling things outside the scope of XSLT 1.0

"""

from lxml import etree
from math import floor, log10, inf

ns = etree.FunctionNamespace('http://pypop.org/lxml/functions')
ns.prefix = 'es'

def num_zeros(decimal):
    return inf if decimal == 0 else -floor(log10(abs(decimal))) - 1

@ns
def convert_to_scientific(context, a):
    a = float(a)
    if num_zeros(a) >= 4:
        retval = "{:.1E}".format(a)
    else:
        retval = "{:g}".format(a)
    return retval

if __name__ == "__main__":

    # some tests
    
    ns['convert_to_scientific'] = convert_to_scientific
    
    root = etree.XML('<a><b>0.0000043</b></a>')
    print(root.xpath("es:convert_to_scientific('0.032')"))
    doc = etree.ElementTree(root)

    xslt = etree.XSLT(etree.XML('''
      <stylesheet version="1.0"
          xmlns="http://www.w3.org/1999/XSL/Transform"
          xmlns:es="http://pypop.org/lxml/functions">
     <output method="text" encoding="ASCII"/>
     <template match="/">
       <text>Yep [</text>
       <value-of select="es:convert_to_scientific(string(/a/b))"/>
       <text>]</text>
     </template>
      </stylesheet>
    '''))

    print(xslt(doc))
    

