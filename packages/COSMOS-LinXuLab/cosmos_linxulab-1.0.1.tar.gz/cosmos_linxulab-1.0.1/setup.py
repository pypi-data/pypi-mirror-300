#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='COSMOS_LinXuLab',
    version='1.0.1',
    description='The software is to implement the COSMOS. Please see the website for details.',
    url='https://github.com/Lin-Xu-lab/COSMOS.git',
    packages=find_packages(where='COSMOS'), 
    package_dir={'': 'COSMOS'},  # Here was the missing comma
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
