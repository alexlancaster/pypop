# generates frozen standalone installation in a single file

# location of Python Installer directory
INSTALLER = '/home/alex/src/python-installer'
a = Analysis([INSTALLER + '/support/_mountzlib.py',
              INSTALLER + '/support/useUnicode.py',
              'pypop.py'],
             pathex=[])

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries+[('VERSION', 'VERSION', 'BINARY'),('O',"",'OPTION')],
          name='pypop',
          debug=0,
          strip=0, 
          console=1)

# Local variables:
# mode: python
# End:
