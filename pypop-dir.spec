# generates frozen standalone installation in a single directory
import os, shutil

# generate name of executable
if sys.platform == 'cygwin':
    exec_name = 'pypop.exe'
    wrapper_name = 'pypop.bat'
    type = 'Win32'
    compression = 'zip'
elif sys.platform == 'linux2':
    exec_name = 'pypop'
    wrapper_name = 'pypop.sh'
    type = 'Linux'
    compression = 'gzip'
else:
    exec_name = 'pypop'

# get version from VERSION file
VERSION = (open('VERSION', 'r').readline()).strip()

# distribution bin directory name
bin_dir = 'bin'

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
          name='buildpypop-dir/' + exec_name,
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
for file in ['README', 'INSTALL', 'VERSION']:
    shutil.copy(file, dist_dir)

# copy sample 'demo' files
shutil.copyfile('minimal-noheader-noids.ini', \
                os.path.join(dist_dir, 'sample.ini'))
               
shutil.copyfile(os.path.join('data','samples',\
                             'USAFEL-UchiTelle-noheader-noids.pop'), \
                os.path.join(dist_dir, 'sample.pop'))

# create a wrapper script
wrapper = open(os.path.join(dist_dir, wrapper_name), 'wx')
wrapper.write(os.path.join(bin_dir, exec_name) + " -i")
wrapper.close()
os.chmod(os.path.join(dist_dir, wrapper_name), 0755)

# create xslt subdirectory
xslt_dir = os.path.join(dist_dir, 'xslt')
os.mkdir(xslt_dir)

for file in ['xslt' + os.sep + i + '.xsl' \
             for i in ['text', 'html', 'lib', 'common', 'filter',
                       'hardyweinberg', 'homozygosity', 'emhaplofreq',
                       'meta-to-r', 'sort-by-locus']]:
    shutil.copy(file, xslt_dir)


if compression == 'gzip':
    # cheat and execute system command
    command = "tar zcf %s %s" % (package, dist_dir)
    print command
    os.popen(command)

print "Cleaning up"
shutil.rmtree(dist_dir)


# Local variables:
# mode: python
# End:
