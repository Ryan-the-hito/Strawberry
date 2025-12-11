# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

__version__ = '2.0.8'


a = Analysis(
    ['Strawberry.py'],
    pathex=['/Users/ryanshenefield/Downloads/Strawberry.py'],
    binaries=[],
    datas=[('BeamerCN.sty', '.'), ('IEEEtran.cls', '.'), ('Strawberry.py', '.'), ('Strawberry.spec', '.'), ('alipay10.png', '.'), ('alipay20.png', '.'), ('alipay5.png', '.'), ('alipay50.png', '.'), ('api.txt', '.'), ('api2.txt', '.'), ('archive.png', '.'), ('bear.txt', '.'), ('bot.png', '.'), ('card.png', '.'), ('chapterreplacesection.txt', '.'), ('cite.png', '.'), ('currentcursor.txt', '.'), ('currentcursor2.txt', '.'), ('down.png', '.'), ('dskstb.icns', '.'), ('elegantnote.cls', '.'), ('elegantpaper.cls', '.'), ('grid.png', '.'), ('history.txt', '.'), ('input.png', '.'), ('journalCNdef.tex', '.'), ('journalCNdef2.tex', '.'), ('journalCNpicins.sty', '.'), ('max.txt', '.'), ('modelnow.txt', '.'), ('newarchivepath.txt', '.'), ('output.txt', '.'), ('output2.txt', '.'), ('path_art.txt', '.'), ('path_aut.txt', '.'), ('path_boo.txt', '.'), ('path_con.txt', '.'), ('path_dec.txt', '.'), ('path_ins.txt', '.'), ('path_lat.txt', '.'), ('path_met.txt', '.'), ('path_pat.txt', '.'), ('path_pro.txt', '.'), ('path_pub.txt', '.'), ('path_ref.txt', '.'), ('path_rst.txt', '.'), ('path_scr.txt', '.'), ('path_std.txt', '.'), ('path_ste.txt', '.'), ('path_the.txt', '.'), ('path_ttl.txt', '.'), ('setpath.png', '.'), ('showref.txt', '.'), ('strmenu.icns', '.'), ('strmenu.png', '.'), ('temp.txt', '.'), ('third.txt', '.'), ('timeout.txt', '.'), ('total.txt', '.'), ('up.png', '.'), ('wechat10.png', '.'), ('wechat20.png', '.'), ('wechat5.png', '.'), ('wechat50.png', '.'), ('which.txt', '.'), ('win_width.txt', '.'), ('wp.txt', '.'), ('/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/jieba', 'jieba'), ('filename.txt', '.'), ('cite_position.txt', '.')],
    hiddenimports=['torch', 'transformers', 'anyio', 'anyio._backends', 'requests', 'tqdm'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Strawberry',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Strawberry',
)
app = BUNDLE(
    coll,
    name='Strawberry.app',
    icon='dskstb.icns',
    bundle_identifier=None,
    version=__version__,
)
