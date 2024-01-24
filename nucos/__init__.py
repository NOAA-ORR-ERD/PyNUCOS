#!/usr/bin/env python

"""
unit_conversion package

All it really contains is the one unit_conversion module,
a data module, plus a module for lat-lon conversion.

All of unit_conversion is imported here for convenience

"""

__version__ = "3.1.2"


from .unit_conversion import (UnitConversionError,
                              InvalidUnitError,
                              InvalidUnitTypeError,
                              NotSupportedUnitError,
                              is_same_unit,
                              is_supported,
                              is_supported_unit,
                              get_supported_names,
                              # not sure these should be used externally
                              FindUnitTypes,
                              GetUnitTypes,
                              GetUnitNames,
                              GetUnitAbbreviation,
                              # ConverterClass,
                              # Converters,
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

# this should probably not be exposed
from .unit_data import ConvertDataUnits

from nucos import lat_long

