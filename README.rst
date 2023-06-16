Python for Population Genomics (PyPop)
======================================

PyPop is a framework for processing genotype and allele data and
running population genetic analyses.  See the `PyPop User Guide
<http://pypop.org/docs>`__ for a more detailed description.

.. |pkgname| replace:: ``pypopgen``

.. _guide-include-start:

Installation (end user)
=======================

.. note::

   The package name for installation purposes is ``pypopgen`` - to
   avoid conflicting with an unrelated package with the name ``pypop``
   already on PyPI. 


Install Python 3 and ``pip``
----------------------------

A full description of installing Python and ``pip`` on your system is
beyond the scope of this guide, we recommend starting here:

   https://wiki.python.org/moin/BeginnersGuide/Download

Note that many systems (mostly Linux distributions) come with Python 3
preinstalled. MacOS 10.9 (Jaguar) up until 12.3 (Catalina), used to
ship with Python 2 pre-installed, but it now has to be manually
installed.  There are quick-start guides for `MacOS
<https://docs.python.org/3/using/mac.html>`__ and `Windows
<https://docs.python.org/3/using/windows.html>`__ in the official
documentation.

Install package from GitHub Releases
------------------------------------

Once you have both python and ``pip`` installed, you can use ``pip``
to install pre-compiled binary "wheels" of ``pypopgen`` pre-releases,
available from the GitHub release page:

   https://github.com/alexlancaster/pypop/releases

.. warning::

   **These pre-release versions are being made available for initial
   testing, they are not intended to be used for production
   applications or analysis**
   
First, visit the release page, and choose the release version you wish
to install (usually the most recent), and note the release tag
(e.g. ``v1.0.0-alpha.8``). Next, use ``pip`` to install the package by
running a command of the form (this will select and install the
correct wheel for your Python version and operating system
automatically):

.. code-block:: shell
      
   pip install --user pypopgen -f 'https://github.com/alexlancaster/pypop/releases/expanded_assets/<TAG_NAME>' 

where *<TAG_NAME>* is replaced with a specific tag, e.g. for the example given above, you would run:

.. code-block:: shell
   
   pip install --user pypopgen -f 'https://github.com/alexlancaster/pypop/releases/expanded_assets/v1.0.0-alpha.8'


You can also manually download the specific wheel from the github
release webpage and install directly, e.g.:

.. code-block:: shell
   
   pip install --user pypopgen-1.0.0a8-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
   
**Upgrade an existing PyPop installation**

To update an existing installation to a newer version, use the same
command as above, but add the ``--upgrade`` (short version: ``-U``)
flag, i.e. ``pip install -U --user pypopgen -f ...``.

		
Install package from PyPI
-------------------------

TBA.  Eventually, we will be making PyPop available directly on `PyPI
<https://pypi.org/>`__.

.. note::

   If, for whatever reason, you cannot use the these binaries
   (e.g. the pre-compiled binaries are not available for your
   platform), you may need to follow the developer installation
   instructions, below.

Once you have installed the package, you can skip ahead to the
`section on Examples <Examples_>`_

Installation (developer)
========================

There are four main steps to the developer installation:

1. install a build environment
2. clone the repository
3. build
4. run tests

For most casual users and developers, we recommend using the miniconda
approach described below.

Install the build environment
-----------------------------

To install the build environment, you should choose either ``conda`` or
system packages. Once you have chosen and installed the build
environment, you should follow the instructions related to the option
you chose here in all subsequent steps.

