.PHONY: doc

doc:
	test -d doc || mkdir doc
	happydoc -d doc -p README -t "Python class library" ParseFile.py Haplo.py HardyWeinberg.py Utils.py Arlequin.py

clean:
	rm $(wildcard *.pyc)