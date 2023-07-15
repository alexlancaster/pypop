Python for Population Genomics (PyPop)
======================================

PyPop is a framework for processing genotype and allele data and
running population genetic analyses.  See the `PyPop User Guide
<http://pypop.org/docs>`__ for a more detailed description.

.. |pkgname| replace:: ``pypop-genomics``

.. _guide-include-start:

.. ATTENTION:: 

   The working package name for installation purposes is
   ``pypop-genomics`` - to avoid conflicting with an unrelated package with
   the name ``pypop`` already on `PyPI <https://pypi.org>`__. This may
   change and is not yet the final package name until the package is
   released to PyPI.

Installation (end user)
=======================

There are two steps to the end-user installation:

1. install Python and ``pip``
2. install package from Github release


Install Python 3 and ``pip``
----------------------------

A full description of installing Python and ``pip`` on your system is
beyond the scope of this guide, we recommend starting here:

   https://wiki.python.org/moin/BeginnersGuide/Download

Here are some additional platform-specific notes that may be helpful:
   
- Most Linux distributions come with Python 3 preinstalled. On most
  modern systems, ``pip`` and ``python`` will default to Python 3.

- MacOS 10.9 (Jaguar) up until 12.3 (Catalina), used to ship with
  Python 2 pre-installed, but it now has to be manually installed.
  See the `MacOS quick-start guide
  <https://docs.python.org/3/using/mac.html>`__ in the official
  documentation for how to install Python 3. (Note that if Python is
  installed on Mac via the MacOS developer tools, it may include the
  version ``3`` suffix on commands, e.g. ``python3`` and ``pip3``, so
  modify the below, accordingly).

- For Windows, see also the `Windows quick-start guide
  <https://docs.python.org/3/using/windows.html>`__ in the official
  documentation. Running ``python`` in the Windows command terminal
  in Windows 11 and later will launch the installer for the
  Microsoft-maintained Windows package of Python 3.

Install package from GitHub Releases
------------------------------------

Once you have both python and ``pip`` installed, you can use ``pip``
to install pre-compiled binary "wheels" of ``pypop-genomics`` pre-releases,
available from the GitHub release page:

   https://github.com/alexlancaster/pypop/releases

.. warning::

   **These pre-release versions are being made available for initial
   testing, they are not intended to be used for production
   applications or analysis**

.. note::

   If, for whatever reason, you cannot use the these binaries
   (e.g. the pre-compiled binaries are not available for your
   platform), you may need to follow the `developer installation
   instructions <Installation (developer)_>`_, below.
   
1. First, visit the release page, and choose the release version you
   wish to install (usually the most recent), and note the release tag
   (e.g. ``v1.0.0-a23``).

   .. admonition:: Release version numbers

      Note that version of the release is slightly different to the
      ``git`` tag.  This is because the ``git`` tag follows `Semantic
      Versioning <https://semver.org/>`__, which Python internally
      normalizes and abbreviates.  So the release with the ``git`` tag
      ``v1.0.0-a23`` is actually version ``1.0.0a23`` of the
      ``pypop-genomics`` package, and the version that ``pip`` "sees".

2. Next, use ``pip`` to install the package by running a command of
   the form (this will select and install the correct wheel for your
   Python version and operating system automatically):

   .. code-block:: shell
      
      pip install pypop-genomics -f https://github.com/alexlancaster/pypop/releases/expanded_assets/<TAG_NAME>

   where *<TAG_NAME>* is replaced with a specific tag, e.g. for the example given above, you would run:

   .. code-block:: shell
   
      pip install pypop-genomics -f https://github.com/alexlancaster/pypop/releases/expanded_assets/v1.0.0-a23

   You can also manually download the specific wheel from the github
   release webpage and install directly, e.g.:

   .. code-block:: shell
   
      pip install pypop-genomics-1.0.0a23-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
		
**Upgrade an existing PyPop installation**

To update an existing installation to a newer version, use the same
command as above, but add the ``--upgrade`` (short version: ``-U``)
flag, i.e.

.. code-block:: shell

   pip install -U pypop-genomics -f ...

**Issues with installation permission**

