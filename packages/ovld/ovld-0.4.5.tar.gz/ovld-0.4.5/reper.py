# from ovld.dependent import Regexp
from ovld import dependent

r = dependent.Regexp["a"]
print(repr(r))
print(repr(r | int))
