"""
a couple tests to make sure the old package name still works

These just happen to be the ones used on ResponseLink :-)
"""

import nucos
from math import isclose
import unit_conversion

def test_version():
    assert unit_conversion.__version__ == nucos.__version__


def test_convert():
    result = unit_conversion.convert("Volume", 'liter', "gallons", 10.0)

    assert isclose(result, 2.6417205, rel_tol=1e-6)


def test_lat_format():
    assert unit_conversion.lat_long.format_lat(-32.5) == '32° 30.00′ South'


def test_lon_format():
    assert unit_conversion.lat_long.format_lon(-32.5) == '32° 30.00′ West'



