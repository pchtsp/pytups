from collections.abc import Iterable


def is_really_iterable(var):
    return isinstance(var, Iterable) and not isinstance(var, str)
