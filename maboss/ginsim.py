"""Function to import the ginsim out in Python.

The ginsim output is a special case of MaBoSS format. This parser uses
the very specific structure of the ginsim output and not able to parse every
MaBoSS file.
"""

import pyparsing as pp
from logic import varName, logExp
externVar = pp.Suppress('$') + ~pp.White() + varName

# ====================
# bnd grammar
# ====================
logDecl = (pp.Suppress("logic =") + logExp + pp.Suppress(';'))
rt_up_decl = (pp.Suppress("rate_up") +  pp.Suppress('=') + pp.Suppress('@logic')
              + pp.Suppress('?') + externVar + pp.Suppress(':') + pp.Suppress('0')

              + pp.Suppress(';'))

rt_down_decl = (pp.Suppress("rate_down") +  pp.Suppress('=')
                + pp.Suppress('@logic')  + pp.Suppress('?') + pp.Suppress('0')
                + pp.Suppress(':') + externVar + pp.Suppress(';'))

node_decl = pp.Group(pp.Suppress("Node") + varName + pp.Suppress('{') + logDecl
             + rt_up_decl + rt_down_decl + pp.Suppress('}') )

bnd_file = pp.OneOrMore(node_decl)

# =====================
# cfg grammar
# =====================

intPart = pp.Word(pp.nums)
decPart = pp.Literal(".") + ~pp.White() + pp.Word(pp.nums)
floatMantissa = ((intPart + pp.Optional(~pp.White() + pp.Literal(".")
                                        + pp.Optional( ~pp.White() + intPart)))
                 | decPart)
floatNum = floatMantissa + pp.Optional(pp.Suppress(pp.oneOf("eE"))
                                       + pp.Optional("-") + intPart)
var_decl = (varName | externVar) + pp.Suppress('=') + (floatNum | intPart) + pp.Suppress(';')

stateSet = (pp.Suppress('[') + intPart + pp.ZeroOrMore(pp.Suppress(',') + intPart)
            + pp.Suppress(']'))
stateProb = floatNum + stateSet
istate_decl = (pp.Suppress('[') + varName + pp.Suppress('].istate')
              + pp.Suppress('=') + stateProb
              + pp.ZeroOrMore(pp.Suppress(',') + stateProb) + pp.Suppress(';'))

cfg_decl = var_decl | istate_decl
cfg_file = pp.ZeroOrMore(cfg_decl)
