#!/usr/bin/env python

"""Unit conversion calculators.

CHANGELOG:
  2005/07/14 CB: Initial import.
  2005/07/15 MO: Latitude and Longitude classes.
  2005/07/18 MO: Limit Latitude range to 90.
  2007/05/03 CB: Tweaked lat-long to get correct answer for 40 minutes.
                 Added "convert" as alias for "Convert"
  2007/12/17 MO: Add .format() method to Latitude/Longitude returning Unicode.
                 .factor_html() remains for backward compatibility, using
                 .format() internally.
                 Make Latitude/Longitude.__repr__ more robust in case
                 .__init__ raises an exception; workaround for Pylons bug
                 http://pylonshq.com/project/pylonshq/ticket/341
  2008/02/22 CB: Added a few more units for Ian
  2008/06/05 CB: Various changes before putting the Converter GUI on the web: new units, changed, spelling, etc.
  2009/09/29 CB: Re-factored the lat-long stuff:
                 - it's not in a separate module
                 - Mike and Chris' code has been merged for less duplication
                 - Unit data moved to separate module
"""

from __future__ import unicode_literals, absolute_import

__version__ = "1.2.2"

from . import unit_data
import imp
imp.reload(unit_data)

from .unit_data import ConvertDataUnits
from .lat_long import (LatLongConverter, Latitude, Longitude,
                       DummyLatitude, DummyLongitude)  # Backward compatibility.

# A few utilities


def Simplify(String):
    """
    Simplify(String)

    returns the string with the whitespace and capitalization removed
    """
    return "".join(String.lower().split())


def GetUnitTypes():
    """
    returns a list of all the unit types available

    a unit type is something like "mass", "velocity", etc.
    """
    return ConvertDataUnits.keys()


def GetUnitNames(UnitType):
    """
    returns a list of all the units available for a given unit type available

    a unit type is something like "mass", "velocity", etc.

    a unit of mass would be "kilogram", "slug", etc.
    """
    return ConvertDataUnits[UnitType].keys()


def FindUnitTypes():
    """
    returns a mapping of all the unit names to the unit types

    raises an exception if there is more than one option -- this will check
    the unit database for duplicated names

    Usually not called from user code.
    """
    unit_types = {}
    for unit_type in ConvertDataUnits.keys():
        if unit_type == "Oil Concentration" or unit_type == "Concentration In Water":
            continue  # skipping Oil Concentration, 'cause this is really length -- lots of duplicate units!
            # skipping Concentration in water, cause this has lots of duplicate units
        for PrimaryName, data in ConvertDataUnits[unit_type].items():
            # strip out whitespace and capitalization
            #Pname = Simplify(PrimaryName)
            Pname = PrimaryName
            # add the primary name:
            unit_types[Pname] = unit_type
            # now the synonyms:
            for n in data[1]:
                if unit_type == "Volume" and n == 'oz':
                    continue  # skip, "oz" is only mass
                if n in unit_types:
                    raise ValueError("Duplicate name in units table: %s" % n)
                unit_types[n] = unit_type
    return unit_types


def GetUnitAbbreviation(unit_type, unit):
    """
    return the standard abbreviation for a given unit

    :param unit_type: the type of unit: "mass", "length", etc.
    :param unit: the unit you want the abbreviation for: "gram", etc.
    """
    return ConvertDataUnits[unit_type][unit][1][0]


def is_same_unit(unit1, unit2):
    """
    Checks if the two unit names passed in are the same

    :param unit1: name of unit to compare
    :type unit1: string

    :param unit2: name of unit to compare
    :type unit2: string

    :returns: True if they are synonyms for the same unit.
              False if they are different units.
              False if one of them is not in the database.

    """
    all_types = FindUnitTypes()
    try:
        type1 = all_types[unit1]
        type2 = all_types[unit2]
    except KeyError:
        return False
    if type1 != type2:
        return False
    else:
        Synonyms = Converters[Simplify(type1)].Synonyms
        return Synonyms[Simplify(unit1)] == Synonyms[Simplify(unit2)]


def is_valid_conversion(unit1, unit2):
    """
    Determines if the two units are of the same type and legal to convert

    :param unit1: name of unit to compare
    :type unit1: string

    :param unit2: name of unit to compare
    :type unit2: string

    :returns: True if they can be converted to one another
              False if they cannot
    """

    for s in unit_data.unit_sets.values():
        if unit1 in s and unit2 in s:
            return True
    return False


