## Python for Population Genomics (PyPop)

PyPop is a framework for processing genotype and allele data and running analyses.

## Installation

### 1. Install OS-specific tools

#### MacOS X

1. install developer command-line tools: https://developer.apple.com/downloads/  (includes ```git```, ```gcc```)
2. Visit http://macports.org to find the latest version for your version of MacOS X.

* To install via the GUI follow the instructions 
 
OR

* To install via the command-line you can run the following (substituting the current link):

```
curl -L 'https://github.com/macports/macports-base/releases/download/v2.4.1/MacPorts-2.4.1-10.12-Sierra.pkg' > MacPorts-2.4.1-10.12-Sierra.pkg
sudo installer -pkg MacPorts-2.4.1-10.12-Sierra.pkg  -target /
```

* Set environment variables to use macports version of Python and other packages, packages add the following to ```~/.bash_profile```

```
export PATH=/opt/local/bin:$PATH
export LIBRARY_PATH=/opt/local/lib/:$LIBRARY_PATH
export CPATH=/opt/local/include:$CPATH
```

### 2. Clone the repository:

    git clone https://github.com/alexlancaster/pypop.git
  
### 3. (optional) Create a new virtual environment within the repository

    cd pypop
    virtualenv pypopenv
    source pypopenv/bin/activate

Note that throughout we use ```<ENV>``` to refer to the full path name to the 'env' directory created in the previous step, e.g. ```/home/username/pypop/pypopenv```

### 4. Install external dependencies

* ```swig``` (Simple Wrapper Interface Generator) 
* ```gsl``` (GNU Scientific Library)
* ```Numeric``` (Python Numeric)
* ```libxml2/libxslt``` (Python bindings)

* MacOS:

      sudo port install swig-python gsl py27-numeric py-libxml2 py27-libxslt

* Linux/Fedora: 

      sudo dnf install swig gsl-devel python-numeric python-libxml2 python-libxslt

* Linux/Debian: 

      sudo apt-get install swig gsl-devel python-libxml2

### 5. Build

    ./setup.py build

## Examples

These are examples of how to use PyPop. Specify the `--help` option to see an
explanation of the options available.

### Run a minimal dataset:

    ./pypop.py -c  data/samples/minimal.ini data/samples/USAFEL-UchiTelle-small.pop

This will generate the following three files, an XML output file, the plain text version and a filter information:


    USAFEL-UchiTelle-small-out.xml
    USAFEL-UchiTelle-small-out.txt
    USAFEL-UchiTelle-small-filter.xml

## Support

Please submit bug reports and feature requests

    https://github.com/alexlancaster/pypop/issues

### Bug reporting

When reporting bugs, please run the following and include the output:

    echo $CPATH
    echo $LIBRARY_PATH
    echo $PATH

If you are MacOS please also run and include the output of:

    port installed

## Development

The code for PyPop is at

    https://github.com/alexlancaster/pypop

## Copyright and License

PyPop is Copyright (C) 2003-2015. The Regents of the University of California (Regents)

PyPop is distributed under the terms of GPLv2
