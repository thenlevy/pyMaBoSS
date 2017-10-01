"""utilitary functions to manipulate boolean expressions."""


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
