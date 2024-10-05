from typing import Callable

from ovld.core import ovld

# from plum import dispatch as ovld
# from multimethod import multimethod as ovld


class Animal:
    pass


class Mammal(Animal):
    pass


class Cat(Mammal):
    pass


@ovld
def f(t: Callable[[Mammal], Mammal]):
    return 1


@ovld
def f(t: Callable[[Mammal, Mammal], Mammal]):
    return 2


def f1(x: Mammal, y: Mammal) -> Mammal:
    return "X"


def f2(x: Animal, y: Animal) -> Mammal:
    return "X"


print(f(f1))
print(f(f2))


# @ovld
# def f(t: tuple[()]):
#     return 0

# @ovld
# def f(t: tuple[int]):
#     return 1

# @ovld
# def f(t: tuple[str]):
#     return 2

# @ovld
# def f(t: tuple[int, str]):
#     return 3

# assert f(()) == 0
# assert f((1,)) == 1
# assert f(("x",)) == 2
# assert f((2, "y")) == 3


# @ovld
# def f(d: Sequence[int]):
#     return 0


# @ovld
# def f(d: Sequence[str]):
#     return 1


# print(f([1]))
# print(f(["x"]))
# print(f([1, "x"]))
# print(f(["x", "y", "z", 1]))
# print(f([]))
