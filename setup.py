#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0111,W6005,W6100
from __future__ import absolute_import, print_function

import os
import re
from setuptools import setup


def get_version(*file_paths):
    """
    Extract the version string from the file at the given relative path fragments.
    """
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.

    Returns a list of requirement strings.
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.split('#')[0].strip() for line in open(path).readlines()
            if is_requirement(line.strip())
        )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement.

    that is, it is not blank, a comment, a URL, or an included file.
    """
    return not (line == '' or line.startswith(('-r', '#', '-e', 'git+', '-c')))


VERSION = get_version('edx_block_exporter', '__init__.py')

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
CHANGELOG = open(os.path.join(os.path.dirname(__file__), 'CHANGELOG.rst')).read()

config_python_path = "edx_block_exporter = edx_block_exporter.apps:EdxBlockExporterConfig"

setup(
    name='edx_block_exporter',
    version=VERSION,
    description='Module to export exist xBlock information',
    long_description=README + '\n\n' + CHANGELOG,
    author='Flying PI',
    zip_safe=False,
    keywords='edx',
    packages=[
        'edx_block_exporter',
    ],
    include_package_data=True,
    install_requires=load_requirements("requirements/base.txt"),
    entry_points={
        "cms.djangoapp": [config_python_path],
        'xblock.v1': [
            "toy_xblock_with_fields_only = edx_block_exporter.tests.resource.toy_items:ToyXblockWithFieldsOnly",
        ],
    }
)
