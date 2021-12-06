# -*- mode: python -*-

import ctypes.util
import enum
import logging
import pathlib
import platform
import sys

import pkg_resources

import glfw
from pyglui import ui

logger = logging.getLogger()
block_cipher = None

cwd = SPECPATH  # temporally add SPECPATH to Python path to import _packaging
sys.path.insert(0, cwd)

import _packaging.linux
import _packaging.macos
import _packaging.windows
from _packaging.utils import app_name, move_packaged_bundle, package_name

sys.path.remove(cwd)


class SupportedPlatform(enum.Enum):
    macos = "Darwin"
    linux = "Linux"
    windows = "Windows"


icon_ext = {
    SupportedPlatform.macos: ".icns",
    SupportedPlatform.linux: ".svg",
    SupportedPlatform.windows: ".ico",
}

current_platform = SupportedPlatform(platform.system())
deployment_root = pathlib.Path(cwd)


def Entrypoint(dist, group, name, **kwargs):
    """https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Setuptools-Entry-Point"""
    kwargs.setdefault("pathex", [])
    # get the entry point
    ep = pkg_resources.get_entry_info(dist, group, name)
    # insert path of the egg at the verify front of the search path
    kwargs["pathex"] = [ep.dist.location] + kwargs["pathex"]
    # script name must not be a valid module name to avoid name clashes on import
    script_path = os.path.join(workpath, name + "-script.py")
    logger.info(f"Creating script for entry point {dist}:{group}.{name}")
    with open(script_path, "w") as fh:
        print("import", ep.module_name, file=fh)
        print("%s.%s()" % (ep.module_name, ".".join(ep.attrs)), file=fh)

    return Analysis([script_path] + kwargs.get("scripts", []), **kwargs)


pyglui_hidden_imports = [
    "pyglui.pyfontstash",
    "pyglui.pyfontstash.fontstash",
    "pyglui.cygl.shader",
    "pyglui.cygl.utils",
]
if current_platform != SupportedPlatform.windows:
    pyglui_hidden_imports.append("cysignals")

binaries = []

glfw_path = pathlib.Path(glfw._glfw._name)
if glfw_path.exists():
    glfw_path = str(glfw_path)
else:
    glfw_path = ctypes.util.find_library(glfw_path.name)
binaries.append((glfw_path, "."))

datas = [
    (ui.get_opensans_font_path(), "pyglui/"),
    (ui.get_roboto_font_path(), "pyglui/"),
    (ui.get_pupil_icons_font_path(), "pyglui/"),
]

runtime_hooks = []
if current_platform == SupportedPlatform.linux:
    datas.append(("icons/*.svg", "."))
elif current_platform == SupportedPlatform.macos:
    runtime_hooks = ["find_opengl_bigsur.py"]

a = Entrypoint(
    "pupil-invisible-monitor",
    "console_scripts",
    package_name,
    pathex=[pathlib.Path.cwd()],
    binaries=binaries,
    datas=datas,
    hiddenimports=["pyzmq", "pyre"] + pyglui_hidden_imports,
    runtime_hooks=runtime_hooks,
    # hookspath=[],
    # excludes=[],
    # win_no_prefer_redirects=False,
    # win_private_assemblies=False,
    # cipher=block_cipher,
    # noarchive=False,
)

blacklist = []
if current_platform == SupportedPlatform.linux:
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
logger.info(f"Removed {len(a.binaries) - len(binaries)} blacklisted binaries")

icon_name = package_name + icon_ext[current_platform]
icon_path = (deployment_root / "icons" / icon_name).resolve()

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=package_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=str(icon_path),
    resources=[f"{icon_path},ICON,{icon_name}"],
)
coll = COLLECT(
    exe, binaries, a.zipfiles, a.datas, strip=False, upx=True, name=package_name
)

app_version = pkg_resources.get_distribution(package_name).version
app = BUNDLE(
    coll,
    name=f"{app_name}.app",
    icon=icon_path,
    version=app_version,
    info_plist={"NSHighResolutionCapable": "True"},
)

packaged_bundle: pathlib.Path = None
if current_platform == SupportedPlatform.linux:
    packaged_bundle = _packaging.linux.deb_package(deployment_root)

elif current_platform == SupportedPlatform.macos:
    _packaging.macos.sign_app(deployment_root)
    packaged_bundle = _packaging.macos.dmg_app(deployment_root)

elif current_platform == SupportedPlatform.windows:
    packaged_bundle = _packaging.windows.archive_7z(deployment_root)

move_packaged_bundle(deployment_root, packaged_bundle)
