"""Test the functions in logic.py."""


import sys
sys.path.append('..')
from src import logic

print("Check _check_logic_defined")
print("   zerology")
assert(logic._check_logic_defined([], []))
assert(logic._check_logic_defined([], ["_True"]))
print("   normal case")
assert(logic._check_logic_defined(['foo', 'bar'], ['(foo || bar)']))
print("   syntax error")
assert(not logic._check_logic_defined(['foo', 'bar'], ['foo bar']))
print("   undifined variable")
assert(not logic._check_logic_defined(['foo', 'bar'], ['(foo && barr)']))


print("All test passed")
