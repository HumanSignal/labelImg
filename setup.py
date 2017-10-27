#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from libs.version import __version__

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: Different OS have different requirements
]

required_packages = find_packages()
required_packages.append('labelImg')

setup(
    name='labelImg',
    version=__version__,
    description="LabelImg is a graphical image annotation tool and label object bounding boxes in images",
    long_description=readme + '\n\n' + history,
    author="TzuTa Lin",
    author_email='tzu.ta.lin@gmail.com',
    url='https://github.com/tzutalin/labelImg',
    package_dir={'labelImg': '.'},
    packages=required_packages,
    entry_points={
        'console_scripts': [
            'labelImg=labelImg.labelImg:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='labelImg labelTool development annotation deeplearning',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    package_data={'data/predefined_classes.txt': ['data/predefined_classes.txt']}
)
