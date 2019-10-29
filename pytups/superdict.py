import numpy as np
from . import tools
import warnings

class SuperDict(dict):
    """
    A dictionary with additional methods
    """
    def keys_l(self):
        """
        Shortcut to:

        >>> list(SuperDict().keys())

        :return: list with keys
        :rtype: list
        """
        return list(self.keys())

    def values_l(self):
        """
        Shortcut to:

        >>> list(SuperDict().values())

        :return: list with values
        :rtype: list
        """
        return list(self.values())

    def values_tl(self):
        """
        Shortcut to:

        >>> tl.TupList(SuperDict().values())

        :return: tuple list with values
        :rtype: :py:class:`pytups.tuplist.TupList`
        """
        from . import tuplist as tl

        return tl.TupList(self.values())

    def keys_tl(self):
        """
        Shortcut to:

        >>> tl.TupList(SuperDict().keys())

        :return: tuple list with keys
        :rtype: :py:class:`pytups.tuplist.TupList`
        """
        from . import tuplist as tl

        return tl.TupList(self.keys())

    def clean(self, default_value=0, func=None, **kwargs):
        """
        Filters elements by value

        :param default_value: value of elements to take out
        :param function func: function that evaluates to true if we take out the element
        :param **kwags: optional arguments for func
        :return: new :py:class:`SuperDict`
        :rtype: :py:class:`SuperDict`

        >>> SuperDict({'a': 1, 'b': 0, 'c': 1}).clean(0)
        {'a': 1, 'c': 1}
        """
        if func is None:
            func = lambda x: x != default_value
        return self.vfilter(func=func, **kwargs)

    def vfilter(self, func, **kwargs):
        """
        apply a filter over the dictionary values
        :param function func: True for values we want to filter
        :param kwargs: other arguments for func
        :return: new :py:class:`SuperDict`
        :rtype: :py:class:`SuperDict`

        >>> SuperDict({'a': 2, 'b': 3, 'c': 1}).vfilter(lambda v: v > 1)
        {'a': 2, 'b': 3}
        """
        return SuperDict({key: value for key, value in self.items() if func(value, **kwargs)})

    def kfilter(self, func, **kwargs):
        """
        apply a filter over the dictionary keys
        :param function func: True for keys we want to filter
        :param kwargs: other arguments for func
        :return: new :py:class:`SuperDict`
        :rtype: :py:class:`SuperDict`

        >>> SuperDict({'a': 2, 'b': 3, 'c': 1}).kfilter(lambda k: k > 'a')
        {'b': 3, 'c': 1}
        """
        return SuperDict({key: value for key, value in self.items() if func(key, **kwargs)})

    def len(self):
        """
        Shortcut to:

        >>> len(SuperDict())

        :return: length of dictionary
        :rtype: int
        """
        return len(self)

    def filter(self, indices, check=True):
        """
        takes out elements that are not in `indices`

        :param indices: keys to keep in new dictionary
        :type indices: int or list
        :param bool check: if True, only return valid ones
        :return: new :py:class:`SuperDict`
        :rtype: :py:class:`SuperDict`

        >>> SuperDict({'a': 1, 'b': 0, 'c': 1}).filter(['a', 'b'])
        {'a': 1, 'b': 0}

        """
        if not tools.is_really_iterable(indices):
            indices = [indices]
        if not check:
            return SuperDict({k: self[k] for k in indices if k in self})
        bad_elem = set(indices) - self.keys()
        if len(bad_elem) > 0:
            raise KeyError("following elements not in keys: {}".format(bad_elem))
        return SuperDict({k: self[k] for k in indices})

    def to_dictdict(self):
        """
        Expands tuple keys to nested dictionaries
        Useful to get json-compatible objects from the solution

        :return: new (nested) :py:class:`SuperDict`

        >>> SuperDict({('a', 'b'): 1, ('b', 'c'): 0, 'c': 1}).to_dictdict()
        {'a': {'b': 1}, 'b': {'c': 0}, 'c': 1}

        """
        dictdict = SuperDict()
        for key in self:
            if isinstance(self[key], dict):
                # if it's a nested dictionary, we traverse it first:
                self[key] = self[key].to_dictdict()
            value = self[key]
            if not isinstance(key, tuple):
                # in some cases, the key is just one value that's a string
                # we need to be careful not to expand the string
                key = key,
            dictdict.set_m(*key, value=value)
        return dictdict

    def set_m(self, *args, value=None):
        """
        uses `args` as nested keys and then assigns `value`

        :param args: keys to nest
        :param value: value to assign to last dictionary
        :return: modified :py:class:`SuperDict`

        >>> SuperDict({('a', 'b'): 1, ('b', 'c'): 0, 'c': 1}).set_m('c', 'd', 'a', value=1)
        {'a': {'b': 1}, 'b': {'c': 0}, 'c': {'d': {'a': 1}}}

        """
        elem, *args = args
        if not args:
            self[elem] = value
            return self
        # we reach here, we still need to go deeper:
        if elem not in self or not isinstance(self[elem], SuperDict):
            self[elem] = SuperDict()
        self[elem].set_m(*args, value=value)
        return self

    def dicts_to_tup(self, keys, content):
        """
        compacts nested dictionaries into one single dictionary
        with tuples as keys.

        :param list keys: list of keys to use as new key
        :param content:
        :return: modified :py:class:`SuperDict`
        :rtype: :py:class:`SuperDict`
        """
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

        :return: new (flat) :py:class:`SuperDict`
        :rtype: :py:class:`SuperDict`
        """
        return SuperDict().dicts_to_tup([], self)

    def list_reverse(self):
        """
        transforms dictionary of lists to another dictionary of lists only indexed by the values.

        :return: new :py:class:`SuperDict`
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

        :return: new :py:class:`pytups.tuplist.TupList`
        :rtype: :py:class:`pytups.tuplist.TupList`
        """
        from . import tuplist as tl

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
        """
        guarantees dictionary will have specific keys

        :param list keys: dictionary will have at least these keys
        :param default:
        :return: new :py:class:`SuperDict`
        """
        rem_keys = set(keys) - self.keys()
        _dict = {k: default for k in rem_keys}
        _dict.update(self)
        return SuperDict(_dict)

    def get_property(self, property):
        return SuperDict({key: value[property] for key, value in self.items() if property in value})

    def to_lendict(self):
        """
        get length of values in dictionary

        :return: new :py:class:`SuperDict`
        """
        return self.vapply(len)

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

    def apply(self, *args, **kwargs):
        warnings.warn("use kvapply instead", DeprecationWarning)
        return self.kvapply(*args, **kwargs)

    def kvapply(self, func, *args, **kwargs):
        """Applies a function to the dictionary and returns the result

        :param callable func: function with two arguments: one for the key, another for the value
        :return: new :py:class:`SuperDict`
        """
        return SuperDict({k: func(k, v, *args, **kwargs) for k, v in self.items()})

    def vapply(self, func, *args, **kwargs):
        """
        Same as apply but only on values

        :param callable func: function to apply.
        :return: new :py:class:`SuperDict`
        """
        return SuperDict({k: func(v, *args, **kwargs) for k, v in self.items()})

    def kapply(self, func, *args, **kwargs):
        """
        Same as apply but only on keys

        :param callable func: function to apply.
        :return: new :py:class:`SuperDict`
        """
        return SuperDict({k: func(k, *args, **kwargs) for k in self})

    def sapply(self, func, other):
        """
        Applies function to both dictionaries.
        Using keys of the self.
        It's like applying a function over the left join.

        :param callable func: function to apply.
        :param dict other: dictionary to apply function to
        :return: new :py:class:`SuperDict`
        """
        return SuperDict({k: func(v, other[k]) for k, v in self.items()})

    def get_m(self, *args, default=None):
        """
        Safe way to search for something in a nested dictionary

        :param args: keys in nested dictionary
        :return: content after traversing the nested dictionary. None if doesn't exit
        """
        d = self
        try:
            for i in args:
                d = d[i]
            return d
        except KeyError:
            return default

    def update(self, *args, **kwargs):
        """
        updates a nested dictionary.

        :param args: dictionary to update with
        :param kwargs: specific keys and values to update
        :return: the edited dictionary
        """
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
        return self

    def _update(self, dict):
        """
        Like the dict update but it returns the result without modifying the input

        :return: new :py:class:`SuperDict`
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
        """
        Applies sorted function to dictionary keys

        :param kwargs: arguments for sorted
        :return:
        """
        return sorted(self, **kwargs)

    def to_df(self, **kwargs):
        try:
            import pandas as pd
            return pd.DataFrame.from_dict(self, **kwargs)
        except ImportError:
            raise ImportError('Pandas is not present in your system.\nTry: pip install pandas')

    def reverse(self):
        return SuperDict({v: k for k, v in self.items()})

    @classmethod
    def from_dict(cls, data):
        """
        Main initialization. Deals with nested dictionaries.

        :param dict data: a (possibly nested) dictionary
        :return: new :py:class:`SuperDict`
        """
        if not isinstance(data, dict):
            return data
        data = cls(data)
        for key, value in data.items():
            data[key] = cls.from_dict(value)
        return data
