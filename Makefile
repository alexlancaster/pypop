.PHONY: doc

# before running happydoc, use CVS to fix the RCS keywords in README
# non-verbose form, then restore them immediately after
doc:
	test -d doc || mkdir doc
	cvs update -kv README
	happydoc -d doc -p README -t "Python class library" ParseFile.py Haplo.py HardyWeinberg.py Utils.py Arlequin.py Homozygosity.py
	cvs update -kkv README
clean:
	rm $(wildcard *.pyc)