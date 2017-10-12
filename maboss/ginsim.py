"""Function to import the ginsim out in Python.

The ginsim output is a special case of MaBoSS format. This parser uses
the very specific structure of the ginsim output and not able to parse every
MaBoSS file.
"""

import pyparsing as pp
from logic import varName, logExp
externVar = pp.Suppress('$') + ~pp.White() + varName

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
