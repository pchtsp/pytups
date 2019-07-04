import collections as col


class OrderSet(col.MutableSequence):

    def __init__(self, _list):
        # _pos is the real list
        # _store is the reverse-key mapping

        self._pos = list(_list)
        _data = [(key, pos) for pos, key in enumerate(self._pos)]
        self._store = dict(_data)

    def __getitem__(self, key):
        return self._pos[key]

    def __setitem__(self, key, value):
        prev_value = self[key]
        self._store.pop(prev_value)
        self._store[value] = key
        self._pos[key] = value

    def __delitem__(self, key):
        del self._store[self[key]]
        if key!=-1:
            rest = self._pos[key+1:]
            for item in rest:
                self._store[item] -= 1
        del self._pos[key]

    def __iter__(self):
        return iter(self._pos)

    def __len__(self):
        return len(self._pos)

    def __repr__(self):
        return repr(self._pos)

    def insert(self, key, value):
        self._store[value] = len(self)
        self._pos.append(value)

    def ord(self, key):
        return self._store[key]

    def next(self, key, num=1):
        return self[self._store[key] + num]

    def prev(self, key, num=1):
        return self[self._store[key] - num]

# TODO: forbid list of lists.
# TODO: add operations.

if __name__ == '__main__':

    ttt = OrderSet(['1', 'll', 'lll'])
    ttt._store
    ttt[1] = 'lllll'
    ttt.prev(ttt.prev('1'))


    ttt._store


    d = col.OrderedDict()
    d['1'] = 0
    d['11'] = 1

