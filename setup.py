from setuptools import setup

from deployment.version_utils import get_version

requirements = [
	"pyglui >= 1.25",
	"ndsi >= 0.5",
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
