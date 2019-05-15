import numpy as np


class SuperDict(dict):

    # def __init__(self, seq=None, **kwargs):
    #     super().__init__(seq=seq, **kwargs)

    def keys_l(self):
        return list(self.keys())

    def values_l(self):
        return list(self.values())

    def clean(self, default_value=0, func=None):
        if func is None:
            func = lambda x: x != default_value
        return SuperDict({key: value for key, value in self.items() if func(value)})

    def len(self):
        return len(self)

    def filter(self, indices, check=True):
        if not isinstance(indices, list):
            indices = [indices]
        if not check:
            return SuperDict({k: self[k] for k in indices if k in self})
        bad_elem = np.setdiff1d(indices, list(self.keys()))
        if len(bad_elem) > 0:
            raise KeyError("following elements not in keys: {}".format(bad_elem))
        return SuperDict({k: self[k] for k in indices})

    def to_dictdict(self):
        """
        Useful to get json-compatible objects from the solution
        :param self: a dictionary with tuples as keys
        :return: a (recursive) dictionary of dictionaries
        """
        dictdict = SuperDict()
        for tup, value in self.items():
            dictdict.set_m(*tup, value=value)
        return dictdict

    def set_m(self, *args, value):
        elem = args[0]
        if elem not in self:
            self[elem] = SuperDict()
        if len(args) == 1:
            self[elem] = value
            return self
        else:
            self[elem].set_m(*args[1:], value=value)
        return self

    def dicts_to_tup(self, keys, content):
        if not isinstance(content, dict):
            self[tuple(keys)] = content
            return self
        for key, value in content.items():
            self.dicts_to_tup(keys + [key], value)
        return self

    def to_dictup(self):
        """
        Useful when reading a json and wanting to convert it to tuples.
        Opposite to to_dictdict
        :param self: a dictionary of dictionaries
        :return: a dictionary with tuples as keys
        """
        return SuperDict().dicts_to_tup([], self)

    def list_reverse(self):
        """
        :param self: a dictionary with a list as a result
        :return: a dictionary with the list elements as keys and
        old keys as values.
        """
        new_keys = list(set(val for l in self.values() for val in l))
        dict_out = SuperDict({k: [] for k in new_keys})
        for k, v in self.items():
            for el in v:
                dict_out[el].append(k)
        return dict_out

    def to_tuplist(self):
        """
        The last element of the returned tuple was the dict's value.
        We try really hard to expand the tuples so it's a flat tuple list.
        :param self: dictionary indexed by tuples
        :return: a list of tuples.
        """
        from . import tuplist as tl
        # import pytups.tuplist as tl

        tup_list = tl.TupList()
        for key, value in self.items():
            if not isinstance(value, list):
                value = [value]
            if not isinstance(key, tuple):
                key = [key]
            else:
                key = list(key)
            # now we assume key is a list and value is a list of values.
            for val in value:
                if isinstance(val, tuple):
                    val = list(val)
                else:
                    val = [val]
                # we also assume val is a list
                tup_list.append(tuple(key + val))
        return tup_list

    def fill_with_default(self, keys, default=0):
        _dict = {k: default for k in keys}
        _dict.update(self)
        return SuperDict(_dict)

    def get_property(self, property):
        return SuperDict({key: value[property] for key, value in self.items() if property in value})

    def to_lendict(self):
        return SuperDict({k: len(v) for k, v in self.items()})

    def index_by_property(self, property, get_list=False):
        el = self.keys_l()[0]
        if property not in self[el]:
            raise IndexError('property {} is not present in el {} of dict {}'.
                             format(property, el, self))

        result = {v[property]: {} for v in self.values()}
        for k, v in self.items():
            result[v[property]][k] = v

        result = SuperDict.from_dict(result)
        if get_list:
            return result.values_l()
        return result

    def index_by_part_of_tuple(self, position, get_list=False):
        el = self.keys_l()[0]
        if len(el) <= position:
            raise IndexError('length of dict {} keys is smaller than position {}'.
                             format(self, position))

        result = {k[position]: {} for k in self.keys()}
        for k, v in self.items():
            result[k[position]][k] = v

        result = SuperDict.from_dict(result)
        if get_list:
            return result.values_l()
        return result

    def apply(self, func):
        """
        applies a function to the dictionary and returns the result
        :param func: function with two arguments: one for the key, another for the value
        :return: new Superdict
        """
        return SuperDict({k: func(k, v) for k, v in self.items()})

    def get_m(self, *args):
        try:
            d = self
            for i in args:
                d = d[i]
            return d
        except KeyError:
            return None

    def vapply(self, func):
        """
        same as apply but not using the key
        :param func:
        :return:
        """
        return SuperDict({k: func(v) for k, v in self.items()})

    def update(self, *args, **kwargs):
        other = {}
        if args:
            if len(args) > 1:
                raise TypeError()
            other.update(args[0])
        other.update(kwargs)
        for k, v in other.items():
            if ((k not in self) or
                (not isinstance(self[k], dict)) or
                (not isinstance(v, dict))):
                self[k] = v
            else:
                self[k].update(v)

    def _update(self, dict):
        """
        like the dict update but it returns the result
        without modifying the input
        :return: Superdict
        """
        temp_dict = SuperDict.from_dict(self)
        temp_dict.update(dict)
        return temp_dict

    # def to_dict(self):
    #     return self._to_dict(self)
    #
    # def _to_dict(self, dictionary):
    #     if not isinstance(dictionary, SuperDict):
    #         return dictionary
    #     for key, value in dictionary.items():
    #         dictionary[key] = dictionary._to_dict(value)
    #     dictionary = dict(dictionary)
    #     return dictionary

    def sorted(self, **kwargs):
        return sorted(self, **kwargs)
    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return data
        data = cls(data)
        for key, value in data.items():
            data[key] = cls.from_dict(value)
        return data
