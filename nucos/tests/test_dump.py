#!/usr/bin/env python

"""
Testing dumping options

Not really good tests, but at least shows they run

And it generates the files in the repo.
"""

import os
from pathlib import Path
from nucos import unit_data


def test_write_unit_data_file_rst():
    """
    technically not a test, but a way to get the file re-written automatically
    """
    project_dir = Path(__file__).parent.parent.parent

    filename = project_dir / "NUCOS_unit_list.rst"
    unit_data.write_all_unit_names(format="rst", filename=filename)

def test_write_unit_data_file_txt():
    """
    technically not a test, but a way to get the file re-written automatically
    """
    project_dir = Path(__file__).parent.parent.parent

    filename = project_dir / "NUCOS_unit_list.txt"
    unit_data.write_all_unit_names(format="txt", filename=filename)


def test_dump_to_json():
    '''
    does the dump_to_json_ run without error
    '''
    unit_data.dump_to_json("junk.json")


def test_write_all_unit_names():
    '''
    only tests if if doesn't crash and give SOME answers
    '''
    names = unit_data.write_all_unit_names(format='txt', filename='str')

    assert "Kinematic Viscosity:" in names
    assert "API degree" in names


# def test_write_units():
#     """ just makes sure it doesn't crash"""
#     unit_data.write_units()
#     # and to a file
#     unit_data.write_units("all_units.txt")
