from abc import ABC, abstractmethod

class CompareInterface(ABC):

    @abstractmethod
    def compare_for_symbols_with_test_values(self, expr1, expr2, symbols, test_value_set, significance):
        pass