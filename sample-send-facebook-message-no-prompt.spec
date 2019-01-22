# -*- mode: python -*-

block_cipher = None


a = Analysis(['send-facebook-message-no-prompt.py'],
             pathex=['S:\\Python\\cmd-facebook-message'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          Tree('data', prefix='data'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='send-facebook-message-no-prompt',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
