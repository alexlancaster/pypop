# generates frozen standalone installation in a single file
a = Analysis(['/home/alex/src/python-installer/support/useUnicode.py', 'pypop.py'],
             pathex=[])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
	  a.binaries+[('VERSION', 'VERSION', 'BINARY')],
	  name='pypop',
          debug=0,
          console=1)

# Local variables:
# mode: python
# End:
