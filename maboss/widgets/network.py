from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython import get_ipython
from .code_cell import create_code_cell
import ast

def wg_set_istate(network):
    node_list = list(network.keys())
    selector = widgets.SelectMultiple(options=node_list, description='Nodes')
    display(selector)
    istate_input = widgets.Text(value='', description='istate')
    display(istate_input)

    def trigger(b):
        istate = ast.literal_eval(istate_input.value)
        if istate == 1:
            istate = [0, 1]
        elif istate == 0:
            istate = [1, 0]
        python_code=[]
        python_code.append('nodes = {}'.format(str(selector.value)))
        python_code.append('istate = {}'.format(str(istate)))
        python_code.append("for nd in nodes:\n    master_simulation.network.set_istate(nd, istate)")
        create_code_cell("\n".join(python_code))
        print("Run cell below to validate,"
              " (you may have to change the network variable)")
    ok_button = widgets.Button(description='Ok')
    ok_button.on_click(trigger)
    display(ok_button)

def wg_transfer_istate(network, model):
    for nd in network.keys():
        states = set()
        for state in [0, 1]:
            if network._initState[nd][state]:
                states.add(state)
        model.initial_state[nd] = states.pop() if len(states) == 1 else states
    print(model.initial_state)
