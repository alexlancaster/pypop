#/bin/sh
echo -n "If you are certain that module is completely up-to-date with CVS (run 'cvs update'), enter y: "
read UPTODATE
if test x$UPTODATE != xy; then
    echo "run 'cvs update'"
    exit
fi
test -f VERSION && rm VERSION
DATE=$(date +%Y-%m-%d)
echo -n "Enter the CVS tag prefix (only alphanumeric, _ or - allowed): "
read TAG_PREFIX
VERSION=${TAG_PREFIX}-${DATE}
echo "CVS tag is $VERSION"
echo tagging pypop with $VERSION
cvs tag $VERSION
echo $VERSION > VERSION
echo building $VERSION
./setup.py build
echo installing $VERSION
sudo ./setup.py install
echo rm VERSION

