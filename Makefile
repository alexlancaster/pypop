.PHONY: doc

doc:
	test -d doc || mkdir doc
	happydoc -d doc -p README -t "IHWG Python class library" ParseFile.py Haplo.py HardyWeinberg.py

clean:
	rm $(wildcard *.pyc)