PDF2PS = pdf2ps
CVSPRE = cvs update -kv
CVSPOST = cvs update -kkv
XSLCOMMON = --param section.autolabel 1 --param use.extensions 1 --param tablecolumns.extension 0
XSLHTML =
XSLFO = --param fop.extensions 1 --param variablelist.as.blocks 1 --param generate.division.figure.lot 1 
XSLTPROC = XML_CATALOG_FILES=$(CATOPTS) xsltproc

ifeq ($(XML_CATALOG_FILES),)
	CATOPTS=/net/etc/xml/catalog
else
	CATOPTS=$(XML_CATALOG_FILES)
endif

# set default location of stylesheets, if envar is not set
# alternatively if envar is set, it will use that 
ifeq ($(DOCBOOKXSLDIR),)
	DOCBOOKXSLDIR=/net/share/xml/docbook/xsl-stylesheets
endif

FIGS = $(addprefix work-flow., png eps) $(addprefix design., png eps) api.png
OUTPUTS =  $(addprefix biostat., html txt pdf)

all: $(OUTPUTS) $(FIGS) api/index.html

%.txt: %.html
	lynx -dump -nolist $< > $@

%.html: %.xml $(FIGS) html.xsl
	$(CVSPRE) $<
	$(XSLTPROC) $(XSLCOMMON) $(XSLHTML) -o $@ html.xsl $<
	$(CVSPOST) $<

%.fo: %.xml $(FIGS) fo.xsl
	$(CVSPRE) $<
	$(XSLTPROC) $(XSLCOMMON) $(XSLFO) -o $@ fo.xsl $<
	$(CVSPOST) $<

%.pdf: %.fo
	Fop $< $@

%.ps: %.fo
	Fop $< -ps $@

%.png: %.dia
	dia --nosplash -e $@ $<

%.eps: %.dia
	dia --nosplash -e $@ $<


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
	- rm -f $(OUTPUTS) 

reallyclean: clean
	- rm -f $(FIGS) api.dia
	- rm -rf api
