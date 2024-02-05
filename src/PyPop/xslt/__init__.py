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
from numpy import format_float_scientific

ns = etree.FunctionNamespace('http://pypop.org/lxml/functions')
ns.prefix = 'es'

def num_zeros(decimal):
    return inf if decimal == 0 else -floor(log10(abs(decimal))) - 1

@ns
def format_number_fixed_width(context, *args):

    num = float(args[0])
    places = int(args[1])
    zeros_before_sig_figs = num_zeros(num)
    
    # need to reserve 4 characters for exponent
    precision = places - 4 if places >= 4 else 0
    if zeros_before_sig_figs >= places and zeros_before_sig_figs != inf:
        #retval = "{0:.{1}E}".format(num, precision)
        retval = format_float_scientific(num, exp_digits=1, precision=precision, trim='-')
    else:
        retval = "{0:.{1}f}".format(num, places)
    return retval

if __name__ == "__main__":

    # some tests
    
    ns['format_number_fixed_width'] = format_number_fixed_width
    
    root = etree.XML('<a><b>0.0000043</b></a>')
    doc = etree.ElementTree(root)

    xslt = etree.XSLT(etree.XML('''
      <stylesheet version="1.0"
          xmlns="http://www.w3.org/1999/XSL/Transform"
          xmlns:es="http://pypop.org/lxml/functions">
     <output method="text" encoding="ASCII"/>
     <template match="/">
       <text>Yep [</text>
       <value-of select="es:format_number_fixed_width(string(/a/b), 5)"/>
       <text>]</text>
     </template>
      </stylesheet>
    '''))

    print(xslt(doc))
    

