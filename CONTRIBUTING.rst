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
articles, and such. Write us a `documentation issue <https://github.com/alexlancaster/pypop/issues/new>`_ describing what you
would like to see improved in here, and, if you can do
it, just `Pull Request <https://github.com/alexlancaster/pypop/pulls>`_ your proposed updates ``:-)``.

Feature requests and feedback
-----------------------------

The best way to send feedback is to file an issue using the `feature
template
<https://github.com/alexlancaster/pypop/issues/new?assignees=&labels=&projects=&template=feature_request.md>`_.

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
5. updating your branch when "upstream" (the main repository has changes) to include those changes in your local branch
6. updating the changelog in ``NEWS.rst``
7. checking unit tests pass
8. making a pull request


Fork this repository
--------------------

`Fork this repository before contributing`_. Forks creates a cleaner representation of the `contributions to the
project`_.

Clone the main repository
-------------------------

Next, clone the main repository to your local machine:

::

    git clone https://github.com/alexlancaster/pypop.git
    cd pypop

Add your fork as an upstream repository:

::

    git remote add myfork git://github.com/YOUR-USERNAME/pypop.git
    git fetch myfork

Make a new branch
-----------------

From the ``main`` branch create a new branch where to develop the new code.

::

    git checkout main
    git checkout -b new_branch


**Note** the ``main`` branch is from the main repository.

Build locally
-------------

Now you are ready to make your changes.  First, you need to build
``pypop`` locally on your machine, and ensure it works, see the
separate section on `building and installing a development version
<Installation for developers>`_.

Once you have done the installation and have verified that it works
you can start to develop the feature, or make the bug fix, and keep
regular pushes to your fork with comprehensible commit messages.

::

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

::

    git checkout main  # return to the main branch
    git pull  # retrieve the latest source from the main repository
    git checkout new_branch  # return to your devel branch
    git merge --no-ff main  # merge the new code to your branch

At this point you may need to solve merge conflicts if they exist. If you don't
know how to do this, I suggest you start by reading the `official docs
<https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-on-github>`_

You can push to your fork now if you wish:

::

    git push myfork new_branch

And, continue doing your developments are previously discussed.

Update NEWS.rst
---------------

Update the changelog file under :code:`NEWS.rst` with an explanatory
bullet list of your contribution. Add that list under the "Notes
towards the next release" under the appropriate category, e.g. for a
new feature you would add something like:

.. code-block:: text

    Notes towards next release
    --------------------------
    (unreleased)

    New features
    ^^^^^^^^^^^^
    
    * here goes my new additions
    * explain them shortly and well


Also add your name to the authors list at :code:`website/docs/AUTHORS.rst`.

Run unit tests with ``pytest``
------------------------------

Once you have done your initial installation, you should first check
that the build worked, by running the test suite, via ``pytest``:

::

   pytest tests

If ``pytest`` is not already installed, you can install via:

::

    pip install pytest
   
If you run into errors during your initial installationg, please first
carefully repeat and/or check your installation. If you still get
errors, file a bug, and include the output of ``pytest`` run in
verbose mode and capturing the output

::

   pytest -s -v tests
   
   
You should also continuously run ``pytest`` as you are developing your
code, to ensure that you don't inadvertently break anything.

Also before creating a Pull Request from your branch, check that all
the tests pass correctly, using the above.

These are exactly the same tests that will be performed online via
Github Actions continuous integration (CI).  This project follows CI
good practices (let us know if something can be improved).

Make a Pull Request
-------------------

Once you are finished, you can create a pull request to the main
repository and engage with the developers.  If you need some code
review or feedback while you're developing the code just make a pull
request.

**However, before submitting a Pull Request, verify your development branch passes all
tests as** `described above <run unit tests with pytest_>`_ **. If you are
developing new code you should also implement new test cases.**

**Pull Request checklist**

Before requesting a finale merge, you should:

1. Make sure your PR passes all ``pytest`` tests.
2. Add unit tests if you are developing new features
3. Update documentation when there's new API, functionality etc.
4. Add a note to ``NEWS.rst`` about the changes.
5. Add yourself to ``website/docs/AUTHORS.rst``.


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

3. PyPop is ready-to-use, you should `run unit tests with pytest`_.

4. if you later decide you want to switch to using the developer
   approach, below, follow the `cleaning up build`_ before
   starting.

Build-and-run-from-checkout (recommended for developers)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

3. You will be runnning PyPop, directly out of the ``src/PyPop``
   subdirectory (e.g. ``./src/PyPop/pypop.py`` and
   ``./src/PyPop/popmeta.py``). Note that you have to include the
   ``.py`` extension when you run from an uninstalled checkout,
   because the script is not installed.

Cleaning up build
~~~~~~~~~~~~~~~~~

If you installed using the approach in `Build-and-install (not recommended
for developers)`_, above, follow the end-user instructions on
:ref:`uninstalling PyPop`.  In addition, to clean-up any compiled
files and force a recompilation from scratch, run the ``clean``
command:

::

   ./setup clean --all


.. _Fork this repository before contributing: https://github.com/alexlancaster/pypop/network/members
.. _up to date with the upstream: https://gist.github.com/CristinaSolana/1885435
.. _contributions to the project: https://github.com/alexlancaster/pypop/network
.. _Gitflow Workflow: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow
.. _Pull Request: https://github.com/alexlancaster/pypop/pulls
