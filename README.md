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

      sudo port install swig-python gsl py27-numeric py-libxml2 py27-libxslt py-setuptools py27-pip
      
Set MacPorts to use the just-installed 2.7 MacPorts version of Python and pip:

      sudo port select --set python python27
      sudo port select --set pip pip27

Check that the MacPorts version of Python is active by typing: ```which python```, if it is working correctly you should see the following:

```
/opt/local/bin/python
````

#### Linux (Fedora/Centos/RHEL): 

Need at least Fedora 25 for the appropriate dependencies:

      sudo dnf install swig gsl-devel python-numeric python-libxml2 libxslt-python python-setuptools python-pip

See [DEV_NOTES.md](DEV_NOTES.md) for instructions on containerizing the install on a Centos/RHEL release.

#### Linux (Ubuntu)

Install the following packages

      apt install git swig libgsl-dev python-libxml2 python-libxslt1 python-setuptools python-pip

The ```python-numeric``` package is not included in the current version of Ubuntu, please see [DEV_NOTES.md](DEV_NOTES.md) for details of how to setup your repository to find python-numeric, once found, install using the following

      apt-get install python-numeric 

### 4. Build

    ./setup.py build

## Examples

These are examples of how to use PyPop. Specify the `--help` option to see an
explanation of the options available.

### Run a minimal dataset:

    ./bin/pypop.py -c  data/samples/minimal.ini data/samples/USAFEL-UchiTelle-small.pop

This will generate the following two files, an XML output file and a plain text version:

    USAFEL-UchiTelle-small-out.xml
    USAFEL-UchiTelle-small-out.txt

## Running test suite

Use pip to install ```pytest```:

      pip install --user pytest

(Ensure that the local user path is in ```PATH```, you may need to modify ```~/.bash_profile``` accordingly.  On MacOS e.g. ```export PATH=$HOME/Library/Python/2.7/bin:$PATH```, on Linux ```export PATH=$HOME/.local/bin:$PATH```.)  Verify that py.test is in your ```PATH``` by running ```which py.test```.

Run the test suite:

      py.test

If you run into errors, file a bug (as per Support, below), include the output of ```py.test``` run in verbose mode and capturing the output:

      py.test -s -v

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
