from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from .code_cell import create_code_cell


def wg_set_output(simul):

    node_list = list(simul.network.keys())
    selector = widgets.SelectMultiple(options=node_list, description='Output')
    display(selector)
    def trigger(b):
        arg = str(selector.value)
        python_code = "master_simulation.network.set_output({})".format(arg)
        create_code_cell(python_code)
        print("Run cell below to validate,"
              " (you may have to change the network variable)")
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
    name_input = widgets.Text(value='', description='Mutant name')
    display(name_input)
    def trigger(b):
        python_code = []
        arg_gene = str(mutation_selector.value)
        arg_name = name_input.value
        arg_mut = mutation_selector.value
        python_code.append("genes = {}".format(arg_gene))
        python_code.append("{}_simulation = master_simulation.copy()".format(arg_name))
        python_code.append("for gene in genes:\n"
                           "    {}_simulation.mutate(gene, {})".format(arg_name,
                                                                       arg_mut))
        create_code_cell("\n".join(python_code))
        print("Run cell below to validate")
    ok_button = widgets.Button(description='Ok')
    ok_button.on_click(trigger)
    display(ok_button)
    return mutant_simul