Install build environment via miniconda (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Visit https://docs.conda.io/en/latest/miniconda.html to download the
   miniconda installer for your platform, and follow the instructions to
   install.

      In principle, the rest of the PyPop miniconda installation process
      should work on any platform that is supported by miniconda, but
      only Linux and MacOS have been tested in standalone mode, at this
      time.

2. Once miniconda is installed, create a new conda environment, using
   the following commands:

   .. code-block:: shell

      conda create -n pypop3 gsl swig python=3

   This will download and create a self-contained build-environment that
   uses of Python to the system-installed one, along with other
   requirements. You will need to use this this environment for the
   build, installation and running of PyPop. The conda environment name,
   above, ``pypop3``, can be replaced with your own name.

      When installing on MacOS, before installing ``conda``, you should
      first to ensure that the Apple Command Line Developer Tools
      (XCode) are
      `installed <https://mac.install.guide/commandlinetools/4.html>`__,
      so you have the compiler (``clang``, the drop-in replacement for
      ``gcc``), ``git`` etc. ``conda`` is unable to include the full
      development environment for ``clang`` as a conda package for legal
      reasons.

3. Activate the environment, and set environments variables needed for
   compilation:

   .. code-block:: shell

      conda activate pypop3
      conda env config vars set CPATH=${CONDA_PREFIX}/include:${CPATH}
      conda env config vars set LIBRARY_PATH=${CONDA_PREFIX}/lib:${LIBRARY_PATH}
      conda env config vars set LD_LIBRARY_PATH=${CONDA_PREFIX}/lib:${LD_LIBRARY_PATH}

4. To ensure that the environment variables are saved, reactivate the
   environment:

   .. code-block:: shell

      conda activate pypop3

5. Skip ahead to `Clone the repository <Clone the repository_>`_

Install build environment via system packages (advanced)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unix/Linux:
^^^^^^^^^^^

1. Ensure Python 3 version of ``pip`` is installed:

   ::

      python3 -m ensurepip --user --no-default-pip

   ..

      Note the use of the ``python3`` - you may find this to be
      necessary on systems which parallel-install both Python 2 and 3,
      which is typically the case. On newer systems you may find that
      ``python`` and ``pip`` are, by default, the Python 3 version of
      those tools.

2. Install packages system-wide:

   1. Fedora/Centos/RHEL

      ::

         sudo dnf install git swig gsl-devel python3-devel

   2. Ubuntu

      ::

         sudo apt install git swig libgsl-dev python-setuptools

MacOS X
^^^^^^^

1. Install developer command-line tools:
   https://developer.apple.com/downloads/ (includes ``git``, ``gcc``)

2. Visit http://macports.org and follow the instructions there to
   install the latest version of MacPorts for your version of MacOS X.

3. Set environment variables to use macports version of Python and other
   packages, packages add the following to ``~/.bash_profile``

   .. code:: shell

      export PATH=/opt/local/bin:$PATH
      export LIBRARY_PATH=/opt/local/lib/:$LIBRARY_PATH
      export CPATH=/opt/local/include:$CPATH

4. Rerun your bash shell login in order to make these new exports active
   in your environment. At the command line type:

   .. code:: shell

      exec bash -login

5. Install dependencies via MacPorts and set Python version to use
   (FIXME: currently untested!)

   .. code:: shell

      sudo port install swig-python gsl py39-numpy py39-lxml py39-setuptools py39-pip py39-pytest
      sudo port select --set python python39
      sudo port select --set pip pip39

6. Check that the MacPorts version of Python is active by typing:
   ``which python``, if it is working correctly you should see
   ``/opt/local/bin/python``.

Windows
~~~~~~~

(Currently untested in standalone-mode)

Clone the repository
--------------------

.. code:: shell

   git clone https://github.com/alexlancaster/pypop.git
   cd pypop

Build PyPop
-----------

You should choose *either* of the following two approaches. Don’t try to
mix-and-match the two. The build-and-install approach is recommended for
end-users, or you if don’t plan to make any modifications to the code
locally.

Build-and-install (recommended for end-users)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have setup your environment and cloned the repo, you can use
the following one-liner to examine the ``setup.py`` and pull all the
required dependencies from ``pypi.org`` and build and install the
package.

   Note that if you use this method and install the package, it will be
   available to run anywhere on your system, by running ``pypop.py``.

..

   If you use this installation method, changes you make to the code,
   locally, or via subsequent ``git pull`` requests will not be
   available in the installed version until you repeat the
   ``pip install`` command.

1. if you installed the conda development environment, use:

   ::

      pip install .[test]

   ..

      (the ``[test]`` keyword is included to make sure that any package
      requirements for the test suite are installed as well).

2. if you installed a system-wide environment, the process is slightly
   different, because we install into the user’s ``$HOME/.local`` rather
   than the conda environment:

   ::

      pip install --user .[test]

3. PyPop is ready-to-use, skip to `Run the test suite`_.

4. if you later decide you want to switch to using the developer
   approach, below, follow the `Uninstalling PyPop and cleaning up`_ before
   starting.

Build-and-run-from-checkout (recommended for developers)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. First manually install the dependencies via ``pip``, note that if you
   are running on Python <= 3.8, you will need to also add
   ``importlib-resources`` to the list of packages, below.

   1. conda

      ::

         pip install numpy lxml psutil pytest

   2. system-wide

      ::

         pip install --user numpy lxml psutil pytest

2. Run the build

   ::

      ./setup.py build

3. You will run PyPop, directly out of the ``src/bin`` subdirectory
   (e.g. ``./src/bin/pypop.py``).

Run the test suite
------------------

You should first check that the build worked, by running the test suite,
via ``pytest``:

::

   pytest tests

If you run into errors, please first carefully repeat and/or check your
installation steps above. If you still get errors, file a bug (as per
Support, below), and include the output of ``pytest`` run in verbose
mode and capturing the output

::

   pytest -s -v tests

Uninstalling PyPop and cleaning up
----------------------------------

If you installed using the end-user approach in `Build-and-install (recommended for end-users)`_, above, you
can remove the installed version:

::

   pip uninstall pypopgen

To clean-up any compiled files and force a recompilation from scratch,
run the ``clean`` command:

::

   ./setup clean --all

Examples
========

These are examples of how to use PyPop. Specify the ``--help`` option to
see an explanation of the options available.

Run a minimal dataset:
----------------------

::

   pypop.py -c  tests/data/minimal.ini tests/data/USAFEL-UchiTelle-small.pop

..

   replace ``pypop.py``, by ``./src/bin/pypop.py`` if you installed
   using `Build-and-run-from-checkout (recommended for developers)`_,
   i.e running locally from within the uninstalled checkout of the repository

This will generate the following two files, an XML output file and a
plain text version:

::

   USAFEL-UchiTelle-small-out.xml
   USAFEL-UchiTelle-small-out.txt

Support
=======

Please submit any bug reports,feature requests or questions, via our GitHub issue tracker:


   https://github.com/alexlancaster/pypop/issues

Please **do not** report via private email to developers.

Bug reporting
-------------

When reporting bugs, especially during installation, please run the
following and include the output:

.. code:: shell

   echo $CPATH
   echo $LIBRARY_PATH
   echo $PATH
   which python

If you are running on MacOS, and you used the MacPorts installation
method, please also run and include the output of:

::

   port installed

Development
-----------

The development of the code for PyPop is via our GitHub project:

   https://github.com/alexlancaster/pypop

.. _guide-include-end:

More detailed notes and background relevant for maintainers, packagers
and developers are maintained in `DEV_NOTES.md <DEV_NOTES.md>`__. Source for website and the documentation is located in the `website <website>`__ subdirectory.

Copyright and License
=====================

PyPop is Copyright (C) 2003-2015. The Regents of the University of
California (Regents)

PyPop is distributed under the terms of GPLv2
