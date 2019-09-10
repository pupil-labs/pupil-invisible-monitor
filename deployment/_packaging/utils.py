# -*- coding: utf-8 -*-
# Author: Douglas Creager <dcreager@dcreager.net>
# Changes, Additions: Moritz Kassner <moritz@pupil-labs.com>, Will Patera <will@pupil-labs.com>
# This file is placed into the public domain.

import logging
import os
import sys
from itertools import filterfalse
from pathlib import Path
from subprocess import STDOUT, CalledProcessError, check_output

from packaging.version import Version

logger = logging.getLogger(__name__)
app_name = "Pupil Invisible Monitor"
package_name = "pupil_invisible_monitor"


def dist_dir(root: Path):
    return root.resolve() / "dist"


def move_packaged_bundle(root: Path, bundle: Path):
    bundle_destination_parent = root / "bundles"
    bundle_destination_parent.mkdir(exist_ok=True)
    bundle_destination = bundle_destination_parent / bundle.name
    bundle.rename(bundle_destination)


def get_tag_commit():
    """
    returns string: 'tag'-'commits since tag'-'7 digit commit id'
    """
    try:
        desc_tag = check_output(
            ["git", "describe", "--tags", "--long"],
            stderr=STDOUT,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )
        desc_tag = desc_tag.decode("utf-8")
        desc_tag = desc_tag.replace("\n", "")  # strip newlines
        return desc_tag
    except CalledProcessError as e:
        logger.error('Error calling git: "{}" \n output: "{}"'.format(e, e.output))
        return None
    except OSError as e:
        logger.error('Could not call git, is it installed? error msg: "{}"'.format(e))
        return None


def pupil_version():
    """
    [major].[minor].[trailing-untagged-commits]
    """
    version = get_tag_commit()
    if version is None:
        raise ValueError("Version Error")

    version = version.replace("v", "")  # strip version 'v'
    # print(version)
    if "-" in version:
        parts = version.split("-")
        version = ".".join(parts[:-1])
    return version


def get_version(version_file=None):
    # get the current software version
    if getattr(sys, "frozen", False):
        with open(version_file, "r") as f:
            version = f.read()
    else:
        version = pupil_version()
    version = Version(version)
    logger.debug("Running version: {}".format(version))
    return version


def get_size(start_path="."):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


if __name__ == "__main__":
    print(get_tag_commit())
    print(pupil_version())
