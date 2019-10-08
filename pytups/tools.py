import collections

def is_really_iterable(var):
    return isinstance(var, collections.Iterable) \
           and not isinstance(var, str)