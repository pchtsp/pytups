from . import tools
import operator as op
import pickle
from typing import (
    Callable,
    Iterable,
    Any,
    Union,
    TypeVar,
    Generic,
    Mapping,
    Iterator,
    List,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from .tuplist import TupList

try:
    import ujson as json
except:
    import json

K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


class SuperDict(dict, Generic[K, V], Mapping[K, V]):
    """
    A dictionary with additional methods
    """

    def __getitem__(self, key: K) -> V:
        return dict.__getitem__(self, key)

    def __iter__(self) -> Iterator[K]:
        return dict.__iter__(self)

    def __add__(self, other: Union[dict, int, float, str]) -> "SuperDict":
        """
        Applies the adding operator to the values in the SuperDict and another object.
        This operation might raise a TypeError based on the types of the values of the SuperDict and the other object.
        """
        return self.sapply(op.__add__, other)

    # def __radd__(self, other):
    #     return self.sapply(op.__add__, other)

    def __sub__(self, other: Union[dict, int, float, str]) -> "SuperDict":
        """
        Applies the substract operator to the values in the SuperDict and another object.
        This operation might raise a TypeError based on the types of the values of the SuperDict and the other object.
        """
        return self.sapply(op.__sub__, other)

    # def __rsub__(self, other):
    #     return other.sapply(op.__sub__, self)

    def __mul__(self, other: Union[dict, int, float, str]) -> "SuperDict":
        """
        Applies the multiply operator to the values in the SuperDict and another object.
        This operation might raise a TypeError based on the types of the values of the SuperDict and the other object.
        """
        return self.sapply(op.__mul__, other)

    # def __rmul__(self, other):
    #     return self.sapply(op.__mul__, other)

    def __truediv__(self, other: Union[dict, int, float, str]) -> "SuperDict":
        """
        Applies the true division (float division) operator to the values in the SuperDict and another object.
        This operation might raise a TypeError based on the types of the values of the SuperDict and the other object.
        """
        return self.sapply(op.__truediv__, other)

    def __floordiv__(self, other: Union[dict, int, float, str]) -> "SuperDict":
        """
        Applies the floor division (integer division) operator to the values in the SuperDict and another object.
        This operation might raise a TypeError based on the types of the values of the SuperDict and the other object.
        """
        return self.sapply(op.__floordiv__, other)

    def head(self) -> str:
        """
        Returns a string representation with the first pair of key values in the SuperDict, the last pair of key value
        and the number of elements on the SuperDict.

        :return: the head string representation of the SuperDict
        :rtype: str
        """
        if len(self) <= 2:
            return dict.__repr__(self)
        _keys = self.keys_l()
        first, last = (_keys[n] for n in [0, -1])
        first_v, last_v = (self[n] for n in [first, last])
        return '"{{{}: {}\n,..., \n{}: {}}}"\n{} elements'.format(
            first.__repr__(),
            first_v.__repr__(),
            last.__repr__(),
            last_v.__repr__(),
            len(self),
        )

    @staticmethod
    def _list_or_value(val_list: List[T], pos: int) -> Union[List[T], T]:
        if pos is None:
            return val_list
        return val_list[pos]

    def keys_l(self, pos: int = None) -> list:
        """
        Shortcut to:

        >>> list(SuperDict().keys())

        :return: list with keys
        :param int pos: position to extract
        :rtype: list or object
        """
        result = list(self.keys())
        return self._list_or_value(result, pos)

    def values_l(self, pos: int = None) -> list:
        """
        Shortcut to:

        >>> list(SuperDict().values())

        :return: list with values
        :param int pos: position to extract
        :rtype: list or object
        """
        result = list(self.values())
        return self._list_or_value(result, pos)

    def values_tl(self, pos: int = None) -> "TupList":
        """
        Shortcut to:

        >>> tl.TupList(SuperDict().values())

        :return: tuple list with values
        :param int pos: position to extract
        :rtype: :py:class:`pytups.tuplist.TupList`
        """
        from . import tuplist as tl

        result = tl.TupList(self.values())
        return self._list_or_value(result, pos)

    def keys_tl(self, pos: int = None) -> "TupList":
        """
        Shortcut to:

        >>> tl.TupList(SuperDict().keys())

        :return: tuple list with keys
        :param int pos: position to extract
        :rtype: :py:class:`pytups.tuplist.TupList`
        """
        from . import tuplist as tl

        result = tl.TupList(self.keys())
        return self._list_or_value(result, pos)

    def items_tl(self, pos: int = None) -> "TupList":
        """
        Shortcut to:

        >>> tl.TupList(SuperDict().items())

        :return: tuple list with keys
        :param int pos: position to extract
        :rtype: :py:class:`pytups.tuplist.TupList`
        """
        from . import tuplist as tl

        result = tl.TupList(self.items())
        return self._list_or_value(result, pos)

    def clean(self, default_value=0, func: Callable = None, **kwargs) -> "SuperDict":
        """
        Filters elements by value

        :param default_value: value of elements to take out
        :param function func: function that evaluates to true if we take out the element
        :param kwargs: optional arguments for func
        :return: new :py:class:`SuperDict`
        :rtype: :py:class:`SuperDict`

        >>> SuperDict({'a': 1, 'b': 0, 'c': 1}).clean(0)
        {'a': 1, 'c': 1}
        """
        if func is None:
            func = lambda x: x != default_value
        return self.vfilter(func=func, **kwargs)

    def vfilter(self, func: Callable, **kwargs) -> "SuperDict":
        """
        apply a filter over the dictionary values
        :param function func: True for values we want to filter
        :param kwargs: other arguments for func
        :return: new :py:class:`SuperDict`
        :rtype: SuperDict

        >>> SuperDict({'a': 2, 'b': 3, 'c': 1}).vfilter(lambda v: v > 1)
        {'a': 2, 'b': 3}
        """
        return SuperDict(
            {key: value for key, value in self.items() if func(value, **kwargs)}
        )

    def kfilter(self, func: Callable, **kwargs) -> "SuperDict":
        """
        apply a filter over the dictionary keys
        :param function func: True for keys we want to filter
        :param kwargs: other arguments for func
        :return: new :py:class:`SuperDict`
        :rtype: :py:class:`SuperDict`

        >>> SuperDict({'a': 2, 'b': 3, 'c': 1}).kfilter(lambda k: k > 'a')
        {'b': 3, 'c': 1}
        """
        return SuperDict(
            {key: value for key, value in self.items() if func(key, **kwargs)}
        )

    def kvfilter(self, func: Callable, **kwargs) -> "SuperDict":
        """
        apply a filter over the dictionary values
        :param callable func: True for values we want to filter
        :param kwargs: other arguments for func
        :return: new :py:class:`SuperDict`
        :rtype: SuperDict

        >>> SuperDict({'a': 2, 'b': 3, 'c': 1}).kvfilter(lambda k, v: v > 1 and k=='a')
        {'a': 2}
        """
        return SuperDict(
            {key: value for key, value in self.items() if func(key, value, **kwargs)}
        )

    def len(self) -> int:
        """
        Shortcut to:

        >>> len(SuperDict())

        :return: length of dictionary
        :rtype: int
        """
        return len(self)

    def filter(self, indices: Iterable, check: bool = True) -> "SuperDict":
        """
        takes out elements that are not in `indices`

        :param indices: keys to keep in new dictionary
        :param bool check: if True, only return valid ones
        :return: new :py:class:`SuperDict`
        :rtype: :py:class:`SuperDict`

        >>> SuperDict({'a': 1, 'b': 0, 'c': 1}).filter(['a', 'b'])
        {'a': 1, 'b': 0}

        """
        if not tools.is_really_iterable(indices):
            indices = {indices}
        else:
            indices = set(indices)
        if not check:
            intersection = indices & self.keys()
            return SuperDict({k: self[k] for k in intersection})
        difference = indices - self.keys()
        if len(difference) > 0:
            raise KeyError("following elements not in keys: {}".format(difference))
        return SuperDict({k: self[k] for k in indices})

    def to_dictdict(self) -> "SuperDict":
        """
        Expands tuple keys to nested dictionaries
        Useful to get json-compatible objects from the solution

        :return: new (nested) :py:class:`SuperDict`

        >>> SuperDict({('a', 'b'): 1, ('b', 'c'): 0, 'c': 1}).to_dictdict()
        {'a': {'b': 1}, 'b': {'c': 0}, 'c': 1}

        """
        dictdict = SuperDict()
        for key in self:
            # TODO: checking all the time for isinstance is inneficient
            if isinstance(self[key], dict):
                # if it's a nested dictionary, we traverse it first:
                self[key] = self[key].to_dictdict()
            value = self[key]
            if not isinstance(key, tuple):
                # in some cases, the key is just one value that's a string
                # we need to be careful not to expand the string
                key = (key,)
            dictdict.set_m(*key, value=value)
        return dictdict

    def set_m(self, *args, value=None) -> "SuperDict":
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

    def dicts_to_tup(self, keys: list, content) -> "SuperDict":
        """
        compacts nested dictionaries into one single dictionary
        with tuples as keys.

        :param list keys: list of keys to use as new key
        :param content:
        :return: modified :py:class:`SuperDict`
        :rtype: :py:class:`SuperDict`
        """
        try:
            for key, value in content.items():
                self.dicts_to_tup(keys + [key], value)
        except AttributeError:
            # content is not a dict, we store it
            self[tuple(keys)] = content
            return self
        return self

    def to_dictup(self) -> "SuperDict":
        """
        Useful when reading a json and wanting to convert it to tuples.
        Opposite to to_dictdict

        :return: new (flat) :py:class:`SuperDict`
        :rtype: :py:class:`SuperDict`
        """
        return SuperDict().dicts_to_tup([], self)

    def list_reverse(self) -> "SuperDict":
        """
        transforms dictionary of lists to another dictionary of lists only indexed by the values.

        :return: new :py:class:`SuperDict`
        """
        from . import tuplist as tl

        new_keys = list(set(val for l in self.values() for val in l))
        dict_out = SuperDict({k: tl.TupList() for k in new_keys})
        for k, v in self.items():
            for el in v:
                dict_out[el].append(k)
        return dict_out

    def to_tuplist(self) -> "TupList":
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

    def fill_with_default(self, keys: Iterable, default=0) -> "SuperDict":
        """
        guarantees dictionary will have specific keys

        :param Iterable keys: dictionary will have at least these keys
        :param default:
        :return: new :py:class:`SuperDict`
        """
        rem_keys = set(keys) - self.keys()
        _dict = {k: default for k in rem_keys}
        _dict.update(self)
        return SuperDict(_dict)

    def get_property(self, property):
        return SuperDict(
            {key: value[property] for key, value in self.items() if property in value}
        )

    def to_lendict(self) -> "SuperDict":
        """
        get length of values in dictionary

        :return: new :py:class:`SuperDict`
        """
        return self.vapply(len)

    def index_by_property(self, property, get_list=False) -> Union["SuperDict", list]:
        el = self.keys_l()[0]
        if property not in self[el]:
            raise IndexError(
                "property {} is not present in el {} of dict {}".format(
                    property, el, self
                )
            )

        result = {v[property]: {} for v in self.values()}
        for k, v in self.items():
            result[v[property]][k] = v

        result = SuperDict.from_dict(result)
        if get_list:
            return result.values_l()
        return result

    def index_by_part_of_tuple(
        self, position, get_list=False
    ) -> Union["SuperDict", list]:
        el = self.keys_l()[0]
        if len(el) <= position:
            raise IndexError(
                "length of dict {} keys is smaller than position {}".format(
                    self, position
                )
            )

        result = {k[position]: {} for k in self.keys()}
        for k, v in self.items():
            result[k[position]][k] = v

        result = SuperDict.from_dict(result)
        if get_list:
            return result.values_l()
        return result

    def kvapply(self, func: Callable, *args, **kwargs) -> "SuperDict":
        """Applies a function to the dictionary and returns the result

        :param callable func: function with two arguments: one for the key, another for the value
        :return: new :py:class:`SuperDict`
        """
        return SuperDict({k: func(k, v, *args, **kwargs) for k, v in self.items()})

    def vapply(self, func: Callable, *args, **kwargs) -> "SuperDict":
        """
        Same as apply but only on values

        :param callable func: function to apply.
        :return: new :py:class:`SuperDict`
        """
        return SuperDict({k: func(v, *args, **kwargs) for k, v in self.items()})

    def kapply(self, func: Callable, *args, **kwargs) -> "SuperDict":
        """
        Same as apply but only on keys

        :param callable func: function to apply.
        :return: new :py:class:`SuperDict`
        """
        return SuperDict({k: func(k, *args, **kwargs) for k in self})

    def sapply(
        self, func: Callable, other: Union[dict, int, float, str], *args, **kwargs
    ) -> "SuperDict":
        """
        Applies function to both dictionaries.
        Using keys of the self.
        It's like applying a function over the left join.

        :param callable func: function to apply.
        :param Union[dict, int, float,s tr] other: either an int, a float, a string or another dictionary to
          perform the operation over
        :return: new :py:class:`SuperDict`
        """
        if isinstance(other, (int, float, str)):
            return self.vapply(lambda v: func(v, other, *args, **kwargs))

        return self.kvapply(lambda k, v: func(v, other[k], *args, **kwargs))

    def get_m(self, *args, default=None) -> Any:
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

    def update(self, *args, **kwargs) -> "SuperDict":
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
            if (
                (k not in self)
                or (not isinstance(self[k], dict))
                or (not isinstance(v, dict))
            ):
                self[k] = v
            else:
                self[k].update(v)
        return self

    def _update(self, dict) -> "SuperDict":
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

    def sorted(self, **kwargs) -> list:
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
            raise ImportError(
                "Pandas is not present in your system.\nTry: pip install pandas"
            )

    def reverse(self):
        return SuperDict({v: k for k, v in self.items()})

    @classmethod
    def from_dict(cls, data) -> "SuperDict":
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

    def copy_shallow(self) -> "SuperDict":
        """
        Copies the immediate keys only.

        :return: new :py:class:`SuperDict`
        """
        return SuperDict(self)

    def copy_deep(self) -> "SuperDict":
        """
        Copies the complete object using python's pickle
        """
        return pickle.loads(pickle.dumps(self, -1))

    def copy_deep2(self) -> "SuperDict":
        """
        Copies the complete object using json (or ujson if available)
        """
        return json.loads(json.dumps(self))

    @classmethod
    def from_df(cls, data) -> "SuperDict":
        # TODO: this assuming the object is a pandas dataframe

        pass
