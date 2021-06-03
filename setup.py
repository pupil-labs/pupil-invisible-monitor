from setuptools import setup

from deployment._packaging.utils import get_version

# Libs with Windows wheels need a fixed version to install the wheels automatically.
PYLGUI_VERSION = "1.28"
PYNDSI_VERSION = "1.4"

requirements = [
    "numpy",
    "glfw>=1.8.4",
    "PyOpenGL",
    "pyzmq",
    # Install pyglui from source for Unix and from wheel for Windows. Note we install
    # via git, not from archive, as pyglui contains submodules which are not included in
    # archive, but will be checked out when installing via git.
    f'pyglui @ git+https://github.com/pupil-labs/pyglui.git@v{PYLGUI_VERSION} ; platform_system != "Windows"',
    f'pyglui @ https://github.com/pupil-labs/pyglui/releases/download/v{PYLGUI_VERSION}/pyglui-{PYLGUI_VERSION}-cp36-cp36m-win_amd64.whl ; platform_system == "Windows"',
    
    # Install pyndsi from source until it is available via PyPI
    f'ndsi @ https://github.com/pupil-labs/pyndsi/archive/master.zip',
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
