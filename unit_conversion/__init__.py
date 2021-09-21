"""
This here for backward compatibility only

It intends to present all the names actually used in the old
unit_conversion namespace

This API is deprecated -- please use the nucos package instead.
"""

import warnings

from nucos import __version__

from nucos.unit_conversion import *

from nucos import lat_long

from nucos.lat_long import (LatLongConverter,
                            Latitude,
                            Longitude,
                            format_lat,
                            format_lon,
                            format_lat_d,
                            format_lon_d,
                            format_lat_dm,
                            format_lon_dm,
                            format_lat_dms,
                            format_lon_dms,
                            )

warnings.warn(DeprecationWarning(
    "The unit_conversion module is deprecated -- "
    "import as `nucos` instead"))


