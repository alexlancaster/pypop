#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2017. 
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

__version__ = '1.0.0-alpha'
__pkgname__ = 'PyPop'

copyright_message = """Copyright (C) 2003-2006 Regents of the University of California.
Copyright (C) 2007-2023 PyPop team.
This is free software.  There is NO warranty; not even for
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."""

import locale
import logging
import platform
import sys
import os
import re

def setup_logging(debug=False, filename=None):
    """Provide defaults for logging."""
    level = logging.DEBUG if debug else logging.INFO
    if filename is None:
        filename = '-'

    if filename == '-':
        hand = logging.StreamHandler()
    else:
        hand = logging.FileHandler(filename)

    fmt = '%(asctime)s %(levelname)s %(funcName)s: %(message)s' if level == logging.DEBUG else '%(asctime)s %(message)s'
    datefmt = '%Y.%m.%d %H:%M:%S'
    hand.setFormatter(logging.Formatter(fmt, datefmt))

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = []
    root_logger.addHandler(hand)

    logging.debug('PyPop: %s' % __version__)
    logging.debug('Python: %s' % sys.version.replace('\n', ' '))
    logging.debug('Platform: %s' % platform.platform())
    logging.debug('Locale: %s' % locale.setlocale(locale.LC_ALL))

def convert_line_endings(file, mode):
    # 1 - Unix to Mac, 2 - Unix to DOS
    if mode == 1:
        if os.path.isdir(file):
            sys.exit(file + "Directory!")
        data = open(file, "r").read()
        if '\0' in data:
            sys.exit(file + "Binary!")
        newdata = re.sub("\r?\n", "\r", data)
        if newdata != data:
            f = open(file, "w")
            f.write(newdata)
            f.close()
    elif mode == 2:
        if os.path.isdir(file):
            sys.exit(file + "Directory!")
        data = open(file, "r").read()
        if '\0' in data:
            sys.exit(file + "Binary!")
        newdata = re.sub("\r(?!\n)|(?<!\r)\n", "\r\n", data)
        if newdata != data:
            f = open(file, "w")
            f.write(newdata)
            f.close()
    
