#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit conversion calculators.

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
  2008/06/05 CB: Various changes before putting the Converter GUI on the web:
                 new units, changed spelling, etc.
  2009/09/29 CB: Re-factored the lat-long stuff:
                 - it's not in a separate module
                 - Mike and Chris' code has been merged for less duplication
                 - Unit data moved to separate module
  2018/01/24 CB: Added unicode exponents in unit names
                 Added __all__
                 Fixed concentration in water units!
"""

import warnings

from .unit_data import ConvertDataUnits

from nucos import lat_long

from .lat_long import (LatLongConverter,
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

# reset this to get some more print statements on import
DEBUG = False

# A few utilities
def Simplify(string):
    """
    Simplify(string)

    returns the string with the whitespace and capitalization removed
    """
    # This should perhaps be made smarter -- but what to do with whitespace?
    # "m / s" -- "m/s"
    # "meters-1" "meter s-1"

    try:
        return "".join(string.lower().split()).replace(".", "")
    except AttributeError:
        raise NotSupportedUnitError(string)


def GetUnitTypes():
    """
    returns a list of all the unit types available

    a unit type is something like "mass", "velocity", etc.
    """
    return list(ConvertDataUnits.keys())


def get_unit_type(unit):
    """
    Return the unit type for a given unit name.

    Note that this will only work for unambiguous units

    :param unit: the unit you want the type of
    :type unit: str

    In [2]: nucos.get_unit_type('meter')
    Out[2]: 'length'
    """
    unit = Simplify(unit)

    try:
        unit_type = UNIT_TYPES[unit]
    except KeyError:
        raise NotSupportedUnitError(unit)
    return unit_type


def get_unit_types():
    return list(PRETTY_UNIT_TYPES.values())


def GetUnitNames(UnitType):
    """
    returns a list of all the units available for a given unit type available

    a unit type is something like "Mass", "Velocity", etc.

    a unit of mass would be "kilogram", "slug", etc.
    """
    return list(ConvertDataUnits[UnitType.title()].keys())



def FindUnitTypes():
    """
    Returns a mapping of all the unit names to the unit types

    Raises an exception if there is more than one option -- this will check
    the unit database for duplicated names

    Primarily used to do conversions without specifying the unit types

    Usually not called from user code.
    """

    # compute units that are unique to Mass and Volume Fraction
    mf = ConvertDataUnits["Mass Fraction"]
    vf = ConvertDataUnits["Volume Fraction"]
    # not_to_skip = {Simplify(u) for u in mf.keys() ^ vf.keys()}
    to_skip = {Simplify(u) for u in mf.keys() & vf.keys()}

    unit_types = {}

    for unit_type, unit_data in ConvertDataUnits.items():
        unit_type = Simplify(unit_type)

        # - skipping Oil Concentration, 'cause this is really length
        #   - lots of duplicate units!
        # - skipping Concentration in water, 'cause it's weird
        #   - mass/volume and mass/mass !
        # - skipping Mass Fraction, because there are lots of duplicate units
        #   that conflict with Concentration & Concentration In Water.
        if unit_type in ('oilconcentration',
                         'concentrationinwater',
                         #'massfraction',
                         #'volumefraction',
                         'deltatemperature',
                         'dimensionless',
                         ):
            continue

        for pname, data in unit_data.items():
            # strip out whitespace and capitalization
            pname = Simplify(pname)

            if (unit_type in {'massfraction', 'volumefraction'}
                    and pname in to_skip):
                continue

            # add the primary name:
            if pname in unit_types:
                raise ValueError(f"Duplicate primary name in units table: {pname}")
            unit_types[pname] = unit_type
            # now the synonyms:
            for n in data[1]:
                n = Simplify(n)

                # skip duplicate units, "oz" is only mass, "s" is only time
                if (unit_type, n) in [("volume", "oz"),
                                      ("density", "s")]:
                    continue
                if DEBUG:
                    try:
                        print(f"Adding: {unit_type}: {n}")
                    except UnicodeEncodeError:
                        print(f"Adding: {unit_type}: {n}".encode("utf-8"))
                if n in unit_types:
                    raise ValueError("Duplicate name in units table: %s" % n)

                unit_types[n] = unit_type

    return unit_types


def FindAllUnitNames():
    """
    returns a mapping of all the valid unit names to unit type

    Usually not called from user code.
    """
    unit_names = {}

    for unit_type, unit_data in ConvertDataUnits.items():
        unit_type = Simplify(unit_type)

        for pname, data in unit_data.items():
            # add the primary name:
            if DEBUG:
                print("adding:", pname)
            unit_names.setdefault(unit_type, []).append(pname)
            # now the synonyms:
            unit_names[unit_type].extend(data[1])
    return unit_names


UNIT_TYPES = FindUnitTypes()
UNIT_NAMES = FindAllUnitNames()
PRETTY_UNIT_TYPES = {Simplify(unit_type): unit_type for unit_type in ConvertDataUnits.keys()}


def is_supported_unit(unit_type, unit):
    """
    checks if a unit name is supported for the given unit type
    """
    unit_type = Simplify(unit_type)
    converter = Converters[unit_type]
    return Simplify(unit) in converter.Synonyms


def get_supported_names(unit_type):
    """
    Returns the list of all supported unit names for a unit_type
    """
    return UNIT_NAMES[Simplify(unit_type)]

def get_primary_name(unit, unit_type=None):
    """
    Returns the primary name for a given unit.

    This is usually the spelled out version, e.g.
    kilogram
    """
    unit = Simplify(unit)
    if unit_type is None:
        unit_type = UNIT_TYPES[unit]
    else:
        unit_type = Simplify(unit_type)
    return Converters[unit_type].GetPrimaryName(unit)

def get_primary_names(unit_type):
    """
    return the primary names of all the units supported for a given unit type
    """
    p_names = []

    unit_type = Simplify(unit_type)
    unit_type = PRETTY_UNIT_TYPES[unit_type]
    unit_data = ConvertDataUnits[unit_type]
    for pname, data in unit_data.items():
        p_names.append(pname)

    return p_names


def get_abbreviation(unit, unit_type=None):
    """
    return the standard abbreviated form for a given unit

    :param unit: name of the unit
    :type unit: str

    :param unit=None: Unit type -- helpful if the unit name conflicts,
                      e.g. oz: weight or volume?
    :type unit: str
    """
    unit = Simplify(unit)
    if unit_type is None:
        unit_type = UNIT_TYPES[unit]
    else:
        unit_type = Simplify(unit_type)

    unit_type = PRETTY_UNIT_TYPES[unit_type]
    unit = get_primary_name(unit, unit_type)
    synonyms = ConvertDataUnits[unit_type][unit][1]
    try:
        return synonyms[0]
    except IndexError:
        # If there are no synonyms, return the primary name
        return unit


def GetUnitAbbreviation(unit_type, unit):
    """
    return the standard abbreviation for a given unit

    :param unit_type: the type of unit: "mass", "length", etc.
    :param unit: the unit you want the abbreviation for: "gram", etc.
    """
    warnings.warn('`GetUnitAbbreviation` is deprecated -- use `get_abbreviation`', DeprecationWarning)
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
    Main class for performing the conversion.
    There will be one instance for each unit type.

    sub-classes will handle special cases
    """
    def __init__(self, TypeName, UnitsDict):
        """
        Create a Converter

        :param TypeName: the name of the unit type, such as "length"
        :param UnitsDict: A dict will the unit data.
                          See unit_data.py for format
        """
        self.Name = TypeName

        self.Synonyms = {}
        self.Convertdata = {}
        self.PrettyNames = {}

        for PrimaryName, data in UnitsDict.items():
            # strip out whitespace and capitalization
            Pname = Simplify(PrimaryName)
            self.PrettyNames[Pname] = PrimaryName

            self.Convertdata[Pname] = data[0]
            self.Synonyms[Pname] = Pname

            for synonym in data[1]:
                # duplicate check
                if synonym in self.Synonyms:
                    raise ValueError("Duplicate synonym: "
                                     "unit_type: {}, name: {}".format(TypeName,
                                                                      synonym)
                                     )
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

    def GetPrimaryName(self, unit):
        return self.PrettyNames[self.Synonyms[Simplify(unit)]]


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
#        breakpoint()
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

        if FromUnit == "apidegree":
            # another Special case (could I do this the same as temp?)
            Value = 141.5 / (Value + 131.5)
            FromUnit = u"specificgravity(15\xb0c)"

        if ToUnit == "apidegree":
            ToVal = (141.5 /
                     (Value * self.Convertdata[FromUnit] /
                      self.Convertdata[u"specificgravity(15\xb0c)"]) -
                     131.5)
        else:
            ToVal = (Value *
                     self.Convertdata[FromUnit] /
                     self.Convertdata[ToUnit])

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
    Returns True is the unit is in the list of supported units for the
    API that does not require unit_type
    """
    return Simplify(unit) in UNIT_TYPES


def convert(unit1, unit2, value, unit_type=None):
    """
    convert(unit1, unit2, value, unit_type)

    :param unit1: the unit the original value is in
    :param unit2: the unit you want the value converted to
    :param value: the original value

    If unit_type is None, then it will look in the data
    to see if it can figure out what unit type to use.

    so you should be able to do:

    convert(unit1='meter', unit2='feet', value=32)

    NOTE: Some odd units have overlapping names, so only the more common one
          is used (oz is mass, not fluid oz, for instance).
          You can get around this by using a more precise name ('fluid oz')
          or specify the unit type.

    If you do want to specify the unit type, you can use the "old" API:

      convert(unit_type, unit1, unit2, value)

    such as:

      convert('volume', 'oz', 'cc', 25)

    :param unit_type: the type of the unit: 'mass', 'length', etc.
    :param unit1: the unit the original value is in
    :param unit2: the unit you want the value converted to
    :param value: the original value
    """
    if unit_type is None:
        # the new API: no need to specify unit type
        unit1, unit2 = (Simplify(s) for s in (unit1, unit2))

        try:
            unit_type = UNIT_TYPES[unit1]
        except KeyError:
            raise NotSupportedUnitError(unit1)

        # try:
        #     unit_type2 = UNIT_TYPES[unit2]
        # except KeyError:
        #     raise NotSupportedUnitError(unit2)

        # if unit_type != unit_type2:
        #     raise UnitConversionError("Cannot convert {0} to {1}"
        #                               .format(unit1, unit2))

        unit_type = Simplify(unit_type)
    else:
        # the old API: specify the unit type
        # re-defining the inputs:
        unit_type, unit1, unit2, value = unit1, unit2, value, unit_type
        unit_type, unit1, unit2 = (Simplify(s)
                                   for s in (unit_type, unit1, unit2))

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
    warnings.warn('"Convert()" is deprecated -- use "convert()"',
                  DeprecationWarning)

    return convert(*args, **kwargs)


# fixme: we should probably simjply get rid of these and use ValueError
class UnitConversionError(ValueError):
    """
    Exception type for unit conversion errors

    Perhaps this should be subclassed more, but at the moment,
    it doesn't do anything special
    """
    pass


class NotSupportedUnitError(UnitConversionError):
    def __init__(self, unit):
        self.unit = unit

    def __str__(self):
        return ('The unit: {} is not supported or not recognized'
                .format(self.unit))


class InvalidUnitError(UnitConversionError):
    """
    Exception raised when a unit is not in the Unit conversion database
    """
    def __init__(self, unit_unit_type):
        if isinstance(unit_unit_type, (list, tuple)):
            (unit, unit_type) = unit_unit_type[:2]

            self.unit = unit
            self.type = unit_type if unit_type else ""
        else:
            super(InvalidUnitError, self).__init__(unit_unit_type)

    def __str__(self):
        if hasattr(self, 'unit'):
            return ('The unit: {} is not in the list for Unit Type: {}'
                    .format(self.unit, self.type))
        else:
            return super(InvalidUnitError, self).__str__()


class InvalidUnitTypeError(UnitConversionError):
    """
    Exception raised when a unit is not in the Unitconversion database
    """
    def __init__(self, unitType):
        self.unitType = unitType

    def __str__(self):
        return ('The unit type: {} is not in the UnitConversion database'
                .format(self.unitType))
