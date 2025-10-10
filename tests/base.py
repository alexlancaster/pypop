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


"""This is a class of common functions for running PyPop tests."""

import os.path
import platform
import shutil
import subprocess
import sys
import tempfile
from difflib import unified_diff
from pathlib import Path, PurePath

import pytest

from PyPop.popmeta import main as main_popmeta
from PyPop.pypop import main as main_pypop

# global XFAIL condition for win32
xfail_windows = pytest.mark.xfail(
    sys.platform == "win32",
    reason="certain tests currently fail on windows due to minor numerical issues",
)


def is_check_musllinux_enabled():
    return False


# FIXME: this is a somewhat hacky check to see if on musllinux
def is_musllinux():
    """Check if running on a musl-based Linux system."""
    if sys.platform != "linux":
        return False

    # Check if `ldd` output contains 'musl'
    try:
        output = subprocess.check_output(
            ["ldd", "--version"], stderr=subprocess.STDOUT, text=True
        )
        if "musl" in output:
            return True
    except Exception:
        pass  # `ldd` might not exist

    # Fallback: Check if running on Alpine (common musl distribution)
    try:
        with open("/etc/os-release") as f:
            if "ID=alpine" in f.read():
                return True
    except FileNotFoundError:
        pass

    return False


def debug_musllinux_check():
    if not is_check_musllinux_enabled():
        return

    """Print debug info about musllinux detection."""
    print("=== musllinux detection debug ===")
    print(f"sys.platform: {sys.platform}")
    print(f"platform.libc_ver(): {platform.libc_ver()}")
    print(f"platform.machine(): {platform.machine()}")
    print("===============================")

    # Run `ldd --version` to check if it's musl
    try:
        output = subprocess.check_output(
            ["ldd", "--version"], stderr=subprocess.STDOUT, text=True
        )
        print("ldd --version output:")
        print(output.strip())
    except Exception as e:
        print(f"ldd check failed: {e}")

    # Check `/etc/os-release`
    try:
        with open("/etc/os-release") as f:
            print("/etc/os-release contents:")
            print(f.read().strip())
    except FileNotFoundError:
        print("/etc/os-release not found")

    print("===============================")

    if is_musllinux() and platform.machine() == "x86_64":
        print("Skipping test due to musllinux_1_2 on x86_64")


# call the debug function before applying the skip
debug_musllinux_check()

# global skip condition for musllinux on x86_64
# FIXME: currently disabled, to re-enable, change "False" to "True" in condition
skip_musllinux_x86_64 = pytest.mark.skipif(
    is_check_musllinux_enabled() and is_musllinux() and platform.machine() == "x86_64",
    reason="certain tests segfault or fail on musllinux/x86_64, so skipping for now",
)

CUR_DIR = Path(__file__).parent.resolve()
PARENT_DIR = Path(CUR_DIR) / ".."
sys.path.append(PARENT_DIR)
SRC_DIR = Path(CUR_DIR) / "../src"
sys.path.append(SRC_DIR)

DEFAULT_GOLD_OUTPUT_DIR = Path("./tests/data/gold-output")


def abspath_test_data(filename):
    parent_path = PurePath(PARENT_DIR)
    suffix_path = PurePath(filename)
    return str(parent_path / suffix_path)


def filecmp_ignore_newlines(out_filename, gold_out_filename):
    l1 = l2 = True
    retval = True  # default to match, unless there is a diff
    # opening up files defaults to 'universal newlines' this ignores OS-specific newline differences
    with open(out_filename) as f1, open(gold_out_filename) as f2:
        while l1 and l2:
            l1 = f1.readline()
            l2 = f2.readline()
            if l1 != l2:
                # generate the full-diff

                with open(gold_out_filename) as gold_file, open(
                    out_filename
                ) as out_file:
                    diff = unified_diff(gold_file.readlines(), out_file.readlines())
                delta = "".join(diff)
                print(delta)

                retval = False  # mismatch
                break

    return retval


def filecmp_list_of_files(filename_list, gold_out_directory):
    retval = True  # assume true by default

    for out_filename in filename_list:
        gold_out_filename = abspath_test_data(Path(gold_out_directory) / out_filename)
        if not filecmp_ignore_newlines(out_filename, gold_out_filename):
            retval = False
            print("failed file:", out_filename)
            return retval  # once a file fails, return

    return retval


def run_script_process_shell(script_name, args):
    # first search for script in current PATH
    default_script = shutil.which(script_name)
    # no Python executable needed, by default
    python_exe = None

    if not default_script:
        # then check for uninstalled version in local subdirectory
        default_script = shutil.which(
            PurePath(Path("./src/PyPop") / (script_name + ".py"))
        )

        if not default_script:
            # otherwise, check location the python interpreter in a
            # virtual environment, and assume pypop has been installed
            # in same PATH this handles the Windows case on
            # cibuildwheels
            # FIXME: not a super-robust solution
            python_exe = shutil.which("python")
            parent_dir = Path(python_exe).parent
            default_script = str(parent_dir / script_name)

    # if we need to include the Python executable, we prepend it before the script
    if python_exe:
        exe_cmd = [python_exe, default_script]
        print("script_exe: ", python_exe, str(default_script), end=" ")
    else:
        exe_cmd = [default_script]
        print(str(default_script), end=" ")

    cmd_line = exe_cmd + args
    process = subprocess.Popen(
        cmd_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    _output, _err = process.communicate()
    return process.wait()  # wait until script completed


def run_script_process_entry_point(script_name, args):
    argv = [script_name, *args]
    print(argv)

    if script_name == "pypop":
        ret_val = main_pypop(argv=argv)
    elif script_name == "popmeta":
        ret_val = main_popmeta(argv=argv)
    else:
        sys.exit("script:", script_name, "doesn't exist")

    return 1 if ret_val else 0


def run_pypop_process(inifile, popfile=None, *, poplistfile=None, args=None):
    # convert relative data files to absolute
    if args is None:
        args = []

    if popfile and poplistfile:
        sys.exit("Cannot specify both popfile and poplistfile")

    inifile = abspath_test_data(inifile)
    if popfile:
        popfile = abspath_test_data(popfile)
        pypop_args = ["-m", *args, "-c", inifile, popfile]
    elif poplistfile:
        poplistfile = abspath_test_data(poplistfile)
        pypop_args = ["-m", *args, "--filelist", poplistfile, "-c", inifile]
    else:
        sys.exit("need to include either popfile or poplistfile")

    return run_script_process_entry_point("pypop", pypop_args)


def run_popmeta_process(xmlfiles, args=None):
    # convert relative data files to absolute
    if args is None:
        args = []
    input_files = []
    for xml in xmlfiles:
        input_files.append(abspath_test_data(xml))
    popmeta_args = args + input_files
    return run_script_process_entry_point("popmeta", popmeta_args)


@pytest.fixture(autouse=True)
def in_temp_dir(request):
    curr_dir = Path.cwd()  # save current directory

    # get test case name for temporary directory
    test_case_name = request.function.__name__

    # create the new temporary directory

    test_dir = tempfile.mkdtemp(
        dir=".", prefix="run_" + test_case_name + "_", suffix=""
    )
    os.chdir(test_dir)  # change current directory to temp

    try:
        yield
    finally:
        # restore original directory
        os.chdir(curr_dir)
        verbose_level = request.config.getoption("verbose")

        # by default (verbosity level == 0), we delete the temporary
        # directory, otherwise we skip it
        if verbose_level == 0:
            # cleaning up the temporary directory
            shutil.rmtree(test_dir)
