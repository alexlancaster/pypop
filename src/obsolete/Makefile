.PHONY: FORCE doc

VERSION=$(shell cat VERSION)
SYSTEM=$(shell uname)
DOCPATH=reference
DISTRIB=DISTRIB=true

# binary distribution to create
ifeq ($(SYSTEM),Linux)
NAME_BIN=PyPopLinux-$(VERSION).tar.gz
endif
ifeq ($(findstring CYGWIN_NT, $(SYSTEM)),CYGWIN_NT)
NAME_BIN=PyPopWin32-$(VERSION).zip
endif

# source distribution to create
NAME_SRC=dist/pypop-$(VERSION).tar.gz

all: FORCE $(NAME_BIN) $(NAME_SRC) 

# check to see whether up-to-date with CVS and create version
# number
FORCE:
	./check-status-tag.sh

# use MANIFEST file to generate dependencies
DEPS=$(shell cat MANIFEST)

$(NAME_BIN): MANIFEST $(DEPS)
	@echo deps are $(DEPS)
	rm -rf build                # remove temp build directory
	rm -f _*.so		    # force rebuild of Python extensions
	$(DISTRIB) python setup.py build
	rm -rf buildstandalone      # remove package dependency area
	rm -rf bin		    # remove staging area
	Build.py standalone.spec
	rm -rf build
	rm -f _*.so		    # remove Python extensions


# rule to generate documentation files
# make sure that it does not attempt to rebuild pypop from pypop.xml
%: $(DOCPATH)/%.xml VERSION
	@if [ "X$@" != "Xpypop" ]; then  \
		(cd $(DOCPATH); $(MAKE) $@.txt); \
		cp $(DOCPATH)/$@.txt $@; \
	fi

# rule to remake MANIFEST if either setup.py or MANIFEST.in change
MANIFEST: MANIFEST.in setup.py README AUTHORS COPYING INSTALL 
	$(DISTRIB) python setup.py sdist --manifest-only

# rule to regenerate source distribution
$(NAME_SRC):  $(NAME_BIN)
	$(DISTRIB) python setup.py sdist

# # before running happydoc, use CVS to fix the RCS keywords in README
# # non-verbose form, then restore them immediately after
doc: 
	(cd $(DOCPATH); $(MAKE) pypop-guide.pdf pypop-reference.pdf)


clean:

# currently unused, support for generating happydoc documentation
#	test -d doc || mkdir doc
#	cvs update -kv README
#	happydoc -d doc -p README -t "Python class library" ParseFile.py Haplo.py HardyWeinberg.py Utils.py Arlequin.py Homozygosity.py
#	cvs update -kkv README
