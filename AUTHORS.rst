.. _guide-preface-authors:

Authors of software components
==============================

Alex Lancaster
   Co-designer of Python framework: author of main engine, text file
   parser, Python extension module framework using SWIG, XML output and
   XSLT post-processing framework (to generate plain text and HTML
   output).

Mark P. Nelson
   Co-designer of Python framework: implemented and maintained Python
   modules, particularly the module for Hardy-Weinberg analysis. Updated
   and maintained XSLT code.

Richard M. Single
   Author of haplotype frequency and linkage disequilibrium analysis
   module "emhaplofreq", author of R programs to do further statistical
   analysis and generate graphs and figures in PostScript.

Diogo Meyer 
   Contributed further statistical analysis code for the R programs.

Owen Solberg 
   Implemented filter modules, including conversion to allele name
   information to sequence data.

Yingssu Tsai
   Implemented prototype of the allele names to sequence conversion
   filter module.

Glenys Thomson
   Principal investigator and project lead.

gthwe
   The Hardy-Weinberg "exact test" implementation is a modified version
   of Guo & Thompson's Guo:Thompson:1992 code. Dr. Sun-Wei Guo has
   kindly allowed us to release the code under the `GNU General Public
   License <http://www.gnu.org/licenses/gpl.html>`__. Original code
   available at
   http://www.stat.washington.edu/thompson/Genepi/Hardy.shtml.

``slatkin-exact/monte-carlo.c``
   Montgomery Slatkin's implementation of a Monte Carlo approximation of
   the Ewens-Watterson exact test of neutrality (Slatkin:1994,
   Slatkin:1996). Original code can be found at:
   http://ib.berkeley.edu/labs/slatkin/monty/Ewens_exact.program.

``pval``
   The code in the '``pval``' directory (with the exception of
   '``pval.c``' the SWIG wrapper, ``'pval_wrap.i``' and the Makefile) is
   part of the R project's '``nmath``' numerical library
   http://www.r-project.org/ and is also licensed under the GNU General
   Public License (GPL). Minor modifications have been made to allow the
   module to build correctly.

