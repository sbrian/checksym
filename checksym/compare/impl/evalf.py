from checksym.util import compare_to_significance_complex
from .compare_base import CompareBase
from sympy import re, im

class Evalf(CompareBase):

    def _evaluate(self):
        """
        Doesn't work yet
        """
        full_test_values = list(zip(self.symbols, self.test_value_set))
        expr1_evaled = self.expr1.subs(full_test_values).evalf()
        expr2_evaled = self.expr2.subs(full_test_values).evalf()
        return (expr1_evaled, re(expr1_evaled), im(expr1_evaled),
                expr2_evaled, re(expr2_evaled), im(expr2_evaled))
    
    def _check_for_zero(self, value):
        return value == 0