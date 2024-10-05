from ovld.core import ovld
from ovld.dependent import Equals
from ovld.types import Dataclass, Exactly, HasMethod

# U = Union[str, int]
# U = str | Equals[0]
# print(isinstance("ah", U))
# print(isinstance(0, U))
# print(is_dependent(U))


@ovld
def f(x: str | Equals[0]):
    return x


breakpoint()
print(f(0))
print(f(1))
print(f("what"))


print(Equals[4].__instancecheck__.__func__)
print(HasMethod["__len__"].__instancecheck__.__func__)
print(Exactly[int].__instancecheck__.__func__)
print(Dataclass.__instancecheck__.__func__)


print(isinstance(4, Equals[4]))
print(isinstance(4, Equals[4.0]))
print(isinstance([1], HasMethod["__len__"]))
print(issubclass(type([1]), HasMethod["__len__"]))


# from multimethod import multimethod as dispatch
# from plum import dispatch
# from runtype import multidispatch as dispatch

# from ovld import ovld as dispatch


# @dispatch
# def f(x: type[int]):
#     return "ah"


# @dispatch
# def f(x: type[object]):
#     return "something else"


# @dispatch
# def f(x: type[dict[str, object]]):
#     return ("didi", x)


# print(f(int))
# print(f(str))
# print(f(dict[str, int]))
# print(f(dict[int, int]))
