import unittest
from checksym import remove, compare
from sympy import Integral, symbols, exp, oo, E, sqrt, I, pi
from sympy.physics.quantum import hbar

class TestCheckFunctions(unittest.TestCase):
    
    def test_compare_with_symbols_one_symbol(self):
        '''Case of only one symbols. Debug not iterable error.

        Test derived from actual use case, involving uncertainty
        calculation.
        '''
        x = symbols("x", real=True)
        a = symbols("a", positive=True)
        alpha = symbols("alpha")
        formula = Integral(x**2 * E**(- alpha * x**2), (x, -oo, oo))
        formula = formula.subs(alpha, 1/(a**2))
        formula2 = 1/(2*alpha) * Integral(E**(- alpha * x**2), (x, -oo, oo))
        formula2 = formula2.subs(alpha, 1/(a**2))
        result = compare(formula, formula2, a)
        self.assertEqual(None, result)
        pass

    def test_remove_fraction_from_mul_in_integral(self):
        '''Where a fraction within a Mul() within an integral is removed
        
        In this case, remove 1/a**4 from inside the integral.
        '''
        x = symbols("x", real=True)
        a = symbols("a", positive=True)
        n = symbols("N", real=True)
        expr = Integral(-hbar**2*n**2*x**2*exp(-x**2/a**2)/a**4, (x, -oo, oo))
        modified_expr = remove(expr, 1/(a**4))
        self.assertEqual(Integral(-hbar**2*n**2*x**2*exp(-x**2/a**2), (x, -oo, oo)),
            modified_expr)
        pass

    def test_remove_from_sum_in_denominator(self):
        '''Where an expression is removed from a sum in a denominator.

        '''
        a, b, c = symbols("a b c", real=True)
        expr = a / ( b + c )
        modified_expr = remove(expr, b)
        self.assertEqual(a / c, modified_expr)
        pass

    def test_constant_in_and_out_of_integral(self):
        '''A case where constant gives a different result, in and out of the integral
        
        '''
        x = symbols("x", real=True)
        p = symbols("p", real=True)
        a = symbols("a", positive=True)
        n = symbols("N", real=True)
        expr1 = sqrt(2)*Integral(n*exp(-x**2/(2*a**2))*exp(-I*p*x/hbar), (x, -oo, oo))/(2*sqrt(hbar)*sqrt(pi))
        expr2 = sqrt(2)*Integral(n*exp(-x**2/(2*a**2) - I*p*x/hbar), (x, -oo, oo))/(2*sqrt(hbar)*sqrt(pi))
        result = compare(expr1, expr2, a, p, n)
        print(result)
        self.assertEqual(None, result)
        pass


if __name__ == '__main__':
    unittest.main()
