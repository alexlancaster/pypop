# generates frozen standalone installation in a single file
import os

# generate name of executable
if sys.platform == 'cygwin':
    exec_name = 'pypop.exe'
else:
    exec_name = 'pypop'

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
          a.binaries+[('VERSION', 'VERSION', 'BINARY'),('O',"",'OPTION')],
          name=exec_name,
          debug=0,
          strip=0, 
          console=1)

# Local variables:
# mode: python
# End:
