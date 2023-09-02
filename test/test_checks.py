import unittest
from checksym import remove, Compare, get_test_numbers_for_assumptions
from sympy import Integral, symbols, exp, oo, E, sqrt, I, pi, conjugate, Abs, im
from sympy.physics.quantum import hbar
from pprint import pp

class TestCheckFunctions(unittest.TestCase):

    def setUp(self):
        self.compare = Compare()

    def test_compare_with_symbols_one_symbol(self):
        """
        Case of only one symbols. Debug not iterable error.

        Test derived from actual use case, involving uncertainty
        calculation.
        """
        x = symbols("x", real=True)
        a = symbols("a", positive=True)
        alpha = symbols("alpha")
        formula = Integral(x**2 * E**(- alpha * x**2), (x, -oo, oo))
        formula = formula.subs(alpha, 1/(a**2))
        formula2 = 1/(2*alpha) * Integral(E**(- alpha * x**2), (x, -oo, oo))
        formula2 = formula2.subs(alpha, 1/(a**2))
        result = self.compare.compare(formula, formula2, a)
        self.assertEqual(None, result)

    def test_remove_fraction_from_mul_in_integral(self):
        """
        Where a fraction within a Mul() within an integral is removed
        
        In this case, remove 1/a**4 from inside the integral.
        """
        x = symbols("x", real=True)
        a = symbols("a", positive=True)
        n = symbols("N", real=True)
        expr = Integral(-hbar**2*n**2*x**2*exp(-x**2/a**2)/a**4, (x, -oo, oo))
        modified_expr = remove(expr, 1/(a**4))
        self.assertEqual(Integral(-hbar**2*n**2*x**2*exp(-x**2/a**2), (x, -oo, oo)),
            modified_expr)
        
    def test_remove_multiple(self):
        x, y, z = symbols("x y z")
        expr = x * y * z
        modified_expr = remove(expr, x, y)
        self.assertEqual(z, modified_expr)

    def test_remove_from_sum_in_denominator(self):
        """
        Where an expression is removed from a sum in a denominator.

        """
        a, b, c = symbols("a b c", real=True)
        expr = a / ( b + c )
        modified_expr = remove(expr, b)
        self.assertEqual(a / c, modified_expr)

    # I can't get this one working 
    #
    # def test_constant_in_and_out_of_integral(self):
    #     """
    #     A case where constant gives a different result, in and out of the integral
    #
    #     """
    #     x = symbols("x", real=True)
    #     p = symbols("p", real=True)
    #     a = symbols("a", positive=True)
    #     n = symbols("N", real=True)
    #     expr1 = sqrt(2)*Integral(exp((-x**2/(2*a**2)) *  exp(- I*p*x/hbar)), (x, -1, 1))/(2*sqrt(hbar)*sqrt(pi))
    #     expr2 = sqrt(2)*Integral(exp((-x**2/(2*a**2)) + (- I*p*x/hbar)), (x, -1, 1))/(2*sqrt(hbar)*sqrt(pi))
    #     #expr1 = sqrt(2)*Integral(exp(-x**2 - I*x), (x, -1, 1))
    #     #expr2 = sqrt(2)*Integral(exp(-x**2 - I*x), (x, -1, 1))
    #     result = compare(expr1, expr2, a, p, n)
    #     pp(result)
    #     self.assertEqual(None, result)
    #     pass


    def test_gaussian_convert_formula(self):
        alpha, beta = symbols("alpha, beta", real=True, positive=True)
        x = symbols("x")
        expr1 = Integral(exp(-alpha*x**2 + beta*x), (x, -oo, oo))
        expr2 = sqrt(pi)*exp(beta**2/(4*alpha))/sqrt(alpha)
        result = self.compare.compare(expr1, expr2, alpha, beta)
        self.assertEqual(None, result)

    def test_moving_constants_around(self):
        """
        Sanity test. Make sure a wrong factor results in a failures.
        
        """
        x = symbols("x", real=True)
        p = symbols("p", real=True)
        a = symbols("a", positive=True)
        n = symbols("N", real=True)
        expr1 = hbar*n**2*Integral(exp(-a**2*x**2/hbar**2), (x, -oo, oo))/2
        expr2 = hbar**2*Integral(n**2*a**2*exp(-a**2*p**2/hbar**2)/hbar, (p, -oo, oo))/a**2
        result = self.compare.compare(expr1, expr2, a, n)
        self.assertNotEqual(None, result)

    def test_integrate_small_value(self):
        """
        Sanity test. Make sure a wrong factor results in a failures.
        
        """
        x = symbols("x", real=True)
        a = symbols("a", real=True, positive=True)
        expr1 = Integral(exp(-x**2/hbar**2), (x, -oo, oo))/2
        expr2 = Integral(exp(-x**2/hbar**2), (x, -oo, oo))
        result = self.compare.compare(expr1, expr2, a)
        self.assertNotEqual(None, result)

    def test_moving_constants_around_2(self):
        """
        Sanity test. Make sure it doesn't matter which variable name we integrate over.
        
        """
        x = symbols("x", real=True)
        p = symbols("p", real=True)
        a = symbols("a", positive=True)
        n = symbols("N", real=True)
        expr1 = hbar*n**2*Integral(exp(-a**2*x**2/hbar**2), (x, -oo, oo))/2
        expr2 = hbar**2*Integral(n**2*a**2*exp(-a**2*p**2/hbar**2)/hbar, (p, -oo, oo))/(2*a**2)
        result = self.compare.compare(expr1, expr2, a, n)
        self.assertEqual(None, result)

    def test_complex_number(self):
        z = symbols("z", complex=True)
        n = symbols("n", positive=True)
        x = symbols("x", real=True)
        expr1 = 2*(n+E**z*x**2)
        expr2 = 2*n+2*E**z*x**2
        result = self.compare.compare(expr1, expr2, z, n, x)
        self.assertEqual(None, result)

    def test_complex_number_with_gaussian(self):
        z = symbols("z", complex=True)
        n = symbols("n", positive=True)
        x = symbols("x", real=True)
        expr1 = Integral(n*E**(z*x**2), (x, -oo, oo))
        expr2 = n*Integral(E**(z*x**2), (x, -oo, oo))
        result = self.compare.compare(expr1, expr2, z, n)
        self.assertEqual(None, result)

    def test_complex_number_with_gaussian_reversed(self):
        z = symbols("z", complex=True)
        n = symbols("n", positive=True)
        x = symbols("x", real=True)
        expr1 = Integral(n*E**(z*x**2), (x, oo, -oo))
        expr2 = n*Integral(E**(z*x**2), (x, oo, -oo))
        result = self.compare.compare(expr1, expr2, z, n)
        self.assertEqual(None, result)

    def test_complex_number_with_gaussian_2(self):
        x = symbols("x", real=True)
        Delta = symbols("Delta", complex=True, real_part_positive=True)
        expr1 = Integral(exp(-x**2/(Delta**2))*exp(-x**2/(conjugate(Delta)**2)), (x, -oo, oo))
        expr2 = Integral(exp(-x**2*(conjugate(Delta)**2 + Delta**2)/(Abs(Delta)**4)), (x, -oo, oo))
        result = self.compare.compare(expr1, expr2, Delta)
        self.assertEqual(None, result)

    def test_complex_number_with_gaussian_3(self):
        n = symbols("n", positive=True)
        x = symbols("x", real=True)
        Delta = symbols("Delta", complex=True, real_part_positive=True)
        expr1 = Integral(n**2*x**2*exp(-x**2/(2*Delta**2))*exp(-x**2/(2*conjugate(Delta)**2)), (x, -oo, oo))
        expr2 = Integral(n**2*x**2*exp(-x**2*(conjugate(Delta)**2 + Delta**2)/(2*Abs(Delta)**4)), (x, -oo, oo))
        result = self.compare.compare(expr1, expr2, n, Delta)
        self.assertEqual(None, result)

    def test_complex_number_will_fail(self):
        z = symbols("z", complex=True)
        expr1 = z
        expr2 = 2*z
        result = self.compare.compare(expr1, expr2, z)
        self.assertNotEqual(None, result)

    def test_complex_number_will_fail_2(self):
        z = symbols("z", complex=True)
        expr1 = im(z)
        expr2 = im(2*z)
        result = self.compare.compare(expr1, expr2, z)
        self.assertNotEqual(None, result)

    def test_complex_number_will_fail_3(self):
        z = symbols("z", complex=True)
        x = symbols("x", real=True)
        expr1 = Integral(im(z), (x, -1, 1))
        expr2 = Integral(im(2*z), (x, -1, 1))
        result = self.compare.compare(expr1, expr2, z)
        self.assertNotEqual(None, result)

    def test_complex_number_integral(self):
        z = symbols("z", complex=True)
        x = symbols("x", real=True)
        expr1 = 2*Integral(im(z), (x, -1, 1))
        expr2 = Integral(im(2*z), (x, -1, 1))
        result = self.compare.compare(expr1, expr2, z)
        self.assertEqual(None, result)

if __name__ == '__main__':
    unittest.main()
