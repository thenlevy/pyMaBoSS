
import ipywidgets as widgets

from colomoto_jupyter.widget_utils import jupyter_replace_cell_call

import ast

def wg_set_output(simul):
    node_list = list(simul.network.keys())
    selector = widgets.SelectMultiple(options=node_list, description='Output')
    display(selector)
    def trigger(b):
        jupyter_replace_cell_call("wg_set_output",
                "set_output", (selector.value,))
    ok_button = widgets.Button(description='Ok')
    ok_button.on_click(trigger)
    display(ok_button)

def wg_make_mutant(simul):
    node_list = list(simul.network.keys())
    gene_selector = widgets.SelectMultiple(options=node_list,
                                           description='gene')
    mutation_selector = widgets.Select(options=['ON', 'OFF'],
                                       description='mutation')
    display(gene_selector)
    display(mutation_selector)
    def trigger(b):
        jupyter_replace_cell_call("wg_make_mutant",
                "copy_and_mutate", (gene_selector.value, mutation_selector.value))
    ok_button = widgets.Button(description='Ok')
    ok_button.on_click(trigger)
    display(ok_button)

def wg_set_istate(simul):
    network = simul.network
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
        jupyter_replace_cell_call("wg_set_istate",
                "set_nodes_istate", (selector.value, istate))

    ok_button = widgets.Button(description='Ok')
    ok_button.on_click(trigger)
    display(ok_button)


