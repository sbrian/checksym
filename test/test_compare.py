import unittest
from checksym import Compare, remove
from sympy import Integral, symbols, exp, oo, E, sqrt, I, pi, conjugate, Abs, im, simplify, expand, diff, UnevaluatedExpr
from sympy.physics.quantum import hbar
from pprint import pp

class TestCompare(unittest.TestCase):

    def setUp(self):  
        self.compare = Compare(convert_exceptions=True)

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
        self.assertCompareResultSuccess(result)

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
        #pp(result)
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

    def test_integrate_small_value_ensure_non_zero(self):
        """
        Sanity test. They are same, but will it fail due to values being zero?
        
        """
        x = symbols("x", real=True)
        a = symbols("a", real=True, positive=True)
        expr1 = Integral(exp(-x**2/hbar**2), (x, -oo, oo))
        expr2 = Integral(exp(-x**2/hbar**2), (x, -oo, oo))
        result = self.compare.compare(expr1, expr2, a)
        self.assertCompareResultSuccess(result)

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
        self.assertCompareResultSuccess(result)

    def test_complex_number(self):
        z = symbols("z", complex=True)
        n = symbols("n", positive=True)
        x = symbols("x", real=True)
        expr1 = 2*(n+E**z*x**2)
        expr2 = 2*n+2*E**z*x**2
        result = self.compare.compare(expr1, expr2, z, n, x)
        self.assertCompareResultSuccess(result)

    def test_simplest_complex_number_with_gaussian(self):
        '''
        This only verifies that nothing goes to 0
        '''
        z = symbols("z", complex=True)
        n = symbols("n", positive=True)
        x = symbols("x", real=True)
        expr1 = Integral(E**(-x**2), (x, -oo, oo))
        expr2 = Integral(E**(-x**2), (x, -oo, oo))
        result = self.compare.compare(expr1, expr2, z, n)
        self.assertCompareResultSuccess(result)

    def test_complex_number_with_gaussian(self):
        z = symbols("z", complex=True)
        n = symbols("n", positive=True)
        x = symbols("x", real=True)
        expr1 = Integral(n*E**(z*x**2), (x, -oo, oo))
        expr2 = n*Integral(E**(z*x**2), (x, -oo, oo))
        result = self.compare.compare(expr1, expr2, z, n)
        self.assertCompareResultSuccess(result)

    def test_complex_number_with_gaussian_reversed(self):
        z = symbols("z", complex=True)
        n = symbols("n", positive=True)
        x = symbols("x", real=True)
        expr1 = Integral(n*E**(z*x**2), (x, oo, -oo))
        expr2 = n*Integral(E**(z*x**2), (x, oo, -oo))
        result = self.compare.compare(expr1, expr2, z, n)
        self.assertCompareResultSuccess(result)

    def test_complex_number_with_gaussian_2(self):
        """
        This will get converted to an integral from -1 to 1 that evaluates to 2.0281284727644744

        Verified with Mathematica
        delta := 12/5 - 24*\\[ImaginaryI]/5
        N[Integrate[\\[ExponentialE]^(-x^2/delta^2)*\\[ExponentialE]^(-x^2/Conjugate[delta]^2), {x, -1, 1}]]
        """
        x = symbols("x", real=True)
        Delta = symbols("Delta", complex=True, real_part_positive=True)
        expr1 = Integral(exp(-x**2/(Delta**2))*exp(-x**2/(conjugate(Delta)**2)), (x, -oo, oo))
        expr2 = Integral(exp(-x**2*(conjugate(Delta)**2 + Delta**2)/(Abs(Delta)**4)), (x, -oo, oo))
        result = self.compare.compare(expr1, expr2, Delta)
        self.assertCompareResultSuccess(result)

    def test_complex_number_with_gaussian_3(self):
        n = symbols("n", positive=True)
        x = symbols("x", real=True)
        Delta = symbols("Delta", complex=True, real_part_positive=True)
        expr1 = Integral(n**2*x**2*exp(-x**2/(2*Delta**2))*exp(-x**2/(2*conjugate(Delta)**2)), (x, -oo, oo))
        expr2 = Integral(n**2*x**2*exp(-x**2*(conjugate(Delta)**2 + Delta**2)/(2*Abs(Delta)**4)), (x, -oo, oo))
        result = self.compare.compare(expr1, expr2, n, Delta)
        self.assertCompareResultSuccess(result)

    def test_complex_number_with_gaussian_4_with_error(self):
        """
        This will fail on a compare, and then do the retry that gives the exception, but we want to test
        that it returns the failure from the compare, not the one that gives the exception
        """
        n = symbols("n", positive=True)
        x = symbols("x", real=True)
        Delta = symbols("Delta", complex=True, real_part_positive=True)
        expr1 = hbar**2*n**2*Integral(x**2*exp(-x**2*(conjugate(Delta)**2 + Delta**2)/(2*Abs(Delta)**4)), (x, -1, 1))/(Delta**2*conjugate(Delta)**2)
        expr2 = hbar**2*n**2*Abs(Delta)**4*Integral(exp(-x**2*(conjugate(Delta)**2 + Delta**2)/(2*Abs(Delta)**4)), (x, -1, 1))/(Delta**2*(conjugate(Delta)**2 + Delta**2)*conjugate(Delta)**2)
        result = self.compare.compare(expr1, expr2, n, Delta) 
        self.assertNotEqual(None, result)
        self.assertFalse(result.get('error'))
        self.assertFalse(result.get('exception'))



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
        self.assertCompareResultSuccess(result)

    def test_integral_that_is_wrong_without_doit(self):
        """
        Trying without doit(), we get

        {'symbols': (a, n),
        'test_value_set': [13/10, 39/10],
        'expr1': Integral(hbar**2*n**2*x**2*exp(-x**2/a**2)/a**4, (x, -oo, oo)),
        'expr2': hbar**2*n**2*Integral(x**2*exp(-x**2/a**2), (x, -oo, oo))/a**4,
        'expr1_final': 1.1547787718384969e-67,
        'expr2_final': (1.153142455075021e-67+0j)}

        Make sure it falls back to trying again with doit()
        """
        x = symbols("x", real=True)
        a = symbols("a", positive=True)
        n = symbols("n", positive=True)
        expr1 = Integral(hbar**2*n**2*x**2*exp(-x**2/a**2)/a**4, (x, -oo, oo))
        expr2 = hbar**2*n**2*Integral(x**2*exp(-x**2/a**2), (x, -oo, oo))/a**4
        result = self.compare.compare(expr1, expr2, a, n)
        self.assertCompareResultSuccess(result)


    def test_compare_two_real_expressions(self):
        """
        1c from the exercises for Act 2 of Visual Differential Geometry
        and Forms
        """
        u, v, du, dv = symbols("u v du dv", Real=True)
        x = u**2 - v**2
        y = 2*u*v
        ds_squared = simplify(expand((diff(x, u)*du+diff(x, v)*dv)**2 + (diff(y, u)*du+diff(y, v)*dv)**2))
        ds_squared_a = UnevaluatedExpr(4)*(u**2+v**2)*(du**2+dv**2)
        result = self.compare.compare(ds_squared, ds_squared_a, u, v, du, dv)
        self.assertCompareResultSuccess(result)

    def test_detects_failure_to_get_all_free_variables(self):
        """
        I left out one "dv" variable. Make sure it gets the right emssage.
        """
        u, v, du, dv = symbols("u v du dv", Real=True)
        x = u**2 - v**2
        y = 2*u*v
        ds_squared = simplify(expand((diff(x, u)*du+diff(x, v)*dv)**2 + (diff(y, u)*du+diff(y, v)*dv)**2))
        ds_squared_a = UnevaluatedExpr(4)*(u**2+v**2)*(du**2+dv**2)
        result = self.compare.compare(ds_squared, ds_squared_a, u, v, dv)
        self.assertNotEqual(None, result)
        self.assertEqual(result["exception"], "Result is still an expression. Check to be sure all free variables are passed in the compare call.")


    def assertCompareResultSuccess(self, result):
        if result != None:
            raise AssertionError("Compare failed", result)

if __name__ == '__main__':
    unittest.main()
