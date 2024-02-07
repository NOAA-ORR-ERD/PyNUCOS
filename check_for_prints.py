#!/usr/bin/env python

"""
Find any extraneous prints on import

at least it's something
"""

import sys
import io
import contextlib

with contextlib.redirect_stdout(io.StringIO()) as output:
    import nucos

if output.getvalue():
    print("OOPs -- something got printed in import!")
    print(output.getvalue())
    sys.exit(1)
sys.exit(0)



print("contents of stdout:", output.getvalue())
