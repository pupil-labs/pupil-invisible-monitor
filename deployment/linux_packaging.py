import shutil
from pathlib import Path
from subprocess import call

from version_utils import pupil_version


def deb_package():
    app_version = pupil_version()
    # lets build the structure for our deb package.
    dist_root = Path("dist").resolve()
    deb_root = Path(f"pi_monitor_linux_os_x64_{app_version}").resolve()
    if deb_root.exists():
        shutil.rmtree(str(deb_root))

    control = deb_root / "DEBIAN" / "control"
    desktop = deb_root / "usr" / "share" / "applications" / "pi_monitor.desktop"
    starter = deb_root / "usr" / "local" / "bin" / "pi_monitor"
    opt_dir = deb_root / "opt"
    ico_dir = deb_root / "usr" / "share" / "icons" / "hicolor" / "scalable" / "apps"

    control.parent.mkdir(mode=0o755, exist_ok=True, parents=True)
    starter.parent.mkdir(mode=0o755, exist_ok=True, parents=True)
    desktop.parent.mkdir(mode=0o755, exist_ok=True, parents=True)
    ico_dir.mkdir(mode=0o755, exist_ok=True, parents=True)

    # DEB control file
    with control.open("w") as f:
        dist_size = sum(f.stat().st_size for f in dist_root.rglob("*"))
        content = f"""\
Package: pi-monitor
Version: {app_version}
Architecture: amd64
Maintainer: Pupil Labs <info@pupil-labs.com>
Priority: optional
Description: PI Monitor is the easy way to preview scene video and gaze streams of your Pupil Invisible devices.
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
        content = f"""\
[Desktop Entry]
Version={app_version}
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
    src_path = dist_root / "pi_monitor" / svg_file_name
    dst_path = ico_dir / svg_file_name
    shutil.copy(str(src_path), str(dst_path))
    dst_path.chmod(0o755)

    # copy the actual application
    shutil.copytree(str(dist_root), str(opt_dir))
    for f in opt_dir.rglob("*"):
        if f.is_file():
            if f.name == "pi_monitor":
                f.chmod(0o755)
            else:
                f.chmod(0o644)
        elif f.is_dir():
            f.chmod(0o755)
    opt_dir.chmod(0o755)

    call(f"fakeroot dpkg-deb --build {deb_root}", shell=True)


if __name__ == "__main__":
    deb_package()
