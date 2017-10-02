"""User interface for MaBoSS."""


import subprocess
from sys import stderr
from contextlib import ExitStack
from src.simulation import Simulation
from src.types import Node, Network

def export_and_run(simul, output='a'):
    """
    Print simul as in a .bnd and a .cfg file and run MaBoSS on it.

    MaBoSS needs to be accessible from your $PATH for this function to run.
    """
    with ExitStack() as stack: 
        bnd_file = stack.enter_context(open(output + '.bnd', 'w'))
        cfg_file = stack.enter_context(open(output + '.cfg', 'w'))
        simul.print_bnd(out=bnd_file)
        simul.print_cfg(out=cfg_file)

    err = subprocess.call(["MaBoSS", "-c", cfg_file.name, "-o", output,
                     bnd_file.name])
    if err:
        print("Error, MaBoSS returned non 0 value", file=stderr)
    else:
        print("MaBoSS returned 0", file=stderr)
    



