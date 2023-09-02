def remove(expr, *search):

    """
    Remove an expression from another expression
    
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

    """

    def _remove(expr, search):

        if expr.is_Atom or expr.is_Dummy:
            return expr
        elif expr.is_Mul or expr.is_Add:
            newargs = map(lambda arg: remove(arg, search), filter(lambda n: n!=search, expr.args))
            return expr.func(*newargs)
        else:
            newargs = map(lambda arg: remove(arg, search), expr.args)
            return expr.func(*newargs)
    
    expr = _remove(expr, search[0])
    if len(search) == 1:
        return expr
    else:
        return remove(expr, *search[1:])