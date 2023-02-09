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
import pytest
from difflib import unified_diff
from pathlib import Path, PurePath

# global XFAIL condition for win32
xfail_windows = pytest.mark.xfail(sys.platform == "win32", reason="pipeline tests currently fail on windows")

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(CUR_DIR, '..')
sys.path.append(PARENT_DIR)

def abspath_test_data(filename):
    parent_path = PurePath(PARENT_DIR)
    suffix_path = PurePath(filename)
    return str (parent_path / suffix_path)

def filecmp_ignore_newlines(out_filename, gold_out_filename):

    l1 = l2 = True
    # opening up files defaults to 'universal newlines' this ignores OS-specific newline differences
    with open(out_filename, 'r') as f1, open(gold_out_filename, 'r') as f2:
        while l1 and l2:
            l1 = f1.readline()
            l2 = f2.readline()
            if l1 != l2:
                # generate the full-diff
                diff = unified_diff(open(out_filename, 'r').readlines(), open(gold_out_filename, 'r').readlines())
                delta = ''.join(diff)
                print (delta)
                
                return False
    return True
    
def run_pypop_process(inifile, popfile, args=[]):

    # convert relative data files to absolute
    inifile = abspath_test_data(inifile)
    popfile = abspath_test_data(popfile)

    # first search for pypop.py in current PATH
    default_pypop = shutil.which("pypop.py")
    # no Python executable needed, by default
    python_exe = None  

    if not default_pypop:
        # then in local subdirectory
        default_pypop = shutil.which(PurePath("./bin/pypop.py"))

        if not default_pypop:
            # otherwise, check location the python interpreter in a
            # virtual environment, and assume pypop has been installed
            # in same PATH this handles the Windows case on
            # cibuildwheels
            # FIXME: not a super-robust solution
            python_exe = shutil.which('python')
            parent_dir = Path(python_exe).parent
            default_pypop = str(parent_dir / 'pypop.py')

    # if we need to include the Python executable, we prepend it before the script
    if python_exe:
        exe_cmd = [python_exe, default_pypop]
    else:
        exe_cmd = [default_pypop]
    
    print ("pypop_exe: ", exe_cmd, end=" ")
    
    cmd_line = exe_cmd + ['-m'] + args + ['-c', inifile, popfile]
    process=subprocess.Popen(
        cmd_line,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )
    output, err = process.communicate()

    print(output.decode("utf-8"))
    exit_code = process.wait()  # wait until script completed

    return exit_code
