#!/usr/bin/env python3

from setuptools import setup

packages = ["pytups"]

with open("README.rst", "r") as fh:
    long_description = fh.read()

version_dict = {}
exec(open("pytups/constants.py").read(), version_dict)
VERSION = version_dict["VERSION"]

required = []

kwargs = {
    "name": "pytups",
    "version": VERSION,
    "packages": packages,
    "description": "data wrangling for lists of tuples and dictionaries",
    "long_description": long_description,
    "long_description_content_type": "text/x-rst",
    "author": "Franco Peschiera",
    "maintainer": "Franco Peschiera",
    "author_email": "pchtsp@gmail.com",
    "maintainer_email": "pchtsp@gmail.com",
    "install_requires": required,
    "url": "https://github.com/pchtsp/pytups",
    "download_url": "https://github.com/pchtsp/pytups/archive/master.zip",
    "keywords": "super dict dictionary tuple list math pulp",
    "classifiers": [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
}

setup(**kwargs)
