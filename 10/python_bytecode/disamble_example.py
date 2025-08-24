'''This module makes the bytecode human readable.'''

import dis, marshal

with open("__pycache__/add_axample.cpython-313.pyc", "rb") as f:
    f.read(16)              # skip header (magic number, timestamp, etc.)
    code = marshal.load(f)  # load the code object

dis.dis(code)