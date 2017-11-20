"""Create code cell taken from https://github.com/ipython/ipython/issues/4983"""
import base64
from IPython.display import Javascript, display
from IPython.utils.py3compat import str_to_bytes, bytes_to_str
def create_code_cell(code='', where='below'):
    """Create a code cell in the IPython Notebook.

    Parameters
    code: unicode
        Code to fill the new code cell with.
    where: unicode
        Where to add the new code cell.
        Possible values include:
            at_bottom
            above
            below"""
    encoded_code = bytes_to_str(base64.b64encode(str_to_bytes(code)))
    display(Javascript("""
        var code = IPython.notebook.insert_cell_{0}('code');
        code.set_text(atob("{1}"));
    """.format(where, encoded_code)))
