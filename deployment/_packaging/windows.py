import logging
from pathlib import Path
from subprocess import call

from .utils import dist_dir, get_tag_commit, package_name

logger = logging.getLogger()


def archive_7z(deployment_root: Path) -> Path:
    logger.info("Creating 7z archive...")
    bundle_path = dist_dir(deployment_root) / package_name

    archive_name = f"{package_name}_windows_x64_{get_tag_commit()}.7z"
    archive_path = dist_dir(deployment_root) / archive_name

    archive_7z_cmd = f"7z a -t7z {archive_path} {bundle_path}"
    call(archive_7z_cmd, shell=True)
    return archive_path
