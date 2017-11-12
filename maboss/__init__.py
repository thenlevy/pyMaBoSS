from .network import Node, Network
from .simulation import Simulation, Result
from .gsparser import build_network, load_file


from colomoto_jupyter import IN_IPYTHON
if IN_IPYTHON:
    from colomoto_jupyter import jupyter_setup
    import ginsim

    menu = [
        {'name': 'Load network (MaBoSS format)',
         'snippet': ["mysimulation = maboss.load_file(\"filename\") #replace "
                     "filename by a file with extension .bnd or .cfg"]},
        {'name': 'Load network (zginml format)',
         'snippet': ["m = ginsim.open(\"myModel.zginml\")",
                     "ginsim.service(\"maboss\").export(m, \"mybdnfile.bnd\")",
                     "mysimulation = maboss.load_file(\"mybndfile.bnd\")"]}
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

    jupyter_setup("mymodule",
        label="MaBoSS",
        color="blue", # for menu and toolbar
        menu=menu,
        toolbar=toolbar,
        js_api=js_api)
