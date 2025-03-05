#!/usr/bin/env python

"""
testing dumping options

not really good tests, but at least shows they run
"""

import os
from pathlib import Path
from nucos import unit_data



def test_write_unit_data_file():
    """
    technically not a test, but a way to get the file re-written automatically
    """
    project_dir = Path(__file__).parent.parent.parent

    with open(project_dir / "NUCOS_unit_list.rst", 'w', encoding="utf-8") as outfile:
        content = unit_data.all_unit_names(format="rst", filename=None)
        outfile.write(content)


def test_dump_to_json():
    '''
    does the dump_to_json_ run without error
    '''
    unit_data.dump_to_json("junk.json")


def test_all_unit_names():
    '''
    only tests if if doesn't crash and give SOME answers
    '''
    names = unit_data.all_unit_names(format='str', filename=None)

    assert "Kinematic Viscosity:" in names
    assert "API degree" in names


def test_write_units():
    """ just makes sure it doesn't crash"""
    unit_data.write_units()
    # and to a file
    unit_data.write_units("all_units.txt")
