# -*- mode: python -*-

import platform
import shutil
from pathlib import Path
from subprocess import call

import pkg_resources
from pyglui import ui

block_cipher = None


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
    "pi-monitor",
    "console_scripts",
    "pi_monitor",
    # pathex=["/Users/papr/work/pi_monitor/pi_monitor/"],
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
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="pi_monitor",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name="pi_monitor"
)

app_version = pkg_resources.get_distribution("pi_monitor").version
app = BUNDLE(
    coll,
    name="PI Monitor.app",
    icon="PPL-Capture",
    version=app_version,
    info_plist={"NSHighResolutionCapable": "True"},
)

if platform.system() == "Linux":
    # lets build the structure for our deb package.
    dist_root = Path("dist/")
    deb_root = Path(f"pi_monitor_linux_os_x64_{app_version}")
    control = deb_root / "DEBIAN" / "control"
    desktop = deb_root / "usr" / "share" / "applications" / "pi_monitor.desktop"
    starter = deb_root / "usr" / "local" / "bin" / "pi_monitor"
    opt_dir = deb_root / "opt"
    ico_dir = deb_root / "usr" / "share" / "icons" / "hicolor" / "scalable" / "apps"

    control.parent.mkdir(mode=0o755, exist_ok=True)
    starter.parent.mkdir(mode=0o755, exist_ok=True, parents=True)
    desktop.parent.mkdir(mode=0o755, exist_ok=True, parents=True)
    ico_dir.mkdir(mode=0o755, exist_ok=True, parents=True)

    # DEB control file
    with control.open("w") as f:
        dist_size = sum(f.stat().st_size for f in dist_root.rglob("*"))
        content = f"""\
Package: pi_monitor
Version: {app_version}
Architecture: amd64
Maintainer: Pupil Labs <info@pupil-labs.com>
Priority: optional
Description: PI Monitor is the easy way to preview scene video
 and gaze streams of your Pupil Invisible devices.
Installed-Size: {dist_size / 1024}
"""
        f.write(content)
    control.chmod(0o644)

    # bin_starter script

    with starter.open("w") as f:
        content = '''\
#!/bin/sh
exec /opt/pi_monitor/pi_monitor "$@"'''
        f.write(content)
    starter.chmod(0o755)

    # .desktop entry
    with desktop.open("w") as f:
        content = """\
[Desktop Entry]
Version=1.0
Type=Application
Name=PI Monitor
Comment=Preview Pupil Invisible data streams
Exec=/opt/pi_monitor/pi_monitor
Terminal=false
Icon=PPL-Capture
Categories=Application;
Name[en_US]=PI Monitor
Actions=Terminal;

[Desktop Action Terminal]
Name=Open in Terminal
Exec=x-terminal-emulator -e pi_monitor"""
        f.write(content)
    desktop.chmod(0o644)

    svg_file_name = "PPL-Capture.svg"
    src_path = dist_root / svg_file_name
    dst_path = dist_root / svg_file_name
    shutil.copy(str(src_path), str(dst_path))
    dst_path.chmod(0o755)

    call(f"fakeroot dpkg-deb --build {deb_root}", shell=True)
