from math import floor, log10

def convert_to_order_one(n):
    """
    Shift the decimal point until exactly one digit is to the right
    
    Return the new value and the number of places shifted
    """

    places = floor(log10(n))

    return (n * 10 ** (-places), places)


def compare_to_significance_complex(a_real, a_imaginary, b_real, b_imaginary, places):
    return (compare_to_significance(a_real, b_real, places)
        and compare_to_significance(a_imaginary, b_imaginary, places))
    

def compare_to_significance(a, b, places):
    """
    Returns True only if the arguments are indentical to the requested number of places
    
    """
    
    if a == 0 and b == 0:
        return True
    
    if a == 0 or b == 0:
        return False
    
    if a > 0 and b < 0:
        return False
    
    if b > 0 and a < 0:
        return False
    
    a = abs(a)
    b = abs(b)

    # Shift the decimal point to where exactly one digit is to the right
    (a_converted, a_places) = convert_to_order_one(a)
    (b_converted, b_places) = convert_to_order_one(b)

    # If the numbers were not the same magnitude, return false
    if a_places != b_places:
        if a_places == b_places - 1:
            a_converted = a_converted / 10
        elif a_places == b_places + 1:
            b_converted = b_converted / 10
        else:
            return False

    # Convert to integers of the desired number of digits
    a_converted_2 = round(a_converted*10**(places-1))
    b_converted_2 = round(b_converted*10**(places-1))

    return a_converted_2 == b_converted_2
