#!/usr/bin/env python

"""
unit_conversion package

All it really contains is the one unit_conversion module,
a data module, plus a module for lat-lon conversion.

All of unit_conversion is imported here for convenience

"""

__version__ = "3.0.0"


from .unit_conversion import (UnitConversionError,
                              InvalidUnitError,
                              InvalidUnitTypeError,
                              NotSupportedUnitError,
                              # ConverterClass,
                              is_same_unit,
                              is_supported,
                              # Converters,
                              FindUnitTypes,
                              GetUnitTypes,
                              GetUnitNames,
                              GetUnitAbbreviation,
                              # UNIT_TYPES,
                              # Simplify,
                              # DensityConverterClass,
                              # TempConverterClass,
                              # LatLongConverter,
                              # OilQuantityConverter,
                              convert,
                              )

from .lat_long import (LatLongConverter,
                       format_lat,
                       format_lon,
                       format_lat_d,
                       format_lon_d,
                       format_lat_dm,
                       format_lon_dm,
                       format_lat_dms,
                       format_lon_dms,
                       )

from .unit_data import ConvertDataUnits

from nucos import lat_long

