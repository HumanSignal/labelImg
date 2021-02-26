# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['labelImg.py'],
             pathex=['./libs', './', 'C:\\Users\\Administrator\\Anaconda3\\envs\\labelimg\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'O:\\Documents\\programs\\software\\labelImg_copyfunc'],
             binaries=[],
             datas=[],
             hiddenimports=['xml', 'xml.etree', 'xml.etree.ElementTree', 'lxml.etree', 'PyQt5.sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='labelImg',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
