import itertools
from sympy import *
from pprint import pp

def get_test_numbers_for_assumptions(assumptions0):
    '''Return a representative set of numbers for the assumptions.
    
    These "sets" are actually lists, because Python sets are unordered and
    that causes non-deterministic tests. The items in the lists should
    all be unique, though, although I have not verified that.
    '''
    if assumptions0.get('imaginary'):
        return map(lambda n: n * I, get_real_test_numbers_for_assumptions(assumptions0))
    
    if assumptions0.get('real'):
        return get_real_test_numbers_for_assumptions(assumptions0)

    imaginary_set = get_real_test_numbers_for_assumptions(map_special(assumptions0, 'imaginary_part_'))

    real_set = get_real_test_numbers_for_assumptions(map_special(assumptions0, 'real_part_'))

    return map(lambda n: n[0] + I * n[1], itertools.product(real_set, imaginary_set))

def map_special(assumptions0, prefix):
    new_assumptions = assumptions0.copy()
    for k in assumptions0:
        if k.startswith(prefix):
            new_assumptions[k.removeprefix(prefix)] = assumptions0[k]
    dummy_symbol = Symbol("__dummy_symbol_for_checksym_assumptions", **new_assumptions)
    return dummy_symbol.assumptions0

def get_real_test_numbers_for_assumptions(assumptions0):
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
    if not assumptions0.get('noninteger'):
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

    return my_set