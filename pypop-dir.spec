# generates frozen standalone installation in a single directory
import os, sys, shutil, string, re

def convert_line_endings(file, mode, re=re):
    # 1 - Unix to Mac, 2 - Unix to DOS
    if mode == 1:
        if os.path.isdir(file):
            sys.exit(file + "Directory!")
        data = open(file, "r").read()
        if '\0' in data:
            sys.exit(file + "Binary!")
        newdata = re.sub("\r?\n", "\r", data)
        if newdata != data:
            f = open(file, "w")
            f.write(newdata)
            f.close()
    elif mode == 2:
        if os.path.isdir(file):
            sys.exit(file + "Directory!")
        data = open(file, "r").read()
        if '\0' in data:
            sys.exit(file + "Binary!")
        newdata = re.sub("\r(?!\n)|(?<!\r)\n", "\r\n", data)
        if newdata != data:
            f = open(file, "w")
            f.write(newdata)
            f.close()

def platform_fix(filename, txt_ext=0, convert_line_endings=convert_line_endings):
    # make file read-writeable by everybody
    os.chmod(filename, 0666)

    # create as a DOS format file LF -> CRLF
    if sys.platform == 'cygwin':
        convert_line_endings(filename, 2)
        # give it a .txt extension so that lame Windows realizes it's text
        if txt_ext:
            os.rename(filename, filename + '.txt')        

def copyfile_for_platform(src, dest, txt_ext=0, platform_fix=platform_fix):
    print "copying %s to %s" % (src, dest)
    shutil.copyfile(src, dest)
    platform_fix(dest, txt_ext=txt_ext)
    
def copy_for_platform(file, dist_dir, txt_ext=0, platform_fix=platform_fix):
    new_filename=os.path.join(dist_dir, os.path.basename(file))
    print "copying %s to %s" % (file, new_filename)
    shutil.copy(file, dist_dir)
    platform_fix(new_filename, txt_ext=txt_ext)

# generate name of executable
if sys.platform == 'cygwin':
    exec_name = 'pypop.exe'
    wrapper_name = 'pypop.bat'
    type = 'Win32'
    file_sep = '\\'
    compression = 'zip'
elif sys.platform == 'linux2':
    exec_name = 'pypop'
    wrapper_name = 'pypop.sh'
    type = 'Linux'
    file_sep = '/'
    compression = 'gzip'
else:
    sys.exit(sys.platform + " is currently unsupported")

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
for file in ['README', 'INSTALL', 'AUTHORS', 'COPYING']:
    copy_for_platform(file, dist_dir, txt_ext=1)

# VERSION file must not be renamed
copy_for_platform('VERSION', dist_dir)

# copy sample 'demo' files
copyfile_for_platform('minimal-noheader-noids.ini', \
                      os.path.join(dist_dir, 'sample.ini'))
               
copyfile_for_platform(os.path.join('data','samples',\
                                   'USAFEL-UchiTelle-noheader-noids.pop'), \
                      os.path.join(dist_dir, 'sample.pop'))

# create a wrapper script
wrapper = open(os.path.join(dist_dir, wrapper_name), 'w')
wrapper.write(bin_dir + file_sep + exec_name + " -i")
wrapper.close()
os.chmod(os.path.join(dist_dir, wrapper_name), 0755)

# create xslt subdirectory
xslt_dir = os.path.join(dist_dir, 'xslt')
os.mkdir(xslt_dir)

for file in ['xslt' + os.sep + i + '.xsl' \
             for i in ['text', 'html', 'lib', 'common', 'filter',
                       'hardyweinberg', 'homozygosity', 'emhaplofreq',
                       'meta-to-r', 'sort-by-locus']]:
    copy_for_platform(file, xslt_dir)


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
