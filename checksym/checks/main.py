import itertools
from sympy import *

def get_test_numbers_for_assumptions(assumptions0):
    #integer_set = {1, 2, 10, 97, 100, 1000}
    integer_set = {1, 3}
    #rational_test_set = {Rational(1,4), Rational(56, 70), Rational(5, 3),
    #                     Rational(3, 5), Rational(100, 3), Rational(1000, 79)}
    rational_test_set = {Rational(1,4), Rational(5, 3)}
    #algebraic_test_set = {sqrt(2), sqrt(3)}
    algebraic_test_set = {sqrt(2)}
    #transcendental_test_set = {pi, 0.375*pi, E, 0.783*E, Rational(9,7)*E}
    transcendental_test_set = {pi, E}
    my_set = set()
    if assumptions0.get('complex') and not assumptions0.get('noninteger'):
        my_set.update(integer_set)
    if not assumptions0.get('integer'):
        my_set.update(rational_test_set)
    if not assumptions0.get('rational'):
        my_set.update(algebraic_test_set)
    if not assumptions0.get('algebraic'):
        my_set.update(transcendental_test_set)
    if not assumptions0.get('nonnegative'):
        my_set.update(set(map(lambda n: -n, my_set)))
    if not assumptions0.get('nonzero'):
        my_set.update({0})
    if assumptions0.get('real'):
        return my_set
    if assumptions0.get('imaginary'):
        return set(map(lambda n: n * I, my_set))
    return set(map(lambda n: n[0] + I * n[1], itertools.product(my_set, my_set)))

def get_test_numbers_for_symbol(symbol):
    return get_test_numbers_for_assumptions(symbol.assumptions0)

def test_values_replace(expr, symbols, test_value_set):
    replacement_tuples = []
    for n in range(0, len(symbols)):
        replacement_tuples.append((symbols[n], test_value_set[n]))
    return expr.subs(replacement_tuples)

def compare_for_symbols_with_test_values(expr1, expr2, symbols, test_value_set):
    expr1_evaled = expr1.doit()
    expr2_evaled = expr2.doit()
    if len(symbols) != len(test_value_set):
        raise Exception("Invalid test_value_set length")
    for n in range(0, len(symbols)):
        this_expr1 = test_values_replace(expr1_evaled, symbols, test_value_set)
        this_expr2 = test_values_replace(expr2_evaled, symbols, test_value_set)
        if N(this_expr1) != N(this_expr2):
            return {
                'symbols' : symbols,
                'test_value_set': test_value_set,
                'expr1': expr1,
                'expr1_evaluated': this_expr1,
                'expr2': expr2,
                'expr2_evaluated': this_expr2
            }
    return None

def compare_for_symbols(expr1, expr2, symbols):
    test_numbers = map(lambda sym: get_test_numbers_for_symbol(sym), symbols)
    test_value_sets = list(itertools.product(*test_numbers))
    for test_value_set in test_value_sets:
        this_result = compare_for_symbols_with_test_values(expr1, expr2, symbols, test_value_set)
        if not (this_result is None):
            return this_result
    return None

def extr(expr, search):
    def fn(rv):
        return rv.func(*(filter(lambda n: n!=search, rv.args)))
    return bottom_up(expr, fn)

def compare(expr1, expr2, test_symbols):
    return True

def chnge(expr, op, test_symbols):
    new_expr = op(expr)
    this_result = compare_for_symbols(expr, new_expr, test_symbols)
    if not (this_result is None):
        return this_result
    return new_expr