from strongtyping_pyoverload import overload


@overload
def smap_what(x: list, y: list):
    """Three."""
    return [smap_what(a, b) for a, b in zip(x, y)]


@overload
def smap_what(x: tuple, y: tuple):
    return tuple(smap_what(a, b) for a, b in zip(x, y))


@overload
def smap_what(x: dict, y: dict):
    return {k: smap_what(v, y[k]) for k, v in x.items()}


@overload
def smap_what(x: object, y: object):
    return x + y


@overload
def smap_what(x: str, y: str):
    return x + y


print(smap_what("a", "b"))
