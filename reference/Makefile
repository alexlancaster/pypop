PDF2PS = pdf2ps
XMLLINT = xmllint --noout --xinclude --postvalid $<
JADE = 	SGML_CATALOG_FILES=$(SGML_CATALOG_FILES) jade

ifeq ($(PUBLISH),)
CVSPRE =
CVSPOST =
else
CVSPRE = cvs update -kv $(wildcard *.xml)
CVSPOST = cvs update -kkv $(wildcard *.xml)
endif

XSLCOMMON = --param use.svg 0 --param section.autolabel 1 --param tablecolumns.extension 0 --param use.extensions 1 --param callout.graphics 0 --param callout.unicode 1 --param callouts.extension 0 --stringparam tex.math.in.alt 'latex' --param section.label.includes.component.label 1  --param shade.verbatim 1 --xinclude

# --stringparam draft.watermark.image images/draft.png
XSLHTML =
XSLFO = --param variablelist.as.blocks 1
XSLTPROC = XML_CATALOG_FILES=$(CATOPTS) xsltproc

ifeq ($(XML_CATALOG_FILES),)
	CATOPTS=/net/etc/xml/catalog
else
	CATOPTS=$(XML_CATALOG_FILES)
endif

ifneq ($(USEFOP),)
XSLFO += --param fop.extensions 1
%.pdf: %.fo
	Fop $< $@
else
XSLFO += --param passivetex.extensions 1
%.pdf: %.fo
	xmlto pdf $<
endif

# set default location of stylesheets
DOCBOOKXSLDIR=http://docbook.sourceforge.net/release/xsl/snapshot/

# phony target for equation bitmaps for which we don't know the name of yet
.PHONY: eqns 

FIGS = $(addprefix work-flow., png eps) $(addprefix design., png eps) api.png
OUTPUTS = $(addprefix biostat., html txt pdf) $(addprefix tex-math-equations., tex dvi) eqns
EXTRA_CLEAN = $(addprefix biostat., aux log out) $(addprefix tex-math-equations., tex dvi)
EXTRA_XML_SOURCE = hlaintro.xml methods.xml pypop.xml glossary.xml biblio-sorted.xml instructions.xml

all: $(OUTPUTS) $(FIGS) api/index.html

tex-math-equations.tex: biostat.xml $(EXTRA_XML_SOURCE)

# convert LaTeX images into DVI
%.dvi: %.tex
	- latex $<

# convert DVI into bitmaps
eqns: tex-math-equations.dvi
	dvi2bitmap -fp /var/cache/fonts/pk/ibmvga/public/cm $<

%.txt: %.html
	lynx -dump -nolist $< > $@

# profiling for 'main' version of document
%-main-profile.xml: %.xml
	$(XSLTPROC) --stringparam profile.condition main --xinclude -o $@ profile.xsl $<

# profiling for 'anthro' version of document
%-anthro-profile.xml: %.xml
	$(XSLTPROC) --stringparam profile.condition anthro-book --xinclude -o $@ profile.xsl $<

# generated a sorted <bibliography> where needed (for DSSSL)
%-sorted.xml: %.xml
	$(XSLTPROC) -o $@ alex-sort-biblio.xsl $<

# rules to produce final version of HTML, FO, PDF etc.

%.html: %.xml html.xsl citation.xsl $(EXTRA_XML_SOURCE) color
	$(CVSPRE)
	$(XMLLINT)	
	$(XSLTPROC) $(XSLCOMMON) --param profiling-highlighting $(if $(findstring profile,$<),0,1) $(XSLHTML) -o $@ html.xsl $<
	$(CVSPOST)

%.fo: %.xml fo.xsl citation.xsl $(EXTRA_XML_SOURCE) color
	$(CVSPRE)
	$(XMLLINT)
	$(XSLTPROC) $(XSLCOMMON) $(XSLFO) -o $@ fo.xsl $<
	$(CVSPOST)

%.ps: %.fo
	Fop $< -ps $@

%.png: %.dia
	dia --nosplash -e $@ $<

%.eps: %.dia
	dia --nosplash -e $@ $<

%.jpg: %.ps
	convert -crop 0x0 -rotate 90 $< $@

%.rtf: %.xml grayscale biblio-sorted.xml
	(cat /usr/share/sgml/xml.dcl; xmllint --xinclude $<)| $(JADE) -V rtf-backend -t rtf -V biblio-filter-used -V biblio-citation-check -o $@ -d print.dsl

# phony targets for generating images
.PHONY: color grayscale

# use the color version of images (default)
color:
	for f in $(wildcard *-color.jpg); do \
	   ln -sf $$f $${f%-color.jpg}.jpg; \
	done

# use the grayscale version of images
grayscale:
	for f in $(wildcard *-grayscale.jpg); do \
	   ln -sf $$f $${f%-grayscale.jpg}.jpg; \
	done

# convert XML to LaTeX using latex.xsl (a customization of db2latex)
%-latex.tex: %.xml grayscale
	$(XSLTPROC) --xinclude -o $@ latex.xsl $<

# convert LaTeX to PDF using PDFLaTeX
%.pdf: %.tex
	- pdflatex -interaction=nonstopmode $<
	- pdflatex -interaction=nonstopmode $<
	- pdflatex -interaction=nonstopmode $<

PYTHON_SOURCE_PREFIX = ../../src
PYTHON_SOURCE = ParseFile.py Haplo.py HardyWeinberg.py Utils.py Arlequin.py Homozygosity.py

HAPPYDOC_VERSION=$(shell happydoc -h|grep "HappyDoc version"|cut -d" " -f3)

ifeq ($(HAPPYDOC_VERSION),WORKING)
	DOCOPTIONS = --no-private-names
else
	DOCOPTIONS = --no_private_names
endif

PYTHON_SOURCE_PATH = $(addprefix $(PYTHON_SOURCE_PREFIX)/, $(PYTHON_SOURCE))

# before running happydoc, use CVS to fix the RCS keywords in README
# non-verbose form, then restore them immediately after 

# run happydoc from the directory which contains the src, and redirect
# output back to the 'api' directory

api/index.html: $(addprefix $(PYTHON_SOURCE_PREFIX)/, $(PYTHON_SOURCE) README)
	(cd $(PYTHON_SOURCE_PREFIX); \
	cvs update -kv README ; \
	happydoc -d $(PWD)/api -p README  -t "PyPop API" $(DOCOPTIONS) $(PYTHON_SOURCE); \
	cvs update -kkv README)

api/index.docb: 
	(cd $(PYTHON_SOURCE_PREFIX); \
	happydoc -d $(PWD)/api -p README -F docbookx -T mstruct formatter_encoding=utf-8 -t "PyPop API" $(DOCOPTIONS) $(PYTHON_SOURCE);)

#api/index.html: api/index.docb
#	$(XSLTPROC) --xinclude $(XSLCOMMON) $(XSLHTML) -o $@ $(DOCBOOKXSLDIR)/html/chunk.xsl $<	

api/index.fo: api/index.docb
	$(XSLTPROC) --xinclude $(XSLCOMMON) $(XSLFO) -o $@ fo.xsl $<	

api.dia: $(PYTHON_SOURCE_PATH)
	happydoc -d . --dia -t "" $(DOCOPTIONS) $(PYTHON_SOURCE_PATH)
	mv dia.dia api.dia

clean:
	- rm -f $(OUTPUTS) $(EXTRA_CLEAN)

reallyclean: clean
	- rm -f $(FIGS) api.dia
	- rm -rf api
