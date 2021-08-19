#######
PyNUCOS
#######

Python NOAA Unit Converter for Oil Spills

This repo provides a python package for doing physical unit conversion. It includes the odd units (API gravity, etc) that are used for oil spill response and planning, but not the odd units that other fields may require.

It also includes many common units for general use.

It also includes a few utilities that are not strictly unit conversion:
  - converting latitude/longitude to/from degrees, degrees minutes seconds, etc (and formatting as Unicode objects)
  - converting to/from oil mass units to/from volume units.

Installing
==========

PYNUCOS is not yet on PyPi, so you need to get the source from this repo and install with the regular::

  python setup.py install

If you use conda, there is a conda package available conda-forge::


  conda install pynucos -c conda-forge


Use Cases:
==========

There are many unit conversion codes out there, but none that easily support the strange units used in Oil Spill Response (and the petroleum industry in general), such as API Gravity and conversion of amount of oil from mass to volume.

This code is used as the core lib for a desktop unit conversion application:

https://github.com/NOAA-ORR-ERD/wxNUCOS

It is available as an installable binary from:

http://response.restoration.noaa.gov/oil-and-chemical-spills/oil-spills/response-tools/nucos-unit-converter-spill-responders.html

The code is also used in the NOAA Oil Spill modeling tools:

https://response.restoration.noaa.gov/oil-and-chemical-spills/oil-spills/response-tools/gnome-suite-oil-spill-modeling.html

Available on gitHub here:

https://github.com/NOAA-ORR-ERD

Javascript Version
------------------

There is also a Javascript version available for use in Browser Client-side applications:

https://github.com/NOAA-ORR-ERD/NUCOS

Usage
=====

Most of the primary functionality is available with a single function::

  In [7]: from unit_conversion import convert

  In [8]: convert('gal', 'liter', 1.0)
  Out[8]: 3.7854118

  In [9]: convert('oz', 'ml', 1.0)
  ---------------------------------------------------------------------------
  UnitConversionError                       Traceback (most recent call last)
  <ipython-input-9-86edffc0a76a> in <module>
  ----> 1 convert('oz', 'ml', 1.0)

  ~/Hazmat/ERD-PythonPackages/PyNUCOS/unit_conversion/unit_conversion.py in convert(unit1, unit2, value, unit_type)
      464
      465         if unit_type != unit_type2:
  --> 466             raise UnitConversionError("Cannot convert {0} to {1}"
      467                                       .format(unit1, unit2))
      468

  UnitConversionError: Cannot convert oz to ml

  In [10]: convert('volume', 'oz', 'ml', 1.0)
  Out[10]: 29.57353




