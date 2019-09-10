# -*- mode: python -*-

import pathlib
import platform

import pkg_resources
from pyglui import ui

block_cipher = None

package = "pupil_invisible_monitor"

def Entrypoint(dist, group, name, **kwargs):
    """https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Setuptools-Entry-Point"""
    kwargs.setdefault("pathex", [])
    # get the entry point
    ep = pkg_resources.get_entry_info(dist, group, name)
    # insert path of the egg at the verify front of the search path
    kwargs["pathex"] = [ep.dist.location] + kwargs["pathex"]
    # script name must not be a valid module name to avoid name clashes on import
    script_path = os.path.join(workpath, name + "-script.py")
    print("creating script for entry point", dist, group, name)
    with open(script_path, "w") as fh:
        print("import", ep.module_name, file=fh)
        print("%s.%s()" % (ep.module_name, ".".join(ep.attrs)), file=fh)

    return Analysis([script_path] + kwargs.get("scripts", []), **kwargs)


pyglui_hidden_imports = [
    "pyglui.pyfontstash",
    "pyglui.pyfontstash.fontstash",
    "pyglui.cygl.shader",
    "pyglui.cygl.utils",
    "cysignals",
]

binaries = []
datas = [
    (ui.get_opensans_font_path(), "pyglui/"),
    (ui.get_roboto_font_path(), "pyglui/"),
    (ui.get_pupil_icons_font_path(), "pyglui/"),
]

if platform.system() == "Darwin":
    binaries.append(("/usr/local/lib/libglfw.dylib", "."))
    datas.append(("icons/*.icns", "."))
elif platform.system() == "Linux":
    binaries.append(("/usr/lib/x86_64-linux-gnu/libglfw.so", "."))
    datas.append(("icons/*.svg", "."))


a = Entrypoint(
    "pupil-invisible-monitor",
    "console_scripts",
    "pupil_invisible_monitor",
    pathex=[pathlib.Path.cwd()],
    binaries=binaries,
    datas=datas,
    hiddenimports=["pyzmq", "pyre"] + pyglui_hidden_imports,
    # hookspath=[],
    # runtime_hooks=[],
    # excludes=[],
    # win_no_prefer_redirects=False,
    # win_private_assemblies=False,
    # cipher=block_cipher,
    # noarchive=False,
)

blacklist = []
if platform.system() == "Linux":
    blacklist += [
        # libc is also not meant to travel with the bundle.
        # Otherwise pyre.helpers with segfault.
        "libc.so",
        # libstdc++ is also not meant to travel with the bundle.
        # Otherwise nvideo opengl drivers will fail to load.
        "libstdc++.so",
        # required for 14.04 16.04 interoperability.
        "libgomp.so.1",
        # required for 17.10 interoperability.
        "libdrm.so.2",
    ]

binaries = list(b for b in a.binaries if b[0] not in blacklist)
print(f"Removed {len(a.binaries) - len(binaries)} blacklisted binaries")

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=package,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe, binaries, a.zipfiles, a.datas, strip=False, upx=True, name=package
)

app_version = pkg_resources.get_distribution(package).version
app = BUNDLE(
    coll,
    name="Pupil Invisible Monitor.app",
    icon="pupil-invisible-monitor",
    version=app_version,
    info_plist={"NSHighResolutionCapable": "True"},
)

if platform.system() == "Linux":
    from linux_packaging import deb_package
    deb_package()
