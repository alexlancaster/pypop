VERSION=$(shell cat VERSION)
SYSTEM=$(shell uname)

NAME_BIN=PyPop$(SYSTEM)-$(VERSION).tar.gz
NAME_SRC=PyPop-$(VERSION).tar.gz

.PHONY: FORCE doc 


COMMAND=$(shell cvs -Q status|grep "Status: "|grep -v "Up-to-date")

$(NAME_BIN):  $(wildcard *.py) $(wildcard */*.h) $(wildcard */*.c)
	rm -rf build                # remove temp build directory
	python setup.py build
	rm -rf buildstandalone      # remove package dependency area
	rm -rf bin		    # remove staging area
	Build.py standalone.spec


dist/$(NAME_SRC):  $(NAME_BIN)
	python setup.py sdist

# # before running happydoc, use CVS to fix the RCS keywords in README
# # non-verbose form, then restore them immediately after
doc:


clean:
	rm $(wildcard *.pyc)

# currently unused, support for generating happydoc documentation
#	test -d doc || mkdir doc
#	cvs update -kv README
#	happydoc -d doc -p README -t "Python class library" ParseFile.py Haplo.py HardyWeinberg.py Utils.py Arlequin.py Homozygosity.py
#	cvs update -kkv README