def get_unit_type(unit):
    """
    Gets the type of a unit

    :param unit: name of unit
    :type unit: string

    :returns: string name of unit's type
    """

    for name, s in unit_data.unit_sets.items():
        if unit in s:
            return name


class ConverterClass:
    """
    Main class for performing the conversion there will be one instance for each unit type

    sub-classes will handle special cases
    """

    def __init__(self, TypeName, UnitsDict):
        """
        Create a Converter

        :param TypeName: the name of the unit type, such as "length"
        :param UnitsDict: a dict will the unit data. See unit_data.py for format
        """
        self.Name = TypeName

        self.Synonyms = {}
        self.Convertdata = {}
        for PrimaryName, data in UnitsDict.items():
            # strip out whitespace and capitalization
            Pname = Simplify(PrimaryName)
            self.Convertdata[Pname] = data[0]
            self.Synonyms[Pname] = Pname
            for synonym in data[1]:
                self.Synonyms[Simplify(synonym)] = Pname

    def Convert(self, FromUnit, ToUnit, Value):
        """
        Convert(FromUnit, ToUnit, Value)

        returns a new value, in the units of ToUnit.

        :param FromUnit: the unit the original value is in
        :param ToUnit: the unit you want the value converted to
        :param Value: the original value
        """
        FromUnit = Simplify(FromUnit)
        ToUnit = Simplify(ToUnit)

        try:
            FromUnit = self.Synonyms[FromUnit]
        except KeyError:
            raise InvalidUnitError((FromUnit, self.Name))
        try:
            ToUnit = self.Synonyms[ToUnit]
        except KeyError:
            raise InvalidUnitError((ToUnit, self.Name))

        return Value * self.Convertdata[FromUnit] / self.Convertdata[ToUnit]

# the special case classes:


class TempConverterClass(ConverterClass):
    """
    Special case class for temperature conversion.

    handles the zero-offset shift for K, C, F...
    """

    def Convert(self, FromUnit, ToUnit, Value):
        """
        Convert(FromUnit, ToUnit, Value)

        returns a new value, in the units of ToUnit.

        :param FromUnit: the unit the original value is in
        :param ToUnit: the unit you want the value converted to
        :param Value: the original value
        """

        FromUnit = Simplify(FromUnit)
        ToUnit = Simplify(ToUnit)

        try:
            FromUnit = self.Synonyms[FromUnit]
        except KeyError:
            raise InvalidUnitError((FromUnit, self.Name))
        try:
            ToUnit = self.Synonyms[ToUnit]
        except KeyError:
            raise InvalidUnitError((ToUnit, self.Name))

        A1 = self.Convertdata[FromUnit][0]
        B1 = self.Convertdata[FromUnit][1]
        A2 = self.Convertdata[ToUnit][0]
        B2 = self.Convertdata[ToUnit][1]

        to_val = ((Value + B1) * A1 / A2) - B2

        return to_val


class DensityConverterClass(ConverterClass):
    """
    Special case class for Density conversion.

    handles the special case of API gravity, etc.
    """

    def Convert(self, FromUnit, ToUnit, Value):
        """
        Convert(FromUnit, ToUnit, Value)

        returns a new value, in the units of ToUnit.

        :param FromUnit: the unit the original value is in
        :param ToUnit: the unit you want the value converted to
        :param Value: the original value
        """

        FromUnit = Simplify(FromUnit)
        ToUnit = Simplify(ToUnit)

        try:
            FromUnit = self.Synonyms[FromUnit]
        except KeyError:
            raise InvalidUnitError((FromUnit, self.Name))
        try:
            ToUnit = self.Synonyms[ToUnit]
        except KeyError:
            raise InvalidUnitError((ToUnit, self.Name))
        if FromUnit == "apidegree":  # another Special case (could I do this the same as temp?)
            Value = 141.5 / (Value + 131.5)
            FromUnit = u"specificgravity(15\xb0c)"
        if ToUnit == "apidegree":
            ToVal = 141.5 / (Value * self.Convertdata[FromUnit] / self.Convertdata[u"specificgravity(15\xb0c)"]) - 131.5
        else:
            ToVal = Value * self.Convertdata[FromUnit] / self.Convertdata[ToUnit]
        return ToVal


