from itertools import cycle, islice
from sympy import *
from pprint import pp

def get_test_numbers_for_assumptions(assumptions0, scale):
    """
    Return a representative set of numbers for the assumptions.
    
    These "sets" are actually lists, because Python sets are unordered and
    that causes non-deterministic tests. The items in the lists should
    all be unique, though, although I have not verified that.
    """

    if assumptions0.get('imaginary'):
        return map(lambda n: n * I, get_real_test_numbers_for_assumptions(assumptions0, scale))
    
    if assumptions0.get('real'):
        return get_real_test_numbers_for_assumptions(assumptions0, scale)

    real_set = get_real_test_numbers_for_assumptions(map_special(assumptions0, 'real_part_'), scale)

    # We shift the scale of the imagainary part by one, so we have numbers with different real and imaginary parts.
    # I don't really have a use-case for this, but it seems like a good idea.
    imaginary_set = get_real_test_numbers_for_assumptions(map_special(assumptions0, 'imaginary_part_'), scale + 1)


    length = max(len(real_set), len(imaginary_set))

    return [a + I * b for a, b in zip(islice(cycle(real_set), length), islice(cycle(imaginary_set), length))] 
    #return list(map(lambda n: n[0] + I * n[1], itertools.zip(real_set, imaginary_set)))

def map_special(assumptions0, prefix):
    new_assumptions = assumptions0.copy()
    for k in assumptions0:
        if k.startswith(prefix):
            new_assumptions[k.removeprefix(prefix)] = assumptions0[k]
    dummy_symbol = Symbol("__dummy_symbol_for_checksym_assumptions", **new_assumptions)
    return dummy_symbol.assumptions0

def get_real_test_numbers_for_assumptions(assumptions0, scale):

    my_set = []
    if assumptions0.get('integer'):
        my_set.append(2)
        my_set.append(5)
        if assumptions0.get('nonnegative'):
            my_set.append(3)
        else:
            my_set.append(-3)
    else:
        my_set.append(Rational(13, 10))
        my_set.append(Rational(1, 7))
        if assumptions0.get('nonnegative'):
            my_set.append(Rational(12, 5))
        else:
            my_set.append(Rational(-12, 5))
        
    my_set = list(map(lambda n: n*scale, my_set))
    return my_set 

def build_test_value_sets(*symbols):
    """
    Build a list of tuples where each element in the tuple
    is a test value for one of the symbols passed as an argument.

    This list is all sympy types. They can be coverted later to proper types.

    For example, if the symbols are [x, y] where x and y are both non-negative
    integers, the return might be:

    [(x0, y0), (x1, y1)] = [(2, 2), (-3, -3)]

    And then tests are run substituting the symbols with the values in each tuple.

    Because many check operations are quite slow, we want to keep the tests to the
    smallest number possible. This is more important than ensuring absolute correctness.

    One thing that can obscure discrepancies is the value zero. For example,
    if x is replaced with zero, 3x+2 and 4x+2 appear equivalent. But any number
    could result in a zero factor. If x is replaced with 2, 3*(2-x)+2 and 4*(2-x)+2
    appear equivalent. To avoid this we will ensure that every symbol is replaced
    with at least three values with distinct absolute values. The distinct absolute
    value restriction handles the case where the symbol is squared. If x is replaced
    with both 2 and -2, 3*(x**2-4) and 4*(x**2-4) appear equivalent. The three value
    requirement handles the case where the variable is shifted and squared. If x
    is replaced with both -1 and 3, 3*((x-1)**2-4) and 4*((x-1)**2-4) appear equivalent.

    For multiple symbols, take the same list of test values and multiply by a different
    scaling factor for each, to avoid cases where either x and y are the same, or the
    difference between x and y in successive tests is constant. Therefore if one x - y
    difference results in a zero factor, another test will not give 0.

    As best as I can understand now, testing with zero is not that important. I can't
    find a case where a test would succeed with non-zero numbers and fail on zero, other
    than division by zero cases, which aren't really a use-case I'm concerned with.

    The way that this is done, for each test set, the interval between the test values
    for is the same between each variable. For example, x, y, and z might be 2, 6, 10.
    However, I can't think of any reason this matters for testing.

    """

    scale = 1
    scale_increment = 2

    def get_test_numbers_for_symbol(symbol):
        nonlocal scale
        ret_val = get_test_numbers_for_assumptions(symbol.assumptions0, scale)
        scale = scale + scale_increment
        return ret_val
    
    # This gives a list of sets. There's one entry in the list for each symbol.
    # Each of those entries contains test values for that symbol. The sets are
    # not necessarily all the same length.
    #
    # [ [x_test_value_1, x_test_value_2, x_test_value_3], [y_test_value_1, y_test_value_2] ]
    test_numbers = list(map(get_test_numbers_for_symbol, symbols))

    # This rearranges the above into a list of sets, where each set contains
    # a test value for each symbol. Thus, an entry in the list represents the full
    # set of values needed for one test. For sets that are too short, we wrap around
    # and repeat values.
    #
    # For example, for 2 tests
    # [ [x_test_value_1, y_test_value_1], [x_test_value_2, y_test_value_2], [x_test_value_3, y_test_value 1] ]
    test_value_sets_size = max(list(map(lambda v: len(v), test_numbers)))
    test_value_sets = []
    for i in range(0, test_value_sets_size):
        def fn(set_for_symbol):
            return set_for_symbol[i % len(set_for_symbol)]
        this_set = list(map(fn, test_numbers))
        test_value_sets.append(this_set)

    return test_value_sets