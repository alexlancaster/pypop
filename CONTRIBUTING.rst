============
Contributing
============

.. _guide-contributing-start:

Contributions to PyPop are welcome, and they are greatly appreciated!
Every little bit helps, and `credit will always be given <Crediting
contributors_>`_.

Reporting and requesting
========================

.. _guide-contributing-bug-report:

Did you find a bug?
-------------------

When `reporting a bug
<https://github.com/alexlancaster/pypop/issues>`_ please use one of
the provided issue templates if applicable, otherwise just start a
blank issue and describe your situation.  Here is a checklist:

* **Check previous issues**.  Ensure the bug was not already reported
  by searching on GitHub under `Issues
  <https://github.com/alexlancaster/pypop/issues>`_.

* **Provide complete self-contained examples**. If you're unable to
  find an open issue addressing the problem, open a new one. Be sure
  to include a title and clear description, as much relevant
  information as possible, and a code sample or an executable test
  case (including any input files) demonstrating the expected behavior
  that is not occurring.

* **Use templates**. If possible, use the relevant bug report
  templates to create the issue.  For a standard bug report (including
  installation issues), please use this: `bug report template
  <https://github.com/alexlancaster/pypop/issues/new?assignees=&labels=bug&projects=&template=bug_report.yml>`__,
  for feature requests or documentation issues, see below.

* **Provide full commands and errors as plaintext, not screenshots**.
  When you are including the output of an error in your bug report
  (whether an installation error, a build error, an error running
  ``pypop`` or an error building docs), please cut-and-paste from your
  console application or terminal, the entire set of commands leading
  up to the error, along with the **complete** error output as a
  **single plaintext** output. E.g. here is an example error from
  running ``pypop`` on a badly formed ``.ini`` file:

  .. code:: 
	    
     $ pypop -c minimal.ini USAFEL-UchiTelle-small.pop 
     Traceback (most recent call last):
       File "/home/user/.conda/envs/pypop/bin/pypop", line 8, in <module>
         sys.exit(main())
       File "/home/user/.conda/envs/pypop/lib/python3.10/site-packages/PyPop/pypop.py", line 250, in main
         config = getConfigInstance(configFilename, altpath)
       File "/home/user/.conda/envs/pypop/lib/python3.10/site-packages/PyPop/Main.py", line 62, in getConfigInstance
         config.read(configFilename)
       File "/home/user/.conda/envs/pypop/lib/python3.10/configparser.py", line 698, in read
         self._read(fp, filename)
       File "/home/user/.conda/envs/pypop/lib/python3.10/configparser.py", line 1086, in _read
         raise MissingSectionHeaderError(fpname, lineno, line)
     configparser.MissingSectionHeaderError: File contains no section headers.
     file: 'minimal.ini', line: 4
     '   j[General]\n'

  **Please do not just post screenshots of commands and error
  output**. It's OK if you want to also include a screenshot as
  supplement, but be sure you also include the commands and output as
  plaintext as well. (If the output is too long for including inline
  as a comment on the issue, you can save it in a file, and
  drag-and-drop it into an issue comment).

* **Include environment**. When reporting bugs, especially during
  installation, please run the following and include the output of:

  .. code:: shell

     echo $CPATH
     echo $LIBRARY_PATH
     echo $PATH
     which python

  If you are running on MacOS, and you used the MacPorts installation
  method, please also run and include the output of:

  ::

    port installed

* **Keep each issue focused on one specific problem**. Each issue
  should be focused on one problem. Don't use an issue for open-ended
  discussion, or as a place to collect all issues with pypop you run
  into. If, during the comments, you discover another bug, unrelated
  to the current issue, please open up a new issue and reference it in
  the current issue.

* **Run the test suite**. In many cases, especially if you are
  investigating a new platform (e.g. new architecture) developers may
  ask you run the full test suite via ``pytest``, see `run unit tests
  with pytest`_.  in "verbose" mode (i.e. ``pytest -v``).  If you do
  this, please supply the output of the resulting temporary
  directories on your issue (see the unit test section for more
  details). Note that you will likely need to `<clone the main
  repository_>`_ as the unit tests are not distributed with the binary
  wheels.
  
  
Documentation improvements
--------------------------

