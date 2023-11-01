|PyPI version shields.io| |Build status| |Website pypop.org| |GitHub license| |Citations|

PyPop: Python for Population Genomics
=====================================

PyPop is a framework for processing genotype and allele data and
running population genetic analyses, including conformity to
Hardy-Weinberg expectations; tests for balancing or directional
selection; estimates of haplotype frequencies and measures and tests
of significance for linkage disequilibrium (LD). See the `PyPop
User Guide <http://pypop.org/docs>`__ for a more detailed description.

.. _guide-include-pypop-cite-start:
		       
**How to cite PyPop**

If you write a paper that uses PyPop in your analysis, please cite
**both**:

1. our 2007 paper from *Tissue Antigens*:

      Lancaster AK, Single RM, Solberg OD, Nelson MP and G
      Thomson (2007) "PyPop update - a software pipeline for
      large-scale multilocus population genomics" *Tissue Antigens* 69
      (s1), 192-197.  [`journal page
      <http://dx.doi.org/10.1111/j.1399-0039.2006.00769.x>`__,
      `preprint PDF (112 kB)
      <http://pypop.org/tissue-antigens-lancaster-2007.pdf>`__].

2. **and** the Zenodo record for the software.  Citation metadata for
   the current Zenodo record is stored in `CITATION.cff
   <https://github.com/alexlancaster/pypop/blob/main/CITATION.cff>`__
   It will be of the form and contain link to the DOI:

      Lancaster, AK et al. (2023) "PyPop: Python for Population
      Genomics" (Version 1.0.0) [Computer
      software]. https://doi.org/10.5281/zenodo.XXXXX

   When you follow the DOI link to the Zenodo record, you will see all
   the versions listed on the right, make sure you choose the
   version-specific DOI that matches the specific version of PyPop in
   your citation.
      
.. _guide-include-pypop-cite-end:

.. _guide-include-start:

.. ATTENTION:: 

   The package name for installation purposes is |pkgname| - to avoid
   conflicting with an unrelated package with the name ``pypop``
   already on `PyPI <https://pypi.org>`__.

Quickstart Guide
================

**Installing** |pkgname|

If you already have Python and ``pip`` installed, install a test pre-releases using the following:

.. code-block:: shell

   pip install pypop-genomics

Otherwise, follow `these instructions <Install Python 3 and pip_>`_ to install Python 3 and pip.

.. warning::

   **These pre-release versions are being made available for initial
   testing, they are not intended to be used for production
   applications or analysis**

Once |pkgname| is installed, depending on your platform, you may also
need to `adjust <Post-install PATH adjustments_>`_ your ``PATH``
environment variable.  

**Upgrading** |pkgname|

.. code-block:: shell

   pip install -U pypop-genomics

**Uninstalling** |pkgname|

.. code-block:: shell

   pip uninstall pypop-genomics

**For more, including handling common installation issues, see the** `detailed installation instructions`_ **.**
   
Once you have installed |pkgname|, you can move on to try some
`example runs <Examples_>`__.
   
   
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
<https://raw.githubusercontent.com/alexlancaster/pypop/main/tests/data/minimal.ini>`_
and `USAFEL-UchiTelle-small.pop
<https://raw.githubusercontent.com/alexlancaster/pypop/main/tests/data/USAFEL-UchiTelle-small.pop>`_.
You can then run them

.. code-block:: shell

   pypop -c  minimal.ini USAFEL-UchiTelle-small.pop

If you have already cloned the git repository and it is your working
directory, you can simply run

.. code-block:: shell

   pypop -c  tests/data/minimal.ini tests/data/USAFEL-UchiTelle-small.pop


This will generate the following two files, an XML output file and a
plain text version:

::

   USAFEL-UchiTelle-small-out.xml
   USAFEL-UchiTelle-small-out.txt


Detailed installation instructions
==================================

There are three main steps:

1. install Python and ``pip``
2. install package from Test PyPI
3. adjusting your ``PATH`` variable after installation


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

Install package from PyPI
-------------------------

Once you have both python and ``pip`` installed, you can use ``pip``
to install pre-compiled binary "wheels" of |pkgname|
pre-releases, directly from  `PyPI <https://pypi.org/>`__.

.. warning::

   **These pre-release versions are being made available for initial
   testing, they are not intended to be used for production
   applications or analysis**

.. code-block:: shell

   pip install pypop-genomics

.. note::

   If, for whatever reason, you cannot use the these binaries
   (e.g. the pre-compiled binaries are not available for your
   platform), you may need to follow the `developer installation
   instructions <http://pypop.org/docs/guide-chapter-contributing.html#installation-for-developers>`_ in the contributors
   guide.
		
**Upgrade an existing PyPop installation**

To update an existing installation to a newer version, use the same
command as above, but add the ``--upgrade`` (short version: ``-U``)
flag, i.e.

.. code-block:: shell

   pip install -U pypop-genomics

**Installing from Test PyPI**

From time to time, we may make available packages on the `Test PyPI
<https://test.pypi.org/>`__ instance, rather than the through the main
instance. The above installation and updating instructions can be
used, by appending the following:

