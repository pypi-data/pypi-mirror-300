import timeit
from dataclasses import dataclass

from beartype import (
    BeartypeConf,  # <-- this isn't your fault
    beartype,
)
from beartype.claw import (
    beartype_all,
)  # <-- you didn't sign up for this
from strongtyping.strong_typing import match_typing
from typeguard import typechecked

# from enforce import runtime_validation
from ovld import ovld

# from ovld.check import typecheck

beartype_all(conf=BeartypeConf())
# beartype_this_package()                                        # <-- raise exceptions in your code
# beartype_all(conf=BeartypeConf(violation_type=UserWarning))


@beartype
def f_bear(x: int, y: int):
    return x + y


@ovld
def f_ovld(x: int, y: int):
    return x + y


@ovld
def f_ovld_D(x: int, y: int):
    # breakpoint()
    return x + y


@match_typing
def f_strong(x: int, y: int):
    return x + y


@typechecked
def f_guard(x: int, y: int):
    return x + y


# @runtime_validation
# def f_enforce(x: int, y: int):
#     return x + y


def f_custom(x: int, y: int):
    assert isinstance(x, int) and isinstance(y, int)
    return x + y


class digdug(dict):
    pass


def adder(x, y):
    return x + y


didi = digdug({int: adder})
didi2 = digdug({(int, int): adder})


@dataclass
class Poop:
    didi: dict


poo2 = Poop(didi2)


def f_custom_2(x: int, y: int):
    assert didi2[type(x), type(y)]
    return x + y


# def f_custom_2(x: int, y: int):
#     func = didi[type(x)] and didi[type(y)]
#     return func(x, y)


class Gusto:
    def __init__(self, didi):
        self.didi = didi
        self.__name__ = "gusto"

    def __call__(self, x: int, y: int):
        func = self.didi[type(x), type(y)]
        return func(x, y)


# f_bear(7, 8)
# f_ovld("a", 3)
# assert f_ovld(3, 4) == 7


for fn in (
    f_bear,
    f_strong,
    f_guard,
    f_ovld_D,
    f_ovld,
    f_custom,
    f_custom_2,
    Gusto(didi2),
    Gusto(didi2).__call__,
):
    timing = timeit.timeit(stmt=lambda: fn(3, 4), number=300000)
    print(f"{fn.__name__:10}{1000 * timing:>10.3f}ms")

breakpoint()
f_ovld(4, 5)
