#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
unit_data.py

This is the data used by unit_conversion

it also includes a utility function for dumping the units to the console
or a file:
   write_units(filename=None)
"""
from __future__ import unicode_literals, absolute_import
import itertools

ConvertDataUnits = {
    # All lengths in terms of meter
    # All conversion factors from "Handbook of Chemistry and Physics" (HCP)
    # except where noted.

    "Length": {"meter": (1.0, ["m", "meters", "metre"]),
               "centimeter": (0.01, ["cm", "centimeters"]),
               "millimeter": (0.001, ["mm", "millimeters"]),
               "micron": (0.000001, ["\N{MICRO SIGN}m", "micrometer", "microns"]),
               "kilometer": (1000.0, ["km", "kilometers"]),
               "foot": (0.3048, ["ft", "feet"]),
               "inch": (0.0254, ["in", "inches"]),
               "yard": (0.9144, ["yrd", "yards"]),
               "mile": (1609.344, ["mi", "miles"]),
               "nautical mile": (1852.0, ["nm", "nauticalmiles"]),
               "fathom": (1.8288, ["fthm", "fathoms"]),
               "latitude degree": (111120.0, ["latitudedegrees"]),
               "latitude minute": (1852.0, ["latitudeminutes"])
               },

    # this is technically length but used differently, so I'm keeping it
    # separate.
    # micron is the base unit
    "Oil Concentration": {
        "micron": (1.0, ["\N{MICRO SIGN}m", "microns", "micrometer"]),
        "cubic meter per square kilometer": (1.0, ["m\N{SUPERSCRIPT THREE}/km\N{SUPERSCRIPT TWO}", "m^3/km^2"]),
        "millimeter": (1000., ["mm", "millimeters"]),
        "inch": (25400., ["in", "inches"]),
        "barrel per acre": (39.2866176, ["bbl/acre"]),  # calculated from HCP
        "barrel per square mile": (0.06138533995, ["bbl/mile\N{SUPERSCRIPT TWO}",
                                                   "bbl/sq.mile"]),  # calculated from HCP
        "gallon per acre": (0.93539563202687404, ["gal/acre", ]),  # calculated from HCP
        "liter per hectare": (0.1, ["liter/hectare", "l/hectare"]),  # calculated from HCP
        "liter per square meter": (1000.0, ["l/m\N{SUPERSCRIPT TWO}", "l/m^2"]),
        # these are mass/area -- so technically different.
        # but hard coding density of 0.95 -- so we can do it easily.
        "gram per square meter": (1.0526315789473684, ["g/m\N{SUPERSCRIPT TWO}", "g/m^2"]),
        "kilogram per square meter": (1052.6315789473684, ["kg/m\N{SUPERSCRIPT TWO}", "kg/m^2"]),
        "kilogram per square kilometer": (.0010526315789473684, ["g/km\N{SUPERSCRIPT TWO}", "kg/km^2" ]),
    },

    # All Areas in terms of square meter
    "Area": {
        "square meter": (1.0, ["m\N{SUPERSCRIPT TWO}", "m^2", "sq m"]),
        "square centimeter": (.0001, ["cm\N{SUPERSCRIPT TWO}", "cm^2", "sq cm"]),
        "square kilometer": (1e6, ["km\N{SUPERSCRIPT TWO}", "km^2", "sq km"]),
        "acre": (4046.8564, ["ac", "acres"]),
        "square mile": (2589988.1, ["sq miles"]),
        "square nautical mile": (3429904, ["nm\N{SUPERSCRIPT TWO}",
                                           "sq nm", "nm^2"]),
        "square yard": (0.83612736, ["yd\N{SUPERSCRIPT TWO}",
                                     "sq yards", "square yards"]),
        "square foot": (0.09290304, ["ft\N{SUPERSCRIPT TWO}", "ft^2",
                                     "sq foot", "square feet"]),
        "square inch": (0.00064516, ["in\N{SUPERSCRIPT TWO}", "in^2",
                                     "sq inch", "square inches"]),
        "hectare": (10000.0, ["hectares", "ha"]),
    },

    # All volumes in terms of cubic meter
    "Volume": {
        "cubic meter": (1.0, ["m\N{SUPERSCRIPT THREE}", "m^3", "cu m", "cubic meters"]),
        "cubic kilometer": (1e9, ["km\N{SUPERSCRIPT THREE}", "km^3", "cu km", "cubic kilometers"]),
        "cubic centimeter": (1e-6, ["cm\N{SUPERSCRIPT THREE}", "cm^3", "cu cm", "cc"]),
        "milliliter": (1e-6, ["ml", "milliters"]),
        "barrel (petroleum)": (.1589873, ["bbl", "barrels", "barrel", "bbls"]),
        "liter": (1e-3, ["l", "liters"]),
        "gallon": (0.0037854118, ["gal", "gallons", "usgal"]),
        "gallon (UK)": (0.004546090, ["ukgal", "gallons(uk)"]),
        "million US gallon": (3785.4118, ["milliongallons", "milgal"]),
        "cubic foot": (0.028316847, ["ft\N{SUPERSCRIPT THREE}", "ft^3", "cu feet", "cubicfeet"]),
        "cubic inch": (16.387064e-6, ["in\N{SUPERSCRIPT THREE}", "in^3", "cu inch", "cubicinches"]),
        "cubic yard": (.76455486, ["yd\N{SUPERSCRIPT THREE}", "yd^3", "cu yard", "cubicyards"]),
        "fluid ounce": (2.9573530e-5, ["oz", "ounces(fluid)", "fluid oz"]),
        "fluid ounce (UK)": (2.841306e-5, ["ukoz", "fluid oz(uk)"]),
    },

    # All Temperature units in K (multiply by, add)
    "Temperature": {
        "Kelvin": ((1.0, 0.0), ["K", "degrees k", "degree k", "degrees kelvin",
                                "degree kelvin", "deg k"]),
        "Celsius": ((1.0, 273.15), ["C", "degrees c", "degrees celsius",
                                    "deg c", "centigrade"]),
        "Fahrenheit": ((0.55555555555555558, (273.15 * (9. / 5.) - 32.0)),
                       ["F", "degrees f", "degree f", "degrees fahrenheit",
                        "deg f"]),
    },

    # All Temperature units in K (C)
    # This for temperature differences, where you don't want to reset the
    # zero point
    "Delta Temperature": {
        "Kelvin": (1.0, ["K", "degrees k", "degree k", "degrees kelvin",
                         "degree kelvin", "deg k"]),
        "Celsius": (1.0, ["C", "degrees c", "degrees celsius", "deg c",
                          "centigrade"]),
        "Fahrenheit": ((5.0 / 9.0), ["F", "degrees f", "degree f", "deg f",
                                     "degrees fahrenheit"]),
    },


    # All Mass units in Kg (weight is taken to be mass at standard g)
    "Mass": {"kilogram": (1.0, ["kg", "kilograms"]),
             "pound": (0.45359237, ["lb", "pounds", "lbs"]),
             "gram": (.001, ["g", "grams"]),
             "milligram": (.000001, ["mg"]),
             "microgram": (.000000001, ["\N{MICRO SIGN}g", "ug"]),
             "ton": (907.18474, ["tons", "uston"]),
             "metric ton (tonne)": (1000.0, ["tonnes", "metric ton",
                                             "metric tons", "mt"]),
             "slug": (14.5939, ["slugs"]),
             "ounce": (.028349523, ["oz", "ounces"]),
             "ton (UK)": (1016.0469, ["ukton", "long ton"]),
             },

    # All Time In second
    "Time": {"second": (1.0, ["s", "sec", "seconds"]),
             "minute": (60.0, ["min", "minutes"]),
             "hour": (3600.0, ["hr", "hours", "hrs"]),
             "day": (86400.0, ["days"]),
             },

    # All Velocities in meter per second
    "Velocity": {"meter per second": (1.0, ["m/s", "meters per second", "mps",
                                            "meter second-1", "meters s-1",
                                            "m s-1", "meter/sec"]),
                 "centimeter per second": (.01, ["cm/s"]),
                 "meter per minute": (0.01666666666, ["m/min",
                                                      "meters per minute"]),
                 "kilometer per hour": (0.277777, ["km/h", "km/hr"]),
                 "kilometer per day": (0.0115740416666666, ["km/day", "km/d"]),
                 "knot": (0.514444, ["kts", "knots"]),
                 "mile per hour": (0.44704, ["mph", "miles per hour"]),

                 "foot per second": (0.3048, ["ft/s", "ft/sec",
                                              "feet per second", "feet/s"]),
                 "foot per minute": (0.00508, ["ft/min", "feet per minute",
                                               "feet/min"]),
                 "foot per hour": (0.000084666, ["ft/hr", "feet per hour",
                                                 "feet/hour"]),
                 },

    # All Discharges in cubic meter per second
    "Discharge": {
        "cubic meter per second": (1.0, ["m\N{SUPERSCRIPT THREE}/s", "m^3/s", "cu m/s", "cms"]),
        "cubic meter per min": (1.0 / 60., ["m\N{SUPERSCRIPT THREE}/min", "m^3/min"]),
        "cubic meter per hour": (1.0 / 3600.0, ["m\N{SUPERSCRIPT THREE}/hr", "m^3/hr"]),
        "liter per second": (0.001, ["l/s", "lps"]),
        "liter per minute": (0.001 / 60, ["l/min", ]),
        "cubic foot per second": (.02831685, ["ft\N{SUPERSCRIPT THREE}/s", "cfs", "cu feet/s", "feet^3/s"]),
        "cubic foot per minute": (0.00047194744, ["ft\N{SUPERSCRIPT THREE}/min", "ft^3/min"]),  # calculated from cm^3/s
        "gallon per day": (4.3812636805555563e-08, ["gal/day"]),  # calculated from gal/hr
        "gallon per hour": (1.0515032833333335e-06, ["gal/hr"]),
        "gallon per minute": (6.3090197000000006e-05, ["gal/min", "gpm"]),
        "gallon per second": (0.0037854118, ["gal/s", "gal/sec"]),
        "barrel per hour": (4.4163138888888885e-05, ["bbl/hr"]),
        "barrel per day": (1.84013078e-06, ["bbl/day", "bbl/d"]),  # calculated from bbl/hr
    },

    # All Mass Discharges in kilogram per second
    "Mass Discharge": {
        "kilogram per second": (1.0, ["kg/s"]),
        "gram per second": (0.001, ["g/s"]),
    },


    # Density in g/cc
    # NOTE: Specific Gravity can only be defined for a given
    #       reference temperature.
    #       The most common standard in the oil industry is 15C (or 60F). The
    #       following is based on the value for the Density of water at 15C
    #       (CRC Handbook of Chemistry and Physics)
    "Density": {
        "gram per cubic centimeter": (1.0, ["g/cm\N{SUPERSCRIPT THREE}", "g/cm^3", "grams per cubic centimeter"]),
        "gram per liter": (.001, ["g/L", "gram per litre"]),
        "kilogram per liter": (1.0, ["kg/L", "kilogram per litre"]),
        "gram per milliliter": (1.0, ["g/mL",
                                      "gram per millilitre"]),
        "specific gravity (15\xb0C)": (0.999016, ["S", "specificgravity",  # ASTM D1250
        # "specific gravity (15\xb0C)": (0.99913, ["S", "specificgravity",
                                                 "Spec grav", "SG",
                                                 "specificgravity(15C)"]),
        "kilogram per cubic meter": (.001, ["kg/m\N{SUPERSCRIPT THREE}", "kg/m^3"]),
        "tonne per cubic meter": (1.0, ["tonne/m\N{SUPERSCRIPT THREE}", "tonne/m^3",
                                        "t/m^3", "t/m\N{SUPERSCRIPT THREE}"]),
        "pound per cubic foot": (0.016018463, ["lb/ft\N{SUPERSCRIPT THREE}", "lbs/ft^3", "lb/ft^3"]),
        "pound per gallon": (0.11982643, ["lbs/gal", "lb/gal"]),
        "API degree": (1, ["api"]),  # this is special cased in the code.
    },

    # Kinematic Viscosity in Stokes
    # NOTE: there is a more detailed way to do this, specified in:
    # ASTM D 2161 Standard Practice for Conversion of Kinematic Viscosity to
    # Saybolt Universal Viscosity or to Saybolt Furol Viscosity
    # for the moment, this will only handle approximation for SFS and SUS
    "Kinematic Viscosity": {
        "Stoke": (1.0, ["St", "stokes"]),
        "centiStoke": (.01, ["cSt", "centistokes"]),
        "square millimeter per second": (.01, ["mm\N{SUPERSCRIPT TWO}/s", "mm^2/s"]),
        "square centimeter per second": (1.0, ["cm\N{SUPERSCRIPT TWO}/s",
                                               "cm^2/s"]),
        "square meter per second": (10000, ["m\N{SUPERSCRIPT TWO}/s", "m^2/s"]),
        "square inch per second": (6.4516, ["in\N{SUPERSCRIPT TWO}/s", "in^2/s", "squareinchespersecond"]),
        # from CRC - only good for > 100cSt
        "Saybolt Universal Second": (1 / 462.0, ["SSU", "SUS"]),
        # from Fuel Oil Manual: good for 724cSt
        "Saybolt Furol Second": (0.02116959064, ["SSF", "SFS"]),
    },

    # Dynamic Viscosity
    "Dynamic Viscosity": {
        "kilogram per meter per second": (1.0, ["kg/(m s)"]),
        "Pascal second": (1.0, ["Pa s"]),
        "milliPascal second": (0.001, ["mPa s"]),
        "Newton seconds per square meter": (1.0, ["N s/m\N{SUPERSCRIPT TWO}",
                                                  "N s/m^2",
                                                  ]),

        "gram per centimeter per second": (0.1, ["g/(cm s)"]),
        "poise": (0.1, ["p"]),
        "dyne seconds per square centimeter": (0.1, ["dyne s/cm\N{SUPERSCRIPT TWO}",
                                                     "dyne s/cm^2",
                                                     ]
                                               ),

        "centipoise": (0.001, ["cP"]),
    },

    # Interfacial Tension
    # This is quantified as a force/length measurement in most cases, but a
    # couple exceptions quantify in ergs/area.  An erg is an amount of work,
    # not force, but the conversion is pretty straightforward.
    # FIXME: remove the weirdos: like poundal per inch
    "Interfacial Tension": {
        "Newton per meter": (1.0, ["N/m"]),
        "milliNewton per meter": (0.001, ["mN/m"]),
        "dyne per centimeter": (0.001, ["dyne/cm", "dyn/cm"]),
        "Poundal per inch": (5.443108492, ["pdl/in"]),
        "Pound force per inch": (175.126837, ["lbf/in"]),
        "erg per square centimeter": (0.001, ["erg/cm\N{SUPERSCRIPT TWO}", "erg/cm^2"]),
        "erg per square millimeter": (0.1, ["erg/mm\N{SUPERSCRIPT TWO}", "erg/mm^2"]),
        "joule per square meter": (1.0, ["j/m\N{SUPERSCRIPT TWO}", "j/m^2"]),
    },

    "Pressure": {
        "Pascal": (1.0, ["Pa"]),
        "kiloPascal": (1000.0, ["kPa"]),
        "megaPascal": (1000000.0, ["MPa"]),
        "Newton per square meter": (1.0, ["N/m\N{SUPERSCRIPT TWO}", "N/m^2"]),
        "bar": (100000.0, ["bars"]),
        "millibar": (100.0, ["mbar"]),
        "dyne per square centimeter": (0.1, ["dyn/cm\N{SUPERSCRIPT TWO}", "dyn/cm^2"]),
        "pound per square inch": (6894.76, ["lb/in\N{SUPERSCRIPT TWO}", "lb/in^2", "psi"]),
    },


    # Concentration in water (note: this is converting between mass/volume)
    #                               and mass/mass, hence the "water" part
    "Concentration In Water": {
        "kilogram per cubic meter": (1.0, ["kg/m\N{SUPERSCRIPT THREE}", "kg/m^3"]),
        "gram per cubic meter": (1e-3, ["g/m\N{SUPERSCRIPT THREE}", "g/m^3"]),
        "part per million": (1e-3, ["ppm", "parts per million"]),
        "part per billion": (1e-6, ["ppb", "parts per billion"]),
        "part per thousand": (1.0, [ '\u2030', '0/00', 'ppt', 'parts per thousand']),
        "part per trillion": (1e-9, ["pptr", "parts per trillion"]),
        "fraction (decimal)": (1e3, ["fraction", "mass per mass", "1"]),
        "percent": (10.0, ["%", "parts per hundred"]),
        "pound per cubic foot": (16.018450433864, ["lb/ft\N{SUPERSCRIPT THREE}",
                                                   "lb/ft^3",
                                                   ]),
        "milligram per liter": (0.001, ["mg/l"]),
        "gram per liter": (1.0, ["g/l"]),
        "kilogram per liter": (1000.0, ["kg/l"]),
        "milligram per gram": (1.0, ["mg/g"]),
        "milligram per kilogram": (0.001, ["mg/kg"]),
        "milligram per milliliter": (1.0, ["mg/ml"]),
        "microgram per liter": (1e-6, ["\N{MICRO SIGN}g/l", "ug/l"]),
        "microgram per gram": (1e-3, ["\N{MICRO SIGN}g/g", "ug/g"]),
        "nanogram per liter": (1e-9, ["ng/l"]),
    },

    # Concentration:
    #  This is technically unitless -- just a fraction
    "Concentration": {
        "fraction (decimal)": (1.0, ["fraction", "mass per mass", "1"]),
        "percent": (0.01, ["%", "parts per hundred"]),
        'part per thousand': (1e-3, [ '\u2030', '0/00', 'parts per thousand']),
        "part per million": (1e-6, ["ppm", "parts per million"]),
        "part per billion": (1e-9, ["ppb", "parts per billion"]),
        'part per trillion': (1e-12, ['parts per trillion']),
    },

    "Dimensionless": {
        "fraction (decimal)": (1.0, ["number", "fraction", "1"]),
        "percent": (0.01, ["%", "parts per hundred"]),
        'part per thousand': (1e-3, ['\u2030', '0/00', 'ppt', 'parts per thousand']),
    },

    # Mass Fraction: Any unit that is a mass/mass ratio.  This will be very
    # similar to Concentration, but we want the notion of a generalized mass
    # fraction to be distinct.
    'Mass Fraction': {
        'fraction (decimal)': (1.0, ['fraction', '1', 'mass per mass']),
        'percent': (0.01, ['%', 'parts per hundred']),
        'part per thousand': (1e-3, ['\u2030', '0/00', 'ppt', 'parts per thousand']),
        'part per million': (1e-6, ['ppm', 'parts per million']),
        'part per billion': (1e-9, ['ppb', 'parts per billion']),
        'part per trillion': (1e-12, ['parts per trillion']),
        "gram per kilogram": (1e-3, ["g/kg"]),
        "milligram per gram": (1e-3, ["mg/g"]),
        "milligram per kilogram": (1e-6, ["mg/kg"]),
        "microgram per gram": (1e-6, ["\N{MICRO SIGN}g/g", "ug/g"]),
        "nanogram per gram": (1e-9, ["ng/g", "nanograms per gram"]),
    },

    # Volume Fraction: Any unit that is a volume/volume ratio.  There will be
    # a lot of overlap here with mass fraction, as some units do not allude to
    # a specific unit (% for example).
    'Volume Fraction': {
        'fraction (decimal)': (1.0, ['fraction', '1', 'mass per mass']),
        'percent': (0.01, ['%', 'parts per hundred']),
        'part per thousand': (1e-3, ['\u2030', '0/00', 'ppt', 'parts per thousand']),
        'part per million': (1e-6, ['ppm', 'parts per million']),
        'part per billion': (1e-9, ['ppb', 'parts per billion']),
        'part per trillion': (1e-12, ['parts per trillion']),
        'milliliter per liter': (1e-3, ['ml/l', 'mL/L', 'mL/dm^3']),
        'liter per cubic meter': (1e-3, ['l/m^3', 'L/m^3']),
    },

    "Angular Measure": {
        "radians": (1.0, ["radian", "rad"]),
        "degrees": (3.141592653589793 / 180.0, ["degree", "deg"])
    },

    "Angular Velocity": {
        "rad/s": (1.0, ["1/s", "radians/sec"]),
        "hertz": (2 * 3.141592653589793, ["hz", "cycles/sec"]),
        "rpm": (3.141592653589793 / 30, ["rotations per minute"])
    },

}


#fixme -- this was already here, yes ???
# need to check for duplicate (and correct) functionality)
# Build the unit sets to allow quick lookup of type and conversion legality
# this creates something like the following:
# unit_sets = {'Length': set(['m','km','mm',...]),
#              'Area': set(['m^2','cm^2',...]),
#              ...
#              }

unit_sets = {}
for k in ConvertDataUnits.keys():
    unit_sets[k] = set(itertools.chain(*[y for (x, y)
                                         in ConvertDataUnits[k].values()]))

# fixme: what is this used for?
# if it's just for listing known units, then we should leave it in
# del unit_sets['Concentration In Water']

# not always length -- can be mass/area too.
# unit_sets['Oil Concentration'] = unit_sets['Length']

# Build the global unit list

supported_units = set([])
for s in unit_sets.values():
    supported_units = supported_units.union(s)


def write_units(filename=None):
    """
    fixme: why is this ASCII only?
    """
    import sys
    if filename is None:
        f = sys.stdout
    else:
        f = open(filename, 'w')
    f.write("NUCOS unit set:\n")
    for key, value in ConvertDataUnits.items():
        f.write("\n%s:\n" % key)
        for key2 in value:
            f.write("    %s\n" % key2.encode('ascii', 'ignore'))


def all_unit_names(format="str"):
    """
    returns a string of all unit names, grouped by unit type

    :param format="str": format for output -- default is plain python str
                         other option: "rst" for restuctured text
    """
    if format == "str":
        result = []
        for key, value in ConvertDataUnits.items():
            result.append('\n%s:\n' % key)
            for key2 in value:
                result.append("    %s\n        " % key2)
                result.append(", ".join(value[key2][1]))
                result.append("\n")
        return "".join(result)
    elif format == "rst":
        result = []
        for unit_type, value in ConvertDataUnits.items():
            result.append('\n%s:\n' % unit_type)
            result.append('-' * (len(unit_type) + 1) + '\n\n')
            for unit in value:
                result.append("%s\n" % unit)
                result.append('.' * len(unit) + '\n\n    ')
                result.append(", ".join(value[unit][1]))
                result.append("\n\n")
        return "".join(result)
    else:
        raise ValueError('only supported formats are "str" and "rst"')


def dump_to_json(filename=None):
    """
    dumps the full unit data to JSON, for use in the Javascript version, or ...
    """
    import sys
    import json

    f = open(filename, 'w') if filename else sys.stdout
    f.write(json.dumps(ConvertDataUnits, indent=2, separators=(',', ':')))
