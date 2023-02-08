# This file is part of PyPop

# Copyright (C) 2017. 

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


"""This is a class of common functions for running PyPop tests"""

import os.path
import sys
import subprocess
import shutil
from pathlib import PurePath

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(CUR_DIR, '..')
sys.path.append(PARENT_DIR)

def abspath_test_data(filename):
    parent_path = PurePath(PARENT_DIR)
    suffix_path = PurePath(filename)
    
    return str (parent_path / suffix_path)

def run_pypop_process(inifile, popfile, args=[]):

    # convert relative data files to absolute
    inifile = abspath_test_data(inifile)
    popfile = abspath_test_data(popfile)

    # first try pypop.py in current PATH
    default_pypop = shutil.which("pypop.py")
    if not default_pypop:
        default_pypop = shutil.which("./bin/pypop.py")
        #print ("using local pypop:", default_pypop)
    
    cmd_line = [default_pypop, '-m'] + args + ['-c', inifile, popfile]
    process=subprocess.Popen(
        cmd_line,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )
    process.communicate()
    exit_code = process.wait()  # wait until script completed
    return exit_code
