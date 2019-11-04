from setuptools import setup

from deployment._packaging.utils import get_version

requirements = [
    "pyglui>=1.25",
    "ndsi>=1.0.dev0",
    "numpy",
    "PyOpenGL",
    "pyzmq",
    "pyre",
    "glfw",
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
