.. _guide-preface-authors:

PyPop contributors
==================

(Listed in alphabetical order)

Alex Lancaster | `0000-0002-0002-9263 <https://orcid.org/0000-0002-0002-9263>`_ | Amber Biology LLC, Ronin Institute
   Lead developer. Co-designer of Python framework: author of main engine, text file
   parser, Python extension module framework using SWIG, XML output and
   XSLT post-processing framework (to generate plain text and HTML
   output).

Steven J. Mack | `0000-0001-9820-9547 <https://orcid.org/0000-0001-9820-9547>`__ | University of California, San Francisco
   Contributed bug reports, documentation, reviewed PRs.

Michael P. Mariani | `0000-0001-5235-4159 <https://orcid.org/0000-0001-5235-4159>`__ | University of Vermont
   Contributed bug reports, documentation, reviewed PRs.

Diogo Meyer | `0000-0002-7155-5674 <https://orcid.org/0000-0002-7155-5674>`__ | University of São Paulo
   Reviewed and tested PyPop, contributed some statistical analysis code.
   
Mark P. Nelson | University of California, Berkeley
   Co-designer of Python framework: implemented and maintained Python
   modules, particularly the module for Hardy-Weinberg analysis. Updated
   and maintained XSLT code.
   
Richard M. Single | `0000-0001-6054-6505 <https://orcid.org/0000-0001-6054-6505>`__ | University of Vermont
   Author of haplotype frequency and linkage disequilibrium analysis
   module ``emhaplofreq``.  Contributed documentation and testing/reviewing PRs.
   
Owen Solberg  | `0000-0003-3060-9709 <https://orcid.org/0000-0003-3060-9709>`__ 
   Implemented filter modules, including conversion to allele name
   information to sequence data.

Glenys Thomson | `0000-0001-5235-4159 <https://orcid.org/0000-0001-5235-4159>`__ | University of California, Berkeley
   Principal investigator

Yingssu Tsai
   Implemented prototype of the allele names to sequence conversion
   filter module.
   
Gordon Webster | Amber Biology LLC
   Contributed documentation and testing framework.


Third-party modules
-------------------

Included with permission, or via GPL-compatible licenses.

``gthwe``
   The Hardy-Weinberg "exact test" implementation is a modified version
   of Guo & Thompson's [Guo:Thompson:1992]_ code. Dr. Sun-Wei Guo has
   kindly allowed us to release the code under the `GNU General Public
   License <http://www.gnu.org/licenses/gpl.html>`__. Original code
   available at
   http://www.stat.washington.edu/thompson/Genepi/Hardy.shtml.

``slatkin-exact/monte-carlo.c``
   Montgomery Slatkin's implementation of a Monte Carlo approximation of
   the Ewens-Watterson exact test of neutrality ([Slatkin:1994]_,
   [Slatkin:1996]_). Original code can be found at:
   http://ib.berkeley.edu/labs/slatkin/monty/Ewens_exact.program.

``pval``
   The code in the '``pval``' directory (with the exception of
   '``pval.c``' the SWIG wrapper, ``'pval_wrap.i``' and the Makefile) is
   part of the R project's '``nmath``' numerical library
   http://www.r-project.org/ and is also licensed under the GNU General
   Public License (GPL). Minor modifications have been made to allow the
   module to build correctly.
