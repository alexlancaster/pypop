# PyPop website documentation

Interested in maintaining the PyPop website and/or documentation?
Here are ways to help.

## Overview

All the documentation (including the website homepage) are maintained
in this directory (and subdirectories) as
[reStructuredText](https://docutils.sourceforge.io/rst.html) (`.rst`)
documents.  RestructuredText is very similar to GitHub markdown
(`.md`) and should be fairly self-explanatory to edit (especially for
pure text changes). From the .rst "source" files which are maintained
here on github, we use [sphinx](https://www.sphinx-doc.org/en/master/)
to generate (aka "compile") the HTML for both the pypop.org user guide
and and PDF (via LaTeX) output.  We have setup a GitHub action, so
that as soon as a documentation source file is changed, it will
automatically recompile all the documentation, update the `gh-pages`
branch (which is synced to the GitHub pages) and update the files on
the website.

Here's an overview of the process:

```
.rst files -> sphinx -> HTML / PDF -> push to gh-pages branch -> publish on pypop.org
````

This means that any changes to the source will automatically update
both website home page the documentation.

## Structure:

Here's an overview of the source files for the website/documentation at the time of writing:

- `index.rst` (this is the source for the homepage at http://pypop.org/)
- `README.md` (this is file you're reading right now - about the documentation process *not* included in the documentation itself)
- `docs` (directory containing the source for the _PyPop User Guide_, which will eventually live at http://pypop.org/docs)
   - `conf.py` (Sphinx configuration file - project name and other global settings are stored here)
   - `index.rst` (source for the top-level of the _PyPop User Guide_)
   - `guide-chapter-install.rst` (individual chapters of the _Guide_)
   - `guide-chapter-usage.rst`
   - `guide-chapter-instructions.rst`
   - `guide-chapter-install-obsolete.rst`
   - `AUTHORS.rst`
   - `COPYING.rst` (license information)
   - `biblio.rst`
- `html_root` (any files or directories commited in this directory will appear at the top-level of the website)
   - `psb-pypop.pdf`  (e.g. this resides at http://pypop.org/psb-pypop.pdf)
   - `tissue-antigens-lancaster-2007.pdf`
   - `PyPopLinux-0.7.0.tar.gz` (old binaries - will be removed soon)
   - `PyPopWin32-0.7.0.zip`
   - `popdata` (directory - Suppl. data for Solberg et. al 2018 - https://pypop.org/popdata/)

## Modifying documentation

### Minor modifications

For small typo fixes, moderate copyedits at the paragraph level
(e.g. adding or modifying paragraphs with little or no embedded
markup), you can make changes directly on the github website.

1. navigate to the `.rst` file you want to modify in the GitHub code
   directory, you'll see a preview of how most of the `.rst` will be
   rendered

2. hover over the edit button - you'll see an "**Edit the file in a fork
   in your project**"

3. click it and it will open up a window where you can make your changes

4. make your edits (it's a good idea to look at the preview tab
   periodically as you make modifications)

5. once you've finished with the modifications, click "**Commit changes**"

6. put in an a commit message, and click "**Propose changes**"

7. this will automatically create a new branch in your local fork, and
   you can immediately open up a pull-request by clicking "**Create pull
   request**"

8. open up a pull-request and submit - new documentation will be
   automatically built and reviewed.  if all is good, it will be
   merged by the maintainer and made live on the site.

### Major modifications

For larger structural changes involving restructuring documentation or
other major changes across multiple `.rst` files, **it is highly
recommended** that you should make all changes in your own local fork,
by cloning the repository on your computer and then building the
documentation locally. Here's an overview of how to do that:

> The commands in
  [`.github/workflows/documentation.yaml`](/.github/workflows/documentation.yaml)
  which are used to run the GitHub Action that builds the
  documentation when it it deployed, is the best source for the most
  update-to-date commands to run, and should be consulted if the
  instructions in this README become out of date.

1. install sphinx and sphinx extensions

   ```
   pip install --user sphinx piccolo-theme sphinx_rtd_theme myst_parser rst2pdf sphinx_togglebutton
   ```

2. make a fork of pypop (if  one doesn't already exist)

3. clone the fork of the repository on your local computer

4. make your changes to your `.rst` files and/or `conf.py`

5. build the HTML documentation:

   ```
   sphinx-build docs _build
   ```

6. view the local documention: you can open up browser and navigate to
   the `index.html` in the top-level of the newly-created `_build`
   directory

7. use `git commit` to commit your changes to your local fork.

8. open up a pull-request against the upstream repository

Building the PDF for the _PyPop User Guide_ is a bit more involved, as
you will need to have various TeX packages installed.  


1. install the LaTeX packages (these are packages needed for Ubuntu,
   they may be different on your distribution):

   ```
   sudo apt-get install -y latexmk texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-luatex texlive-xetex
   ```

2. build the LaTeX and then compile the PDF:

   ```
   sphinx-build -b latex docs _latexbuild
   make -C _latexbuild
   ```

3. the user guide will be generated in `_latexbuild/pypop-guide.pdf`


