## Python for Population Genomics (PyPop)

PyPop is a framework for processing genotype and allele data and running population genetic analyses.

## Installation

### 1. Install OS-specific development environment

#### MacOS X

1. install developer command-line tools: https://developer.apple.com/downloads/  (includes ```git```, ```gcc```)
2. Visit http://macports.org and follow the instructions there to install the latest version of MacPorts for your version of MacOS X.
3. Set environment variables to use macports version of Python and other packages, packages add the following to ```~/.bash_profile```

```
export PATH=/opt/local/bin:$PATH
export LIBRARY_PATH=/opt/local/lib/:$LIBRARY_PATH
export CPATH=/opt/local/include:$CPATH
```

4. Rerun your bash shell login in order to make these new exports active in your environment.  At the command line type: 

```
exec bash -login
```

### 2. Clone the repository:

    git clone https://github.com/alexlancaster/pypop.git
  
### 3. Install dependencies

#### MacOS:

Install the MacPorts packages

      sudo port install swig-python gsl py27-numpy py-libxml2 py27-libxslt py-setuptools py27-pip
      
Set MacPorts to use the just-installed 2.7 MacPorts version of Python and pip:

      sudo port select --set python python27
      sudo port select --set pip pip27

Check that the MacPorts version of Python is active by typing: ```which python```, if it is working correctly you should see the following:

```
/opt/local/bin/python
```

#### Linux (Fedora/Centos/RHEL): 

Need at least Fedora 25 for the appropriate dependencies:

      sudo dnf install swig gsl-devel python2-numpy python-libxml2 libxslt-python python-setuptools python-pip

See [DEV_NOTES.md](DEV_NOTES.md) for instructions on containerizing the install on a Centos/RHEL release.

#### Linux (Ubuntu)

Install the following packages

      sudo apt install git libgsl-dev python-numpy python-libxml2 python-libxslt1 python-setuptools python-pip

The ```swig``` package in recent Ubuntu releases has bugs, you will need to compile the most recent from source, see also [DEV_NOTES.md](DEV_NOTES.md) for details.

### 4. Build

    ./setup.py build

## Examples

These are examples of how to use PyPop. Specify the `--help` option to see an
explanation of the options available.

### Run a minimal dataset:

    ./bin/pypop.py -c  tests/data/minimal.ini tests/data/USAFEL-UchiTelle-small.pop

This will generate the following two files, an XML output file and a plain text version:

    USAFEL-UchiTelle-small-out.xml
    USAFEL-UchiTelle-small-out.txt

## Running test suite

      ./setup.py test

If you run into errors, file a bug (as per Support, below), include the output of ```py.test``` run in verbose mode and capturing the output

      py.test -s -v

(See DEV_NOTES.md for more details on installing or running ```py.test``` outside the context of setuptools.)

## Support

Please submit bug reports and feature requests

    https://github.com/alexlancaster/pypop/issues

### Bug reporting

When reporting bugs, especially during installation, please run the following and include the output:

    echo $CPATH
    echo $LIBRARY_PATH
    echo $PATH
    which python

If you are running on MacOS please also run and include the output of:

    port installed

## Development

The code for PyPop is at

    https://github.com/alexlancaster/pypop

## Copyright and License

PyPop is Copyright (C) 2003-2015. The Regents of the University of California (Regents)

PyPop is distributed under the terms of GPLv2
