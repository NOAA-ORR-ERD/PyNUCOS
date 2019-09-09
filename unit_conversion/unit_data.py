#!/usr/bin/env python

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
               "micron": (0.000001, ["microns"]),
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
        "micron": (1.0, ["microns"]),
        "cubic meter per square kilometer": (1.0, ["m^3/km^2", "m\N{SUPERSCRIPT THREE}/km\N{SUPERSCRIPT TWO}"]),
        "millimeter": (1000., ["mm", "millimeters"]),
        "inch": (25400., ["in", "inches"]),
        "barrel per acre": (39.2866176, ["bbl/acre"]),  # calculated from HCP
        "barrel per square mile": (0.06138533995, ["bbl/sq.mile",
                                                   "bbl/mile\N{SUPERSCRIPT TWO}"]),  # calculated from HCP
        "gallon per acre": (0.93539563202687404, ["gal/acre", ]),  # calculated from HCP
        "liter per hectare": (0.1, ["liter/hectare"]),  # calculated from HCP
        # these are mass/area -- so technically different.
        # but hard coding density of 0.95 -- so we can do it easily.
        "gram per square meter": (1.0526315789473684, ["g/m^2", "g/m\N{SUPERSCRIPT TWO}"]),
        "kilogram per square meter": (1052.6315789473684, ["kg/m^2", "kg/m\N{SUPERSCRIPT TWO}"]),
        "kilogram per square kilometer": (.0010526315789473684, ["kg/km^2", "g/km\N{SUPERSCRIPT TWO}"])
    },

    # All Areas in terms of square meter
    "Area": {
        "square meter": (1.0, ["m^2", "m\N{SUPERSCRIPT TWO}", "sq m"]),
        "square centimeter": (.0001, ["cm^2", "cm\N{SUPERSCRIPT TWO}", "sq cm"]),
        "square kilometer": (1e6, ["km^2", "km\N{SUPERSCRIPT TWO}", "sq km"]),
        "acre": (4046.8564, ["acres"]),
        "square mile": (2589988.1, ["sq miles"]),
        "square nautical mile": (3429904, ["sq nm", "nm^2",
                                           "nm\N{SUPERSCRIPT TWO}"]),  # calculated from HCP
        "square yard": (0.83612736, ["sq yards", "squareyards"]),
        "square foot": (0.09290304, ["ft^2", "ft\N{SUPERSCRIPT TWO}",
                                     "sq foot", "square feet"]),
        "square inch": (0.00064516, ["in^2", "in\N{SUPERSCRIPT TWO}",
                                     "sq inch", "square inches"]),
        "hectare": (10000.0, ["hectares", "ha"]),
    },

    # All volumes in terms of cubic meter
    "Volume": {
        "cubic meter": (1.0, ["m^3", "cu m", "cubic meters",
                              "m\N{SUPERSCRIPT THREE}"]),
        "cubic kilometer": (1e9, ["km^3", "cu km", "cubic kilometers",
                                  "km\N{SUPERSCRIPT THREE}"]),
        "cubic centimeter": (1e-6, ["cm^3", "cu cm", "cc",
                                    "cm\N{SUPERSCRIPT THREE}"]),
        "barrel (petroleum)": (.1589873, ["bbl", "barrels", "barrel", "bbls"]),
        "liter": (1e-3, ["l", "liters"]),
        "gallon": (0.0037854118, ["gal", "gallons", "usgal"]),
        "gallon (UK)": (0.004546090, ["ukgal", "gallons(uk)"]),
        "million US gallon": (3785.4118, ["milliongallons", "milgal"]),
        "cubic foot": (0.028316847, ["ft^3", "cu feet", "cubicfeet",
                                     "ft\N{SUPERSCRIPT THREE}"]),
        "cubic inch": (16.387064e-6, ["in^3", "cu inch", "cubicinches",
                                      "in\N{SUPERSCRIPT THREE}"]),
        "cubic yard": (.76455486, ["yd^3", "cu yard", "cubicyards",
                                   "yd\N{SUPERSCRIPT THREE}"]),
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

    # All Mass units in Kg (weight is taken to be mass at standard g)
    "Mass": {"kilogram": (1.0, ["kg", "kilograms"]),
             "pound": (0.45359237, ["lb", "pounds", "lbs"]),
             "gram": (.001, ["g", "grams"]),
             "milligram": (.000001, ["mg"]),
             "microgram": (.000000001, ["ug", "\N{MICRO SIGN}g"]),
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
                                            "m s-1"]),
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
        "cubic meter per second": (1.0, ["m^3/s", "cu m/s", "cms",
                                         "m\N{SUPERSCRIPT THREE}/s"]),
        "cubic meter per min": (1.0 / 60., ["m^3/min",
                                            "m\N{SUPERSCRIPT THREE}/min"]),
        "cubic meter per hour": (1.0 / 3600.0, ["m^3/hr",
                                                "m\N{SUPERSCRIPT THREE}/hr"]),
        "liter per second": (0.001, ["l/s", "lps"]),
        "liter per minute": (0.001 / 60, ["l/min", ]),
        "cubic foot per second": (.02831685, ["cfs", "cu feet/s", "feet^3/s",
                                              "ft\N{SUPERSCRIPT THREE}/s"]),
        "cubic foot per minute": (0.00047194744, ["ft^3/min",
                                                  "ft\N{SUPERSCRIPT THREE}/min"]),  # calculated from cm^3/s
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
        "gram per cubic centimeter": (1.0, ["g/cm^3",
                                            "g/cm\N{SUPERSCRIPT THREE}",
                                            "grams per cubic centimeter"]),
        "gram per liter": (.001, ["g/L",
                                  "gram per litre"]),
        "gram per milliliter": (1.0, ["g/mL",
                                      "gram per millilitre"]),
        "specific gravity (15\xb0C)": (0.99913, ["S", "specificgravity",
                                                 "Spec grav", "SG",
                                                 "specificgravity(15C)"]),
        "kilogram per cubic meter": (.001, ["kg/m^3",
                                            "kg/m\N{SUPERSCRIPT THREE}"]),
        "tonne per cubic meter": (1.0, ["tonne/m^3",
                                        "tonne/m\N{SUPERSCRIPT THREE}",
                                        "t/m^3",
                                        "t/m\N{SUPERSCRIPT THREE}"]),

        "pound per cubic foot": (0.016018463, ["lbs/ft^3",
                                               "lb/ft\N{SUPERSCRIPT THREE}"]),
        "API degree": (1, ["api"]),  # this is special cased in the code.
    },

    # All Time In second
    "Time": {"second": (1.0, ["s", "sec", "seconds"]),
             "minute": (60.0, ["min", "minutes"]),
             "hour": (3600.0, ["hr", "hours", "hrs"]),
             "day": (86400.0, ["days"]),
             },

    # Kinematic Viscosity in Stokes
    # NOTE: there is a more detailed way to do this, specified in:
    # ASTM D 2161 Standard Practice for Conversion of Kinematic Viscosity to
    # Saybolt Universal Viscosity or to Saybolt Furol Viscosity
    # for the moment, this will only handle approximation for SFS and SUS
    "Kinematic Viscosity": {
        "Stoke": (1.0, ["St", "stokes"]),
        "centiStoke": (.01, ["cSt", "centistokes"]),
        "square millimeter per second": (.01, ["mm^2/s",
                                               "mm\N{SUPERSCRIPT TWO}/s", ]),
        "square centimeter per second": (1.0, ["cm^2/s",
                                               "cm\N{SUPERSCRIPT TWO}/s", ]),
        "square meter per second": (10000, ["m^2/s",
                                            "m\N{SUPERSCRIPT TWO}/s"]),
        "square inch per second": (6.4516, ["in^2/s",
                                            "in\N{SUPERSCRIPT TWO}/s",
                                            "squareinchespersecond"]),
        "Saybolt Universal Second": (1 / 462.0, ["SSU", "SUS"]),  # from CRC - only good for > 100cSt
        "Saybolt Furol Second": (0.02116959064, ["SSF", "SFS"]),  # from Fuel Oil Manual: good for 724cSt
    },

    # Dynamic Viscosity
    "Dynamic Viscosity": {
        "kilogram per meter per second": (1.0, ["kg/(m s)"]),
        "Pascal second": (1.0, ["Pa s", "Pa.s"]),
        "milliPascal second": (0.001, ["mPa s", "mPa.s"]),
        "Newton seconds per square meter": (1.0, ["N s/m^2",
                                                  "N s/m\N{SUPERSCRIPT TWO}"
                                                  ]),

        "gram per centimeter per second": (0.1, ["g/(cm s)"]),
        "poise": (0.1, ["p"]),
        "dyne seconds per square centimeter": (0.1,
                                               ["dyne s/cm^2",
                                                "dyne s/cm\N{SUPERSCRIPT TWO}"]
                                               ),

        "centipoise": (0.001, ["cP"]),
    },

    # Interfacial Tension
    # This is quantified as a force/length measurement in most cases, but a
    # couple exceptions quantify in ergs/area.  An erg is an amount of work,
    # not force, but the conversion is pretty straightforward.
    "Interfacial Tension": {
        "Newton per meter": (1.0, ["N/m"]),
        "milliNewton per meter": (0.001, ["mN/m"]),
        "dyne per centimeter": (0.001, ["dyne/cm"]),
        "gram force per centimeter": (0.98066499997877, ["gf/cm"]),
        "Poundal per inch": (5.443108492, ["pdl/in"]),
        "Pound force per inch": (175.126837, ["lbf/in"]),
        "erg per square centimeter": (0.001, ["erg/cm^2",
                                              "erg/cm\N{SUPERSCRIPT TWO}"]),
        "erg per square millimeter": (0.1, ["erg/mm^2",
                                            "erg/mm\N{SUPERSCRIPT TWO}"]),
    },

    # Adhesion
    # This is quantified as a force/area measurement in most cases.
    # There are a lot of conversions in this category that are temperature
    # dependent.  We will not include these for now.
    "Adhesion": {
        "Pascal": (1.0, ["Pa"]),
        "kiloPascal": (1000.0, ["kPa"]),
        "megaPascal": (1000000.0, ["MPa"]),
        "Newton per square meter": (1.0,
                                    ["N/m^2",
                                     "N/m\N{SUPERSCRIPT TWO}"]),
        "bar": (100000.0, ["bars"]),
        "millibar": (100.0, ["mbar"]),
        "gram force per square centimeter": (98.0665,
                                             ["g/cm^2", "gf/cm^2",
                                              "g/cm\N{SUPERSCRIPT TWO}",
                                              "gf/cm\N{SUPERSCRIPT TWO}"]),
        "gram force per square meter": (0.00980665,
                                        ["g/m^2", "gf/m^2",
                                         "g/m\N{SUPERSCRIPT TWO}",
                                         "gf/m\N{SUPERSCRIPT TWO}"]),
        "kilogram force per square centimeter": (98066.5,
                                                 ["kg/cm^2", "kgf/cm^2",
                                                  "kg/cm\N{SUPERSCRIPT TWO}",
                                                  "kgf/cm\N{SUPERSCRIPT TWO}"]
                                                 ),
        "kilogram force per square meter": (9.80665,
                                            ["kg/m^2", "kgf/m^2",
                                             "kg/m\N{SUPERSCRIPT TWO}",
                                             "kgf/m\N{SUPERSCRIPT TWO}"]),
        "dyne per square centimeter": (0.1,
                                       ["dyn/cm^2",
                                        "dyn/cm\N{SUPERSCRIPT TWO}"]),
        "pound force per square inch": (6894.76,
                                        ["lb/in^2", "lbf/in^2",
                                         "psi", "pfsi",
                                         "lb/in\N{SUPERSCRIPT TWO}",
                                         "lbf/in\N{SUPERSCRIPT TWO}"]),
    },

    # Concentration in water in PPM
    "Concentration In Water": {
        "kilogram per cubic meter": (1.0, ["kg/m^3",
                                           "kg/m\N{SUPERSCRIPT THREE}"]),
        "gram per cubic meter": (1e-3, ["g/m^3", "g/m\N{SUPERSCRIPT THREE}"]),
        "part per million": (1e-3, ["ppm", "parts per million"]),
        "part per billion": (1e-6, ["ppb", "parts per billion"]),
        "part per thousand": (1.0, ["ppt", "parts per thousand"]),
        "part per trillion": (1e-9, ["parts per trillion", "pptr"]),
        "fraction (decimal)": (1e3, ["fraction", "mass per mass", "1"]),
        "percent": (10.0, ["%", "parts per hundred", "per cent"]),
        "pound per cubic foot": (16.018450433864, ["lb/ft^3",
                                                   "lb/ft\N{SUPERSCRIPT THREE}"]),
        "milligram per liter": (0.001, ["mg/l"]),
        "gram per liter": (1.0, ["g/l"]),
        "kilogram per liter": (1000.0, ["kg/l"]),
        "milligram per gram": (1.0, ["mg/g"]),
        "milligram per kilogram": (0.001, ["mg/kg"]),
        "milligram per milliliter": (1.0, ["mg/ml"]),
        "microgram per liter": (1e-6, ["ug/l"]),
        "microgram per gram": (1e-3, ["ug/g"]),
        "nanogram per liter": (1e-9, ["ng/l"]),
    },

    "Angular Measure": {
        "radians": (1.0, ["radian", "rad"]),
        "degrees": (3.141592653589793 / 180.0, ["degree", "deg"])
    }

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


def all_unit_names():
    """
    returns a string of all unit names
    """
    result = []
    for key, value in ConvertDataUnits.items():
        result.append('\n%s:\n' % key)
        for key2 in value:
            result.append("    %s\n        " % key2.encode('ascii', 'ignore'))
            result.append(", ".join(value[key2][1]))
            result.append("\n")
    return "".join(result)


def dump_to_json(filename=None):
    """
    dumps the full unit data to JSON, for use in the Javascript version, or ...
    """
    import sys
    import json

    f = open(filename, 'w') if filename else sys.stdout
    f.write(json.dumps(ConvertDataUnits, indent=2, separators=(',', ':')))
