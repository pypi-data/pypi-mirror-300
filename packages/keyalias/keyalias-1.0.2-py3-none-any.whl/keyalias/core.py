import functools

from datahold import *

__all__ = [
    "classdecorator",
    "getdecorator",
    "getproperty",
]


def classdecorator(cls, /, **kwargs):
    for alias, key in kwargs.items():
        pro = getproperty(key)
        setattr(cls, alias, pro)
    return cls


def getdecorator(**kwargs):
    return functools.partial(classdecorator, **kwargs)


def getproperty(key):
    def fget(self, /):
        return self[key]

    def fset(self, value, /):
        self[key] = value

    def fdel(self, /):
        del self[key]

    doc = "self[%r]" % key
    ans = property(fget, fset, fdel, doc)
    return ans
