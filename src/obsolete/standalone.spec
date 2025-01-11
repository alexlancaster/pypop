# generates frozen standalone installation in a single directory

# global imports
import os, sys, shutil, string

# location of Python Installer directory
#INSTALLER = '/home/alex/src/python-installer'
# generate from directory name of Build.py script
INSTALLER = os.path.dirname(sys.argv[0])

# import locally generated class, dynamically (needed because current
# file is also loaded dynamically by Installer's Build.py
execfile('Utils.py', globals())

# create TOCs for standalone directory installation
def createObjects(script, type=type, INSTALLER=INSTALLER):
    basename = script[:-3]
    if type == 'Win32':
        exec_name = basename + '.exe'
    elif type == 'Linux':
        exec_name = basename

    a = Analysis([INSTALLER + '/support/_mountzlib.py',
                  INSTALLER + '/support/useUnicode.py',
                  script],
                 pathex=[])
    pyz = PYZ(a.pure)
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=1,
              name=os.path.join('buildstandalone', exec_name),
              debug=0,
              strip=0,
              console=1)
    return exe, a

# create wrapper scripts for all platforms
def createWrappers(script=None, type=None, bin_dir=None, dist_dir=None):
    basename = script[:-3]
    if type == 'Win32':
        exec_name = basename + '.exe'
        wrapper_common = """@echo off
set PYTHONHOME="."
%s\%s""" % (bin_dir, exec_name)
        wrapper_name = basename + '.bat'
        wrapper_contents = wrapper_common + """ -i
pause"""
        batch_wrapper = basename + '-batch.bat'
        batch_wrapper_contents = wrapper_common + ' %*'
    elif type == 'Linux':
        exec_name = basename
        wrapper_common = """#!/bin/sh
dir=$(dirname $0)
PYTHONHOME=. LD_LIBRARY_PATH=$dir/%s $dir/%s/%s""" % (bin_dir, bin_dir, exec_name)
        wrapper_name = basename
        wrapper_contents = wrapper_common + ' -i'
        batch_wrapper = basename + '-batch'
        batch_wrapper_contents = wrapper_common + ' $@'

    # create an interactive wrapper script
    filename = os.path.join(dist_dir, wrapper_name)
    wrapper = open(filename, 'w')
    wrapper.write(wrapper_contents)
    wrapper.close()
    os.chmod(filename, 0755)

    # apply line ending fixes for Win32
    if type == 'Win32':
        convertLineEndings(filename, 2)

    # create batch-file wrapper script
    filename = os.path.join(dist_dir, batch_wrapper)
    batch = open(filename, 'w')
    batch.write(batch_wrapper_contents)
    batch.close()
    os.chmod(filename, 0755)

    # apply line ending fixes for Win32
    if type == 'Win32':
        convertLineEndings(filename, 2)

# get version from VERSION file
VERSION = (open('VERSION', 'r').readline()).strip()

# distribution bin directory name
bin_dir = 'bin'

# set various platform-specific variables
if sys.platform == 'cygwin':
    type = 'Win32'
    file_sep = '\\'
    compression = 'zip'
elif sys.platform == 'linux2':
    type = 'Linux'
    file_sep = '/'
    compression = 'gzip'
else:
    sys.exit(sys.platform + " is currently unsupported")

# distribution directory name
dist_dir = 'PyPop' + type + "-" + VERSION

# create TOCs so that files can be packaged up
pypop_exe, pypop = createObjects('pypop.py', type=type)
popmeta_exe, popmeta = createObjects('popmeta.py', type=type)

# collect them into a directory
coll = COLLECT(pypop_exe,
               popmeta_exe,
               pypop.binaries,
               popmeta.binaries,
               strip=0,
               name=bin_dir)

# add these later
#[('README', 'README', 'DATA'),('VERSION','VERSION','DATA')],

if compression == 'gzip':
    package = dist_dir + '.tar.gz'
elif compression == 'zip':
    package = dist_dir + '.zip'

# remove directory if it exists, or create if it doesn't
if os.path.isdir(dist_dir):
    shutil.rmtree(dist_dir)

print "Creating directory: " + dist_dir
os.mkdir(dist_dir)

print "Creating package: " + package
shutil.copytree(bin_dir, os.path.join(dist_dir, bin_dir))

# copy top-level files
for file in ['README', 'INSTALL', 'AUTHORS', 'COPYING', 'NEWS']:
    copyCustomPlatform(file, dist_dir, txt_ext=1)

# VERSION file must not be renamed and must be put in bin_dir
# where pypop script now looks for it
copyCustomPlatform('VERSION', os.path.join(dist_dir, bin_dir))

# copy sample 'demo' files
copyfileCustomPlatform(os.path.join('data','samples',\
                                    'minimal-noheader-noids.ini'), \
                      os.path.join(dist_dir, 'sample.ini'))

copyfileCustomPlatform(os.path.join('data','samples',\
                                   'USAFEL-UchiTelle-noheader-noids.pop'), \
                      os.path.join(dist_dir, 'sample.pop'))

# create wrappers
createWrappers(script='pypop.py', type=type, \
               bin_dir=bin_dir, dist_dir=dist_dir)
createWrappers(script='popmeta.py', type=type, \
               bin_dir=bin_dir, dist_dir=dist_dir)


# create xslt subdirectory
xslt_dir = os.path.join(dist_dir, 'xslt')
os.mkdir(xslt_dir)

for file in ['xslt' + os.sep + i + '.xsl' \
             for i in ['text', 'html', 'lib', 'common', 'filter',
                       'hardyweinberg', 'homozygosity', 'emhaplofreq',
                       'meta-to-r', 'sort-by-locus', 'allelelist-by-locus',
                       'haplolist-by-group']]:
    copyCustomPlatform(file, xslt_dir)


if compression == 'gzip':
    command = "tar zcf %s %s" % (package, dist_dir)
elif compression == 'zip':
    # cheat and execute system command
	    command = "zip -r %s %s" % (package, dist_dir)

print command
# cheat and execute system command
os.popen(command)

print "Cleaning up"
shutil.rmtree(dist_dir)


# Local variables:
# mode: python
# End:
