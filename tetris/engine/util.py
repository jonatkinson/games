def chunks(l, n):
    """
    Returns list l in chunks of n.
    """

    for i in range(0, len(l), n):
        yield l[i:i+n]
