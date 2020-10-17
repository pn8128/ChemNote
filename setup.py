# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from setuptools import setup, find_packages

try:
    with open('README.rst') as f:
        readme = f.read()
except IOError:
    readme = ''


def _requires_from_file(filename):
    return open(filename).read().splitlines()


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ChemNote",  # Replace with your own username
    version="0.0.1",
    author="kota oishi",
    author_email="oishi-kota454@g.ecc.u-tokyo.ac.jp",
    description="Physical and chemical arithmetic tools for jupyter notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pn8128/ChemNote",
    install_requires=_requires_from_file('requirements.txt'),
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
