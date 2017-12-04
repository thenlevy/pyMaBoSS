"""Definitions of the different classes provided to the user."""

from . import logic
from sys import stderr, stdout


class Node(object):
    """
    Represent a node of a boolean network.

    name :: str, the name of the node
    rt_up :: double >= 0
    rt_down :: double >= 0
    logExp :: str, a boolean expression.

    when logic evaluates to true, rate_up will take the value rt_up and
    rate_down take the value 0, when logic evaluates to Fales, rate_up take the
    value 0 and rate_down the value rt_down.
    """

    def __init__(self, name, logExp=None, rt_up=1, rt_down=1,
                 is_internal=False, internal_var={}):
        """
        Create a node not yet inserted in a network.

        logic, rt_up and rt_down are optional when creating the node but
        must be set before making a network.
        """
        self.name = name
        self.set_logic(logExp)
        self.rt_up = rt_up
        self.rt_down = rt_down
        self.is_internal = is_internal
        self.internal_var = internal_var.copy()

    def set_rate(self, rate_up, rate_down):
        """Set the value of rate_up and rate_down."""
        self.rt_up = "@logic ? " + rate_up + " : 0"
        self.rt_down = "@logic ? 0 : " + rate_down

    def set_logic(self, string):
        """Set logExp to str if str is a valid boolean expression."""
        if logic._check_logic_syntax(string):
            self.logExp = string
        else:
            print("Warning, syntax error: %s" % string, file=stderr)
            print("logExp set to None", file=stderr)
            self.logExp = None

    def __str__(self):
        return _strNode(self)

    def copy(self):
        return Node(self.name, self.logExp, self.rt_up, self.rt_down,
                    self.is_internal, self.internal_var)


class Network(dict):
    """
    Represent a boolean network.

    Initialised with a list of Nodes whose logExp must contain only names
    present in the list.
    """

    def __init__(self, nodeList):
        super().__init__({nd.name: nd for nd in nodeList})
        self.nodeList = nodeList
        self.names = [nd.name for nd in nodeList]
        self.logicExp = {nd.name: nd.logExp for nd in nodeList}

        if not logic._check_logic_defined(self.names,
                                          [nd.logExp for nd in nodeList]):
            raise ValueError("Some logic rule had unkown variables")

        # _attribution gives for each node the list of node with which it is
        # binded.
        self._attribution = {nd.name: nd.name for nd in nodeList}

        # _initState gives for each list of binded node the initial state
        # probabilities.
        self._initState = {l: {0: 0.5, 1: 0.5} for l in self._attribution}

    def copy(self):
        new_ndList = [nd.copy() for nd in self.nodeList]
        new_network = Network(new_ndList)
        new_network._attribution = self._attribution
        new_network._initState = self._initState.copy()
        return new_network

    def set_istate(self, nodes, probDict):
        if not (isinstance(nodes, list) or isinstance(nodes, tuple)):
            if not len(probDict) in [1, 2]:
                print("Error, must provide a list or dictionary of size 1 or 2",
                      file=stderr)
                return

            if (probDict[0] < 0 or probDict[1] < 0
                  or not probDict[0] + probDict[1] == 1):
                print("Error, bad value for probabilites", file=stderr)
                return
            else:
                if isinstance(self._attribution[nodes], tuple):
                    self._erase_binding(nodes)
                self._initState[nodes] = {0: probDict[0], 1: probDict[1]}

        elif _testStateDict(probDict, len(nodes)):
            for node in nodes:
                if isinstance(self._attribution[node], tuple):
                    print("Warning, node %s was previously bound to other"
                          "nodes" % node, file=stderr)
                    self._erase_binding(node)

            # Now, forall node in nodes, self_attribution[node] is a singleton
            for node in nodes:
                self._initState.pop(node)
                self._attribution[node] = tuple(nodes)

            self._initState[tuple(nodes)] = probDict


    def _erase_binding(self, node):
        self._initState.pop(self._attribution[node])
        for nd in self._attribution[node]:
            self._attribution[nd] = [nd]
            self.set_istate(nd, [0.5, 0.5])


    def __str__(self):
        return _strNetwork(self)


    def print_istate(self, out=stdout):
        print(_str_istateList(self._initState), file=out)

    def set_output(self, output_list):
        """Set all the nodes that are not in the output_list as internal."""
        for nd in self:
            if nd not in output_list:
                self[nd].is_internal = True


def _testStateDict(stDict, nbState):
    """Check if stateDict is a good parameter for set_istate."""
    def goodTuple(t):
        return len(t) == nbState and all(x == 0 or x == 1 for x in t)

    if (not all(isinstance(t, tuple) for t in stDict)
       or not all(goodTuple(t) for t in stDict)):
        print("Error, not all keys are good tuples of length %s" % nbState,
              file=stderr)
        return False
    elif (not all(x >= 0 for x in stDict.values())
          or not sum(stDict.values()) == 1):
        print("Error, the given values must be nonegative and sum up to 1",
              file=stderr)
        return False
    else:
        return True


def _strNode(nd):
    string = ""
    rt_up_str = str(nd.rt_up)
    rt_down_str = str(nd.rt_down)
    internal_var_decl = "\n".join(map(lambda v: v+" = " + nd.internal_var[v],
                                      nd.internal_var.keys()))
    string = "\n".join(["Node " + nd.name + " {",
                        internal_var_decl,
                        "\tlogic = " + nd.logExp + ";",
                        ("\trate_up = " + rt_up_str + ";"),
                        ("\trate_down = " + rt_down_str + ";"),
                        "}"])
    return string


def _strNetwork(nt):
    string = _strNode(nt.nodeList[0])
    if len(nt.nodeList) > 1:
        string += "\n"
        string += "\n\n".join(_strNode(nd) for nd in nt.nodeList[1:])
    return string


def _str_istateList(isl):
    stringList = []
    for binding in isl:
        string = ''
        if isinstance(binding, tuple):
            string += '[' + ", ".join(list(binding)) + '].istate = '
            string += ' , '.join([str(isl[binding][t]) + ' '
                                  + str(list(t)) for t in isl[binding]])
            string += ';'
        else:
            string += '[' + binding + '].istate = '
            string += str(isl[binding][0]) + '[0] , '
            string += str(isl[binding][1]) + '[1];'
        stringList.append(string)
    return '\n'.join(stringList)
