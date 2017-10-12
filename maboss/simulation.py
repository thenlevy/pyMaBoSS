"""Class that handles the parameters of a MaBoSS simulation."""


from sys import stderr, stdout
from .figures import plot_trajectory, plot_piechart
from contextlib import ExitStack
import uuid
import subprocess

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


class Simulation(object):
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
        self._mutations = {}

    def print_bnd(self, out=stdout):
        print(self.network._strMut(self._mutations), file=out)

    def print_cfg(self, out=stdout):
        self.network.print_istate(out=out)
        print('', file=out)

        for p in self.param:
            print(p + ' = ' + str(self.param[p]) + ';', file=out)

        for nd in self.network.nodeList:
            string = nd.name+'.is_internal = ' + str(int(nd.is_internal)) +';'
            print(string, file=out)

    def run(self, prefix=None):
        tmp = prefix is None # Indicates if the MaBoSS files should be temporary
        if prefix is None:
            prefix = str(uuid.uuid4())

        with ExitStack() as stack:
            bnd_file = stack.enter_context(open(prefix + '.bnd', 'w'))
            cfg_file = stack.enter_context(open(prefix + '.cfg', 'w'))
            self.print_bnd(out=bnd_file)
            self.print_cfg(out=cfg_file)
        
            
        err = subprocess.call(["MaBoSS", "-c", cfg_file.name, "-o", prefix,
                     bnd_file.name])
        if err:
            print("Error, MaBoSS returned non 0 value", file=stderr)
        else:
            print("MaBoSS returned 0", file=stderr)

        return Result(prefix)


    def mutate(self, node, state):
        if all([nd.name != node for nd in self.network.nodeList]):
            print("Error, unknown node %s" % node, file=stderr)
            return

        if state not in ["ON", "OFF", "WT"]:
            print("Error, state must be ON, OFF, or WT", file=stderr)
            return

        self._mutations[node] = state
        
            


class Result(object):

    def __init__(self, prefix):
        self._prefix=prefix


    def plot_trajectory(self):
        plot_trajectory(self._prefix) 
        

    def plot_piechart(self):
        plot_piechart(self._prefix)
    

    
