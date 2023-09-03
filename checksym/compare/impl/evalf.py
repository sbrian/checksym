from checksym.util import compare_to_significance
from .compare_interface import CompareInterface

class Evalf(CompareInterface):
    """
    Doesn't work yet
    """
    def compare_for_symbols_with_test_values(self, expr1, expr2, symbols, test_value_set, significance):
        significance = 10
        full_test_values = zip(symbols, test_value_set)
        expr1_evaled = expr1.doit().subs(full_test_values).evalf()
        expr2_evaled = expr2.doit().subs(full_test_values).evalf()
        if not compare_to_significance(expr1_evaled, expr2_evaled, significance):
            return {
                'symbols' : symbols,
                'test_value_set': test_value_set,
                'expr1': expr1,
                'expr1_evaluated': expr1,
                'expr1_final': this_expr1_lambdify_evaled,
                'expr2': expr2,
                'expr2_evaluated': expr2,
                'expr2_final': this_expr2_lambdify_evaled
            }
        return None
    