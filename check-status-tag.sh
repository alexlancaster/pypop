#/bin/sh
echo "Welcome to the PyPop-build sanity check"
echo
echo "* if you build a real package CVS will be checked to make sure it is up-to-date"
echo "  and the source will be tagged via CVS with version number"
echo "* if you don't build real package '-dummy' will be appended to version "
echo
echo -n "do you want to build a real package? enter y: "

read REAL

if test "x$REAL" = xy; then
    echo "running cvs status on directory tree..."
    CHK=$(cvs -Q status|grep "Status: "|grep -v "Up-to-date")
    if test "x$CHK" != x; then
	echo $CHK
	echo
	echo "your module is not up-to-date, you must make sure all source is checked in"
	echo "(using 'cvs commit') and is also up-to-date (use 'cvs update')"
	echo "automatically switching to 'dummy' mode"
	echo
	echo -n "do you want to continue and build a 'dummy' package? enter y:"
	read CONTINUE
	if test "x$CONTINUE" != xy; then
	    echo "exiting..."
	    exit -1
	fi
	DONTTAG=y
	EXTRA=-dummy
    fi
else
    DONTTAG=y
    EXTRA=-dummy
fi

echo -n "Enter the VERSION tag (only alphanumeric, '.', '_' or '-' allowed): "
read VERSION
VERSION=${VERSION}${EXTRA}
echo "VERSION is $VERSION"
echo $VERSION > VERSION

if test x$DONTTAG = xy; then
    echo "skipping tagging"
else
    CVSTAG=PYPOP_SRC-$(cat VERSION|tr . _)
    echo -n "do you really want to tag this version with ${CVSTAG}? enter y: "
    read REALLYTAG
    if test "x$REALLYTAG" = xy; then
	echo running cvs tag $CVSTAG
    else
	echo not tagging
fi

