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

    def __init__(self, name, logExp=None, rt_up=1, rt_down=1, is_internal=False):
        """
        Create a node not yet inserted in a network.

        logic, rt_up and rt_down are optional when creating the node but
        must be set before making a network.
        """
        self.name = name
        self.set_logic(logExp)
        self.set_rate(rt_up, rt_down)
        self.is_internal = is_internal


    def set_rate(self, rate_up, rate_down):
        """Set the value of rate_up and rate_down."""
        if rate_up < 0 or rate_down < 0:
            print("Error, rates must be nonnegative", file=stderr)
            print("Rates were not modified", file=stderr)
            return
        self.rt_up = rate_up
        self.rt_down = rate_down

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


class Network(object):
    """
    Represent a boolean network.

    Initialised with a list of Nodes whose logExp must contain only names
    present in the list.
    """

    def __init__(self, nodeList):
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


    def set_istate(self, nodes, probDict):
        if not isinstance(nodes, list):
            if not len(probDict) == 2:
                print("Error, must provide a list or dictionary of size 2",
                      file=stderr)
                return
            elif (probDict[0] < 0 or probDict[1] < 0
                  or not probDict[0] + probDict[1]==1):
                print("Error, bad value for probabilites", file=stderr)
                return
            else:
                if isinstance(self._attribution[nodes], tuple):
                    print("Warning, node %s was previously bound to other" \
 "node" % nodes,
                        file=stderr)
                    self._erase_binding(nodes)
                self._initState[nodes] = {0: probDict[0], 1: probDict[1]}

        elif _testStateDict(probDict, len(nodes)):
            for node in nodes:
                if (isinstance(self._attribution[node], tuple)
                    and self._attribution[node] != tuple(nodes)): 

                    print("Warning, node %s was previously bound to other" \
 "node" % node,
                          file=stderr)
                    self._erase_binding(node)
                    self._attribution[node] = tuple(nodes)

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


    def _strMut(self, mutations, bnd=False):
        return _strNetwork(self, mutations, bnd)
        
    def print_istate(self, out=stdout):
        print(_str_istateList(self._initState), file=out)


def _testStateDict(stDict, nbState):
    """Check if stateDict is a good parameter for set_istate."""
    def goodTuple(t):
        return len(t) == nbState and all(x == 0 or x == 1 for x in t)

    
    if (not all(isinstance(t, tuple) for t in stDict)
        or not all(goodTuple(t) for t in stDict)):
        print("Error, not all keys are good tuples of length %s" %nbState,
              file=stderr)
        return False
    elif (not all(x >= 0 for x in stDict.values())
          or not sum(stDict.values()) == 1):
        print("Error, the given values must be nonegative and sum up to 1",
              file =stderr)
        return False
    else:
        return True
 

def _strNode(nd, mutations={}, bnd=False):
    string = ""
    if nd.name not in mutations or mutations[nd.name]=="WT":
        rt_up_str = ("$u_" + nd.name) if bnd else str(nd.rt_up)
        rt_down_str = ("$d_" + nd.name) if bnd else str(nd.rt_down)
        string = "\n".join(["Node " + nd.name + " {",
                            "\tlogic = " + nd.logExp + ";",
                            ("\trate_up = @logic ? " + rt_up_str
                             + " : 0;"),
                            ("\trate_down = @logic ? 0 : "
                             + rt_down_str + ";"),
                            "}"])
    elif mutations[nd.name]=="ON":
        string = "\n".join(["Node " + nd.name + " {",
                            "\tlogic = " + nd.logExp + ";",
                            "\trate_up = 1E+99;",
                            "\trate_down = 0;",
                            "}"])
    else:
        assert(mutations[nd.name]=="OFF")
        string = "\n".join(["Node " + nd.name + " {",
                            "\tlogic = " + nd.logExp + ";",
                            "\trate_up = 0;",
                            "\trate_down = 1E+99;",
                            "}"])
    return string


def _strNetwork(nt, mutations={}, bnd=False):
    string = _strNode(nt.nodeList[0])
    if len(nt.nodeList) > 1:
       string += "\n"
       string += "\n\n".join(_strNode(nd, mutations, bnd) for nd in nt.nodeList[1:])
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
        
