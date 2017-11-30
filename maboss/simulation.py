"""Class that handles the parameters of a MaBoSS simulation."""


from sys import stderr, stdout
from .figures import make_plot_trajectory, plot_piechart, plot_fix_point
from contextlib import ExitStack
import os
import subprocess
import tempfile
import shutil
import pyparsing as pp
import matplotlib.pyplot as plt

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
        kwargs : parameters of the simulation
        """
        self.param = _default_parameter_list
        if 'palette' in kwargs:
            self.palette = kwargs.pop('palette')
        else:
            self.palette = {}
        for p in kwargs:
            if p in _default_parameter_list:
                self.param[p] = kwargs[p]
            else:
                print("Warning: unused parameter %s" % p, file=stderr)

        self.network = nt
        self._mutations = {}

    def update_parameters(self, **kwargs):
        for p in kwargs:
            if p in _default_parameter_list:
                self.param[p] = kwargs[p]
            else:
                print("Warning: unused parameter %s" % p, file=stderr)

    def copy(self):
        new_network = self.network.copy()
        return Simulation(new_network, **(self.param), palette=self.palette)

    def print_bnd(self, out=stdout):
        print(self.network, file=out)

    def print_cfg(self, out=stdout):
        for nd in self.network.nodeList:
            print("$u_" + nd.name + " = " + str(nd.rt_up) + ';', file=out)
            print("$d_" + nd.name + " = " + str(nd.rt_down) + ';', file=out)
        self.network.print_istate(out=out)
        print('', file=out)

        for p in self.param:
            print(p + ' = ' + str(self.param[p]) + ';', file=out)

        for nd in self.network.nodeList:
            string = nd.name+'.is_internal = ' + str(int(nd.is_internal)) + ';'
            print(string, file=out)

    def run(self, save=False, prefix=None):
        """Run the simulation with MaBoSS and return a Result object.
        """

        return Result(self, save, prefix)


    def mutate(self, node, state):
        if node not in self.network:
            print("Error, unknown node %s" % node, file=stderr)
            return

        if state == "ON":
            self.network.set_istate(node, [0, 1])
            self.network[node].set_rate(1, 0)

        elif state == "OFF":
            self.network.set_istate(node, [1, 0])
            self.network[node].set_rate(0, 1)

        elif state == "WT":
            self.network.set_istate(node, [0.5, 0.5])
            self.network[node].set_rate(1, 1)

        else:
            print("Error, state must be ON, OFF, or WT", file=stderr)
            return


class Result(object):

    def __init__(self, simul, save, prefix):
        self._path = tempfile.mkdtemp()
        self._cfg = tempfile.mkstemp(dir=self._path, suffix='.cfg')[1]
        self._bnd = tempfile.mkstemp(dir=self._path, suffix='.bnd')[1]
        self._trajfig = None
        self._piefig = None
        self._fpfig = None
        self.palette = simul.palette

        with ExitStack() as stack:
            bnd_file = stack.enter_context(open(self._bnd, 'w'))
            cfg_file = stack.enter_context(open(self._cfg, 'w'))
            simul.print_bnd(out=bnd_file)
            simul.print_cfg(out=cfg_file)

        self._err = subprocess.call(["MaBoSS", "-c", self._cfg, "-o",
                                     self._path+'/res', self._bnd])
        if self._err:
            print("Error, MaBoSS returned non 0 value", file=stderr)
        else:
            print("MaBoSS ended successfuly")

    def plot_trajectory(self):
        if self._trajfig is None:
            if self._err:
                print("Error, plot_trajectory cannot be called because MaBoSS"
                      "returned non 0 value", file=stderr)
                return
            self._trajfig = self.make_trajectory()
            return self._trajfig
        else:
            return self._trajfig.show()

    def make_trajectory(self):
        prefix = self._path+'/res'
        self._trajfig, self._trajax = plt.subplots(1, 1)
        make_plot_trajectory(prefix, self._trajax, self.palette)
        return self._trajfig

    def plot_piechart(self):
        if self._piefig is None:
            if self._err:
                print("Error, plot_piechart cannot be called because MaBoSS"
                      "returned non 0 value", file=stderr)
                return
            self._piefig, self._pieax = plt.subplots(1, 1)
            plot_piechart(self._path+'/res', self._pieax, self.palette)
            return self._piefig
        else:
            return self._piefig

    def plot_fixpoint(self):
        if self._fpfig is None:
            if self._err:
                print("Error maboss previously returned non 0 value",
                      file=stderr)
                return
            self._fpfig, self._fpax = plt.subplots(1, 1)
            plot_fix_point(self._path+'/res', self._fpax, self.palette)
            return self._fpfig


    def save(self, prefix, replace=False):
        if not _check_prefix(prefix):
            return

        # Create the results directory
        try:
            os.mkdir(prefix)
        except FileExistsError:
            if not replace:
                print('Error directory already exists: %s' % prefix,
                      file=stderr)
                return
            elif prefix.startswith('rpl_'):
                shutil.rmtree(prefix)
                os.mkdir(prefix)
            else:
                print('Error only directries begining with "rpl_" can be'
                      'replaced', file=stderr)
                return

        # Moves all the files into it
        shutil.copy(self._bnd, prefix+'/%s.bnd' % prefix)
        shutil.copy(self._cfg, prefix+'/%s.cfg' % prefix)

        maboss_files = filter(lambda x: x.startswith('res'),
                              os.listdir(self._path))
        for f in maboss_files:
            shutil.copy(self._path + '/' + f, prefix)

    def __del__(self):
        shutil.rmtree(self._path)


def _check_prefix(prefix):
    if type(prefix) is not str:
        print('Error save method expected string')
        return False
    else:
        prefix_grammar = pp.Word(pp.alphanums + '_-')
        return prefix_grammar.matches(prefix)
