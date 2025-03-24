import csv
from typing import Callable, Iterable, Union, TypeVar, Generic, TYPE_CHECKING
import pickle
from itertools import chain

if TYPE_CHECKING:
    from .superdict import SuperDict

from .tools import is_really_iterable

T = TypeVar("T")


class TupList(list, Generic[T]):
    """
    A list of tuples or dictionaries
    """

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

    def copy_shallow(self) -> "TupList":
        """
        Copies the list only. Not it's contents

        :return: new :py:class:`TupList`
        """
        return TupList(self)

    def copy_deep(self) -> "TupList":
        """
        Copies the complete object using python's pickle
        """
        return pickle.loads(pickle.dumps(self, -1))

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
        indices: Union[Iterable, int, None] = None,
    ) -> "SuperDict":
        """
        This magic function converts a tuple list into a dictionary
            by taking one or several of the columns as the result.

        :param result_col: a list of keys for the result (positions of the tuple or keys of the dict)
        :type result_col: int or list or None
        :param bool is_list: the value of the dictionary will be a TupList?
        :param list indices: optional way of determining the indices instead of
            being the complement of result_col
        :return: new :py:class:`pytups.superdict.SuperDict`
        """
        from . import superdict as sd

        if len(self) == 0:
            return sd.SuperDict()
        first = self[0]
        # Handle case of list of dict with indices = None
        if isinstance(first, dict) and indices is None:
            raise ValueError(
                "For a list of dicts, to_dict require indices to be specified"
            )

        if result_col is None:
            # if everything is None, we return the same tuple as index and as result
            if indices is None:
                return sd.SuperDict({k: k for k in self})
        elif not is_really_iterable(result_col):
            result_col = [result_col]

        # now that we have a result_col, we can fill indices
        if indices is None:
            indices = [
                col
                for col in range(len(self[0]))
                if col not in result_col and (col - len(self[0])) not in result_col
            ]
        elif not is_really_iterable(indices):
            indices = [indices]

        one_or_tup = lambda _list: _list[0] if len(_list) == 1 else _list

        def get_index(el):
            index = tuple(el[i] for i in indices)
            return one_or_tup(index)

        if result_col is None:
            # the content matches the input, no need to do anything
            get_content = lambda x: x
        else:

            def get_content(el):
                content = tuple(el[i] for i in result_col)
                return one_or_tup(content)

        def assign_result(result, index, content):
            if not is_list:
                result[index] = content
                return
            if index not in result:
                result[index] = TupList()
            result[index].append(content)

        result = sd.SuperDict()
        for el in self:
            index = get_index(el)
            content = get_content(el)
            assign_result(result, index, content)
        return result

    def to_dictlist(self, keys: list) -> "TupList":
        """
        Converts a list of tuples to a list of dictionaries.

        :param list keys: a unique list of dictionary keys
        :return: new :py:class:`TupList`
        """
        return self.vapply(lambda v: dict(zip(keys, v)))

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

    @classmethod
    def from_df(cls, data, **kwargs):
        try:
            import pandas as pd

            return cls(data.to_dict(orient="records", **kwargs))

        except ImportError:
            raise ImportError(
                "Pandas is not present in your system. Try: pip install pandas"
            )

    def sorted(self, **kwargs) -> "TupList":
        """
        Applies sorted function to elements and returns a TupList

        :param kwargs: arguments for sorted function
            main arguments for sorted are:
            - key
            - reverse
        :return: new :py:class:`TupList`
        """
        return TupList(sorted(self, **kwargs))

    def chain(self) -> "TupList":
        """
        Flattens a TupList by applying itertools chain method
        """
        return TupList(chain(*self))

    def to_csv(self, path: str, header: list = None) -> "TupList":
        """
        Exports the list to a csv file
        :param path: filename
        :param header: list of strings to use as header/column names for dict
        :return: the same :py:class:`TupList`
        """
        if len(self) == 0:
            return self
        first = self[0]
        if header is not None and len(first) != len(header):
            raise ValueError("Header length does not match data length")
        # Handle case of list of dict
        if isinstance(first, dict):
            if header is None:
                header = first.keys()
            thing_to_write = self.take(list(header))
        else:
            thing_to_write = self
        with open(path, "w", newline="\n", encoding="utf-8") as out:
            csv_out = csv.writer(out)
            if header is not None:
                csv_out.writerow(header)
            csv_out.writerows(thing_to_write)
        return self

    @classmethod
    def from_csv(cls, path: str, func: Callable = None, **kwargs) -> "TupList":
        """
        Generates a new TupList by reading a csv file

        :param str path: filename
        :param callable func: function to apply to each row
        :param kwargs: arguments to csv.reader
        :return: new :py:class:`TupList`
        """
        if func is None:
            func = tuple
        with open(path) as f:
            data = cls(csv.reader(f, **kwargs)).vapply(func)
        return data

    def vapply_col(self, pos: Union[int, str, None], func: Callable):
        """
        Like vapply, but it stores the result in one of the positions of the tuple (or dictionary)
        :param pos: int or str
        :param callable func: function to apply to create col
        """

        def apply_to_tup(my_tuple):
            # we apply the function before any potential modification
            result = func(my_tuple)
            # if it's un-mutable (tuple), we need to make it a list
            tuple_flag = 0
            if isinstance(my_tuple, tuple):
                tuple_flag = 1
                my_tuple = list(my_tuple)
            # if None, we assume we want it at the end
            if tuple_flag and pos is None:
                my_tuple.append(result)
            else:
                my_tuple[pos] = result
            if tuple_flag:
                my_tuple = tuple(my_tuple)
            return my_tuple

        return self.vapply(apply_to_tup)
