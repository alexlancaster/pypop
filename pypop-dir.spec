# generates frozen standalone installation in a single directory
a = Analysis(['/home/alex/src/python-installer/support/useUnicode.py',
             'pypop.py'], pathex=[])

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name='buildpypop-dir/pypop',
          debug=0,
          console=1)
coll = COLLECT(exe,
               a.binaries+[('README', 'README', 'DATA'),('VERSION','VERSION','DATA')],
               name='distpypop')

# Local variables:
# mode: python
# End:
