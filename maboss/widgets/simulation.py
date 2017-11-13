from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


def wg_set_output(simul):

    node_list = list(simul.network.keys())
    selector = widgets.SelectMultiple(options=node_list, description='Output')
    display(selector)
    def trigger(b):
        simul.network.set_output(selector.value)
    ok_button = widgets.Button(description='Ok')
    ok_button.on_click(trigger)
    display(ok_button)
