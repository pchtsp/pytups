import collections as col


class OrderedList(col.MutableSequence):

    def __init__(self, _list):
        _data = [(key, pos) for pos, key in enumerate(_list)]
        self.store = col.OrderedDict(_data)

    def __getitem__(self, key):
        return list(self.store.keys())[key]

    def __setitem__(self, key, value):
        prev_value = self[key]
        self.store.pop(prev_value)
        self.store[value] = key
        # TODO: the following can be better done by iterating with move_to_end
        _data = sorted(self.store.items(), key=lambda x: x[1])
        self.store = col.OrderedDict(_data)

    def __delitem__(self, key):
        del self.store[self[key]]
        rest = list(self.store.keys())[key:]
        for item in rest:
            self.store[item] -= 1

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def insert(self, key, value):
        self.store[value] = len(self)

    def ord(self, key):
        return self.store[key]

    def next(self, key, num=1):
        return self[self.store[key] + num]

    def prev(self, key, num=1):
        return self[self.store[key] - num]

# TODO: forbid list of lists.
# TODO: add operations.

if __name__ == '__main__':

    ttt = OrderedList(['1', 'll', 'lll'])
    ttt.store
    ttt[1] = 'lllll'
    ttt.prev(ttt.prev('1'))


    ttt.store


    d = col.OrderedDict()
    d['1'] = 0
    d['11'] = 1

