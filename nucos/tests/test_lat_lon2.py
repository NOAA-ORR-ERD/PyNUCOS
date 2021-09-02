"""
PyTest unit tests for 'lat_lon' module.

This tests the new(er) API -- developed for ResponseLink

"""

from __future__ import unicode_literals

import pytest

import nucos.lat_long as ll


@pytest.mark.parametrize(("number", "text"),
                         [(28.2186111111, "28\xb0 13.12\u2032 North"), #from incident 6652
                          (-0.1, "0\xb0 6.00\u2032 South")
                         ])
def test_format_lat(number, text):
    assert ll.format_lat(number) == text


@pytest.mark.parametrize(("number", "text"),
                         [(-92.6244444444, "92\xb0 37.47\u2032 West"), #from incident 6652
                         ])
def test_format_lon(number, text):
    assert ll.format_lon(number) == text


## degrees, minutes, seconds formatting:
@pytest.mark.parametrize(("number", "text"),
                         [(28.2186111111, "28\xb0 13\u2032 7.00\u2033 North"), #from incident 6652
                          (-0.1, "0\xb0 6\u2032 0.00\u2033 South")
                         ])
def test_format_lat_dms(number, text):
    assert ll.format_lat_dms(number) == text

@pytest.mark.parametrize(("number", "text"),
                         [(-92.6244444444, "92\xb0 37\u2032 28.00\u2033 West"), #from incident 6652
                         ])
def test_format_lon_dms(number, text):
    assert ll.format_lon_dms(number) == text



# #### Low-level tests ####
# class TestExtractDegreesMinutes(object):
#     def test1(self):
#         assert ll.extract_degrees_minutes(30.5) == (30.0, 30)

#     def test2(self):
#         assert ll.extract_degrees_minutes(-30.5) == (-30.0, 30.0)

#     def test_minus_zero(self):
#         assert ll.extract_degrees_minutes(-0.1) == (-0.0, 6.0)

# class TestExtractDegreesMinutesSeconds(object):

#     def test1(self):
#         assert ll.extract_degrees_minutes_seconds(30.0) == (30.0, 0.0, 0.0)

#     def test2(self):
#         assert ll.extract_degrees_minutes_seconds(-30.5) == (-30.0, 30.0, 0.0)

#     def test3(self):
#         assert ll.extract_degrees_minutes_seconds(30.001) == (30.0, 0.0, 3.6)


# class TestGetDirection(object):
#     def test1(self):
#         assert ll.get_direction(1.1, "Foo", "Bar") == "Foo"

#     def test2(self):
#         assert ll.get_direction(-1.1, "Foo", "Bar") == "Bar"


# # #### High-level tests ####
# # class TestIncident6652(BaseTestIncident):
# #     lat = 28.2186111111
# #     latf = "28\xb0 13.12\u2032 North"

# #     lon = -92.6244444444
# #     lonf = "92\xb0 37.47\u2032 West"
