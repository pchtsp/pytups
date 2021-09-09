#!/usr/bin/env python3

from setuptools import setup

packages = ["pytups"]

with open("README.rst", "r") as fh:
    long_description = fh.read()

required = []
with open("requirements.txt", "r") as fh:
    required.append(fh.read().splitlines())


kwargs = {
    "name": "pytups",
    "version": "0.81.1",
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
