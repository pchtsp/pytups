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
        try:
            list_set = set(_list)
        except TypeError as e:
            raise TypeError("values in list need to be hashable") from e
        if len(_list) > len(list_set):
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
        """

        :param value: element in the set
        :return: the position of the element in the set
        """
        try:
            return self._store[value]
        except KeyError as e:
            raise MissingValue("value {} does not exist".format(value)) from e

    def next(self, value: T, num: int = 1) -> T:
        """

        :param value: element in set
        :param num: number of elements to offset
        :return: next element in the list
        """
        return self[self.ord(value) + num]

    def prev(self, value: T, num: int = 1) -> T:
        """

        :param value: element in set
        :param num: number of elements to offset backwards
        :return: previous element in the list
        """
        return self[self.ord(value) - num]

    def dist(self, value1, value2) -> int:
        """

        :param value1: element in set
        :param value2: element in set
        :return: difference in position between the two elements
        """
        return self.ord(value2) - self.ord(value1)

    def between(self, value1: T, value2: T) -> List[T]:
        """

        :param value1: element in set
        :param value2: element in set
        :return: elements between value1 and value2, both inclusive
        """
        return [self[i] for i in range(self.ord(value1), self.ord(value2) + 1)]

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


class MissingValue(Exception):
    pass
