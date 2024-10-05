import inspect


def f(x, y):
    return x + y


def g(z):
    return z * z


f.__code__ = g.__code__
print(inspect.signature(f))


print(f(8))
