#! /usr/bin/env python3

import setuptools


def read(readme):
    with open(readme) as f:
        return f.read()


setuptools.setup(
    name="cork",
    version="0.01",
    description="Package web apps for the terminal. Based on PyInstaller and bad intentions.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/psbleep/cork",
    author="Patrick Schneeweis",
    author_email="psbleep@protonmail.com",
    license="GPLv3+",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Religion",  # The dark gods.
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
    ],
    packages=["cork"],
    install_requires=[
        "Click==7.0",
        "Flask==1.0.2",
        "PyInstaller==3.4",
        "requests==2.21.0"
    ],
    entry_points="""
        [console_scripts]
        cork=cork.__main__:run_cork
    """
)
