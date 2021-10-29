from setuptools import setup

from deployment._packaging.utils import get_version

# Libs with Windows wheels need a fixed version to install the wheels automatically.
PYGLUI_VERSION = "1.29"

requirements = [
    "numpy",
    "glfw>=1.8.4",
    "PyOpenGL",
    "pyglui",
    "ndsi",
]

package = "pupil_invisible_monitor"

setup(
    name="pupil-invisible-monitor",
    version=str(get_version()),
    license="MIT",
    packages=[package],
    package_dir={"": "src"},
    zip_safe=False,
    include_package_data=True,
    entry_points={"console_scripts": [f"{package}={package}.__main__:main"]},
    install_requires=requirements,
    extras_require={"deploy": ["pyinstaller", "packaging"]},
)