.. code-block:: shell

   --extra-index-url https://test.pypi.org/simple/

to the above ``pip`` commands.

   
**Issues with installation permission**

By default, ``pip`` will attempt to install the |pkgname|
package wherever the current Python installation is installed.  This
location may be a user-specific virtual environment (like ``conda``,
see below), or a system-wide installation. On many Unix-based systems,
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

   pip install pypop-genomics --user

This may be necessary in certain cases where ``pip install`` doesn't
install into the expected user directory.
   
.. admonition:: Installing within a ``conda`` environment

   In the special case that you installing from within an activated
   user-specific ``conda`` virtual environment that provides Python,
   then you should **not** add the ``--user`` because it will install
   it in ``~/.local/lib/`` rather than under the user-specific conda
   virtual environment in ``~/.conda/envs/``.
  
Install package from GitHub Releases (advanced)
-----------------------------------------------

We also sometimes make binary packages also available from the GitHub
release page:

   https://github.com/alexlancaster/pypop/releases

To install these is similar to installing via PyPI above, except that
you need to explicitly provide a URL to the release page.
   
1. First, visit the release page, and choose the release version you
   wish to install (usually the most recent), and note the release tag
   (e.g. ``v1.0.0-a23``).

   .. admonition:: Release version numbers

      Note that version of the release is slightly different to the
      ``git`` tag.  This is because the ``git`` tag follows `Semantic
      Versioning <https://semver.org/>`__, which Python internally
      normalizes and abbreviates.  So the release with the ``git`` tag
      ``v1.0.0-a23`` is actually version ``1.0.0a23`` of the
      |pkgname| package, and the version that ``pip`` "sees".

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
   
      pip install pypop_genomics-1.0.0a23-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
		
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
   
Uninstalling PyPop
------------------

To uninstall the current version of |pkgname|:

.. code-block:: shell

   pip uninstall pypop-genomics

  
   
Support and development
=======================

Please submit any bug reports, feature requests or questions, via our
GitHub issue tracker (see our `bug reporting guidelines
<http://pypop.org/docs/guide-chapter-contributing.html#reporting-and-requesting>`_
for more details on how to file a good bug report):

   https://github.com/alexlancaster/pypop/issues
   
**Please do not report bugs via private email to developers.**

The development of the code for PyPop is via our GitHub project:

   https://github.com/alexlancaster/pypop

.. _guide-include-end:

For a detailed description on bug reporting as well as how to
contribute to PyPop, please consult our `CONTRIBUTING.rst
<https://github.com/alexlancaster/pypop/blob/main/CONTRIBUTING.rst>`_
guide. We also have additional notes and background relevant for
developers in `DEV_NOTES.md
<https://github.com/alexlancaster/pypop/blob/main/DEV_NOTES.md>`__. Source
for the website and the documentation is located in the `website
<https://github.com/alexlancaster/pypop/blob/main/website>`__ subdirectory.

Copyright and License
=====================

PyPop is Copyright (C) 2003-2006. The Regents of the University of
California (Regents)

Copyright (C) 2007-2023 PyPop team.

PyPop is distributed under the terms of GPLv2


.. |pkgname| replace:: ``pypop-genomics``

.. |PyPI version fury.io| image:: https://badge.fury.io/py/pypop-genomics.svg
   :target: https://pypi.python.org/pypi/pypop-genomics/

.. |PyPI version shields.io| image:: https://img.shields.io/pypi/v/pypop-genomics.svg
   :target: https://pypi.python.org/pypi/pypop-genomics/

.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/pypop-genomics.svg
   :target: https://pypi.python.org/pypi/pypop-genomics/	    
	    
.. |GitHub release| image:: https://img.shields.io/github/release/alexlancaster/pypop.svg
   :target: https://github.com/alexlancaster/pypop/releases/

.. |Build status| image:: https://github.com/alexlancaster/pypop/actions/workflows/build_wheels.yml/badge.svg?branch=main
    :target: https://github.com/alexlancaster/pypop/actions/workflows/build_wheels.yml

.. |GitHub license| image:: https://img.shields.io/github/license/alexlancaster/pypop.svg
   :target: https://github.com/alexlancaster/pypop/blob/main/LICENSE	     

.. |GitHub issues| image:: https://img.shields.io/github/issues/alexlancaster/pypop.svg
    :target: https://github.com/alexlancaster/pypop/issues

.. |Citations| image:: https://api.juleskreuer.eu/citation-badge.php?doi=10.1111/j.1399-0039.2006.00769.x
   :target: https://juleskreuer.eu/projekte/citation-badge/
	    
.. |GitHub version| image:: https://badge.fury.io/gh/alexlancaster%2Fpypop.svg
   :target: https://github.com/alexlancaster/pypop/

.. |GitHub tag| image:: https://img.shields.io/github/tag/alexlancaster/pypop.svg
   :target: https://github.com/alexlancaster/pypop/tags/	    

.. |Website pypop.org| image:: https://img.shields.io/website-up-down-green-red/http/pypop.org.svg
   :target: http://pypop.org/	    
