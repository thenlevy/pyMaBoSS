from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


def wg_set_output(simul):

    node_list = list(simul.network.keys())
    selector = widgets.SelectMultiple(options=node_list, description='Output')
    display(selector)
    def trigger(b):
        simul.network.set_output(selector.value)
        print("Done !")
    ok_button = widgets.Button(description='Ok')
    ok_button.on_click(trigger)
    display(ok_button)

def wg_make_mutant(simul):

    node_list = list(simul.network.keys())
    gene_selector = widgets.SelectMultiple(options=node_list,
                                           description='Output')
    mutation_selector = widgets.Select(options=['ON', 'OFF'],
                                       description='mutation')
    display(gene_selector)
    display(mutation_selector)
    mutant_simul = simul.copy()
    def trigger(b):
        for gene in gene_selector.value:
            mutant_simul.mutate(gene, mutation_selector.value)
    ok_button = widgets.Button(description='Ok')
    ok_button.on_click(trigger)
    display(ok_button)
    return mutant_simul
