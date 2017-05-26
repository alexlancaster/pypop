Developer notes

macports.org

* To install macports via the command-line you can run the following (substituting the current link):

```
curl -L 'https://github.com/macports/macports-base/releases/download/v2.4.1/MacPorts-2.4.1-10.12-Sierra.pkg' > MacPorts-2.4.1-10.12-Sierra.pkg
sudo installer -pkg MacPorts-2.4.1-10.12-Sierra.pkg  -target /
```

# Containerizing

To make pypop more portable (given that some of its dependencies are currently
obsolete), it is possible to build a Singularity container which contains a
minimal Fedora 25 installation (minus the Kernel), pypop, pypop's dependencies,
and some extra tools (`yum`, `rpm`, `less`, and `vim`) in case you need to do
work inside the container.

Singularity containers bind-mount many external directories by default (for
example, `/home` and `/tmp`), with the container image kept read-only.  When
run inside the container, pypop will work on your files, even though they live
outside the container.

Singularity 2.3 or later is required in order to bootstrap this container.  The
container also must be bootstrapped & run on a Linux system, running the
x86\_64 architecture, because that's the OS & architecture the container uses.

To build pypop as a singularity container, once you have Singularity installed,
perform these three steps:

1. `cd path/to/pypop/source`
2. `singularity create -s 2048 image.img`
3. `sudo singularity bootstrap image.img Singularity`

The above commands will give you a 2 GiB executable file named `image.img`.
That is the container.

The first command ensures that you are in the pypop source directory.  This is
required because part of the bootstrap process copies the source into the
container.

The second command creates a 2 GiB (a 2048 MiB) container image.  This should
be large enough, but you can increase or decrease it as you wish.  Note that if
you make it too small, the bootstrap might not have enough room to complete!

The final command performs the bootstrap.  The bootstrap needs to be run as root, so you either need to use `sudo` (as shown in the example above) or you need to run the command in a root shell.  The bootstrap does a number of things:

* Mount the container image read/write.
* Download and install the Fedora 25 GPG key.
* Create a temporary Yum repo file, pointing to the Fedora 24 package archive.
* Install the `basesystem` package; GCC, SWIG, and GSL; Python (both the
* executable and development packages); and the Python modules for Numeric,
libxml2, and libxslt.
* Copy the entire pypop source directory into the container.
* Build pypop (again, inside the container).

Once you have the container image, running it is as simple as executing
`image.img`.  For example:

    akkornel@blargh-yakkety-typical:~/pypop$ ./image.img -V
    pypop 0.8.0
    Copyright (C) 2003-2005 Regents of the University of California
    This is free software.  There is NO warranty; not even for
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    
    akkornel@blargh-yakkety-typical:~/pypop$ ./image.img -h
    Usage: pypop [OPTION]... [INPUTFILE]...
    Process and run population genetics statistics on one or more INPUTFILEs.
    Expects to find a configuration file called 'config.ini' in the
    current directory or in /usr/share/pypop/config.ini.
    
      -l, --use-libxslt    filter XML via XSLT using libxslt (default)
      -s, --use-4suite     filter XML via XSLT using 4Suite
      -x, --xsl=FILE       use XSLT translation file FILE
      -h, --help           show this message
      -c, --config=FILE    select alternative config file
      -d, --debug          enable debugging output (overrides config file setting)
      -i, --interactive    run in interactive mode, prompting user for file names
      -g, --gui            run GUI (currently disabled)
      -o, --outputdir=DIR  put output in directory DIR
      -f, --filelist=FILE  file containing list of files (one per line) to process
                            (mutually exclusive with supplying INPUTFILEs)
          --generate-tsv   generate TSV output files (aka run 'popmeta')
      -V, --version        print version of PyPop
      
      INPUTFILE   input text file

Once built, the container image can be transferred to any other system which is
running Linux x86\_64, and which has the same version of Singularity (or newer).
