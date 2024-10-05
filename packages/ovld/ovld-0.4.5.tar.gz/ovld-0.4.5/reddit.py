import math
from typing import Literal

from ovld import ovld


@ovld
def div(x: int, y: int):
    return x / y


@ovld
def div(x: str, y: str):
    return f"{x}/{y}"


@ovld
def div(x: int, y: Literal[0]):
    return math.inf


assert div(8, 2) == 4
assert div("/home", "user") == "/home/user"
assert div(10, 0) == math.inf
