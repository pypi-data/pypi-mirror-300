from pycinante.utils import export

@export
def is_valexp(exp):
    """
    Return the expression is a valid value expression, i.e. {variable}.
    """
    return exp.startswith("{") and exp.endswith("}")

@export
def eval_valexp(exp, context=None):
    """
    Return the value that is evaluated from the value expression.
    """
    return eval(exp[1:-1], context) if is_valexp(exp) else exp
