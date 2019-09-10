import logging
import zipfile
from pathlib import Path
from subprocess import call

from .utils import package_name, app_name, dist_dir, get_tag_commit

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


def _bundle_app_dir(deployment_root: Path):
    return dist_dir(deployment_root) / f"{app_name}.app"
