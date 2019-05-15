#! /usr/bin/env python3

import setuptools


setuptools.setup(
    name="cork",
    version="0.02",
    description="",
    url="https://github.com/psbleep/cork",
    author="Patrick Schneeweis",
    author_email="psbleep@protonmail.com",
    license="GPLv3+",
    packages=["cork"],
    install_requires=[
        "Click==7.0",
        "Flask==1.0.2",
        "PyInstaller==3.4",
        "requests==2.21.0"
    ],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        cork=cork.__main__:cli
    """
)
