#!/usr/bin/env python

"""
testing dumping options

not really good tests, but at least shows they run
"""

from unit_conversion import unit_data


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
