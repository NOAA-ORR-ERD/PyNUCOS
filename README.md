PyNUCOS
=======

Python NOAA Unit Converter for Oil Spills

This repo provides a python package for doing physical unit conversion. It includes the odd units (API gravity, etc) that are used for oils spill response and planning, but not the odd units that other fields may require.

It also includes may of the comon units for general use.

It also includes a few utilites that are not striclky jsut unit conversion:
  - converting latitude/longitude to/from degrees, degrees minutes seconds, etc (and formatting as unicode objects)
  - converting to oil mass unit to/from volume units.

Use Cases:
-----------

This code is used in the NOAA Oil Spill modeling tools, and as the core lib for a desktop unit conversion application:

http://response.restoration.noaa.gov/oil-and-chemical-spills/oil-spills/response-tools/nucos-unit-converter-spill-responders.html

There is also a JAvascript version available for use in BRowser Client-side applications:

https://github.com/NOAA-ORR-ERD/NUCOS



