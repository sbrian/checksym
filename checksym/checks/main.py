import itertools
from sympy import *
import functools
import sympy
import numpy
import mpmath

def get_test_numbers_for_assumptions(assumptions0):
    '''Return a representative set of numbers for the assumptions.
    
    These "sets" are actually lists, because Python sets are unordered and
    that causes non-deterministic tests. The items in the lists should
    all be unique, though, although I have not verified that.
    '''
    #integer_set = {1, 2, 10, 97, 100, 1000}
    integer_set = [Integer(1), Integer(3)]
    #integer_set = [Integer(1)]
    #rational_test_set = {Rational(1,4), Rational(56, 70), Rational(5, 3),
    #                     Rational(3, 5), Rational(100, 3), Rational(1000, 79)}
    rational_test_set = [Rational(1,4), Rational(5, 3)]
    #algebraic_test_set = [sqrt(2), sqrt(3)]
    algebraic_test_set = [sqrt(2)]
    #transcendental_test_set = {pi, 0.375*pi, E, 0.783*E, Rational(9,7)*E}
    transcendental_test_set = [pi, E]
    my_set = []
    if assumptions0.get('complex') and not assumptions0.get('noninteger'):
        my_set.extend(integer_set)
    if not assumptions0.get('integer'):
        my_set.extend(rational_test_set)
    if not assumptions0.get('rational'):
        my_set.extend(algebraic_test_set)
    if not assumptions0.get('algebraic'):
        my_set.extend(transcendental_test_set)
    if not assumptions0.get('nonnegative'):
        my_set.extend(list(map(lambda n: -n, my_set)))
    if not assumptions0.get('nonzero'):
        my_set.extend([Integer(0)])
    if assumptions0.get('real'):
        return my_set
    if assumptions0.get('imaginary'):
        return map(lambda n: n * I, my_set)
    return map(lambda n: n[0] + I * n[1], itertools.product(my_set, my_set))

def get_test_numbers_for_symbol(symbol):
    return get_test_numbers_for_assumptions(symbol.assumptions0)

def test_values_replace(expr, symbols, test_value_set):
    replacement_tuples = []
    for n in range(0, len(symbols)):
        replacement_tuples.append((symbols[n], test_value_set[n]))
    return expr.subs(replacement_tuples)

def cleanup_for_lambdify(expr):
    real_imag = expr.as_real_imag()
    return float(real_imag[0]) + 1j * float(real_imag[1])

def compare_for_symbols_with_test_values(expr1, expr2, symbols, test_value_set):
    expr1_evaled = expr1.doit()
    expr2_evaled = expr2.doit()
    if len(symbols) != len(test_value_set):
        raise Exception("Invalid test_value_set length")
    test_value_set_for_lambify = list(map(cleanup_for_lambdify, test_value_set))
    this_expr1_lambdify_evaled = lambdify(symbols, expr1_evaled)(*test_value_set_for_lambify)
    this_expr2_lambdify_evaled = lambdify(symbols, expr2_evaled)(*test_value_set_for_lambify)
    if this_expr1_lambdify_evaled != this_expr2_lambdify_evaled:
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

@functools.lru_cache(maxsize=None)
def compare(expr1, expr2, *symbols):
    test_numbers = map(lambda sym: get_test_numbers_for_symbol(sym), symbols)
    test_value_sets = list(itertools.product(*test_numbers))
    #test_value_sets = [(Integer(1), Integer(3), Integer(1))]
    counter = 0
    
    def do_compare(test_value_set):
        return compare_for_symbols_with_test_values(expr1, expr2, symbols, test_value_set)

    for test_value_set in test_value_sets:
        counter = counter+1
        #print("Comparing " + str(counter))
        this_result = do_compare(test_value_set)
        if not (this_result is None):
            return this_result
    
    return None

def remove(expr, search):
    '''Remove an expression from another expression
    
    Keyword arguments:
    expr -- the expression to search through
    search -- the subexpression to find and remove

    We know that the search expression will be one of these
    1) An argument to Add()
    2) An argument to Mul()

    We don't support these cases
    1) An argument to Pow()
    2) An argument to Rational()
    3) An argument to some other function

    '''

    if expr.is_Atom or expr.is_Dummy:
        return expr
    elif expr.is_Mul or expr.is_Add:
        newargs = map(lambda arg: remove(arg, search), filter(lambda n: n!=search, expr.args))
        return expr.func(*newargs)
    else:
        newargs = map(lambda arg: remove(arg, search), expr.args)
        return expr.func(*newargs)
    

def change(expr, op, *test_symbols):
    new_expr = op(expr)
    this_result = compare(expr, new_expr, *test_symbols)
    if not (this_result is None):
        return this_result
    return new_expr