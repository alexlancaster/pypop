## Python for Population Genomics (PyPop)

PyPop is a framework for processing genotype and allele data and running analyses.

## Installation

### 1. Clone the repository:

    git clone https://github.com/alexlancaster/pypop.git
  
### 2. (optional) Create a new virtual environment within the repository

    cd pypop
    virtualenv pypopenv
    source pypopenv/bin/activate

Note that throughout we use ```<ENV>``` to refer to the full path name to the 'env' directory created in the previous step, e.g. ```/home/username/pypop/pypopenv```

### 3. Install Python packages from PyPI

None required yet

### 4. Install external tool dependencies:

We require a developer toolchain, e.g. ```gcc```

#### 4.1 Install ```swig```

TBD

### 5. Build

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
