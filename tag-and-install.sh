#/bin/sh
VERSION=VERSION_FOR_RUN-$(date +%Y-%m-%d)
echo tagging pypop with $VERSION
echo "<version>$VERSION</version>" > version.xml
echo building $VERSION
./setup.py build
echo installing $VERSION
echo sudo ./setup.py install
