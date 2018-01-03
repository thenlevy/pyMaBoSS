"""Function to import the ginsim out in Python.

The ginsim output is a special case of MaBoSS format. This parser uses
the very specific structure of the ginsim output and not able to parse every
MaBoSS file.
"""

from sys import stderr
from os.path import isfile
import pyparsing as pp
from .logic import varName, logExp
from contextlib import ExitStack
from .network import Node, Network
from .simulation import Simulation
externVar = pp.Suppress('$') + ~pp.White() + varName
externVar.setParseAction(lambda token: token[0])
import uuid

# ====================
# bnd grammar
# ====================
internal_var_decl = pp.Group(varName('lhs') + pp.Suppress('=')
                             + pp.SkipTo(';')('rhs') + pp.Suppress(';'))
node_decl = pp.Group(pp.Suppress("Node") + varName("name") + pp.Suppress('{')
                     + pp.OneOrMore(internal_var_decl)('interns')
                     + pp.Suppress('}'))
bnd_grammar = pp.OneOrMore(node_decl)

# =====================
# cfg grammar
# =====================

intPart = pp.Word(pp.nums)
intPart.setParseAction(lambda token: int(token[0]))
floatNum = pp.Word(pp.nums + '.' + 'E' + 'e' + '-' + '+')
floatNum.setParseAction(lambda token: float(token[0]))
var_decl = pp.Group(externVar("lhs") + pp.Suppress('=')
                    + floatNum("rhs") + pp.Suppress(';'))

param_decl = pp.Group(varName("param") + pp.Suppress('=')
                      + (floatNum("value")
                         | (pp.CaselessLiteral("True")
                            | pp.CaselessLiteral("False"))("bValue"))
                      + pp.Suppress(';'))

stateSet = (pp.Suppress('[') + pp.Group(pp.delimitedList(intPart))
            + pp.Suppress(']'))
stateSet.setParseAction(lambda token: list(token))

stateProb = floatNum('proba') + stateSet("states")
stateProb.setParseAction(lambda token: (token.proba, token.states))

istate_decl = pp.Group(pp.Suppress('[') + pp.delimitedList(varName)("nodes")
                       + pp.Suppress('].istate') + pp.Suppress('=')
                       + pp.delimitedList(stateProb)('attrib') + pp.Suppress(';'))

oneIstate_decl = pp.Group(varName("nd_i") + ~pp.White() + pp.Suppress('.istate')
                          + pp.Suppress('=') + pp.oneOf('0 1')('istate_val')
                          + pp.Suppress(';'))

internal_decl = pp.Group(varName("node") + ~pp.White()
                         + pp.Suppress(".is_internal") + pp.Suppress('=')
                         + pp.oneOf('0 1')("is_internal_val")
                         + pp.Suppress(';'))

cfg_decl = var_decl | istate_decl | param_decl | internal_decl | oneIstate_decl
cfg_grammar = pp.ZeroOrMore(cfg_decl)
cfg_grammar.ignore('//' + pp.restOfLine)


def build_network(prefix, simulation_name=None):
    """Read prefix.bnd and prefix.cfg and build the corresponding Network."""
    cfg_filename = prefix + '.cfg'
    if not isfile(cfg_filename):
        cfg_filename = prefix + '.bnd.cfg'  # File produced by the ginsim module
    with ExitStack() as stack:
        bnd_file = stack.enter_context(open(prefix + '.bnd', 'r'))
        cfg_file = stack.enter_context(open(cfg_filename, 'r'))
        bnd_content = bnd_file.read()
        cfg_content = cfg_file.read()

        if not cfg_grammar.matches(cfg_content):
            print("Error: syntax error in cfg file", file=stderr)
            return
        if not bnd_grammar.matches(bnd_content):
            print("Error: syntax error in bnd file", file=stderr)
            return

        (variables, parameters, is_internal_list,
         istate_list) = _read_cfg(cfg_content)

        nodes = _read_bnd(bnd_content, is_internal_list)

        net = Network(nodes)
        for istate in istate_list:
            net.set_istate(istate, istate_list[istate])
        for v in variables:
            lhs = '$'+v
            parameters[lhs] = variables[v]
        return Simulation(net, simulation_name, **parameters)


def load_file(filename, simulation_name=None):
    """Loads a network from a MaBoSS format file.

    filename
      A relative or absolute path to a file with extension ``.bnd`` or ``.cfg``.
    simulation_name
      The name of the returned ``Simulation`` object.
    """

    if filename.endswith(".cfg") or filename.endswith(".bnd"):
        filename = filename[:-4]
        return build_network(filename, simulation_name)
    else:
        print("Error, filename must end with .bnd or .cfg", file=stderr)
        return

def _read_cfg(string):
        variables = {}
        parameters = {}
        is_internal_list = {}
        istate_list = {}
        parse_cfg = cfg_grammar.parseString(string)
        for token in parse_cfg:
            if token.lhs:  # True if token is var_decl
                variables[token.lhs] = token.rhs
            if token.node:  # True if token is internal_decl
                is_internal_list[token.node] = float(token.is_internal_val)
            if token.param:  # True if token is param_decl
                if token.bValue:
                    parameters[token.param] = int(bool(token.bValue))
                else:
                    parameters[token.param] = float(token.value)
            if token.nd_i:
                istate_list[token.nd_i] = {0: 1 - int(token.istate_val),
                                           1: int(token.istate_val)}
            if token.attrib:  # True if token is istate_decl
                # TODO check if lens are consistent
                if len(token.nodes) == 1:
                    istate_list[token.nodes[0]] = {int(t[1][0]): t[0]
                                                   for t in token.attrib}
                else:
                    nodes = tuple(token.nodes)
                    istate_list[nodes] = {tuple(t[1]): t[0]
                                          for t in token.attrib}

        return (variables, parameters, is_internal_list, istate_list)


def _read_bnd(string, is_internal_list):
        nodes = []
        parse_bnd = bnd_grammar.parseString(string)
        for token in parse_bnd:
            interns = {v.lhs: v.rhs for v in token.interns}
            logic = interns.pop('logic')
            rate_up = interns.pop('rate_up')
            rate_down = interns.pop('rate_down')

            internal = (is_internal_list[token.name]
                        if token.name in is_internal_list
                        else False)
            nodes.append(Node(token.name, logic, rate_up, rate_down,
                              internal, interns))
        return nodes
