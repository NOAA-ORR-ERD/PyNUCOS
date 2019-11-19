.. image:: https://travis-ci.org/NOAA-ORR-ERD/PyNUCOS.svg?branch=master
    :target: https://travis-ci.org/NOAA-ORR-ERD/PyNUCOS

PyNUCOS
=======

Python NOAA Unit Converter for Oil Spills

This repo provides a python package for doing physical unit conversion. It includes the odd units (API gravity, etc) that are used for oil spill response and planning, but not the odd units that other fields may require.

It also includes many common units for general use.

It also includes a few utilites that are not strictly unit conversion:
  - converting latitude/longitude to/from degrees, degrees minutes seconds, etc (and formatting as unicode objects)
  - converting to/from oil mass units to/from volume units.

Installing
==========

PYNUCOS is not yet on PyPi, so you need to get the source from this repo and install with the regular::

  python setup.py install

If you use conda, there is a conda package available on the NOAA-ORR-ERD channel::


  conda install unit_conversion -c NOAA-ORR-ERD


Use Cases:
-----------

This code is used in the NOAA Oil Spill modeling tools, and as the core lib for a desktop unit conversion application:

http://response.restoration.noaa.gov/oil-and-chemical-spills/oil-spills/response-tools/nucos-unit-converter-spill-responders.html

There is also a Javascript version available for use in Browser Client-side applications:

https://github.com/NOAA-ORR-ERD/NUCOS



