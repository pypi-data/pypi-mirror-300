from typing import Literal

import pytest

from .common import (
    multimethod_dispatch,
    ovld_dispatch,
    plum_dispatch,
)

###############################
# multiple dispatch libraries #
###############################


def make_tup(dispatch):
    @dispatch
    def tup(t: tuple[()]):
        return 0

    @dispatch
    def tup(t: tuple[int]):
        return 1

    @dispatch
    def tup(t: tuple[Literal["x"]]):
        return 2

    @dispatch
    def tup(t: tuple[int, str]):
        return 3

    @dispatch
    def tup(t: tuple[tuple[str]]):
        return 4

    return tup


#########
# match #
#########


def tup_match(expr):
    match expr:
        case ():
            return 0
        case (int(),):
            return 1
        case (str(),):
            return 2
        case (int(), str()):
            return 3
        case ((str(),),):
            return 4


####################
# Test definitions #
####################


def make_test(fn):
    fn(())
    fn = fn.__call__

    def run():
        return [fn(()), fn((1,)), fn(("x",)), fn((2, "y"))]

    @pytest.mark.benchmark(group="tup")
    def test(benchmark):
        result = benchmark(run)
        assert result == [0, 1, 2, 3]

    return test


test_tup_ovld = make_test(make_tup(ovld_dispatch))
test_tup_plum = make_test(make_tup(plum_dispatch))
test_tup_multimethod = make_test(make_tup(multimethod_dispatch))

test_tup_custom_match = make_test(tup_match)