**pypop** could always use more documentation, whether as part of the
official docs, in docstrings, or even on the web in blog posts,
articles, and such. Write us a `documentation issue
<https://github.com/alexlancaster/pypop/issues/new?assignees=&labels=documentation&projects=&template=documentation.yml>`_
describing what you would like to see improved in here.

If you are able to contribute directly (e.g., via a pull request), please read
our `website contribution guide <Making a documentation or website contribution_>`_.

Feature requests and feedback
-----------------------------

The best way to send feedback is to file an issue using the `feature
template
<https://github.com/alexlancaster/pypop/issues/new?assignees=&labels=enhancement&projects=&template=feature_request.yml>`_.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that code contributions are welcome 

Making a code contribution
==========================

To contribute new code that implement a feature, or fix a bug, this
section provides a step-by-step guide to getting you set-up.  The main
steps are:

1. forking the repository (or "repo")
2. cloning the main repo on to your local machine
3. making a new branch
4. `installing a development version <Installation for developers_>`_ on your machine
5. updating your branch when "upstream" (the main repository) has changes to include those changes in your local branch
6. updating ``AUTHORS.rst``
7. checking unit tests pass
8. making a pull request (including a description of your changes
   suitable for inclusion in ``NEWS.md``)


Fork this repository
--------------------

`Fork this repository before contributing`_. Forks creates a cleaner representation of the `contributions to the
project`_.

Clone the main repository
-------------------------

Next, clone the main repository to your local machine:

.. code-block:: shell

    git clone https://github.com/alexlancaster/pypop.git
    cd pypop

Add your fork as an upstream repository:

.. code-block:: shell

    git remote add myfork git://github.com/YOUR-USERNAME/pypop.git
    git fetch myfork

Make a new branch
-----------------

From the ``main`` branch create a new branch where to develop the new code.

.. code-block:: shell

    git checkout main
    git checkout -b new_branch


**Note** the ``main`` branch is from the main repository.

Build locally and make your changes
-----------------------------------

Now you are ready to make your changes.  First, you need to build
``pypop`` locally on your machine, and ensure it works, see the
separate section on `building and installing a development version
<Installation for developers_>`_.

Once you have done the installation and have verified that it works,
you can start to develop the feature, or make the bug fix, and keep
regular pushes to your fork with comprehensible commit messages.

.. code-block:: shell

    git status
    git add # (the files you want)
    git commit # (add a nice commit message)
    git push myfork new_branch

While you are developing, you can execute ``pytest`` as needed to run
your unit tests. See `run unit tests with pytest`_.

Keep your branch in sync with upstream
--------------------------------------

You should keep your branch in sync with the upstream ``main``
branch. For that:

.. code-block:: shell

    git checkout main  # return to the main branch
    git pull  # retrieve the latest source from the main repository
    git checkout new_branch  # return to your devel branch
    git merge --no-ff main  # merge the new code to your branch

At this point you may need to solve merge conflicts if they exist. If you don't
know how to do this, I suggest you start by reading the `official docs
<https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-on-github>`_

You can push to your fork now if you wish:

.. code-block:: shell

    git push myfork new_branch

And, continue doing your developments are previously discussed.

Update ``AUTHORS.rst``
----------------------

Also add your name to the author table at :code:`AUTHORS.rst`, so you
will also be included in the periodic Zenodo software releases (see
also the section on `Crediting contributors`_).


Run unit tests with ``pytest``
------------------------------

Once you have done your initial installation, you should first check
that the build worked, by running the test suite, via ``pytest``:

.. code-block:: shell

   pytest tests

If ``pytest`` is not already installed, you can install via:

.. code-block:: shell

    pip install pytest
   
If you run into errors during your initial installationg, please first
carefully repeat and/or check your installation. If you still get
errors, file a bug, and include the output of ``pytest`` run in
verbose mode and capturing the output

.. code-block:: shell

   pytest -s -v tests

.. admonition:: Preserving output from unit tests
		
   Supplying the ``-v`` verbose option will preserve the run-time
   output of unit tests that write files to disk in temporary
   directories unique for each run (by default these directories are
   created for the duration of the unit tests and then are deleted
   after the test is run).  The format of the output directories is
   ```run_test_<test-name>_<unique_id>``, e.g. the directories created
   will look similar to the following:

   .. code-block:: 

      run_test_AlleleColon_HardyWeinberg_u3dnf99y
      run_test_USAFEL_49h_exhg
		
You should also continuously run ``pytest`` as you are developing your
code, to ensure that you don't inadvertently break anything.

Also before creating a Pull Request from your branch, check that all
the tests pass correctly, using the above.

These are exactly the same tests that will be performed online via
Github Actions continuous integration (CI).  This project follows CI
good practices (let us know if something can be improved).

Make a Pull Request
-------------------

Once you are finished, create a pull request to the main repository
and engage with the developers.

When you create the pull request in the initial submission box, you
should create a description of your changes with an explanatory bullet
list of the contributions. Please note if any of your changes will
break existing behaviour or anything else that would be important for
an end-user to know. This description should be in Markdown format.
Here is an example:

.. code-block:: markdown

    ### New features
    
    - here goes my new additions, explain them shortly and well
    - this feature will require an an update to your `.ini` file

This will be used to populate the Release Notes and eventually be
included in the :code:`NEWS.md` file.

If you need some code review or feedback while you're developing the
code, you can also make a pull request, even if you're not fully
finished.

**However, before submitting a Pull Request, verify your development branch passes all
tests as** `described above <run unit tests with pytest_>`_ **. If you are
developing new code you should also implement new test cases.**

**Pull Request checklist**

Before requesting a finale merge, you should:

1. Make sure your PR passes all ``pytest`` tests.
2. Add unit tests if you are developing new features
3. Update documentation when there's new API, functionality etc.
4. In the submission for the PR, include a description of the changes,
   in markdown format, suitable for eventual inclusion in ``NEWS.md``.
5. Add yourself to ``AUTHORS.rst``.


Installation for developers
===========================

Once you have setup your branch as described in `making a code
contribution`_, above, you are ready for the four main steps of the
developer installation:

1. install a build environment
2. build
3. run tests

.. note::

   Note that you if you need to install PyPop from source, but do not
   intend to contribute code, you can skip creating your own forking
   and making an additional branch, and clone the main upstream
   repository directly:

   .. code:: shell

      git clone https://github.com/alexlancaster/pypop.git
      cd pypop
   
For most developers, we recommend using the miniconda approach
described below.

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

5. Skip ahead to `Build PyPop`_.

Install build environment via system packages (advanced)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unix/Linux:
^^^^^^^^^^^

1. Ensure Python 3 version of ``pip`` is installed:

   .. code-block:: shell

      python3 -m ensurepip --user --no-default-pip

   ..

      Note the use of the ``python3`` - you may find this to be
      necessary on systems which parallel-install both Python 2 and 3,
      which is typically the case. On newer systems you may find that
      ``python`` and ``pip`` are, by default, the Python 3 version of
      those tools.

2. Install packages system-wide:

   1. Fedora/Centos/RHEL

      .. code-block:: shell

         sudo dnf install git swig gsl-devel python3-devel

   2. Ubuntu

      .. code-block:: shell

         sudo apt install git swig libgsl-dev python-setuptools

MacOS X
^^^^^^^

1. Install the developer command-line tools:
   https://developer.apple.com/downloads/ (includes ``git``,
   ``gcc``). (Note that you may have to sign-in/create a developer
   account with Apple using your Apple ID to access this link.).  You
   may also be able to install via the terminal and skip the above
   step by running ``xcode-select –-install`` (but first check to see
   if you already have a version installed, see
   https://mac.install.guide/commandlinetools/4.html for more
   details).

2. Visit https://www.macports.org and follow the instructions there to
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


Build PyPop
-----------

You should choose *either* of the following two approaches. Don’t try
to mix-and-match the two. The build-and-install approach is only
recommended if don’t plan to make any modifications to the code
locally.

Build-and-install (not recommended for developers)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have setup your environment and cloned the repo, you can use
the following one-liner to examine the ``setup.py`` and pull all the
required dependencies from ``pypi.org`` and build and install the
package.

   Note that if you use this method and install the package, it will be
   available to run anywhere on your system, by running ``pypop``.

..

   If you use this installation method, changes you make to the code,
   locally, or via subsequent ``git pull`` requests will not be
   available in the installed version until you repeat the
   ``pip install`` command.

1. if you installed the conda development environment, use:

   .. code-block:: shell

      pip install .[test]

   ..

      (the ``[test]`` keyword is included to make sure that any package
      requirements for the test suite are installed as well).

2. if you installed a system-wide environment, the process is slightly
   different, because we install into the user’s ``$HOME/.local`` rather
   than the conda environment:

   .. code-block:: shell

      pip install --user .[test]

3. PyPop is ready-to-use, you should `run unit tests with pytest`_.

4. if you later decide you want to switch to using the developer
   approach, below, follow the `cleaning up build`_ before
   starting.

Build-and-install developer-mode (recommended for developers)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installing in `"developer" or "edit" mode
<https://setuptools.pypa.io/en/latest/userguide/development_mode.html>`__
should be used by developers, or anyone who wants to make changes to
PyPop code. It is almost identical to the regular installation above
(e.g. it will pull down all required dependencies automatically), but
instead you will add the ``--editable`` option (``-e`` is the short
version) to the ``pip install`` command. In edit mode, any changes you
make in your local code will be reflected in the installed version.

