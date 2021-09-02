#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tests for unit_conversion main code

designed to be run with pytest

pytest test_unit_conversion.py
"""

import math

try:
    from math import isclose
except ImportError:
    print("nucos > 2.11 only works with Python > 3.7")
    raise

import pytest
from nucos import unit_conversion

RELTOL = 1e-5
ABSTOL = 1e-5  # not used, but maybe some day?

KnownValues = [
    # Known values from Handbook of Chemistry and Physics (HCP),
    # except where noted
    ("length", "meters", "feet", 1, 3.2808398),
    ("length", "feet", "meters", 1, .3048),
    ("length", "feet", "miles", 1, 0.000189393),
    ("length", "feet", "nauticalmiles", 1, .00016457883),
    ("length", "feet", "inches", 1, 12),
    ("length", "fathom", "cm", 1, 182.88),
    ("length", "Latitude Minutes", "NauticalMiles", 1.0, 1.0),
    ("Length", "LatitudeDegrees", "NauticalMiles", 1.0, 60),
    ("Length", "micron", "mm", 100, .1),
    ("Length", "\N{MICRO SIGN}m", "m", 1, 1e-6),
    ("Length", "km", "yard", 1, 1093.6133),


    # all values close to value in the "Open Water Oil Identification Job Aid"
    # and close to values in the Unit Conversion sheet distributed with the
    # dispersant mission planner.
    # Technically, oil concentration is a unit of length, but it's conceptually
    # different.
    # So we treat it differently here: (i.e. using bbl/acre as a length
    # would be really weird)
    # Also: we've now got units of mass/area as well -- which is not a length
    ("Oil Concentration", "micron", "mm", 100, .1),
    ("Oil Concentration", "µm", "mm", 1, 1e-3),
    ("Oil Concentration", "in", "mm", 1.0, 25.4),
    ("Oil Concentration", "micron", "bbl/acre", 1.0, 0.02545396),  # calculated from HCP --
    ("Oil Concentration", "bbl/acre", "m^3/km^2", 1.0, 39.2866),  # calculated from HCP --
    ("Oil Concentration", "bbl/acre", "bbl/sq.mile", 1.0, 640.0),  # calculated from HCP --
    ("Oil Concentration", "gal/acre", "bbl/acre", 42.0, 1.0),  # calculated from HCP --
    ("Oil Concentration", "m\N{SUPERSCRIPT THREE}/km\N{SUPERSCRIPT TWO}",
                          "liter/hectare", 1, 10.0),  # calculated from HCP --
    ("Oil Concentration", "l/m\N{SUPERSCRIPT TWO}",
                          "liter/hectare", 1, 10000.0),  # calculated from HCP --

    # These are mass/area -- using an assumed density of 0.95
    ("Oil Concentration", "micron", "g/m^2", 100.0, 95.0),
    ("Oil Concentration", "kg/m^2", "micron", .95, 1000.0),
    ("Oil Concentration", "kg/km^2", "g/m^2", 1.0, 1e-3),
    ("Oil Concentration", "kg/m^2", "g/m^2", 1.0, 1e3),

    ("Area", "sq m", "ft^2", 10, 107.63910),
    ("Area", "Acre", "square yards", 1, 4840),
    ("Area", "Hectares", "cm^2", 1.0, 1e8),
    ("Area", "ha", "sq miles", 1.0, 0.0038610216),
    ("Area", "ft^2", "in^2", 1.0, 144),
    ("Area", "km^2", "ft^2", 1.0, 1.0763910e7),
    ("Area", "nm^2", "acre", 1.0, 847.547741),  # calculated from HCP values
    ("Area", "nm^2", "square mile", 1.0, 1.3242932),  # calculated from HCP values


    ("Volume", "liters", "gal", 1.0, 0.26417205),
    ("Volume", "cubicmeters", "gal", 0.0037854118, 1.0),
    ("Volume", "ml", "cc", 1.0, 1.0),
    ("Volume", "milliongallons", "gal", 1.0, 1e6),
    ("Volume", "liters", "ft\N{SUPERSCRIPT THREE}", 1.0, 0.035314667),
    ("volume", "bbl", "l", 1.0, 158.9873),
    ("volume", "cubicinches", "cubicfeet", 1.0, 0.00057870370),
    ("volume", "cc", "cubicyard", 1.0, 1.3079506e-6),
    ("volume", "fluid ounce (UK)", "fluid oz", 1.0, 0.9607594),
    ("volume", "gallon (UK)", "gal", 1.0, 1.200949),
    ("volume", "cubic kilometer", "m\N{SUPERSCRIPT THREE}", 1.0, 1e9),
    ("volume", "cubic kilometer", "ft^3", 1.0, 3.531467e10),  # the google converter

    ("mass", "kg", "lb", 1.0, 2.2046226),
    ("Mass", "kg", "metrictons", 1.0, 0.001),
    ("mass", "kg", "lb", 1.0, 2.2046226),
    ("mass", "pound", "slug", 1.0, 0.0310810),
    ("mass", "ounce", "lbs", 1.0, 0.0625),
    ("mass", "ton", "gram", 1.0, 907184.74),
    ("mass", "ton(UK)", "ton", 1.0, 1.12),
    ("mass", "mg", "g", 1000.0, 1.0),
    ("mass", "g", "\N{MICRO SIGN}g", 1.0, 1e6),

    ("Time", "seconds", "minutes", 60, 1.0),
    ("time", "days", "minutes", 1.0, 24 * 60),
    ("time", "hr", "seconds", 1.0, 60 * 60),

    ("Velocity", "m/s", "cm/s", 1.0, 100),
    ("Velocity", "m s-1", "cm/s", 1.0, 100),
    ("Velocity", "m.s-1", "cm/s", 1.0, 100),
    ("Velocity", "km/h", "kts", 1.0, 0.5399568),
    ("Velocity", "mph", "ft/s", 1.0, 1.4666666),
    ("Velocity", "ft/min", "mph", 1.0, 0.01136363),
    ("Velocity", "ft/s", "m/min", 1.0, 18.288),
    ("Velocity", "ft/hr", "cm/s", 1.0, 0.0084666),
    ("Velocity", "ft/hr", "km/hr", 1.0, 0.0003048),
    ("Velocity", "knot", "m/s", 1.0, 0.514444),
    ("Velocity", "km/day", "m/s", 1.0, 0.01157404166666666),
    ("Velocity", "km/hr", "km/day", 1.0, 24.0),


    ("Discharge", "cfs", "l/s", 1.0, 28.31685),
    ("Discharge", "gal/hr", "gal/min", 60.0, 1.0),
    ("Discharge", "bbl/day", "l/s", 1.0, (158.9873 / 24 / 3600)),  # calculated from bll=>liter
    ("Discharge", "ft^3/min", "gal/min", 1.0, 7.4805195),
    ("Discharge", "m^3/min", "m^3/s", 1.0, 1.0 / 60.0),
    ("Discharge", "m^3/min", "gal/min", 1.0, 264.1721),
    ("Discharge", "gal/hr", "m^3/min", 1.0, 6.3090197e-5),
    ("Discharge", "gal/hr", "m^3/hr", 1.0, 6.3090197e-5 * 60.0),  # calculated from m^3/min
    ("Discharge", "bbl/day", "gal/day", 1.0, 42),  # from definition of bbl
    ("Discharge", "l/min", "cfs", 1.0, 0.000588578),
    ("Discharge", "bbl/hr", "cfs", 1.0, 5.614583 / 3600.),  # calculated from cfs
    ("Discharge", "cfs", "gal/sec", 1.0, 448.83117 / 60),  # calculated from gal/min

    ("Mass Discharge", "kg/s", "g/s", 1.0, 1000.0),

    ("Kinematic Viscosity", "stokes", "cSt", 1, 100.0),
    ("Kinematic Viscosity", "cm^2/s", "m^2/s", 1, .0001),
    ("Kinematic Viscosity", "cm^2/s", "square inch per second", 1, 0.15500031),
    ("Kinematic Viscosity", "SSU", "cSt", 462.0, 100.0),
    ("Kinematic Viscosity", "SSF", "cSt", 342.0, 724.0),
    ("Kinematic Viscosity", "mm^2/s", "cSt", 1.0, 1.0),  # from ASTM report

    ("Dynamic Viscosity", "kg/(m s)", "Pa s", 1.0, 1.0),
    ("Dynamic Viscosity", "Pa s", "N s/m^2", 1.0, 1.0),
    ("Dynamic Viscosity", "N s/m^2", "kg/(m s)", 1.0, 1.0),
    ("Dynamic Viscosity", "g/(cm s)", "Pa s", 1.0, 0.1),
    ("Dynamic Viscosity", "poise", "Pa s", 1.0, 0.1),
    ("Dynamic Viscosity", "dyne s/cm^2", "Pa s", 1.0, 0.1),
    ("Dynamic Viscosity", "centipoise", "Pa s", 1.0, 0.001),
    ("Dynamic Viscosity", "mPa s", "Pa s", 1.0, 0.001),

    ("temperature", "F", "C", 32, 0),
    ("temperature", "F", "C", 212, 100),
    ("temperature", "C", "K", 0, 273.15),
    ("temperature", "F", "K", 32, 273.15),

    ("deltatemperature", "F", "C", 1.0, (5.0 / 9.0)),
    ("deltatemperature", "F", "C", 0.0, 0.0),
    ("deltatemperature", "C", "K", 12.2, 12.2),
    ("deltatemperature", "K", "F", 10, 90.0 / 5.0),


    ("density", "g/cm^3", "Specific Gravity (15C)", 1, (1 / 0.999016)),
    ("density", "g/cm^3", "Specific Gravity (15C)", 0.999016, 1),
    ("density", "g/L", "kg/m^3", 1.0, 1.0),
    ("density", "kg/L", "kg/m^3", 1.0, 1000.0),
    ("density", "g/mL", "kg/m^3", 1.0, 1000.0),
    ("density", "Specific gravity", "gramspercubiccentimeter", 1, 0.999016),
    ("density", "SG", "API", 1.0, 10),
    ("density", "SG", "API", 2.0, -60.75),
    ("density", "SG", "API", 0.9, 25.7222),
    ("density", "API", "SG", 25.7222, 0.9),
    ("density", "lbs/ft^3", "Grams per Cubic Centimeter", 1.0, 0.016018463),
    ("density", "tonne per cubic meter", "kg/m^3", 1.0, 1000.0),
    ("density", "T/m³", "kg/m^3", 1.0, 1000.0),
    ("density",  "kg/m^3", "pound per gallon", 1.0, 0.0083454),
    ("density",  "lb/gal", "g/cm³", 1.0, 0.119826427),



    # some from https://en.wikipedia.org/wiki/Surface_tension#Physical_units
    ("Interfacial Tension", "dyn/cm", "N/m", 1.0, 0.001),
    ("Interfacial Tension", "N/m", "dyn/cm", 1.0, 1000),
    ("Interfacial Tension", "N/m", "J/m^2", 0.001, 0.001),
    ("Interfacial Tension", "N/m", "mN/m", 1.0, 1000.0),
    ("Interfacial Tension", "N/m", "dyne/cm", 1.0, 1000.0),
    ("Interfacial Tension", "N/m", "pdl/in", 1.0, 0.1837185500656),
    ("Interfacial Tension", "N/m", "lbf/in", 1.0, 0.0057101470975576),
    ("Interfacial Tension", "N/m", "erg/cm^2", 1.0, 1000.0),
    ("Interfacial Tension", "N/m", "erg/cm\N{SUPERSCRIPT TWO}", 1.0, 1000.0),
    ("Interfacial Tension", "N/m", "erg/mm^2", 1.0, 10.0),
    ("Interfacial Tension", "N/m", "erg/mm\N{SUPERSCRIPT TWO}", 1.0, 10.0),

    # ("Adhesion", "Pa", "kPa", 1.0, 0.001),
    # ("Adhesion", "Pa", "MPa", 1.0, 0.000001),
    # ("Adhesion", "Pa", "N/m^2", 1.0, 1.0),
    # ("Adhesion", "Pa", "bar", 1.0, 0.00001),
    # ("Adhesion", "Pa", "mbar", 1.0, 0.01),
    # ("Adhesion", "Pa", "g/cm^2", 1.0, 0.0101972),
    # ("Adhesion", "Pa", "kg/cm^2", 1.0, 0.0000101972),
    # ("Adhesion", "Pa", "dyn/cm^2", 1.0, 10.0),
    # ("Adhesion", "Pa", "psi", 1.0, 0.0001450377),
    # ("Adhesion", "Pa", "lb/in^2", 1.0, 0.0001450377),
    # ("Adhesion", "Pa", "N/m\N{SUPERSCRIPT TWO}", 1.0, 1.0),
    # ("Adhesion", "Pa", "g/cm\N{SUPERSCRIPT TWO}", 1.0, 0.0101972),
    # ("Adhesion", "Pa", "kg/cm\N{SUPERSCRIPT TWO}", 1.0, 0.0000101972),
    # ("Adhesion", "Pa", "dyn/cm\N{SUPERSCRIPT TWO}", 1.0, 10.0),
    # ("Adhesion", "Pa", "lb/in\N{SUPERSCRIPT TWO}", 1.0, 0.0001450377),
    # ("Adhesion", "kg/cm^2", "kg/m^2", 1.0, 10000.0),
    # ("Adhesion", "g/cm^2", "g/m^2", 1.0, 10000.0),
    # ("Adhesion", "kg/cm^2", "g/cm^2", 1.0, 1000.0),
    # ("Adhesion", "kg/m^2", "g/m^2", 1.0, 1000.0),

    ("Concentration In Water", "ppb", "ppm", 1000, 1),  # calculated
    ("Concentration In Water", "fraction", "%", 1, 100),  # calculated
    ("ConcentrationInWater", "lb/ft^3", "mg/l", 1, 16018.450433864),  # hand calculated
    # ("ConcentrationInWater", "mg/l", "lb/ft^3", 160184.50433864002, 1),  # hand calculated
    # ("ConcentrationInWater", "kg/m^3", "lb/ft^3", 16.018464, 1),  # hand calculated
    ("ConcentrationInwater", "mg/l", "ppm", 1.0, 1.0),  # calculated (and kindof defined)
    ("ConcentrationInwater", "mg/l", "ppb", 1.0, 1000),  # calculated
    ("ConcentrationInwater", "mg/kg", "ppb", 1.0, 1000),  # calculated
    ("ConcentrationInWater", "ppt", "percent", 1.0, .1),  # calculated
    ("ConcentrationInWater", "ug/l", "ppb", 1.0, 1.0),  # calculated
    ("ConcentrationInWater", "\N{MICRO SIGN}g/l", "ppb", 1.0, 1.0),  # calculated
    ("ConcentrationInWater", "ug/g", "ppm", 1.0, 1.0),  # calculated
    ("ConcentrationInWater", "mg/ml", "ppm", 1.0, 1000),  # calculated
    ("ConcentrationInWater", "mg/g", "ppt", 1.0, 1.0),  # calculated
    ("ConcentrationInWater", "nanogramperliter", "partpertrillion", 1.0, 1.0),  # calculated
    ("ConcentrationInWater", "g/m\N{SUPERSCRIPT THREE}", "ppm", 1.0, 1.0),  # calculated
    ("ConcentrationInWater", "g/l", "ppm", 1.0, 1000.0),  # calculated
    ("ConcentrationInWater", "kg/l", "part per thousand", 1.0, 1000.0),  # calculated

    ("Concentration", "fraction", "%", 1.0, 100.0),  # calculated
    ("Concentration", "percent", "\N{PER MILLE SIGN}", 1.0, 10.0),  # calculated
    ("Concentration", "\u2030", "ppm", 1.0, 1000.0),  # calculated
    ("Concentration", "ppm", "ppb", 1.0, 1000.0),  # calculated
    ("Concentration", "ppb", "part per trillion", 1.0, 1000.0),  # calculated
    ("Concentration", "parts per trillion", "1", 1.0, 1e-12),  # calculated

    ("Dimensionless", "fraction", "%", 1.0, 100.0),  # calculated
    ("Dimensionless", "percent", "\N{PER MILLE SIGN}", 1.0, 10.0),  # calculated


    ("MassFraction", "fraction", "%", 1, 100),  # calculated
    ("MassFraction", "\N{PER MILLE SIGN}", "percent", 1.0, .1),  # calculated
    ("MassFraction", "ppb", "ppm", 1000, 1),  # calculated
    ("MassFraction", "parts per trillion", "1", 1.0, 1e-12),  # calculated
    ("MassFraction", "g/kg", "fraction", 1.0, 1e-3),  # calculated
    ("MassFraction", "mg/g", "0/00", 1.0, 1.0),  # calculated
    ("MassFraction", "mg/kg", "ppb", 1.0, 1000),  # calculated
    ("MassFraction", "mg/kg", "fraction", 1.0, 1e-6),  # calculated
    ("MassFraction", "ug/g", "ppm", 1.0, 1.0),  # calculated
    ("MassFraction", "ng/g", "fraction", 1.0, 1e-9),  # calculated
    ("MassFraction", "ng/g", "ppb", 1.0, 1.0),  # calculated

    ("VolumeFraction", "fraction", "%", 1, 100),  # calculated
    ("VolumeFraction", "\u2030", "percent", 1.0, .1),  # calculated
    ("VolumeFraction", "ppb", "ppm", 1000, 1),  # calculated
    ("VolumeFraction", "parts per trillion", "1", 1.0, 1e-12),  # calculated
    ("VolumeFraction", "mL/L", "fraction", 1.0, 1e-3),  # calculated
    ("VolumeFraction", "L/m^3", "0/00", 1.0, 1.0),  # calculated

    ("Angular Measure", "degree", "radian", 180.0, math.pi),  # calculated
    ("Angular Measure", "radians", "degrees", 2 * math.pi, 360.0),  # calculated

    ("Angular Velocity", "1/s", "rad/s", 1.0, 1.0),  # definition
    ("Angular Velocity", "hz", "1/s", 5, 5 * 2 * math.pi),  # calculated
    ("Angular Velocity", "rpm", "1/s", 1, 2 * math.pi / 60),  # calculated

    ("Pressure", "Pa", "N/m^2", 1.0, 1.0),  # definition
    ("Pressure", "psi", "Pa", 5.0, 34473.8),  # from google
    ]


def test_new_api_oneshot():
    """
    just to make sure basic API works!

    and these are a few that have caused problems...
    """

    assert isclose(unit_conversion.convert('meter', 'foot', 1),
                   3.28083989501, rel_tol=RELTOL)

    assert isclose(unit_conversion.convert('API', 'SG', 10),
                   1, rel_tol=RELTOL)

    assert isclose(unit_conversion.convert('meter second-1', 'knot', 1),
                   1.94384, rel_tol=RELTOL)

    assert isclose(unit_conversion.convert('m/s', 'knot', 1), 1.94384, rel_tol=RELTOL)


@pytest.mark.parametrize('unit_type, unit1, unit2, value, new_value',
                         KnownValues)
def test_new_api(unit_type, unit1, unit2, value, new_value):
    """
    this is a parameterized test
    of all the known values, but with the new API
    """
    # filter out the ones that we know are eliminated
    if unit_conversion.Simplify(unit_type) in ('oilconcentration',
                                               'concentrationinwater',
                                               'massfraction',
                                               'volumefraction',
                                               'deltatemperature'):
        return
    # now do the test:
    assert isclose(unit_conversion.convert(unit1, unit2, value),
                   new_value, rel_tol=RELTOL)


@pytest.mark.parametrize('unit_type, unit1, unit2, value, new_value',
                         KnownValues)
def test_old_api(unit_type, unit1, unit2, value, new_value):
    """
    this is a parameterized test
    of all the known values, with the old API
    """
    # now do the test:
    assert isclose(unit_conversion.convert(unit_type, unit1, unit2, value),
                   new_value, rel_tol=RELTOL)


def test_ConverterClass_init_dupcheck():
    # "name1 is a duplicate -- should be caught"
    unit_dict = {"unit_1": (1.0, ["name1", "name2"]),
                 "unit_2": (3.141592653589793 / 180.0, ["name3", "name1"])
                 }

    with pytest.raises(ValueError):
        unit_conversion.ConverterClass("Random Unit Type", unit_dict)

# bad unit names
def test_bad_type_name():
    with pytest.raises(unit_conversion.InvalidUnitTypeError):
        unit_conversion.convert("BadType", "feet", "miles", 0)

def testBadUnit1():
    with pytest.raises(unit_conversion.InvalidUnitError):
        unit_conversion.convert("Length", "eggs", "miles", 0)

def testBadUnit2():
    with pytest.raises(unit_conversion.InvalidUnitError):
        unit_conversion.convert("Length", "feet", "spam", 0)

def testBadUnit3():
    with pytest.raises(unit_conversion.InvalidUnitError):
        unit_conversion.convert("Density", "API", "feet", 0)


class testOilQuantityConverterClass:
    OQC = unit_conversion.OilQuantityConverter

    def testMassToVolume1(self):
        assert isclose(self.OQC.ToVolume(Mass=1,
                                         MassUnits="metricton",
                                         Density=25,
                                         DensityUnits="API",
                                         VolumeUnits="bbl"),
                       6.9626324,
                       rel_tol=RELTOL)

    def testMassToVolume2(self):
        assert isclose(self.OQC.ToVolume(Mass=1,
                                         MassUnits="metricton",
                                         Density=0.816,
                                         DensityUnits="SG",
                                         VolumeUnits="bbl"),
                       7.71481307, rel_tol=RELTOL)

    def testVolumeToMass1(self):
        Expected = 1.0
        Calculated = self.OQC.ToMass(Volume=6.9626324,
                                     VolUnits="bbls",
                                     Density=25,
                                     DensityUnits="API",
                                     MassUnits="metricton")

        print(Expected, Calculated)
        assert isclose(Expected, Calculated, rel_tol=RELTOL)

    def testVolumeToMass2(self):
        Expected = 1.0
        Calculated = self.OQC.ToMass(Volume=7.83861191,
                                     VolUnits="bbls",
                                     Density=0.816,
                                     DensityUnits="SG",
                                     MassUnits="longton")

        assert isclose(Expected, Calculated, rel_tol=RELTOL)


# fixme: there should probably be a full set of tests for the "new" API
class TestNewConvertAPI():

    def test_bad_convert(self):
        with pytest.raises(unit_conversion.UnitConversionError):
            unit_conversion.convert("kg", "miles", 0)

    def test_invalid_unit(self):
        with pytest.raises(unit_conversion.InvalidUnitError):
            unit_conversion.convert("Mass", "kg", "miles", 0)

    @pytest.mark.parametrize('args',
                             [("kgt", "miles", 0),
                              ("kg", "miless", 0),
                              ("foo", "spam", 0),
                              (0, 0, 0),
                              ])
    def test_NotSupportedUnitError(self, args):
        with pytest.raises(unit_conversion.NotSupportedUnitError):
            unit_conversion.convert(*args)

    @pytest.mark.parametrize('args',
                             [("micron", "g/m^2", 1.0),
                              ])
    def test_invalid_combination(self, args):
        with pytest.raises(unit_conversion.UnitConversionError):
            unit_conversion.convert(*args)


def test_GetUnitTypes():
    # note: not testing all of them
    types = unit_conversion.GetUnitTypes()

    assert "Length" in types
    assert "Temperature" in types
    assert "Area" in types
    assert "Discharge" in types
    assert "Velocity" in types
    assert "Volume" in types


def test_GetUnitNames():
    # note: not testing all of them
    #       either all types or all names
    names = unit_conversion.GetUnitNames('Length')
    # print(names)

    assert "meter" in names
    assert "foot" in names
    assert "feet" not in names

    names = unit_conversion.GetUnitNames('Area')
    # print(names)

    assert "square foot" in names
    assert "acre" in names
    assert "square meter" in names
    assert "feet" not in names


def test_GetUnitAbbreviation():
    names = [('Length', 'meter', 'm'),
             ('Volume', 'cubic meter', 'm³'),
             ('Time', 'second', 's'),
             ('Velocity', 'kilometer per hour', 'km/h'),
             ('Discharge', 'cubic foot per second', 'ft³/s'),
             ]

    for unit_type, unit, abrv in names:
        print(unit_type, unit, abrv)
        assert abrv == unit_conversion.GetUnitAbbreviation(unit_type, unit)


def test_FindUnitTypes():
    # just testing that it's there and doesn't crash!
    all_units = unit_conversion.UNIT_TYPES

    assert all_units['s'] == 'time'
    assert all_units['sg'] == 'density'
    assert all_units['feet/s'] == 'velocity'
    assert all_units['m^2/s'] == 'kinematicviscosity'


def test_is_same_unit():
    # a few examples...not complete, but at least it's there and works
    # for some cases

    assert unit_conversion.is_same_unit('knot', 'knots')
    assert unit_conversion.is_same_unit('knot', 'kts')
    assert not unit_conversion.is_same_unit('knot', 'm/s')

    assert unit_conversion.is_same_unit("gal/s", "gal/sec")
    assert unit_conversion.is_same_unit("gallon per second", "gal/sec")

    # these should NOT be the same !
    assert not unit_conversion.is_same_unit("gallon per hour", "gal/sec")

    assert not unit_conversion.is_same_unit("meters", "gal/sec")

    assert not unit_conversion.is_same_unit("something non existant",
                                            "gal/sec")
    assert not unit_conversion.is_same_unit("meter", "meeters")
    assert not unit_conversion.is_same_unit("non_existant", "")


# test the Exceptions
def test_invalid_unit_convert():
    with pytest.raises(unit_conversion.InvalidUnitError):
        unit_conversion.convert("length", "flintstones", "meters", 1.0)

    with pytest.raises(unit_conversion.InvalidUnitError):
        unit_conversion.convert("length", "feet", "flintstones", 1.0)

    with pytest.raises(unit_conversion.InvalidUnitError):
        unit_conversion.convert("temperature", "feet", "C", 1.0)

    with pytest.raises(unit_conversion.InvalidUnitError):
        unit_conversion.convert("temperature", "f", "feet", 1.0)

    with pytest.raises(unit_conversion.InvalidUnitError):
        unit_conversion.convert("length", "feet", "C", 1.0)

    with pytest.raises(unit_conversion.InvalidUnitTypeError):
        unit_conversion.convert("something_wrong", "feet", "meters", 1.0)

    with pytest.raises(unit_conversion.InvalidUnitError):
        unit_conversion.convert("density", "kg/m^33", "g/cm^3", 1.0)


# these really jsut to get 100% coverage :-)
def test_is_supported():
    """not comprehensive...
    """
    assert unit_conversion.is_supported('foot')
    assert unit_conversion.is_supported('FoOt')
    assert unit_conversion.is_supported('meter second-1')
    assert not unit_conversion.is_supported('something random')


def test_NotSupportedUnitError():
    "just test the __str__..."
    err = str(unit_conversion.NotSupportedUnitError('feeet'))

    assert err == 'The unit: feeet is not supported or not recognized'


def test_InvalidUnitError():
    "just testing the __str__..."
    err = str(unit_conversion.InvalidUnitError(('feet', 'volume')))

    assert err == 'The unit: feet is not in the list for Unit Type: volume'


def test_InvalidUnitTypeError():
    "just test the __str__..."
    err = str(unit_conversion.InvalidUnitTypeError('feeet'))

    assert err == 'The unit type: feeet is not in the UnitConversion database'
