# Developer notes

## Release notes for in-progress features not yet officially documented or supported

* New wrapper module `Haplostats`. This wraps a portion of the
  `haplo.stats` R package `haplo-stats` for haplotype
  estimation. [Implementation in alpha-phase - still working on this].

## Build-time notes

### External dependencies

* ```swig``` (Simple Wrapper Interface Generator) (build-time only)
* ```gsl``` (GNU Scientific Library) (build-time only)
* ```Numpy``` (Numpy)
* ```lxml``` (Python bindings)
* ```pytest``` (Python test framework)

### SWIG notes

* Note that within ".i" wrappers, need to include function prototypes
and SWIG wrappers, so functions are duplicated, see this
[StackOverflow
post](https://stackoverflow.com/questions/66995429/cant-run-swig-tutorial-for-python)

### macports.org

* To install macports via the command-line you can run the following (substituting the current link):

```
curl -L 'https://github.com/macports/macports-base/releases/download/v2.4.1/MacPorts-2.4.1-10.12-Sierra.pkg' > MacPorts-2.4.1-10.12-Sierra.pkg
sudo installer -pkg MacPorts-2.4.1-10.12-Sierra.pkg  -target /
```

## GitHub notes

Unused stanzas in `build_wheels.yml` workflow to manually regenerate a
GitHub release based on re-tagging (e.g. after a Zenodo deposition).
They have been disabled for the time being because they are done
internally by the `zenodraft` action.

This first part is needed just after `find -empty type d -delete` in
the `run` part of the "Pubsh changes back to repo files"
`publish_zenodo` job:

```
          git tag -d $GITHUB_REF_NAME
          git push --follow-tags origin :$GITHUB_REF
          git tag $GITHUB_REF_NAME
          git push origin $GITHUB_REF
          git ls-remote origin $GITHUB_REF
```

This second part would be the last step in the same `publish_zenodo`
job:

```
      #
      # FIXME: disabled the rest of these steps (already done by zenodraft)
      #
      - name: Get existing release
        if: false
        id: get_existing_release
        uses: cardinalby/git-get-release-action@v1
        env:
          GITHUB_TOKEN: ${{ github.token }}
        with:
          releaseId: ${{ github.event.release.id }}
      - name: Delete old release
        if: false
        uses: liudonghua123/delete-release-action@v1
        env:
          GITHUB_TOKEN: ${{ github.token }}
        with:
          release_id: ${{ github.event.release.id }}
      - name: Recreate release with new tag
        if: false
        id: recreate_release
        uses: joutvhu/create-release@v1
        with:
          tag_name: ${{ github.event.release.tag_name }}
          name: ${{ steps.get_existing_release.outputs.name }}
          body: ${{ steps.get_existing_release.outputs.body }}
          # FIXME: have to set these both to false, because not copied
          # from the original release properly
          # draft: ${{ steps.get_existing_release.outputs.draft }}
          # prerelease: ${{ steps.get_existing_release.outputs.draft }}
          draft: false
          prerelease: false
          target_commitish: ${{ steps.get_existing_release.outputs.target_commitish }}
          on_release_exists: update
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          # GITHUB_TOKEN: ${{ secrets.PYPOP_RELEASE_TOKEN }}
```

## Design notes

(These should eventually be migrated back in the source code, so that,
if and when we generate API docs, they will appear there.  They would
need updating as part of that migration to make sure they are still
accurate.)

* `Main` is the primary interface to the PyPop modules.  Given a
ConfigParser instance, which can be (1) created from a filename passed
from command-line argument or (2) from values populated by the GUI
(currently selected from an .ini file, but can ultimately be set
directly from the GUI or values based from a form to a web server or
the) it then runs the specified modules (outlined below).

* `GUIApp` is the graphical front-end to PyPop which uses the
"wxPython":http://www.wxpython.org GUI toolkit.  wxPython is a set of
Python bindings to "wxWindows":http://www.wxwindows.org, which is an
open-source cross-platform GUI widget toolkit which has a native look
under GNU/Linux (GTK), Windows (MFC) and MacOS X (Aqua).  [as of 2023,
this was removed]

* `ParseFile` is a base class which has most of the common functionality
for reading files.

* `ParseGenotypeFile` is a subclass of `ParseFile` that deals with
files that consist specifically of data with individual genotyped for
one or more loci.

* `ParseAlleleCount` is another subclass of `ParseFile` that deals
with files consisting of allele counts across a whole population.

* `HardyWeinberg` is a class that calculates Hardy-Weinberg
statistics given genotype data for a single locus.

* `HardyWeinbergGuoThompson` a subclass of `HardyWeinberg` that uses the
Guo & Thompson algorithm for calculating statistics.

* `HardyWeinbergGuoThompsonArlequin` a subclass of `HardyWeinberg`
that uses the Arlequin implementation of the Guo & Thompson algorithm
for calculating statistics.

* `Haplo` is an abstract base class for estimating haplotypes given
genotype data.

- `HaploArlequin` is a subclass of `Haplo` that uses Arlequin for
estimation of haplotypes (obsolete).

* `Emhaplofreq` is a subclass of `Haplo` that uses `emhaplofreq` (Rich
Single`s program) for the estimation of haplotypes and linkage
disequilibrium values.

* `ArlequinWrapper` the underlying class that "wraps" the
functionality of the "Arlequin":http://lgb.unige.ch/arlequin/ program
(obsolete: this class, in turn, supplies `HaploArlequin` with required
information).

* `Homozygosity` Calculates homozygosity statistics for a given locus,
calculates the observed homozygosity and returns the approximate
expected homozygosity statistics taken from previous simulation runs.

Both file formats are assumed to have a population header information
with, consisting of a line of column headers (population metadata)
followed by a line with the actual data, followed by the column
headers for the samples (sample metadata) followed by the sample data
itself (either individuals in the genotyped case, or alleles in the
allele count case).

## Obsolete notes

These are either obsoleted by new versions of dependencies or
platforms, or no longer work, and need to be updated. Keeping around
in case of either old platforms or if there is interest in reviving
the feature(s) in question.

### Installing ```swig``` on certain Ubuntu releases

(obsoleted by newer Ubuntu releases)

There is a bug in versions swig 3.0.6 to 3.0.10 that prevents swig on
```xenial``` (which is version 3.0.8 of swig) working.  You will need
to install the lastest version from source.

1. Get swig dependency: 

```sudo apt install libpcre3-dev```

2. Visit [swig.org](swig.org) to get download link

3. Do the installation:

       tar zxvf ~/swig-3.0.12.tar.gz
       cd swig-3.0.12
       ./configure
       make
       sudo make install

### Containerizing

(WARNING: instructions are obsolete with the Python 3 port) 

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