1. conda

   .. code-block:: shell

      pip install --editable .[test]

2. system-wide

   .. code-block:: shell

      pip install --user --editable .[test]

3. The scripts ``pypop`` and ``popmeta`` will operate the same way,
   and any changes in the underlying Python ``.py`` files will be
   picked up by the scripts.
   

Cleaning up build
~~~~~~~~~~~~~~~~~

To clean up, first uninstall PyPop (whether you installed in editable
mode or not):

.. code-block:: shell
  		
   pip uninstall pypop-genomics

In addition, to clean-up any compiled files and force a recompilation
from scratch, run the ``clean`` command:

.. code-block:: shell

   ./setup clean --all

Install package from GitHub Releases
====================================

Packages that are released to PyPI, are also available via the
releases on the GitHub release page:

   https://github.com/alexlancaster/pypop/releases

.. warning::

   We recommend installing binary packages using the main PyPI
   repository, **not** via the GitHub release packages. However from
   time to time, we also sometimes make binary packages that are not
   necessarily also released via PyPI. In addition, if PyPI is
   unavailable, you may want to install directly from the GitHub
   release.  These instructions will help you do that.

Installing these packages is similar to installing via PyPI, except
that you need to explicitly provide a URL to the release page.
   
1. First, visit the release page, and choose the release version you
   wish to install (usually the most recent), and note the release tag
   (e.g. ``v1.0.0``).

   .. admonition:: Release version numbers

      Note that version of the release is slightly different to the
      ``git`` tag.  This is because the ``git`` tag follows `Semantic
      Versioning <https://semver.org/>`__, which Python internally
      normalizes and abbreviates.  So the release with the ``git`` tag
      ``v1.0.0`` is actually version ``1.0.0`` of the |pkgname|
      package, and the version that ``pip`` "sees" (the difference is
      more notable with prereleases which might have a ``git`` tag of
      ``v1.0.0-rc2`` but the PyPI version will be ``1.0.0rc2``).

2. Next, use ``pip`` to install the package by running a command of
   the form (this will select and install the correct wheel for your
   Python version and operating system automatically):

   .. code-block:: shell
      
      pip install pypop-genomics -f https://github.com/alexlancaster/pypop/releases/expanded_assets/<TAG_NAME>

   where *<TAG_NAME>* is replaced with a specific tag, e.g. for the example given above, you would run:

   .. code-block:: shell
   
      pip install pypop-genomics -f https://github.com/alexlancaster/pypop/releases/expanded_assets/v1.0.0

   You can also manually download the specific wheel from the github
   release webpage and install directly, e.g.:

   .. code-block:: shell
   
      pip install pypop_genomics-1.0.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
   
   
Making a documentation or website contribution
==============================================

Interested in maintaining the PyPop website and/or documentation, such
as the *PyPop User Guide*? Here are ways to help.

Overview
--------

All the documentation (including the website homepage) are maintained in
this directory (and subdirectories) as
`reStructuredText <https://docutils.sourceforge.io/rst.html>`__
(``.rst``) documents. reStructuredText is very similar to GitHub
markdown (``.md``) and should be fairly self-explanatory to edit
(especially for pure text changes). From the .rst “source” files which
are maintained here on github, we use
`sphinx <https://www.sphinx-doc.org/en/master/>`__ to generate (aka
“compile”) the HTML for both the pypop.org user guide and and PDF (via
LaTeX) output. We have setup a GitHub action, so that as soon as a
documentation source file is changed, it will automatically recompile
all the documentation, update the ``gh-pages`` branch (which is synced
to the GitHub pages) and update the files on the website.

