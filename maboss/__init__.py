from .network import Node, Network
from .simulation import Simulation, simulations
from .result import Result, results
from .gsparser import build_network, load_file


from colomoto_jupyter import IN_IPYTHON
if IN_IPYTHON:
    from colomoto_jupyter import jupyter_setup
    from .widgets import *

    jupyter_setup("mymodule",
        label="MaBoSS",
        color="green", # for menu and toolbar
        menu=menu,
        toolbar=toolbar,
        js_api=js_api)

