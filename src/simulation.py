"""Class that handles the parameters of a MaBoSS simulation."""


from sys import stderr, stdout

_default_parameter_list = {'time_tick': 0.1,
                  'max_time': 4,
                  'sample_count': 10000,
                  'discrete_time': 0,
                  'use_physrandgen': 1,
                  'seed_pseudorandom': 0,
                  'display_traj': 0,
                  'statdist_traj_count': 0,
                  'statdist_cluster_threshold': 1,
                  'thread_count': 1,
                  'statdist_similarity_cache_max_size': 20000
                  }


def _str_istate(nd):
    "String representing the initial state probability in cfg format."""
    return ('[' + nd.name + '].istate = '
            + str(nd.istate[0]) + '[0] , '
            + str(nd.istate[1]) + '[1];')


class Simulation():
    def __init__(self, nt, **kwargs):
        """
        Initialize the Simulation object.

        nt : a Network object
        kwarg : parameters of the simulation
        """
        self.param = _default_parameter_list
        for p in kwargs:
            if p in _default_parameter_list:
                self.param[p] = kwarg[p]
            else:
                print("Warning: unused parameter %s" % p, file=stderr)

        self.network = nt

    def print_bnd(self, out=stdout):
        print(self.network, file=out)

    def print_cfg(self, out=stdout):
        for nd in self.network.nodeList:
            print(_str_istate(nd))
        print('')

        for p in self.param:
            print(p + ' = ' + str(self.param[p]) + ';')
