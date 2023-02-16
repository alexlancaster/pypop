# Python for Population Genomics (PyPop)

PyPop is a framework for processing genotype and allele data and
running population genetic analyses.

# Installation (end user)

TBA.  For the end-user, we are currently working on making PyPop
installable via `pip` from downloadable packages (that will include
pre-compiled binary extensions, to avoid the need to download
development tools). Eventually it will be available on
[PyPi](https://pypi.org/).  However, for the time being, you will need
to follow the developer installation instructions, below.

# Installation (developer)

There are four main steps to the installation:
1. install a build environment
2. clone the repository
3. build
4. run tests

For most casual users and developers, we recommend using the miniconda
approach described below.

## 1. Install the build environment

To install the build environment, you should choose either `conda` or
system packages. Once you have chosen and installed the build
environment, you should follow the instructions related to the option
you chose here in all subsequent steps.

### 1.1 Install build environment via miniconda (recommended)

1. Visit https://docs.conda.io/en/latest/miniconda.html to download
the miniconda installer for your platform, and follow the instructions
to install.

   > In principle, the rest of the PyPop miniconda installation
   > process should work on any platform that is supported by
   > miniconda, but only Linux and MacOS have been tested in
   > standalone mode, at this time.

2. Once miniconda is installed, create a new conda environment, using
the following commands:

   ```
   conda create -n pypop3 gsl swig python=3
   ```

   This will download and create a self-contained build-environment that
uses of Python to the system-installed one, along with other
requirements. You will need to use this this environment for the
build, installation and running of PyPop. The conda environment name,
above, `pypop3`, can be replaced with your own name.

   > When installing on MacOS, before installing `conda`, you should
   > first to ensure that the Apple Command Line Developer Tools
   > (XCode) are
   > [installed](https://mac.install.guide/commandlinetools/4.html),
   > so you have the compiler (`clang`, the drop-in replacement for
   > `gcc`), `git` etc. `conda` is unable to include the full
   > development environment for `clang` as a conda package for legal
   > reasons.

3. Activate the environment, and set environments variables needed for
compilation:

   ```
   conda activate pypop3
   conda env config vars set CPATH=${CONDA_PREFIX}/include:${CPATH}
   conda env config vars set LIBRARY_PATH=${CONDA_PREFIX}/lib:${LIBRARY_PATH}
   conda env config vars set LD_LIBRARY_PATH=${CONDA_PREFIX}/lib:${LD_LIBRARY_PATH}
   ```

4. To ensure that the environment variables are saved, reactivate the
environment:

   ```
   conda activate pypop3
   ```

5. Skip ahead to [Clone the repository](#2-clone-the-repository).

### 1.2 Install build environment via system packages (advanced)

#### Unix/Linux:

1. Ensure Python 3 version of `pip` is installed:
   ```
   python3 -m ensurepip --user --no-default-pip
   ```
   > Note the use of the `python3` - you may find this to be necessary on
systems which parallel-install both Python 2 and 3, which is typically
the case. On newer systems you may find that `python` and `pip` are,
by default, the Python 3 version of those tools.

2. Install packages system-wide:
   1. Fedora/Centos/RHEL
      ```
      sudo dnf install git swig gsl-devel python3-devel
      ``` 
   2. Ubuntu
      ```
      sudo apt install git swig libgsl-dev python-setuptools
      ```

#### MacOS X

1. Install developer command-line tools: https://developer.apple.com/downloads/  (includes `git`, `gcc`)
2. Visit http://macports.org and follow the instructions there to install the latest version of MacPorts for your version of MacOS X.
3. Set environment variables to use macports version of Python and other packages, packages add the following to `~/.bash_profile`

   ```shell
   export PATH=/opt/local/bin:$PATH
   export LIBRARY_PATH=/opt/local/lib/:$LIBRARY_PATH
   export CPATH=/opt/local/include:$CPATH
   ```

4. Rerun your bash shell login in order to make these new exports active in your environment.  At the command line type: 

   ```shell
   exec bash -login
   ```

5. Install dependencies via MacPorts and set Python version to use (FIXME: currently untested!)

   ```shell
   sudo port install swig-python gsl py39-numpy py39-lxml py39-setuptools py39-pip py39-pytest
   sudo port select --set python python39
   sudo port select --set pip pip39
   ```

6. Check that the MacPorts version of Python is active by typing:
`which python`, if it is working correctly you should see
`/opt/local/bin/python`.

### Windows

(Currently untested in standalone-mode)

## 2. Clone the repository

```shell
git clone https://github.com/alexlancaster/pypop.git
cd pypop
```

## 3. Build PyPop

You should choose *either* of the following two approaches. Don't try
to mix-and-match the two. The build-and-install approach is
recommended for end-users, or you if don't plan to make any
modifications to the code locally.

### 3.1 Build-and-install (recommended for end-users)

Once you have setup your environment and cloned the repo, you can use
the following one-liner to examine the `setup.py` and pull all the
required dependencies from `pypi.org` and build and install the
package.

> Note that if you use this method and install the package, it will be
available to run anywhere on your system, by running `pypop.py`.

> _**If you use this installation method, changes you make to the
code, locally, or via subsequent `git pull` requests will not be
available in the installed version until you repeat the `pip install`
command.**_

1. if you installed the conda development environment, use:

   ```
   pip install .[test]
   ```
   
   > (the `[test]` keyword is included to make sure that any package
requirements for the test suite are installed as well).

2. if you installed a system-wide environment, the process is slightly
different, because we install into the user's `$HOME/.local` rather
than the conda environment:

   ```
   pip install --user .[test]
   ```

3. PyPop is ready-to-use, skip to [Run the test suite](#4-run-the-test-suite)

4. if you later decide you want to switch to using the developer
approach, below, follow the [uninstallation
instructions](#5-uninstalling-pypop-and-cleaning-up) before starting.

### 3.2 Build-and-run-from-checkout (recommended for developers)

1. First manually install the dependencies via `pip`, note that if you
are running on Python <= 3.8, you will need to also add
`importlib-resources` to the list of packages, below.

   1. conda
      ```
      pip install numpy lxml psutil pytest
      ```

   2. system-wide
      ```
      pip install --user numpy lxml psutil pytest
      ```

2. Run the build
   ```
   ./setup.py build
   ```

3. You will run PyPop, directly out of the `bin` subdirectory (e.g. `./src/bin/pypop.py`).

## 4. Run the test suite

You should first check that the build worked, by running the
test suite, via `pytest`:

```
pytest tests
````

If you run into errors, please first carefully repeat and/or check
your installation steps above.  If you still get errors, file a bug
(as per Support, below), and include the output of `pytest` run in verbose
mode and capturing the output

```
pytest -s -v tests
```

## 5. Uninstalling PyPop and cleaning up

If you installed using the end-user approach in section 3.1, above, you can
remove the installed version:

1. conda:
   ```
   pip uninstall pypop
   ``` 
2. system-wide:
   ```
   pip uninstall --user pypop
   ```

To clean-up any compiled files and force a recompilation from scratch,
run the `clean` command:

```
./setup clean --all
````

# Examples

These are examples of how to use PyPop. Specify the `--help` option to see an
explanation of the options available.

## Run a minimal dataset:

```
pypop.py -c  tests/data/minimal.ini tests/data/USAFEL-UchiTelle-small.pop
```

> replace `pypop.py`, by `./src/bin/pypop.py` if you installed using
section 3.2, i.e running locally from within the uninstalled checkout
of the repository

This will generate the following two files, an XML output file and a plain text version:

    USAFEL-UchiTelle-small-out.xml
    USAFEL-UchiTelle-small-out.txt

# Support

Please submit bug reports and feature requests

    https://github.com/alexlancaster/pypop/issues

## Bug reporting

When reporting bugs, especially during installation, please run the following and include the output:

```shell
echo $CPATH
echo $LIBRARY_PATH
echo $PATH
which python
```

If you are running on MacOS, and you used the MacPorts installation
method, please also run and include the output of:

```
port installed
```

## Development

The code for PyPop is at

    https://github.com/alexlancaster/pypop

More detailed notes and background relevant for maintainers, packagers
and developers are maintained in [DEV_NOTES.md](DEV_NOTES.md)

# Copyright and License

PyPop is Copyright (C) 2003-2015. The Regents of the University of California (Regents)

PyPop is distributed under the terms of GPLv2
