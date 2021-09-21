#!/usr/bin/env python

"""
testing dumping options

not really good tests, but at least shows they run
"""

from __future__ import (unicode_literals,
                        print_function,
                        division,
                        absolute_import
                        )

import os
from nucos import unit_data


def test_write_unit_data_file():
    """
    technically not a test, but a way to get the file re-written automatically
    """
    project_dir = os.path.split(__file__)[0]
    project_dir = os.path.split(project_dir)[0]
    project_dir = os.path.split(project_dir)[0]

    with open(os.path.join(project_dir, "NUCOS_unit_list.rst"), 'w', encoding="utf-8") as outfile:

        outfile.write(
"""
###############
NUCOS Unit List
###############

The NOAA Unit Converter for Oil Spills (NUCOS) is designed specifically to support
oils spill response and planning. As the Oil industry (and the response community)
use some unusual units, this is NOT a general purpose or full featured unit converter.
However, it does try to include all the units that one might need for oil spill work.

Complete unit type, units, and synonym list:

Note that in NUCOS, unit names and synonyms are case and white space insensitive, so, eg:

Pounds per Cubic Foot is the same as poundspercubicfoot

All The Units:
==============
"""
)

        outfile.write(unit_data.all_unit_names("rst"))


def test_dump_to_json():
    '''
    does the dump_to_json_ run without error
    '''
    unit_data.dump_to_json("junk.json")


def test_all_unit_names():
    '''
    only tests if if doesn't crash and give SOME answers
    '''
    names = unit_data.all_unit_names()

    assert "Kinematic Viscosity:" in names
    assert "API degree" in names


def test_write_units():
    """ just makes sure it doesn't crash"""
    unit_data.write_units()
    # and to a file
    unit_data.write_units("all_units.txt")
