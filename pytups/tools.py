from collections.abc import Iterable


def is_really_iterable(var):
    """
    Check if an object is iterable and not a string.

    :param var: a python object
    :return: bool True if the object is really iterable,
     False if it is not iterable or a string
    """
    return isinstance(var, Iterable) and not isinstance(var, str)


def list_splice(target, start, delete_count=None, *items):
    """Remove existing elements and/or add new elements to a list.
    this function was taken from: https://gist.github.com/jonbeebe/44a529fcf15d6bda118fe3cfa434edf3
    target        the target list (will be changed)
    start         index of starting position
    delete_count  number of items to remove (default: len(target) - start)
    *items        items to insert at start index
    Returns a new list of removed items (or an empty list)
    """
    if delete_count is None:
        delete_count = len(target) - start

    # store removed range in a separate list and replace with *items
    total = start + delete_count
    removed = target[start:total]
    target[start:total] = items

    return removed
