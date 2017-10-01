"""utilitary functions to manipulate boolean expressions."""


from sys import stderr
import pyparsing as pp

boolExp = pp.Forward()
varName = pp.Word(pp.alphas, pp.alphanums+'_')
boolCst = pp.oneOf("True False")
boolNot = pp.oneOf("! NOT")
boolBinOp = pp.oneOf("&& & AND || | OR ^ XOR")
lparen = pp.Suppress('(')
rparen = pp.Suppress(')')
boolExp << (boolCst | varName | (boolNot + boolExp) | (lparen + boolExp
                                                       + boolBinOp + boolExp
                                                       + rparen))


def _check_logic_syntax(str):
    """Return True iff str is a syntaxically correct boolean expression."""
    return boolExp.matches(str)


def _check_logic_defined(name_list, logic_list):
    """Check if the list of logic is consistant.

    Return True iff all expression in logic_list are syntaxically correct and
    all contains only variables present in name_list.
    """
    _check_logic_defined.failed = False

    # We modify the behaviour of boolExp.parseString so that the parsing also
    # check if variables exist.
    def check_var(var):
        if var[0] not in name_list:
            print("Error: unkown varriable %s" % var[0], file=stderr)
            _check_logic_defined.failed = True
        return var

    varName.setParseAction(check_var)

    for str in logic_list:
        if not _check_logic_syntax(str):
            print("Error: syntax error %s" % str, file=stderr)
            return False
        if _check_logic_defined.failed:
            varName.setParseAction(lambda x: x)
            return False

    varName.setParseAction(lambda x: x)
    return True
