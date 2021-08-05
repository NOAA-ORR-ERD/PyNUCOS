#!/usr/bin/env python

"""
This setup is suitable for "python setup.py develop" from setuptools.
"""

import os
from setuptools import setup


def get_version(pkg_name):
    """
    Reads the version string from the package __init__ and returns it
    """
    with open(os.path.join(pkg_name, "__init__.py")) as init_file:
        for line in init_file:
            parts = line.strip().partition("=")
            if parts[0].strip() == "__version__":
                return parts[2].strip().strip("'").strip('"')
    return None


setup(
    name="unit_conversion",
    description=('Physical Unit conversion utilities'
                 ' -- units useful for oil and chemical spill response'),
    author='Christopher H. Barker',
    author_email='Chris.Barker@noaa.gov',
    url='https://github.com/NOAA-ORR-ERD/PyNUCOS',
    version=get_version("unit_conversion"),
    packages=['unit_conversion',
              'unit_conversion.tests'],
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Intended Audience :: Developers",
                 "Intended Audience :: Science/Research",
                 "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
                 "Programming Language :: Python :: 3 :: Only",
                 "Topic :: Scientific/Engineering",
                 ],
    zip_safe=False,
    )


