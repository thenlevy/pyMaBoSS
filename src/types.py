"""Definitions of the different classes provided to the user."""

from src import logic
from sys import stderr


class Node:
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
                  istate=[0.5, 0.5]):
        """
        Create a node not yet inserted in a network.

        logic, rt_up and rt_down are optional when creating the node but
        must be set before making a network.
        """
        self.name = name
        self.set_logic(logExp)
        self.set_rate(rt_up, rt_down)
        self.set_istate(istate)


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

    def set_istate(self, istate):
        """
        Set the initial state probability of the node.
        
        istate must be a list [p1, p2] with 0 <= p1, p2 <= 1 and p1 + p2 == 1.
        """
        if len(istate) != 2:
            print("Error, istate must be of length 2. Set to default",
                  file=stderr)
            self.istate = [0.5, 0.5]
        elif istate[0] < 0 or istate[1] < 0 or istate[0] + istate[1] != 1:
            print("Error, inconsistant value for istate. Set to default",
                  file=stderr)
            self.istate = [0.5, 0.5]
        else:
            self.istate = istate
        
    def __str__(self):
        return _strNode(self)


class Network:
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

    def __str__(self):
        return _strNetwork(self)



def _strNode(nd):
    string = "\n".join(["Node " + nd.name + " {",
                        "\tlogic = " + nd.logExp + ";",
                        "\trate_up = @logic ? " + str(nd.rt_up) + " : 0;",
                        "\trate_down = @logic ? 0 : " + str(nd.rt_down) + ";",
                        "}"])
    return string

def _strNetwork(nt):
    string = _strNode(nt.nodeList[0])
    if len(nt.nodeList) > 1:
       string += "\n" + "\n\n".join(_strNode(nd) for nd in nt.nodeList[1:])
    return string
