.PHONY: FORCE doc

VERSION=$(shell cat VERSION)
SYSTEM=$(shell uname)
DOCPATH=reference

# binary distribution to create
ifeq ($(SYSTEM),Linux)
NAME_BIN=PyPopLinux-$(VERSION).tar.gz
endif
ifeq ($(SYSTEM),CYGWIN_NT-5.1)
NAME_BIN=PyPopWin32-$(VERSION).zip
endif

# source distribution to create
NAME_SRC=dist/PyPop-$(VERSION).tar.gz

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
	python setup.py build
	rm -rf buildstandalone      # remove package dependency area
	rm -rf bin		    # remove staging area
	Build.py standalone.spec

# rule to generate documentation files
%: $(DOCPATH)/%.xml VERSION
	(cd $(DOCPATH); $(MAKE) $@.txt)
	cp $(DOCPATH)/$@.txt $@


# rule to remake MANIFEST if either setup.py or MANIFEST.in change
MANIFEST: MANIFEST.in setup.py README AUTHORS COPYING INSTALL 
	python setup.py sdist --manifest-only

# rule to regenerate source distribution
$(NAME_SRC):  $(NAME_BIN)
	python setup.py sdist

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
