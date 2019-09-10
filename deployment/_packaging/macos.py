import logging
import shutil
import zipfile
from pathlib import Path
from subprocess import call

from .utils import app_name, dist_dir, get_size, get_tag_commit, package_name

logger = logging.getLogger()


def sign_app(deployment_root: Path):
    logger.info("Attempting codesigning...")
    cert = "Developer ID Application: Pupil Labs UG (haftungsbeschrankt) (R55K9ESN6B)"
    bundle_app_dir = _bundle_app_dir(deployment_root)
    for DS_Store in bundle_app_dir.rglob(".DS_Store"):
        logger.info(f"Deleting {DS_Store}")
        DS_Store.unlink()

    sign_cmd = (
        "codesign "
        "--force "
        "--verify "
        "--verbose "
        f"-s '{cert}' "
        f"--deep '{bundle_app_dir}'"
    )
    if call(sign_cmd, shell=True) == 0:
        logger.info("Codesigning successful")
    else:
        logger.warning("Codesigning failed!")


def zip_app(deployment_root: Path) -> Path:
    bundle_app_dir = _bundle_app_dir(deployment_root)
    zip_name = f"{package_name}_mac_os_x64_{get_tag_commit()}.zip"
    zip_path = bundle_app_dir.with_name(zip_name)
    with zipfile.ZipFile(zip_path, mode="w") as zip_archive:
        for path in bundle_app_dir.rglob("*"):
            arcname = path.relative_to(bundle_app_dir.parent)
            zip_archive.write(path, arcname)

    return zip_path


def dmg_app(deployment_root: Path) -> Path:
    _remove_pre_bundle(deployment_root)

    bundle_app_dir = _bundle_app_dir(deployment_root)
    bundle_parent = bundle_app_dir.parent
    bundle_dmg_name = f"{package_name}_mac_os_x64_{get_tag_commit()}"
    bundle_dmg_mount_point = f"Install {app_name}"

    applications_target = Path("/Applications")
    applications_symlink = bundle_parent / "Applications"
    if applications_symlink.exists():
        applications_symlink.unlink()
    applications_symlink.symlink_to(applications_target, target_is_directory=True)

    volumen_size = get_size(bundle_parent)
    dmg_cmd = (
        f"hdiutil create "
        f"-volname '{bundle_dmg_mount_point}' "
        f"-srcfolder {bundle_parent} "
        f"-format UDZO "
        f"-size {volumen_size}b "
        f"'{bundle_dmg_name}.dmg'"
    )
    call(dmg_cmd, shell=True)
    return Path(bundle_dmg_name).with_suffix(".dmg")


def _bundle_app_dir(deployment_root: Path):
    return dist_dir(deployment_root) / f"{app_name}.app"


def _remove_pre_bundle(deployment_root: Path):
    pre_bundle = dist_dir(deployment_root) / package_name
    logger.info(f"Building dmg requires removing {pre_bundle}")
    shutil.rmtree(str(pre_bundle))
