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

* Add ```/opt/local/bin``` to your ```$PATH``` variable (e.g. by editing ```~/.bash_profile```)

### 2. Clone the repository:

    git clone https://github.com/alexlancaster/pypop.git
  
### 3. (optional) Create a new virtual environment within the repository

    cd pypop
    virtualenv pypopenv
    source pypopenv/bin/activate

Note that throughout we use ```<ENV>``` to refer to the full path name to the 'env' directory created in the previous step, e.g. ```/home/username/pypop/pypopenv```

### 4. Install Python packages from PyPI

None required yet

### 5. Install external tool dependencies:


#### 5.1 ```swig``` (Simple Wrapper Interface Generator) and ```gsl``` (GNU Scientific Library)

* MacOS: ```sudo port install swig-python gsl```
* Linux/Fedora: ```sudo dnf install swig gsl-devel```
* Linux/Debian: ```sudo apt-get install swig gsl-devel```


### 6. Build

    ./setup.py build

## Examples

These are examples of how to use PyPop. Specify the `--help` option to see an
explanation of the options available.

### Run a minimal dataset:

    ./pypop.py -c  data/samples/minimal-anthonynolan.ini data/samples/USAFEL-UchiTelle-small.pop

This will generate the following three files, an XML output file, the plain text version and a filter information:


    USAFEL-UchiTelle-small-out.xml
    USAFEL-UchiTelle-small-out.txt
    USAFEL-UchiTelle-small-filter.xml

## Support

Please submit bug reports and feature requests

    https://github.com/alexlancaster/pypop/issues

## Development

The code for PyPop is at

    https://github.com/alexlancaster/pypop

## Copyright and License

PyPop is Copyright (C) 2003-2015. The Regents of the University of California (Regents)

PyPop is distributed under the terms of GPLv2
