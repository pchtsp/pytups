import collections as col
from typing import Iterable, TypeVar, Generic, List, Any

K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


class OrderSet(col.MutableSequence, Generic[T]):
    # TODO: uncomment when 3.5 is dropped
    # _store: Dict[Any, int]
    # _pos: List[T]

    def __init__(self, _list: List[T]):
        # _pos is the real list
        # _store is the reverse-key mapping

        self._pos = list(_list)
        _data = [(key, pos) for pos, key in enumerate(self._pos)]
        self._store = dict(_data)

    def __getitem__(self, key: int) -> Any:
        return self._pos[key]

    def __setitem__(self, key: int, value: Any) -> None:
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

    def insert(self, key: int, value: Any) -> None:
        self._store[value] = len(self)
        self._pos.append(value)

    def ord(self, value: Any) -> int:
        return self._store[value]

    def next(self, value: Any, num: int = 1) -> Any:
        return self[self._store[value] + num]

    def prev(self, value: Any, num: int = 1) -> Any:
        return self[self._store[value] - num]


# TODO: forbid list of lists.
# TODO: add operations.

if __name__ == "__main__":

    ttt = OrderSet(["1", "ll", "lll"])
    ttt._store
    ttt[1] = "lllll"
    ttt.prev(ttt.prev("1"))

    ttt._store

    d = col.OrderedDict()
    d["1"] = 0
    d["11"] = 1
