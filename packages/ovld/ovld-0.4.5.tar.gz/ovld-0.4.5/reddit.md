## What My Project Does

[ovld](https://github.com/breuleux/ovld) implements multiple dispatch in Python. This lets you define multiple versions of the same function with different type signatures.

For example:

```python
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
```


## Target Audience

Ovld is pretty generally applicable: multiple dispatch is a central feature of several programming languages, e.g. Julia. I find it particularly useful when doing work on complex heterogeneous data structures, for instance walking an AST, serializing/deserializing data, generating HTML representations of data, etc.


## Features

* Wide range of supported annotations: normal types, protocols, `Union`, `Literal`, generic collections like `list[str]` (only checks the first element).
* Utility types like `HasMethod`, `Intersection`, `Deferred["some.import"]` or `All` (contravariant `Any`).
* Easy to define [custom types](https://ovld.readthedocs.io/en/latest/types/#defining-new-types).
* Support for [dependent types](https://ovld.readthedocs.io/en/latest/dependent/), by which I mean "types" that depend on the values of the arguments. For example you can easily implement a `Regexp[regex]` type that matches string arguments based on regular expressions, or a type that only matches 2x2 torch.Tensor with int8 dtype.
* Dispatch on keyword arguments (with a few limitations).
* Numeric priority levels for disambiguation.
* Define [variants](https://ovld.readthedocs.io/en/latest/usage/#variants) of existing functions (copies of existing overloads with additional functionality)
* Special `recurse()` function for recursive calls that also work with variants.
* Special `call_next()` function to call the next dispatch.


## Comparison

There already exist a few multiple dispatch libraries: plum, multimethod, multipledispatch, runtype, fastcore, and the builtin functools.singledispatch (single argument).

Ovld is faster than all of them. From 1.5x to 100x less overhead depending on use case, and in the ballpark of isinstance/match. It is also generally more featureful: no other library supports dispatch on keyword arguments, and only a few support `Literal` annotations, but with massive performance penalties.

[Whole comparison section, with benchmarks, can be found here.](https://ovld.readthedocs.io/en/latest/compare/)

As an aside, you can also use it on a single function as a runtime typechecker, in which case it performs about as well as beartype, although ovld wasn't really built to do this.
