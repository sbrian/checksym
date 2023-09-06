from abc import ABC, abstractmethod
from checksym.util import compare_to_significance_complex
from checksym.compare.compare_exception import CompareException
from pprint import pformat

class CompareBase(ABC):

    def __init__(self, expr1, expr2, symbols, significance, convert_exceptions):
        self.expr1 = expr1
        self.expr2 = expr2
        self.symbols = symbols
        self.significance = significance
        self.convert_exceptions = convert_exceptions
    
    def compare_for_symbols_with_test_values(self, test_value_set):
        if len(self.symbols) != len(test_value_set):
            raise Exception("Invalid test_value_set length")
        self.test_value_set = test_value_set
        result_dict = {
                'symbols' : self.symbols,
                'test_value_set': self.test_value_set,
                'expr1': self.expr1,
                'expr2': self.expr2
            }
        try:
            (expr1_final, expr1_real, expr1_imag, expr2_final, expr2_real, expr2_imag) = self._evaluate()
        except Exception as e:
            if self.convert_exceptions:
                result_dict['exception'] = str(e)
                return result_dict
            else:
                e.add_note(pformat(result_dict))
                raise e
        
        result_dict['expr1_final'] = expr1_final
        result_dict['expr2_final'] = expr2_final

        if self._check_for_zero(expr1_final) or self._check_for_zero(expr2_final):
            result_dict['message'] = "Some expression evaluated to 0. This usually means values got out of supported ranges."
            return result_dict

        try:
            if not compare_to_significance_complex(
                expr1_real, expr1_imag,
                expr2_real, expr2_imag, self.significance):
                return result_dict
        except Exception as e:
            if self.convert_exceptions:
                result_dict['exception'] = str(e)
                return result_dict
            else:
                e.add_note(pformat(result_dict))
                raise e

        return None       

    @abstractmethod
    def _evaluate(self):
        pass

    @abstractmethod
    def _check_for_zero(self, value):
        pass