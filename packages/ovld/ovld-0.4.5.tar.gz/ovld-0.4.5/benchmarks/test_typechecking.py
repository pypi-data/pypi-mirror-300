# from collections.abc import Collection
# from dataclasses import dataclass
# from itertools import product
# from numbers import Number
# from typing import Literal

# import pytest
# from beartype import beartype

# try:
#     from strongtyping.strong_typing import match_typing
# except ImportError:
#     match_typing = None
# from typeguard import typechecked

# from ovld import Ovld, ovld
# from ovld.dependent import Dependent, Regexp
# from ovld.types import Dataclass


# @dataclass
# class Point:
#     x: int
#     y: int


# def ovld(fn):
#     o = Ovld()
#     o.register(fn)
#     return o.dispatch


# def typecheck_test(cases, checkers):
#     def deco(fn):
#         def make_test(chk_name, case_name, typecheck, params):
#             group = f"{fn.__name__}_{case_name}"

#             @pytest.mark.benchmark(group=group)
#             def test(benchmark):
#                 *args, out = params
#                 tfn = typecheck(fn)
#                 result = benchmark(tfn, *args)
#                 assert result == out

#             test.__name__ = f"test_{group}[{chk_name}]"
#             globals()[test.__name__] = test

#         for (case_name, case), (chk_name, chk) in product(
#             cases.items(), checkers.items()
#         ):
#             if chk is not None:
#                 make_test(chk_name, case_name, chk, case)

#     return deco


# @typecheck_test(
#     cases=dict(normal=(10, 20, 200)),
#     checkers=dict(
#         ovld=ovld,
#         beartype=beartype,
#         typeguard=typechecked,
#         strongtyping=match_typing,
#     ),
# )
# def mul(x: int, y: int):
#     return x * y


# @typecheck_test(
#     cases=dict(
#         ints=(10, 20, 30),
#         lists=([1], [2], [1, 2]),
#     ),
#     checkers=dict(
#         ovld=ovld,
#         beartype=beartype,
#         typeguard=typechecked,
#         strongtyping=match_typing,
#     ),
# )
# def add(x: int | str | float | list, y: int | str | float | list):
#     return x + y


# @typecheck_test(
#     cases=dict(
#         normal=("http://google.com", "google.com"),
#     ),
#     checkers=dict(
#         ovld=ovld,
#         beartype=beartype,
#         # typeguard=typechecked,
#         # strongtyping=match_typing,
#     ),
# )
# def urlregexp(url: Regexp[r"^http://.*"]):
#     return url.split("://")[1]


# @typecheck_test(
#     cases=dict(
#         normal=([1, 2, 3], 1),
#     ),
#     checkers=dict(
#         ovld=ovld,
#         beartype=beartype,
#         typeguard=typechecked,
#         strongtyping=match_typing,
#     ),
# )
# def firstelem(elements: list[int]):
#     return elements[0]


# @typecheck_test(
#     cases=dict(
#         normal=(123, Point(1, 2), "low", "whatever"),
#     ),
#     checkers=dict(
#         ovld=ovld,
#         beartype=beartype,
#         typeguard=typechecked,
#         strongtyping=match_typing,
#     ),
# )
# def misc(
#     numero: Number, dc: Dataclass, method: Literal["low"] | Literal["high"]
# ):
#     return "whatever"


# @typecheck_test(
#     cases=dict(
#         normal=(10, 11),
#     ),
#     checkers=dict(
#         ovld=ovld,
#         beartype=beartype,
#         # typeguard=typechecked,
#         # strongtyping=match_typing,
#     ),
# )
# def positive(x: Dependent[int, lambda x: x > 0]):
#     return x + 1


# @typecheck_test(
#     cases=dict(
#         normal=((1, Point(2, 3), "blah"), ("blah", Point(2, 3), 1)),
#     ),
#     checkers=dict(
#         ovld=ovld,
#         beartype=beartype,
#         typeguard=typechecked,
#         strongtyping=match_typing,
#     ),
# )
# def triple(xyz: tuple[Number, Dataclass, Collection]):
#     return tuple(reversed(xyz))