Here’s an overview of the process:

::

   .rst files -> sphinx -> HTML / PDF -> push to gh-pages branch -> publish on pypop.org

This means that any changes to the source will automatically update both
website home page the documentation.

Once any changes are pushed to a branch (as described below), the GitHub
action will automatically rebuild the website, and the results will be
synced to a “staging” version of the website at:

-  https://alexlancaster.github.io/beta.pypop.org/

Structure
---------

Here’s an overview of the source files for the website/documentation
located in the ``website`` subdirectory at the time of writing.  Note
that some of the documentation and website files, use the
``include::`` directive to include some "top-level" files, located
outside ``website`` like ``README.rst`` and ``CONTRIBUTING.rst``:

-  ``index.rst`` (this is the source for the homepage at
   http://pypop.org/)
-  ``conf.py`` (Sphinx configuration file - project name and other
   global settings are stored here)
   
-  ``docs`` (directory containing the source for the *PyPop User Guide*, which will eventually live at http://pypop.org/docs). 

   -  ``index.rst`` (source for the top-level of the *PyPop User Guide*)
   -  ``guide-chapter-install.rst`` (pulls in parts of the top-level ``README.rst``)
   -  ``guide-chapter-usage.rst``
   -  ``guide-chapter-instructions.rst``
   -  ``guide-chapter-contributing.rst`` (pulls in top-level
      ``CONTRIBUTING.rst`` that contains the source of the text that you are reading right now)
   -  ``guide-chapter-changes.rst`` (pulls in top-level ``NEWS.md`` and ``AUTHORS.rst``)
   -  ``licenses.rst`` (pulls in top-level ``LICENSE``)
   -  ``biblio.rst``
   -  ``pypop.bib`` (BibTeX source file for bibliography)

-  ``html_root`` (any files or directories commited in this directory
   will appear at the top-level of the website)

   -  ``psb-pypop.pdf`` (e.g. this resides at
      http://pypop.org/psb-pypop.pdf)
   -  ``tissue-antigens-lancaster-2007.pdf``
   -  ``PyPopLinux-0.7.0.tar.gz`` (old binaries - will be removed soon)
   -  ``PyPopWin32-0.7.0.zip``
   -  ``popdata`` (directory - Suppl. data for Solberg et. al 2018 -
      http://pypop.org/popdata/)

-  ``reference`` (directory containing the old DocBook-based
   documentation, preserved to allow for unconverted files to be
   converted later, this directory is ignored by the build process)

Modifying documentation
-----------------------

Minor modifications
~~~~~~~~~~~~~~~~~~~

For small typo fixes, moderate copyedits at the paragraph level
(e.g. adding or modifying paragraphs with little or no embedded markup),
you can make changes directly on the github website.

1. navigate to the ``.rst`` file you want to modify in the GitHub code
   directory, you’ll see a preview of how most of the ``.rst`` will be
   rendered

2. hover over the edit button - you’ll see an “**Edit the file in a
   fork in your project**” (if you are already a project collaborator,
   you may also have the optional of creating a branch directly in the
   main repository).

3. click it and it will open up a window where you can make your changes

4. make your edits (it’s a good idea to look at the preview tab
   periodically as you make modifications)

5. once you’ve finished with the modifications, click “**Commit
   changes**”

6. put in an a commit message, and click “**Propose changes**”

7. this will automatically create a new branch in your local fork, and
   you can immediately open up a pull-request by clicking “**Create pull
   request**”

8. open up a pull-request and submit - new documentation will be
   automatically built and reviewed. if all is good, it will be merged
   by the maintainer and made live on the site.

Major modifications
~~~~~~~~~~~~~~~~~~~

For larger structural changes involving restructuring documentation or
other major changes across multiple ``.rst`` files, **it is highly
recommended** that you should make all changes in your own local fork,
by cloning the repository on your computer and then building the
documentation locally. Here’s an overview of how to do that:

   The commands in the "Sphinx build" section of the workflow
   `.github/workflows/documentation.yaml <https://github.com/alexlancaster/pypop/blob/main/.github/workflows/documentation.yaml>`_
   which are used to run the GitHub Action that builds the documentation
   when it it deployed, is the best source for the most update-to-date
   commands to run, and should be consulted if the instructions in this
   document become out of date.

1. install sphinx and sphinx extensions

   .. code-block:: shell

      pip install setuptools_scm sphinx piccolo-theme sphinx_rtd_theme myst_parser rst2pdf sphinx_togglebutton sphinx-argparse sphinx_copybutton sphinxcontrib-bibtex

2. make a fork of pypop if you haven't already (see `previous section <Fork this repository_>`_)

3. `clone the fork and add your fork as an upstream repository <Clone
   the main repository_>`_ on your local computer, and `make a new
   branch`_. Note that you do not have to build the PyPop software first in order 
   to build the documentation, you can build them separately. 

4. make your changes to your ``.rst`` files and/or ``conf.py``

5. build the HTML documentation:

   .. code-block:: shell

      sphinx-build website _build

6. view the local documention: you can open up browser and navigate to
   the ``index.html`` in the top-level of the newly-created ``_build``
   directory

7. use ``git commit`` to commit your changes to your local fork.

8. open up a pull-request against the upstream repository

Building the PDF for the *PyPop User Guide* is a bit more involved, as
you will need to have various TeX packages installed.

1. install the LaTeX packages (these are packages needed for Ubuntu,
   they may be different on your distribution):

   .. code-block:: shell

      sudo apt-get install -y latexmk texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-luatex texlive-xetex

2. build the LaTeX and then compile the PDF:

   .. code-block:: shell

      sphinx-build -b latex website _latexbuild
      make -C _latexbuild

3. the user guide will be generated in ``_latexbuild/pypop-guide.pdf``


Crediting contributors
======================

.. note::

   These guidelines were heavily adapted from `similar guidelines
   <https://github.com/GenericMappingTools/pygmt/blob/main/AUTHORSHIP.md>`__
   in the ``PyGMT`` project.

We define *contributions* in a broad way: including both writing code
as well as documentation, and reviewing issues and PRs etc. Here are
some ways we credit contributors:

``AUTHORS.rst``, ``NEWS.md`` and GitHub Release Notes
------------------------------------------------------

Anyone who has contributed a pull request to the project is welcome to
add themselves (or request to be added) to ``AUTHORS.rst``, which is
part of the repository and included with with distributions.

Every time we make a release, everyone who has made a commit to the
repository since the previous release will be mentioned in either the
``NEWS.md`` or in the GitHub Release Notes.

Authorship on Zenodo archives of releases
-----------------------------------------

Anyone who has contributed to the repository (i.e., appears on ``git log``) will be invited to be an author on the `Zenodo
<https://zenodo.org/>`__ archive of new releases.

To be included as an author, you *must* add the following to the ``AUTHORS.rst``
file of the repository:

1. Full name (and optional link to your website or GitHub page)
2. `ORCID <https://orcid.org>`__ (optional)
3. Affiliation (optional)

The order of authors is generally defined by the number of commits to
the repository (``git shortlog -sne``). The order can also be changed
on a case-by-case basis, such as contributions to PyPop project that
due not relate to commit numbers, such as writing grants/proposals,
and other programming efforts (including reviewing PRs).

If you have contributed and *do not* wish to be included in Zenodo
archives, either don't add yourself to ``AUTHORS.rst``, or open an issue
or file a PR that:

1. Removes yourself from ``AUTHORS.rst``, or;
2. Indicates next to your name on ``AUTHORS.rst`` that you do not wish to be
   included with something like ``(not included in Zenodo)``.

Note that authors included in the Zenodo archive will also have their
name listed in the ``CITATION.cff`` file. This is a machine (and
human) readable file that enables citation of PyPop
easily.

Scientific publications (papers)
--------------------------------

From time to time we may write academic papers for PyPop, e.g., for
major changes or significant new components of the package.

To be included as an author on the paper, you *must* have

1. either made multiple and regular contributions to the PyPop
   repository; or, have made other non-coding contributions (or both);
2. have participated in the writing and reviewing of the paper.
3. added your full name, affiliation, and (optionally) ORCID to the paper. 
4. written and/or read and review the manuscript in a timely manner and provide
   comments on the paper

.. _Fork this repository before contributing: https://github.com/alexlancaster/pypop/network/members
.. _up to date with the upstream: https://gist.github.com/CristinaSolana/1885435
.. _contributions to the project: https://github.com/alexlancaster/pypop/network
.. _Gitflow Workflow: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow
.. _Pull Request: https://github.com/alexlancaster/pypop/pulls
