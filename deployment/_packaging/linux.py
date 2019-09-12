import shutil
from pathlib import Path
from subprocess import call

from .utils import pupil_version, get_tag_commit, app_name, package_name, dist_dir


def deb_package(deployment_root: Path) -> Path:
    app_version = pupil_version()
    git_version = get_tag_commit()
    # lets build the structure for our deb package_name.
    dist_root = dist_dir(deployment_root)
    deb_root = Path(f"{package_name}_linux_os_x64_{git_version}").resolve()
    if deb_root.exists():
        shutil.rmtree(str(deb_root))

    control = deb_root / "DEBIAN" / "control"
    desktop = deb_root / "usr" / "share" / "applications" / f"{package_name}.desktop"
    starter = deb_root / "usr" / "local" / "bin" / package_name
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
Package: {package_name.replace("_", "-")}
Version: {app_version}
Architecture: amd64
Maintainer: Pupil Labs <info@pupil-labs.com>
Priority: optional
Description: {app_name} is the easy way to preview scene video and gaze streams of your Pupil Invisible devices.
Installed-Size: {dist_size / 1024}
"""
        f.write(content)
    control.chmod(0o644)

    # bin_starter script

    with starter.open("w") as f:
        content = f'''\
#!/bin/sh
exec /opt/{package_name}/{package_name} "$@"'''
        f.write(content)
    starter.chmod(0o755)

    # .desktop entry
    # ATTENTION: In order for the bundle icon to display correctly
    # two things are necessary:
    # 1. Icon needs to be the icon's base name/stem
    # 2. The window title must be equivalent to StartupWMClass
    with desktop.open("w") as f:
        content = f"""\
[Desktop Entry]
Version={app_version}
Type=Application
Name={app_name}
Comment=Preview Pupil Invisible data streams
Exec=/opt/{package_name}/{package_name}
Terminal=false
Icon={package_name}
Categories=Application;
Name[en_US]={app_name}
Actions=Terminal;
StartupWMClass={app_name}

[Desktop Action Terminal]
Name=Open in Terminal
Exec=x-terminal-emulator -e {package_name}"""
        f.write(content)
    desktop.chmod(0o644)

    svg_file_name = f"{package_name}.svg"
    src_path = dist_root / package_name / svg_file_name
    dst_path = ico_dir / svg_file_name
    shutil.copy(str(src_path), str(dst_path))
    dst_path.chmod(0o755)

    # copy the actual application
    shutil.copytree(str(dist_root), str(opt_dir))
    for f in opt_dir.rglob("*"):
        if f.is_file():
            if f.name == package_name:
                f.chmod(0o755)
            else:
                f.chmod(0o644)
        elif f.is_dir():
            f.chmod(0o755)
    opt_dir.chmod(0o755)

    call(f"fakeroot dpkg-deb --build {deb_root}", shell=True)
    return Path(f"{deb_root}.deb")


if __name__ == "__main__":
    deb_package()
