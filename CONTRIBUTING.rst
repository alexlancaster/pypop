============
Contributing
============

.. _guide-contributing-start:

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given. You can contribute
from the scope of an user or as a core Python developer.

Reporting and Requesting
========================

Did you find a bug?
-------------------

When `reporting a bug
<https://github.com/alexlancaster/pypop/issues>`_ please use one of
the provided issue templates if applicable, otherwise just start a
blank issue and describe your situation.

* Ensure the bug was not already reported by searching on GitHub under
  `Issues <https://github.com/alexlancaster/pypop/issues>`_.

* If you're unable to find an open issue addressing the problem, open
  a new one. Be sure to include a title and clear description, as much
  relevant information as possible, and a code sample or an executable
  test case demonstrating the expected behavior that is not occurring.

* If possible, use the relevant bug report templates to create the issue.

Documentation improvements
--------------------------

**pypop** could always use more documentation, whether as part of the
official docs, in docstrings, or even on the web in blog posts,
articles, and such. Write us a `documentation issue <https://github.com/alexlancaster/pypop/issues/new?assignees=joaomcteixeira&labels=documentation&template=documentation.md&title=%5BDOCUMENTATION%5D>`_ describing what you
would like to see improved in here, and, if you can do
it, just `Pull Request <https://github.com/alexlancaster/pypop/pulls>`_ your proposed updates ``:-)``.

Feature requests and feedback
-----------------------------

The best way to send feedback is to file an issue using the `feature template <https://github.com/alexlancaster/pypop/issues/new?assignees=joaomcteixeira&labels=enhancement&template=feature_request.md&title=%5BFEATURE%5D>`_.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that code contributions are welcome 

Code Development
================

General instructions
--------------------

Installation for developers
===========================

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
   available to run anywhere on your system, by running ``pypop``.

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

3. You will run PyPop, directly out of the ``src/PyPop`` subdirectory
   (e.g. ``./src/PyPop/pypop.py``). Note that you have to include the
   ``.py`` extension when you run from an uninstalled checkout,
   because the script is not installed.

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



.. this is end of original README.rst info   

1. Create a new environment with the *pypop* dependencies, **only its dependencies**, running the following 3 commands::

    curl https://raw.githubusercontent.com/alexlancaster/pypop/master/requirements-dev.yml -o pypopdev.yml
    conda env create -f pypopenv.yml
    # Activate the conda pypopdev environment
    conda activate pypopdev

2. Fork `pypop <https://github.com/alexlancaster/pypop>`_ (look for the "Fork" button on the top right corner of `our repository <https://github.com/alexlancaster/pypop>`_).

3. `Clone <https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository>`_ your forked repository to your local machine::

    git clone https://github.com/YOUR-USER-NAME/pypop.git <destination folder>

4. Navigate to the fork folder and create a branch for local development::

    git checkout -b name-of-your-bugfix-or-feature

5. Install a development version of your development branch, remember to active the ``pypopdev`` environment beforehand::

    python setup.py develop

Now you can make your changes locally.

6. When you're done making changes run all the checks and docs builder with **pytest** one command::

    pytest

7. Commit your changes and push your branch to your *pypop fork* on GitHub::

    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature

8. `Submit a pull request through the GitHub website <https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request>`_.

Pull Request guidelines
-----------------------

If you need some code review or feedback while you're developing the code just make a pull request.

For merging, you should:

1. Make sure your PR passes all ``pytest`` tests.
2. Update documentation when there's new API, functionality etc.
3. Add a note to ``NEWS.rst`` about the changes.
4. Add yourself to ``website/docs/AUTHORS.rst``.


Continuous integration
======================

This project follows Continuous Integration (CI) good practices
(let us know if something can be improved). 
