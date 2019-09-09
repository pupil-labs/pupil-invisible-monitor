from setuptools import setup

from deployment.version_utils import get_version

requirements = [
    "-e git://github.com/pupil-labs/pyglui/@master#egg=pyglui"
    "-e git://github.com/pupil-labs/pyndsi/@master#egg=ndsi"
    "numpy",
    "PyOpenGL",
]

setup(
    name="pi_monitor",
    version=str(get_version()),
    license="MIT",
    packages=["pi_monitor"],
    zip_safe=False,
    include_package_data=True,
    entry_points={"console_scripts": ["pi_monitor=pi_monitor.__main__:main"]},
)