class OilQuantityConverter:
    """
    class for Oil Quantity conversion -- mass to/from Volume

    requires density info as well
    """
    @classmethod
    def ToVolume(self, Mass, MassUnits, Density, DensityUnits, VolumeUnits):
        """
        Convert Oil Mass to Volume

        :param Mass: mass you want converted to volume
        :param MassUnits: unit of mass input
        :param Density: density of oil
        :param DensityUnits: units of density
        :param VolumeUnits: units of volume desired

        """
        Density = convert("Density", DensityUnits, "kg/m^3", Density)
        # print "Density in kg/m^3", Density
        Mass = convert("Mass", MassUnits, "kg", Mass)
        # print "Mass in kg", Mass
        Volume = Mass / Density
        # print "Volume in m^3", Volume
        Volume = convert("Volume", "m^3", VolumeUnits, Volume)
        # print "Volume in %s"%VolumeUnits, Volume
        return Volume

    @classmethod
    def ToMass(self, Volume, VolUnits, Density, DensityUnits, MassUnits):
        """
        Convert Oil Mass to Volume

        :param Volume: volume you want converted to mass
        :param VolumeUnits: units of volume input
        :param Density: density of oil
        :param DensityUnits: units of density
        :param MassUnits: unit of mass desired for output
        """

        Density = convert("Density", DensityUnits, "kg/m^3", Density)
        # print "Density in kg/m^3", Density
        Volume = convert("Volume", VolUnits, "m^3", Volume)
        # print "Volume in m^3", Volume
        Mass = Volume * Density
        # print "Mass in kg", Mass
        Mass = convert("Mass", "kg", MassUnits, Mass)
        # print "Mass in %s"%MassUnits, Mass
        return Mass

# create the converter objects
Converters = {}
for (unittype, data) in ConvertDataUnits.items():
    if unittype.lower() == 'temperature':
        Converters["temperature"] = TempConverterClass(unittype, data)
    elif unittype.lower() == 'density':
        Converters["density"] = DensityConverterClass(unittype, data)
    else:
        Converters[Simplify(unittype)] = ConverterClass(unittype, data)


def convert(UnitType=None, FromUnit=None, ToUnit=None, Value=None):
    """
    Convert(FromUnit, ToUnit, Value)

    returns a new value, in the units of ToUnit.

    :param FromUnit: the unit the original value is in
    :param ToUnit: the unit you want the value converted to
    :param Value: the original value
    """

    if UnitType is None:
        UnitType = get_unit_type(FromUnit)
    UnitType = Simplify(UnitType)
    try:
        Converter = Converters[UnitType]
    except:
        raise InvalidUnitTypeError(UnitType)
    return Converter.Convert(FromUnit, ToUnit, Value)

Convert = convert  # so to have the old, non-PEP8 compatible name

# This is used by TapInput


# The exceptions
class UnitConversionError(Exception):
    """
    Exception type for unit conversion errors

    perhaps this should be subclassed more, but at the moment, It doesn't do anything special

    """
    pass


class InvalidUnitError(UnitConversionError):
    """
    Exception raised when a unit is not in the Unit conversion database

    """

    def __init__(self, unit_unit_type):
        (unit, unit_type) = unit_unit_type
        self.unit = unit
        self.type = unit_type if unit_type else ""

    def __str__(self):
        return "The unit: %s is not in the list for Unit Type: %s" % (self.unit, self.type)


class InvalidUnitTypeError(UnitConversionError):
    """
    Exception raised when a unit is not in the Unitconversion database

    """

    def __init__(self, unitType):
        self.unitType = unitType

    def __str__(self):
        return "The unit type: %s is not in the UnitConversion database" % self.unitType


class MismatchedUnitError(UnitConversionError):
    """
    Exception raised when a unit is not in the Unitconversion database

    """
    # fixme -- this appear to be used anywhere...

    def __init__(self, FromUnit_FromUnitType_ToUnit_ToUnitType):
        (FromUnit, FromUnitType, ToUnit, ToUnitType) = \
            FromUnit_FromUnitType_ToUnit_ToUnitType
        self.FromUnit = FromUnit
        self.FromUnitType = FromUnitType
        self.ToUnit = ToUnit
        self.ToUnitType = ToUnitType

    def __str__(self):
        return "The unit: %s of  type %s is not compatible with %s of type %s" % \
               (self.FromUnit, self.FromUnitType, self.ToUnit, self.ToUnitType)
