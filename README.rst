#######
PyNUCOS
#######

Python NOAA Unit Converter for Oil Spills

This repo provides a python package for doing physical unit conversion. It includes the odd units (API gravity, etc) that are used for oil spill response and planning, but not the odd units that other fields may require.

It also includes many common units for general use.

There are also a few utilities that are not strictly unit conversion:

- Converting latitude/longitude to/from degrees, degrees minutes seconds, etc (and formatting as Unicode objects)
    
NOTE: lat-long parsing and formatting is also available in the `lat-long parser project <https://github.com/NOAA-ORR-ERD/lat_lon_parser>`_ 

- converting to/from oil mass units to/from volume units: e.g. tons to barrels.


Installing
==========

As of version 3, PyNUCOS is on PyPi and conda-forge, and of course, can be installed from source.

**From PyPi:** ::

    pip install pynucos

**From conda-forge:** ::

    conda install pynucos -c conda-forge

(the ``-c conda-forge`` is optional if you've already got the conda-forge channel)

**From Source:**

Get the source from gitHub::

  https://github.com/NOAA-ORR-ERD/PyNUCOS

Then the usual::

  pip install ./


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

There is also a Javascript version available for use in browser Client-side applications:

https://github.com/NOAA-ORR-ERD/jsNUCOS


Usage
=====

Most of the primary functionality is available with a single function::

  In [7]: from nucos import convert

  In [8]: convert('gal', 'liter', 1.0)
  Out[8]: 3.7854118

However, some unit names can have different meanings, e.g. fluid ounce and weight ounce, so can not be converted::

  In [9]: convert('oz', 'ml', 1.0)
  ---------------------------------------------------------------------------
  UnitConversionError                       Traceback (most recent call last)
  <ipython-input-9-86edffc0a76a> in <module>
  ----> 1 convert('oz', 'ml', 1.0)

  ~/Hazmat/ERD-PythonPackages/PyNUCOS/nucos/unit_conversion.py in convert(unit1, unit2, value, unit_type)
      464
      465         if unit_type != unit_type2:
  --> 466             raise UnitConversionError("Cannot convert {0} to {1}"
      467                                       .format(unit1, unit2))
      468

  UnitConversionError: Cannot convert oz to ml

To be more clearly specified, the unit type can be passed as the first argument::

  In [10]: convert('volume', 'oz', 'ml', 1.0)
  Out[10]: 29.57353

  In [16]: convert('mass', 'oz', 'gram', 1.0)
  Out[16]: 28.349523


Latitude Longitude Conversion
-----------------------------

There are functions for converting latitude and longitude to/from various formats.

Pass ``ustring=True`` to get a Unicode formatted string version.

::

  In [24]: from nucos import LatLongConverter

  In [25]: LatLongConverter.ToDecDeg(-45, 34, 12)
  Out[25]: -45.57

  In [26]: LatLongConverter.ToDecDeg(-45, 34, 12, ustring=True)
  Out[26]: '-45.570000°'

  In [27]: LatLongConverter.ToDegMin(-45.57)
  Out[27]: (-45.0, 34.2)

  In [28]: LatLongConverter.ToDegMin(-45.57, ustring=True)
  Out[28]: "-45° 34.200'"

  In [29]: LatLongConverter.ToDegMinSec(-45.57)
  Out[29]: (-45.0, 34, 12.0)

  In [30]: LatLongConverter.ToDegMinSec(-45.57, ustring=True)
  Out[30]: '-45° 34\' 12.00"'


Unit names
----------

Unit names are simple strings, and there are a lot of synonyms, both in ascii and Unicode formats.

The full list of units and names is in the `NUCOS_unit_list.rst` file.

You can programmatically access the unit types, unit names, etc, via::

  In [46]: nucos.GetUnitTypes()
  Out[46]:
  ['Length',
   'Oil Concentration',
   'Area',
   'Volume',
   'Temperature',
   'Delta Temperature',
   'Mass',
   'Time',
   'Velocity',
   'Discharge',
   'Mass Discharge',
   'Density',
   'Kinematic Viscosity',
   'Dynamic Viscosity',
   'Interfacial Tension',
   'Pressure',
   'Concentration In Water',
   'Concentration',
   'Dimensionless',
   'Mass Fraction',
   'Volume Fraction',
   'Angular Measure',
   'Angular Velocity']

  In [47]: nucos.GetUnitNames('Volume')
  Out[47]:
  ['cubic meter',
   'cubic kilometer',
   'cubic centimeter',
   'milliliter',
   'barrel (petroleum)',
   'liter',
   'gallon',
   'gallon (UK)',
   'million US gallon',
   'cubic foot',
   'cubic inch',
   'cubic yard',
   'fluid ounce',
   'fluid ounce (UK)']

  In [48]: nucos.GetUnitAbbreviation('Volume', 'cubic centimeter')
  Out[48]: 'cm³'


Release History
===============

Version 3.1.2
-------------

Added some more synonyms for meter per second.

Version 3.1.1
-------------


Fixed a bug with GetUnitNames() and capitalization.

Version 3.1.0
-------------

Added code to get valid unit names for a given unit_type


Version 3.1.0
-------------

Added code to get valid unit names for a given unit_type


Version 3.0
-----------

The first release on PyPi -- major change in this release is the top-level package name is now ``nucos`` -- it used to be ``unit_conversion``. The ``unit_conversion`` name is still there, but should raise a ``DeprecationWarning``


Contributing
============

If you have any suggestions for improvements, bug fixes, etc, please post an issue on GitHub:

``https://github.com/NOAA-ORR-ERD/PyNUCOS``

Or better yet, make a Pull Request.

Development Notes
-----------------

Testing
.......

there is a fairly comprehensive set of tests in:

``nucos/tests``

they can be run with pytest -- either directly:

``pytest nucos/tests``

or on the installed package:

``pytest --pyargs nucos``


New units / unit names
......................

Any additional units should be added to:

``nucos/unit_data.py``

It's a big nested dict with units, conversion factors and synonyms all there.
Hopefully, it's self describing :-)

Please add a test if you add a new unit.

Be sure to run the tests after making any changes --
that will catch errors in the format, duplicate names, etc.

Releasing
.........

Minor changes can be done directly in the main branch.

Checklist for a new release:

* Make sure the tests all pass, of course

* make sure the version is properly set: in ``nucos/__init__.py``

* Make sure that ``NUCOS_unit_list.rst`` has been updated -- it should happen when the tests are run.

* Push to GitHub

* Make a release on GitHub -- follow the tag convention already there.

* Increment the `__version__` in the main branch after making the release.

* Push to PyPi:
  - ``conda install twine build``
  - ``python -m build``
  - ``twine upload dist/*``

NOTE: At this point, only Chris Barker has permissions on PyPi to do this -- so either ask him to do it, or ask him for permissions.

* Check conda-forge for a build: conda-forge should detect that a release was made on GitHub, and then build a new package -- you can check the progress here:

``https://github.com/conda-forge/pynucos-feedstock``

ChrisBarker-NOAA and JamesMakela-NOAA have permissions on the feedstock.





