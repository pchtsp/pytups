import csv
from . import tools
from typing import Callable, Iterable, Union, TypeVar, Generic, TYPE_CHECKING

if TYPE_CHECKING:
    from superdict import SuperDict


T = TypeVar("T")


class TupList(list, Generic[T]):
    def __getitem__(self, key: int) -> Union[T, "TupList[T]"]:
        if not isinstance(key, slice):
            return list.__getitem__(self, key)
        if key.start is not None:
            start = (len(self) + key.start) if key.start < 0 else key.start
        else:
            start = 0
        if key.stop is not None:
            stop = (len(self) + key.stop) if key.stop < 0 else key.stop
        else:
            stop = len(self)
        return TupList(self[i] for i in range(start, stop, key.step or 1))

    def __add__(self, *args, **kwargs) -> "TupList":
        return TupList(super().__add__(*args, **kwargs))

    def head(self) -> str:
        # TODO: change to show 5 first and 5 last, at least.
        # still wrong
        if len(self) <= 10:
            return list.__repr__(self)
        text = "[{},\n...,\n{}]\n({} elements)".format(
            self[:5].__repr__(), self[-5:].__repr__(), len(self)
        )
        return repr(text)

    def take(self, indices: Union[Iterable, int], use_numpy=False) -> "TupList":
        if use_numpy:
            try:
                return self.take_np(indices)
            except ImportError:
                pass
        if not isinstance(indices, list):
            return self.vapply(lambda tup: tup[indices])
        return self.vapply(lambda tup: tuple(tup[a] for a in indices))

    def take_np(self, indices: Union[Iterable, int]) -> "TupList":
        """
        filters the tuple of each element of the list according to a list of positions

        :param indices: a list of positions
        :type indices: int or list
        :return: a new :py:class:`TupList`
        """
        import numpy as np

        if not len(self):
            return self
        single = False
        arr = np.array(self, dtype=object)
        if not isinstance(indices, list):
            indices = [indices]
            single = True
        arr_filt = np.take(arr, indices, axis=1)
        if single:
            return TupList(x[0] for x in arr_filt)
        return TupList(tuple(x) for x in arr_filt)

    def vfilter(self, function: Callable) -> "TupList":
        """
        returns new list with only tuples for which `function` returns True

        :param callable function: function to apply to each element
        :return: new :py:class:`TupList`
        """
        return TupList([i for i in self if function(i)])

    def to_dict(
        self,
        result_col: Union[Iterable, int, None] = 0,
        is_list: bool = True,
        indices: Iterable = None,
    ) -> "SuperDict":
        """
        This magic function converts a tuple list into a dictionary
            by taking one or several of the columns as the result.

        :param result_col: a list of positions of the tuple for the result
        :type result_col: int or list or None
        :param bool is_list: the value of the dictionary will be a TupList?
        :param list indices: optional way of determining the indices instead of
            being the complement of result_col
        :return: new :py:class:`pytups.superdict.SuperDict`
        :return: new :py:class:`pytups.superdict.SuperDict`
        """
        from . import superdict as sd

        if result_col is None:
            return sd.SuperDict({k: k for k in self})
        if type(result_col) is not list:
            result_col = [result_col]
        if len(self) == 0:
            return sd.SuperDict()
        if indices is None:
            indices = [col for col in range(len(self[0])) if col not in result_col]
        result = sd.SuperDict()
        for tup in self:
            index = tuple(tup[i] for i in indices)
            if len(index) == 1:
                index = index[0]
            content = tuple(tup[i] for i in result_col)
            if len(content) == 1:
                content = content[0]
            if not is_list:
                result[index] = content
                continue
            if index not in result:
                result[index] = TupList()
            result[index].append(content)
        return result

    def to_dict_new(self, result_col=0, is_list=True, indices=None):
        """
        This magic function converts a tuple list into a dictionary
            by taking one or several of the columns as the result.

        :param result_col: a list of positions of the tuple for the result
        :type result_col: int or list or None
        :param bool is_list: the value of the dictionary will be a TupList?
        :param list indices: optional way of determining the indeces instead of
            being the complement of result_col
        :return: new :py:class:`pytups.superdict.SuperDict`
        """
        from . import superdict as sd

        if not len(self):
            return sd.SuperDict()
        if result_col is None:
            return sd.SuperDict({k: k for k in self})
        if not tools.is_really_iterable(result_col):
            result_col = [result_col]
        if indices is None:
            indices = [col for col in range(len(self[0])) if col not in result_col]
        _to_key = lambda k: k
        if tools.is_really_iterable(indices):
            if len(indices) == 1:
                indices = indices[0]
            else:
                _to_key = lambda k: tuple(k)
        if tools.is_really_iterable(result_col) and len(result_col) == 1:
            result_col = result_col[0]

        keys = self.take(indices)
        values = self.take(result_col)

        if not is_list:
            return sd.SuperDict(zip(keys, values))
        result = sd.SuperDict()
        for i, c in zip(keys, values):
            i = _to_key(i)
            try:
                result[i].append(c)
            except KeyError:
                result[i] = TupList([c])
        return result

    def add(self, *args) -> None:
        """
        this is just a shortcut for doing

        >>> TupList().append((0, 1, 2))

        by doing:

        >>> TupList().add(0, 1, 2)

        which is a little more friendly and short

        :param args: any number of elements to append
        :return: modified :py:class:`TupList`
        """
        return self.append(tuple(args))

    def unique(self, **kwargs) -> "TupList":
        """
        Applies :py:func:`numpy.unique`.

        :param dtype: arguments to :py:func:`numpy.asarray`
        :return: new :py:class:`TupList`
        """
        try:
            import numpy as np

            arr = np.asarray(self, **kwargs)
            return TupList(np.unique(arr, axis=0).tolist())
        except ImportError:
            return self.unique2()

    def unique2(self) -> "TupList":
        """
        Converts to set and then back to TupList.

        :return: new :py:class:`TupList`
        """
        return TupList(set(self))

    def intersect(self, input_list: Iterable) -> "TupList":
        """
        Converts list and argument into sets and then intersects them.

        :param list input_list: list to intersect
        :return: new :py:class:`TupList`
        """
        return TupList(set(self) & set(input_list))

    def set_diff(self, input_list: Iterable) -> "TupList":
        """
        Converts list and argument into sets and then subtracts one from the other.

        :param list input_list: list to subtract
        :return: new :py:class:`TupList`
        """
        return TupList(set(self) - set(input_list))

    def to_start_finish(
        self,
        compare_tups: Callable,
        pp: int = 1,
        sort: bool = True,
        join_func: Callable = None,
    ) -> "TupList":
        """
        Takes a calendar tuple list of the form: (id, month) and
        returns a tuple list of the form (id, start_month, end_month)
        it works with a bigger tuple too.

        :param callable compare_tups: returns True if tups are not consecutive. Takes 3 arguments
        :param int pp: the position in the tuple where the period is
        :param callable join_func: returns joined tuple from list of consecutive tuples. Takes 1 argument.
        :return: new :py:class:`TupList`
        """
        if sort:
            self.sort(key=lambda x: (x[0], x[pp]))
        last_tup = ()
        all_periods = []
        current_period = []
        for tup in self:
            if tup == self[0] or compare_tups(tup, last_tup, pp):
                # we're starting, or it's a new id. Or we're changing month.
                if len(current_period):
                    # if there was a previous list of periods: save it
                    all_periods.append(current_period)
                # start list of consecutive periods
                current_period = [tup]
            else:
                # don't start: just keep on storing it
                current_period.append(tup)
            last_tup = tup

        # The last tup, we need to save it too:
        if len(current_period):
            all_periods.append(current_period)

        if join_func is None:
            join_func = lambda list_tup: tuple(list(list_tup[0]) + [list_tup[-1][pp]])
        res_start_finish = [join_func(list_tup) for list_tup in all_periods]
        return TupList(res_start_finish)

    def to_list(self) -> list:
        """

        :return: list
        """
        return list(self)

    def to_set(self) -> set:
        """

        :return: set
        """
        return set(self)

    def to_zip(self) -> zip:
        return zip(*self)

    def len(self) -> int:
        """
        Shortcut to:

        >>> len(TupList())

        :return: length of list
        :rtype: int
        """
        return len(self)

    def kvapply(self, func: Callable, *args, **kwargs) -> "TupList":
        """
        maps function into each element of TupList with indexes

        :param callable func: function to apply
        :return: new :py:class:`TupList`
        """
        return TupList(func(k, v, *args, **kwargs) for k, v in enumerate(self))

    def kapply(self, func: Callable, *args, **kwargs) -> "TupList":
        """
        maps function into each key of TupList

        :param callable func: function to apply
        :return: new :py:class:`TupList`
        """
        return TupList(func(k, *args, **kwargs) for k, _ in enumerate(self))

    def vapply(self, func: Callable, *args, **kwargs) -> "TupList":
        """
        maps function into each element of TupList

        :param callable func: function to apply
        :return: new :py:class:`TupList`
        """
        return TupList(func(v, *args, **kwargs) for v in self)

    def to_df(self, **kwargs):
        try:
            import pandas as pd

            return pd.DataFrame(self.to_list(), **kwargs)
        except ImportError:
            raise ImportError(
                "Pandas is not present in your system. Try: pip install pandas"
            )

    def sorted(self, **kwargs) -> "TupList":
        """
        Applies sorted function to elements and returns a TupList

        :param kwargs: arguments for sorted function
        :return: new :py:class:`TupList`
        """
        return TupList(sorted(self, **kwargs))

    def to_csv(self, path: str) -> "TupList":
        """
        exports the list to a csv file.
        :param path: filename
        :return: the same :py:class:`TupList`
        """
        with open(path, "w", newline="\n", encoding="utf-8") as out:
            csv_out = csv.writer(out)
            csv_out.writerows(self)
        return self

    @classmethod
    def from_csv(cls, path: str, func: Callable = None, **kwargs) -> "TupList":
        """
        Generates a new TupList by reading a csv file
        :param path: filename
        :param callable func: function to apply to each row
        :**kwargs: arguments to csv.reader
        :return: new :py:class:`TupList`
        """
        if func is None:
            func = tuple
        with open(path) as f:
            data = cls(csv.reader(f, **kwargs)).vapply(func)
        return data
