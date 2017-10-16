"""Function to import the ginsim out in Python.

The ginsim output is a special case of MaBoSS format. This parser uses
the very specific structure of the ginsim output and not able to parse every
MaBoSS file.
"""

from sys import stderr
import pyparsing as pp
from logic import varName, logExp
from contextlib import ExitStack
from network import Node, Network
externVar = pp.Suppress('$') + ~pp.White() + varName

# ====================
# bnd grammar
# ====================
logDecl = pp.Suppress("logic =") + logExp + pp.Suppress(';')
logDecl.setParseAction(lambda token: token[0])
rt_up_decl = (pp.Suppress("rate_up") + pp.Suppress('=') + pp.Suppress('@logic')
              + pp.Suppress('?') + externVar + pp.Suppress(':')
              + pp.Suppress('0') + pp.Suppress(';'))

rt_down_decl = (pp.Suppress("rate_down") + pp.Suppress('=')
                + pp.Suppress('@logic') + pp.Suppress('?') + pp.Suppress('0')
                + pp.Suppress(':') + externVar + pp.Suppress(';'))
rt_up_decl.setParseAction(lambda token: token[0])
rt_down_decl.setParseAction(lambda token: token[0])

node_decl = pp.Group(pp.Suppress("Node") + varName("name") + pp.Suppress('{')
                     + logDecl("logic") + rt_up_decl("rate_up")
                     + rt_down_decl("rate_down") + pp.Suppress('}'))

bnd_grammar = pp.OneOrMore(node_decl)

# =====================
# cfg grammar
# =====================

intPart = pp.Word(pp.nums)
decPart = pp.Literal(".") + ~pp.White() + pp.Word(pp.nums)
floatMantissa = ((intPart + pp.Optional(~pp.White() + pp.Literal(".")
                                        + pp.Optional(~pp.White() + intPart)))
                 | decPart)
floatNum = floatMantissa + pp.Optional(pp.Suppress(pp.oneOf("eE"))
                                       + pp.Optional("-") + intPart)
var_decl = pp.Group((varName | externVar)("lhs") + pp.Suppress('=')
                    + (floatNum | intPart)("rhs") + pp.Suppress(';'))

stateSet = (pp.Suppress('[') + intPart
            + pp.ZeroOrMore(pp.Suppress(',') + intPart) + pp.Suppress(']'))

stateProb = floatNum + stateSet
istate_decl = pp.Group(pp.Suppress('[') + varName + pp.Suppress('].istate')
                       + pp.Suppress('=') + stateProb
                       + pp.ZeroOrMore(pp.Suppress(',') + stateProb)
                       + pp.Suppress(';'))

cfg_decl = var_decl | istate_decl
cfg_grammar = pp.ZeroOrMore(cfg_decl)


def build_network(prefix):
    """Read prefix.bnd and prefix.cfg and build the corresponding Network."""
    with ExitStack() as stack:
        bnd_file = stack.enter_context(open(prefix + '.bnd', 'r'))
        cfg_file = stack.enter_context(open(prefix + '.cfg', 'r'))
        bnd_content = bnd_file.read()
        cfg_content = cfg_file.read()

        if not cfg_grammar.matches(cfg_content):
            print("Error: syntax error in cfg file", file=stderr)
            return
        if not bnd_grammar.matches(bnd_content):
            print("Error: syntax error in bnd file", file=stderr)
            return

        variables = {}
        nodes = []
        parse_cfg = cfg_grammar.parseString(cfg_content)
        for token in parse_cfg:
            if token.lhs:  # This evaluates to False if token is an istate_decl
                variables[token.lhs] = token.rhs

        parse_bnd = bnd_grammar.parseString(bnd_content)
        for token in parse_bnd:
            rate_up = token.rate_up
            if type(rate_up) is str:
                if rate_up not in variables:
                    print("Error unknown variable %s" % rate_up, file=stderr)
                    return
                rate_up = float(variables[rate_up])
            rate_down = token.rate_down
            if type(rate_down) is str:
                if rate_down not in variables:
                    print("Error unknown variable %s" % rate_down, file=stderr)
                    return
                rate_down = float(variables[rate_down])
            nodes.append(Node(token.name, token.logic, rate_up, rate_down))

            # TODO read is_internal value
        return Network(nodes)
