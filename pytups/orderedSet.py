try:
    from collections import MutableSequence
except:
    from collections.abc import MutableSequence
from typing import Iterable, TypeVar, Generic, List, Dict

K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


class OrderSet(MutableSequence, Generic[T]):
    """
    An ordered set of elements.
    """

    _store: Dict[T, int]
    _pos: List[T]

    def __init__(self, _list: List[T]):
        # _pos is the real list
        # _store is the reverse-key mapping
        if len(_list) > len(set(_list)):
            raise ValueError("The list needs to have unique values.")
        self._pos = list(_list)
        _data = [(key, pos) for pos, key in enumerate(self._pos)]
        self._store = dict(_data)

    def __getitem__(self, key: int) -> T:
        return self._pos[key]

    def __setitem__(self, key: int, value: T) -> None:
        prev_value = self[key]
        self._store.pop(prev_value)
        self._store[value] = key
        self._pos[key] = value

    def __delitem__(self, key: int):
        del self._store[self[key]]
        if key != -1:
            rest = self._pos[key + 1 :]
            for item in rest:
                self._store[item] -= 1
        del self._pos[key]

    def __iter__(self) -> Iterable:
        return iter(self._pos)

    def __len__(self) -> int:
        return len(self._pos)

    def __repr__(self) -> str:
        return repr(self._pos)

    def insert(self, key: int, value: T) -> None:
        self._store[value] = len(self)
        self._pos.append(value)

    def ord(self, value: T) -> int:
        return self._store[value]

    def next(self, value: T, num: int = 1) -> T:
        return self[self._store[value] + num]

    def prev(self, value: T, num: int = 1) -> T:
        return self[self._store[value] - num]

    def dist(self, value1, value2) -> int:
        return self._store[value2] - self._store[value1]

    def splice(self, start, delete_count, *items) -> List:
        """Remove existing elements and/or add new elements to a list.
        this function was taken from: https://gist.github.com/jonbeebe/44a529fcf15d6bda118fe3cfa434edf3
        target        the target list (will be changed)
        start         index of starting position
        delete_count  number of items to remove (default: len(target) - start)
        *items        items to insert at start index
        Returns a new list of removed items (or an empty list)
        """
        raise NotImplementedError()
        if delete_count is None:
            delete_count = len(self._pos) - start

        # store removed range in a separate list and replace with *items
        total = start + delete_count
        removed = self._pos[start:total]
        self._pos[start:total] = items

        # TODO: we still need to edit self._store with inserts and removes
        # for i in removed:
        #     self._store
        return removed

        pass


# TODO: forbid list of lists.
