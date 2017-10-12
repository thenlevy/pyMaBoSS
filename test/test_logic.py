"""Test the functions in logic.py."""


import sys
sys.path.append('..')
from maboss import logic

print("Check _check_logic_defined")
print("   zerology")
assert(logic._check_logic_defined([], []))
assert(logic._check_logic_defined([], ["True"]))
print("   normal case")
assert(logic._check_logic_defined(['foo', 'bar'], ['(foo || bar)']))
print("   syntax error")
assert(not logic._check_logic_defined(['foo', 'bar'], ['foo bar']))
print("   undifined variable")
assert(not logic._check_logic_defined(['foo', 'bar'], ['(foo && barr)']))

print("    light syntax")
assert(logic._check_logic_defined(['a', 'b', 'c', 'd'], ["a & !b AND c OR a & b & !c OR !a & b & c"]))

print("All test passed")
