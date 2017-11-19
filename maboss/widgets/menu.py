
menu = [
    {'name': 'Load network (MaBoSS format)',
     'snippet': ["mysimulation = maboss.load_file(\"filename\")"]},

    {'name': 'Load network (zginml format)',
     'snippet': ["m = ginsim.open(\"myModel.zginml\")",
                 "ginsim.service(\"maboss\").export(m, \"mybndfile.bnd\")",
                 "master_simulation = maboss.load_file(\"mybndfile.bnd\")"]},

    {'name': 'Network',
     'sub-menu': [
         {'name': 'Set istate',
          'snippet': ["wg_set_istate(master_simulation.network)"]}
     ]},

    {'name': 'Simulation',
     'sub-menu': [
          {'name': 'Create mutant',
           'snippet': ["mutant_simulation = maboss.wg_make_mutant(master_simulation)"]},

          {'name': 'Run',
           'snippet': ["master_results = master_simulation.run()"]},

          {'name': 'Set initial states',
           'snippet': ["master_simulation.network.set_istate([\"mygenelist\"],{})"]},

          {'name': 'Set output',
           'snippet': ["wg_set_output(master_simulation)"]},

     ]},

    {'name': 'Results',
     'sub-menu': [
                  {'name': 'Save results',
                   'snippet': ["master_results.save(\"master\", replace=False)"]},

                  {'name': 'Plot piechart',
                   'snippet': ["master_results.plot_piechart()"]},

                  {'name': 'Plot trajectory',
                   'snippet': ["master_results.plot_trajectory()"]}]
     }
]

toolbar = [
    {"name": "Label",
     "setup": {
        "icon": "fa-something", # http://fontawesome.io/icons/
        "help": "tooltip text",
        "handler": "javascript_function_1"}}
]

## additional javascript functions, optional
js_api = {
    "javascript_function_1":
        """
        function () { alert("plop"); }
        """,
    "javascript_function_2":
        """
        function () { alert("bar"); }
        """,
}
