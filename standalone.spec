# generates frozen standalone installation in a single directory

# global imports
import os, sys, shutil, string 

# import locally generated class, dynamically (needed because current
# file is also loaded dynamically by Installer's Build.py
execfile('Utils.py', locals())

# get version from VERSION file
VERSION = (open('VERSION', 'r').readline()).strip()

# distribution bin directory name
bin_dir = 'bin'

# generate name of executable
if sys.platform == 'cygwin':
    type = 'Win32'
    file_sep = '\\'
    exec_name = 'pypop.exe'
    wrapper_name = 'pypop.bat'
    wrapper_contents = """%s\pypop.exe -i""" % bin_dir
    batch_wrapper = 'pypop-batch.bat'
    compression = 'zip'
elif sys.platform == 'linux2':
    exec_name = 'pypop'
    type = 'Linux'
    file_sep = '/'
    wrapper_name = 'pypop.sh'
    wrapper_contents = """dir=$(dirname $0)
LD_LIBRARY_PATH=$dir/%s $dir/%s/pypop -i""" % (bin_dir, bin_dir)
    batch_wrapper = 'pypop-batch.sh'
    batch_wrapper_contents = """dir=$(dirname $0)
LD_LIBRARY_PATH=$dir/%s $dir/%s/pypop $@""" % (bin_dir, bin_dir)
    compression = 'gzip'
else:
    sys.exit(sys.platform + " is currently unsupported")

# distribution directory name
dist_dir = 'PyPop' + type + "-" + VERSION

# location of Python Installer directory
#INSTALLER = '/home/alex/src/python-installer'
# generate from directory name of Build.py script
INSTALLER = os.path.dirname(sys.argv[0])

a = Analysis([INSTALLER + '/support/_mountzlib.py',
              INSTALLER + '/support/useUnicode.py',
              'pypop.py'],
             pathex=[])

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('buildstandalone', exec_name),
          debug=0,
          strip=0,
          console=1)
coll = COLLECT(exe,
               a.binaries,
               strip=1,
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
copyfileCustomPlatform('minimal-noheader-noids.ini', \
                      os.path.join(dist_dir, 'sample.ini'))
               
copyfileCustomPlatform(os.path.join('data','samples',\
                                   'USAFEL-UchiTelle-noheader-noids.pop'), \
                      os.path.join(dist_dir, 'sample.pop'))

# create an interactive wrapper script
filename = os.path.join(dist_dir, wrapper_name)
wrapper = open(filename, 'w')
wrapper.write(wrapper_contents)
wrapper.close()
os.chmod(filename, 0755)

# create batch-file wrapper script
filename = os.path.join(dist_dir, batch_wrapper)
if type == 'Win32':
    os.symlink(os.path.join(bin_dir, exec_name), filename)
else:
    batch = open(filename, 'w')
    batch.write(batch_wrapper_contents)
    batch.close()
    os.chmod(filename, 0755)

# create xslt subdirectory
xslt_dir = os.path.join(dist_dir, 'xslt')
os.mkdir(xslt_dir)

for file in ['xslt' + os.sep + i + '.xsl' \
             for i in ['text', 'html', 'lib', 'common', 'filter',
                       'hardyweinberg', 'homozygosity', 'emhaplofreq',
                       'meta-to-r', 'sort-by-locus']]:
    copyCustomPlatform(file, xslt_dir)


if compression == 'gzip':
    command = "tar zcf %s %s" % (package, dist_dir)
elif compression == 'zip':
    # cheat and execute system command
    command = "zip -y -r %s %s" % (package, dist_dir)

print command
# cheat and execute system command
os.popen(command)

print "Cleaning up"
shutil.rmtree(dist_dir)


# Local variables:
# mode: python
# End:
