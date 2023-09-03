from sympy import lambdify
from checksym.util import compare_to_significance_complex
from .compare_interface import CompareInterface

class SciPyNumPy(CompareInterface):
    def compare_for_symbols_with_test_values(self, expr1, expr2, symbols, test_value_set, significance):
        significance = 10
        expr1_evaled = expr1.doit()
        expr2_evaled = expr2.doit()
        if len(symbols) != len(test_value_set):
            raise Exception("Invalid test_value_set length")
        lambdify_modules = ['scipy', 'numpy']
        test_value_set_for_lambdify = list(map(self.cleanup_for_lambdify, test_value_set))
        this_expr1_lambdify_evaled = lambdify(symbols, expr1_evaled, lambdify_modules)(*test_value_set_for_lambdify)
        this_expr2_lambdify_evaled = lambdify(symbols, expr2_evaled, lambdify_modules)(*test_value_set_for_lambdify)
        if not compare_to_significance_complex(
            this_expr1_lambdify_evaled.real, this_expr1_lambdify_evaled.imag,
            this_expr2_lambdify_evaled.real, this_expr1_lambdify_evaled.imag, significance):
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
    
    def cleanup_for_lambdify(self, expr):
        real_imag = expr.as_real_imag()
        return float(real_imag[0]) + 1j * float(real_imag[1])