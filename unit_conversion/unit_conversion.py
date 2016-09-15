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
import warnings

from .unit_data import ConvertDataUnits

from .lat_long import (LatLongConverter,
                       Latitude,
                       Longitude,
                       DummyLatitude,
                       DummyLongitude)  # Backward compatibility.

__version__ = "2.5.3"


# A few utilities
def Simplify(string):
    """
    Simplify(string)

    returns the string with the whitespace and capitalization removed
    """
    try:
        return "".join(string.lower().split())
    except AttributeError:
        raise NotSupportedUnitError(string)


def GetUnitTypes():
    """
    returns a list of all the unit types available

    a unit type is something like "mass", "velocity", etc.
    """
    return ConvertDataUnits.keys()


def GetUnitNames(UnitType):
    """
    returns a list of all the units available for a given unit type available

    a unit type is something like "Mass", "Velocity", etc.

    a unit of mass would be "kilogram", "slug", etc.
    """
    UnitType.capitalize()
    return ConvertDataUnits[UnitType].keys()


def FindUnitTypes():
    """
    returns a mapping of all the unit names to the unit types

    raises an exception if there is more than one option -- this will check
    the unit database for duplicated names

    Usually not called from user code.
    """
    unit_types = {}
    for unit_type, unit_data in ConvertDataUnits.items():
        unit_type = Simplify(unit_type)
        if unit_type == "oilconcentration" or unit_type == "concentrationinwater":
            continue  # skipping Oil Concentration, 'cause this is really length
                      # -- lots of duplicate units!
                      # skipping Concentration in water, cause it's weird
        for pname, data in unit_data.items():
            # strip out whitespace and capitalization
            pname = Simplify(pname)
            # add the primary name:
            unit_types[pname] = unit_type
            # now the synonyms:
            for n in data[1]:
                n = Simplify(n)
                if (unit_type, n) in [("volume", "oz"),
                                      ("density", "s")]:
                    continue  # skip, "oz" is only mass, "s" is only time
                if n in unit_types:
                    raise ValueError("Duplicate name in units table: %s" % n)
                unit_types[n] = unit_type
    return unit_types

UNIT_TYPES = FindUnitTypes()


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
    all_types = UNIT_TYPES
    unit1 = Simplify(unit1)
    unit2 = Simplify(unit2)
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
            raise InvalidUnitError( (FromUnit, self.Name) )
        try:
            ToUnit = self.Synonyms[ToUnit]
        except KeyError:
            raise InvalidUnitError( (ToUnit, self.Name) )
        if FromUnit == "apidegree": # another Special case (could I do this the same as temp?)
            Value = 141.5/(Value + 131.5)
            FromUnit = u"specificgravity(15\xb0c)"
        if ToUnit == "apidegree":
            ToVal = 141.5/(Value * self.Convertdata[FromUnit] / self.Convertdata[u"specificgravity(15\xb0c)"] ) - 131.5
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
        Mass = convert("Mass", MassUnits, "kg", Mass)
        Volume = Mass / Density
        Volume = convert("Volume", "m^3", VolumeUnits, Volume)
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
        Volume = convert("Volume", VolUnits, "m^3", Volume)
        Mass = Volume * Density
        Mass = convert("Mass", "kg", MassUnits, Mass)
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


def is_supported(unit):
    """
    Returns True is the unit is in teh list of supported units for the
    API that does not require unit_type
    """
    return Simplify(unit) in UNIT_TYPES


def convert(unit1, unit2, value, unit_type=None):
    """
    convert(unit1, unit2, value, unit_type)

    :param unit1: the unit the original value is in
    :param unit2: the unit you want the value converted to
    :param value: the original value

    if unit_type is None, then it will look in the data to see if it can figure out what
    unit type to use.

    so you should be able to do:

    convert(unit1='meter', unit2='feet', value=32)

    NOTE: some odd units have overlapping names, so only the more common one is used
          (oz is mass, not fluid oz, for instance). You can get around this by using
          a more precise name ('fluid oz') or specify the unit type.

    If you do want to specify the unit type, you can use the "old" API:

      convert(unit_type, unit1, unit2, value)

    such as:

      convert('volume', 'oz', 'cc', 25)

    :param unit_type: the type of the unit: 'mass', 'length', etc.
    :param unit1: the unit the original value is in
    :param unit2: the unit you want the value converted to
    :param value: the original value
    """

    # the new API: no need to specify unit type
    if unit_type is None:
        unit1, unit2 = (Simplify(s) for s in (unit1, unit2))
        try:
            unit_type = UNIT_TYPES[unit1]
        except KeyError:
            raise NotSupportedUnitError(unit1)
        try:
            unit_type2 = UNIT_TYPES[unit2]
        except KeyError:
            raise NotSupportedUnitError(unit2)
        if unit_type != unit_type2:
            raise UnitConversionError("Cannot convert {0} to {1}".format(unit1, unit2))
        unit_type = Simplify(unit_type)
    # the old API: specify the unit type
    else:
        # re-defining the inputs:
        unit_type, unit1, unit2, value = unit1, unit2, value, unit_type
        unit_type, unit1, unit2 = (Simplify(s) for s in (unit_type, unit1, unit2))
    try:
        Converter = Converters[unit_type]
    except KeyError:
        raise InvalidUnitTypeError(unit_type)
    return Converter.Convert(unit1, unit2, value)


# so as to have the old, non-PEP8 compatible name
# This is used by TapInput (any more???)
def Convert(*args, **kwargs):
    """
    so as to have the old, non-PEP8 compatible name
    This is used by TapInput (any more???)

    for new code, use convert()
    """
    warnings.warn('"Convert" is deprecated -- use "convert()"', DeprecationWarning)
    return convert(*args, **kwargs)


# fixme: we should probably simjply get rid of these and use ValueError
class UnitConversionError(ValueError):
    """
    Exception type for unit conversion errors

    perhaps this should be subclassed more, but at the moment, It doesn't do anything special

    """
    pass


class NotSupportedUnitError(UnitConversionError):

    def __init__(self, unit):
        self.unit = unit

    def __str__(self):
        return "The unit: %s is not supported or not recognized" % (self.unit)


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
