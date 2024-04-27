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
import tempfile

from difflib import unified_diff
from pathlib import Path, PurePath

# global XFAIL condition for win32
xfail_windows = pytest.mark.xfail(sys.platform == "win32", reason="certain tests currently fail on windows due to minor numerical issues")

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(CUR_DIR, '..')
sys.path.append(PARENT_DIR)
SRC_DIR=os.path.join(CUR_DIR, '../src')
sys.path.append(SRC_DIR)

DEFAULT_GOLD_OUTPUT_DIR = './tests/data/gold-output'

def abspath_test_data(filename):
    parent_path = PurePath(PARENT_DIR)
    suffix_path = PurePath(filename)
    return str (parent_path / suffix_path)

def filecmp_ignore_newlines(out_filename, gold_out_filename):

    l1 = l2 = True
    retval = True   # default to match, unless there is a diff
    # opening up files defaults to 'universal newlines' this ignores OS-specific newline differences
    with open(out_filename, 'r') as f1, open(gold_out_filename, 'r') as f2:
        while l1 and l2:
            l1 = f1.readline()
            l2 = f2.readline()
            if l1 != l2:
                # generate the full-diff
                diff = unified_diff(open(gold_out_filename, 'r').readlines(), open(out_filename, 'r').readlines())
                delta = ''.join(diff)
                print (delta)
                
                retval = False # mismatch
                break
            
    return retval

def filecmp_list_of_files(filename_list, gold_out_directory):

    retval = True  # assume true by defualt
    
    for out_filename in filename_list:
        gold_out_filename = abspath_test_data(os.path.join(gold_out_directory, out_filename))
        if not filecmp_ignore_newlines(out_filename, gold_out_filename):
            retval = False
            print ("failed file:", out_filename)
            return retval  # once a file fails, return

    return retval

def run_script_process_shell(script_name, args):

    # first search for script in current PATH
    default_script = shutil.which(script_name)
    # no Python executable needed, by default
    python_exe = None  

    if not default_script:
        # then check for uninstalled version in local subdirectory
        default_script = shutil.which(PurePath(Path("./src/PyPop") / (script_name + '.py')))

        if not default_script:
            # otherwise, check location the python interpreter in a
            # virtual environment, and assume pypop has been installed
            # in same PATH this handles the Windows case on
            # cibuildwheels
            # FIXME: not a super-robust solution
            python_exe = shutil.which('python')
            parent_dir = Path(python_exe).parent
            default_script = str(parent_dir / script_name)

    # if we need to include the Python executable, we prepend it before the script
    if python_exe:
        exe_cmd = [python_exe, default_script]
        print ("script_exe: ", python_exe, str(default_script), end=" ")
    else:
        exe_cmd = [default_script]
        print (str(default_script), end=" ")
    
    cmd_line = exe_cmd + args
    process=subprocess.Popen(
        cmd_line,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )
    output, err = process.communicate()
    exit_code = process.wait()  # wait until script completed

    return exit_code

def run_script_process_entry_point(script_name, args):
    argv = [script_name] + args
    print(argv)

    if script_name == 'pypop':
        from PyPop.pypop import main
        ret_val = main(argv=argv)
    elif script_name == 'popmeta':
        from PyPop.popmeta import main
        ret_val = main(argv=argv)
    else:
        exit("script:", script_name, "doesn't exist")

    if ret_val:
        exit_code = 1
    else:
        exit_code = 0
    return exit_code

def run_pypop_process(inifile, popfile, args=[]):

    # convert relative data files to absolute
    inifile = abspath_test_data(inifile)
    popfile = abspath_test_data(popfile)
    pypop_args = ['-m'] + args + ['-c', inifile, popfile]
    exit_code = run_script_process_entry_point('pypop', pypop_args)
    return exit_code

def run_popmeta_process(xmlfiles, args=[]):

    # convert relative data files to absolute
    input_files = []
    for xml in xmlfiles:
        input_files.append(abspath_test_data(xml))
    popmeta_args = args + input_files
    exit_code = run_script_process_entry_point('popmeta', popmeta_args)
    return exit_code

@pytest.fixture(scope="function", autouse=True)
def in_temp_dir(request):

    curr_dir = os.getcwd() # save current directory

    # get test case name for temporary directory
    test_case_name = request.function.__name__
    
    # create the new temporary directory
    
    test_dir = tempfile.mkdtemp(    
        dir = '.',
        prefix = 'run_'+ test_case_name + '_',
        suffix = ''
    )
    os.chdir(test_dir) # change current directory to temp

    try:
        yield
    finally:
        # restore original directory
        os.chdir(curr_dir)
        verbose_level = request.config.getoption('verbose')

        # by default (verbosity level == 0), we delete the temporary
        # directory, otherwise we skip it
        if verbose_level == 0:
            # cleaning up the temporary directory
            shutil.rmtree(test_dir)
        