By default, ``pip`` will attempt to install the ``pypop-genomics`` package
wherever the current Python installation is installed.  This location
may be a user-specific virtual environment (like ``conda``, see
below), or a system-wide installation. On many Unix-based systems,
Python will generally already be pre-installed in a "system-wide"
location (e.g. under ``/usr/lib``) which is read-only for regular
users. (This can also be true for system-installed versions of Python
on Windows and MacOS.)

When ``pip install`` cannot install in a read-only system-wide
location , ``pip`` will gracefully "fall-back" to installing just for
you in your home directory (typically ``~/.local/lib/python<VER>``
where ``<VER>`` is the version number of your current Python). In
general, this is what is wanted, so the above instructions are
normally sufficient.

However, you can also explicitly set installation to be in the user
directory, by adding the ``--user`` command-line option to the ``pip
install`` command, i.e.:

.. code-block:: shell

   pip install pypop-genomics --user ...

This may be necessary in certain cases where ``pip install`` doesn't
install into the expected user directory.
   
.. admonition:: Installing within a ``conda`` environment

   In the special case that you installing from within an activated
   user-specific ``conda`` virtual environment that provides Python,
   then you should **not** add the ``--user`` because it will install
   it in ``~/.local/lib/`` rather than under the user-specific conda
   virtual environment in ``~/.conda/envs/``.
		
Install package from PyPI [not yet available]
---------------------------------------------

TBA.  Eventually, we will be making PyPop available directly on `PyPI
<https://pypi.org/>`__.

Post-install ``PATH`` adjustments
---------------------------------
   
You may need to adjust the ``PATH`` settings (especially on Windows)
for the ``pypop`` scripts to be visible when run from your console
application, without having to supply the full path to the ``pypop``
executable file.

.. warning::

   Pay close attention to the "WARNINGS" that are shown during the
   ``pip`` installation, they will often note which directories need to
   be added to the ``PATH``.

- On Linux and MacOS, systems this is normally fairly simple and only
  requires edit of the shell ``.profile``, or similar and addition of
  the ``$HOME/.local/bin`` to the ``PATH`` variable, followed by a
  restart of the terminal.

- For Windows, however, as noted in most online `instructions
  <https://www.computerhope.com/issues/ch000549.htm>`_, this may need
  additional help from your system administrator if your user doesn't
  have the right permissions, and also require a system reboot.
   
Once you have installed the package, you can skip ahead to the
`section on Examples <Examples_>`_


Uninstalling PyPop and cleaning up
----------------------------------

If you installed using the end-user approach in `Build-and-install (recommended for end-users)`_, above, you
can remove the installed version:

::

   pip uninstall pypop-genomics

To clean-up any compiled files and force a recompilation from scratch,
run the ``clean`` command:

::

   ./setup clean --all

.. _guide_readme_examples:

Examples
========

These are examples of how to check that the program is installed and
some minimal use cases.

Checking version and installation
---------------------------------

.. code-block:: shell

   pypop --version

This simply reports the version number and other information about
PyPop, and indirectly checks that the program is installed. If all is
well, you should see something like:

.. code-block:: text

   pypop 1.0.0a23
   Copyright (C) 2003-2006 Regents of the University of California.
   Copyright (C) 2007-2023 PyPop team.
   This is free software.  There is NO warranty; not even for
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

You can also run ``pypop --help`` to see a full list and explanation
of all the options available.

Run a minimal dataset:
----------------------

Download test ``.ini`` and ``.pop`` files: `minimal.ini
<https://github.com/alexlancaster/pypop/blob/main/tests/data/minimal.ini>`_
and `USAFEL-UchiTelle-small.pop
<https://github.com/alexlancaster/pypop/blob/main/tests/data/USAFEL-UchiTelle-small.pop>`_.
You can then run them

.. code-block:: shell

   pypop -c  minimal.ini USAFEL-UchiTelle-small.pop

If you installed from source and your working directory is already the
git repository as described in `clone the repository <Clone the
repository_>`_, you can simply run

.. code-block:: shell

   pypop -c  tests/data/minimal.ini tests/data/USAFEL-UchiTelle-small.pop

..

   replace ``pypop``, by ``./src/PyPop/pypop.py`` if you installed
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
