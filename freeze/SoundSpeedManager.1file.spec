# -*- mode: python -*-
# Builds a single-file EXE for distribution.
# Note that an "unbundled" distribution launches much more quickly, but
# requires an installer program to distribute.
#
# To compile, execute the following within the source directory:
#
# python /path/to/pyinstaller.py SoundSpeedManager.1file.spec
#
# The resulting .exe file is placed in the dist/ folder.

from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT, BUNDLE, TOC
from PyInstaller import is_darwin

from hyo.soundspeed import __version__ as ssm_version


def collect_pkg_data(package, include_py_files=False, subdir=None):
    import os
    from PyInstaller.utils.hooks import get_package_paths, remove_prefix, PY_IGNORE_EXTENSIONS

    # Accept only strings as packages.
    if type(package) is not str:
        raise ValueError

    pkg_base, pkg_dir = get_package_paths(package)
    if subdir:
        pkg_dir = os.path.join(pkg_dir, subdir)
    # Walk through all file in the given package, looking for data files.
    data_toc = TOC()
    for dir_path, dir_names, files in os.walk(pkg_dir):
        for f in files:
            extension = os.path.splitext(f)[1]
            if include_py_files or (extension not in PY_IGNORE_EXTENSIONS):
                source_file = os.path.join(dir_path, f)
                dest_folder = remove_prefix(dir_path, os.path.dirname(pkg_base) + os.sep)
                dest_file = os.path.join(dest_folder, f)
                data_toc.append((dest_file, source_file, 'DATA'))

    return data_toc

pkg_data = collect_pkg_data('hyo.soundspeedmanager')
pkg_data_2 = collect_pkg_data('hyo.soundspeedsettings')

icon_file = 'freeze\SoundSpeedManager.ico'
if is_darwin:
    icon_file = 'freeze\SoundSpeedManager.icns'

a = Analysis(['SoundSpeedManager.py'],
             pathex=[],
             hiddenimports=["PIL",],
             excludes=["IPython", "PyQt", "pandas", "scipy", "sphinx", "sphinx_rtd_theme", "OpenGL_accelerate"],
             hookspath=None,
             runtime_hooks=None)

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          pkg_data,
          pkg_data_2,
          name='SoundSpeedManager.%s' % ssm_version,
          debug=False,
          strip=None,
          upx=False,
          console=True,
          icon=icon_file)
if is_darwin:
    app = BUNDLE(exe,
                 name='SoundSpeedManager',
                 icon=icon_file,
                 bundle_identifier=None)
