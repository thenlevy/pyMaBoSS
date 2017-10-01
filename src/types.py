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

    def __init__(self, name, logExp=None, rt_up=None, rt_down=None):
        """
        Create a node not yet inserted in a network.

        logic, rt_up and rt_down are optional when creating the node but
        must be set before making a network.
        """
        self.name = name
        self.logExp = logExp
        self.rt_up = rt_up
        self.rt_down = rt_down

        if logExp:
            if not logic._check_logic_syntax(logExp):
                print("Waring, syntax error: %s" % logExp, file=stderr)
                print("logic set to None", file=stderr)
            self.logExp = None

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
            self.logExp = str
        else:
            print("Warning, syntax error: %s" % string, file=stderr)
            print("logExp was not modified", file=stderr)


class Network:
    """
    Represent a boolean network.

    Initialised with a list of Nodes whose logExp must contain only names
    present in the list.
    """

    def __init__(self, nodeList, stateList=None):
        self.names = [nd.name for nd in nodeList]
        self.logicExp = {nd.name: nd.logExp for nd in nodeList}
        self.state = {nd.name: False for nd in nodeList}

        if stateList:
            for nd in stateList.keys():
                self.state[nd] = stateList[nd]

        if not logic._check_logic_defined(self.names,
                                          [nd.logExp for nd in nodeList]):
            raise ValueError("Some logic rule had unkown variables")
