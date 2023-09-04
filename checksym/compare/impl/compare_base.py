from abc import ABC, abstractmethod
from checksym.util import compare_to_significance_complex

class CompareBase(ABC):

    def __init__(self, expr1, expr2, symbols, test_value_set, significance=10):
        self.expr1 = expr1
        self.expr2 = expr2
        self.symbols = symbols
        self.test_value_set = test_value_set
        self.significance = significance
    
    def compare_for_symbols_with_test_values(self, test_value_set):
        if len(self.symbols) != len(test_value_set):
            raise Exception("Invalid test_value_set length")
        self.test_value_set = test_value_set
        (expr1_final, expr1_real, expr1_imag, expr2_final, expr2_real, expr2_imag) = self._evaluate()
        if not compare_to_significance_complex(
            expr1_real, expr1_imag,
            expr2_real, expr2_imag, self.significance):
            return {
                'symbols' : self.symbols,
                'test_value_set': self.test_value_set,
                'expr1': self.expr1,
                'expr1_final': expr1_final,
                'expr2': self.expr2,
                'expr2_final': expr2_final
            }
        return None       

    @abstractmethod
    def _evaluate(self):
        pass