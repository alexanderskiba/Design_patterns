def factorize(x):
    """
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    fact = 0
    for i in range(1, x + 1):
        fact = fact * i
    return fact
