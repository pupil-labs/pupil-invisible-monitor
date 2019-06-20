from setuptools import setup


setup(
    name="pi_monitor",
    version="1",
    license="MIT",
    packages=["pi_monitor"],
    zip_safe=False,
    include_package_data=True,
    entry_points={"console_scripts": ["pi_monitor=pi_monitor.__main__:main"]},
)
