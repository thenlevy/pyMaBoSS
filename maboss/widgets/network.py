from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
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
        for nd in selector.value:
            network.set_istate(nd, istate)
        print("Done !")
    ok_button = widgets.Button(description='Ok')
    ok_button.on_click(trigger)
    display(ok_button)
