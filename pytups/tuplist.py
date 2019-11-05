import numpy as np
import warnings
# TODO: change vapply, apply and kapply to be consistent with superdict.

class TupList(list):

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.start, key.stop, key.step
            if start is None:
                start = 0
            if stop is None:
                stop = len(self)
            if step is None:
                step = 1
            return TupList(self[i] for i in range(start, stop, step))
        return list.__getitem__(self, key)

    def __add__(self, *args, **kwargs):
        return TupList(super().__add__(*args, **kwargs))

    def filter(self, *args, **kwargs):
        warnings.warn("use take instead of filter", DeprecationWarning)
        return self.take(*args, **kwargs)

    def take(self, indices):
        """
        filters the tuple of each element of the list according to a list of positions

        :param indices: a list of positions
        :type indices: int or list
        :return: a new :py:class:`TupList`
        """
        if not len(self):
            return self
        single = False
        arr = np.array(self, dtype=np.object)
        if not isinstance(indices, list):
            indices = [indices]
            single = True
        arr_filt = np.take(arr, indices, axis=1)
        if single:
            return TupList(x[0] for x in arr_filt)
        return TupList(tuple(x) for x in arr_filt)

    def vfilter(self, function):
        """
        returns new list with only tuples for which `function` returns True

        :param function function: function to apply to each element
        :return: new :py:class:`TupList`
        """
        return TupList([i for i in self if function(i)])

    def filter_list_f(self, *args, **kwargs):
        warnings.warn("use vfilter instead of filter_list_f", DeprecationWarning)
        return self.vfilter(*args, **kwargs)

    def to_dict(self, result_col=0, is_list=True, indices=None):
        """
        This magic function converts a tuple list into a dictionary
            by taking one or several of the columns as the result.

        :param result_col: a list of positions of the tuple for the result
        :type result_col: int or list or None
        :param bool is_list: the value of the dictionary will be a list?
        :param list indices: optional way of determining the indeces instead of
            being the complement of result_col
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
                result[index] = []
            result[index].append(content)
        return result

    def add(self, *args):
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

    def unique(self, **kwargs):
        """
        Applies :py:func:`numpy.unique`.

        :param dtype: arguments to :py:func:`numpy.asarray`
        :return: new :py:class:`TupList`
        """
        arr = np.asarray(self, **kwargs)
        return TupList(np.unique(arr, axis=0).tolist())

    def unique2(self):
        """
        Converts to set and then back to TupList.

        :return: new :py:class:`TupList`
        """
        return TupList(set(self))

    def intersect(self, input_list):
        """
        Converts list and argument into sets and then intersects them.

        :param list input_list: list to intersect
        :return: new :py:class:`TupList`
        """
        return TupList(set(self) & set(input_list))

    def to_start_finish(self, compare_tups, pp=1, sort=True, join_func=None):
        """
        Takes a calendar tuple list of the form: (id, month) and
        returns a tuple list of the form (id, start_month, end_month)
        it works with a bigger tuple too.

        :param function compare_tups: returns True if tups are not consecutive. Takes 3 arguments
        :param int pp: the position in the tuple where the period is
        :param function join_func: returns joined tuple from list of consecutive tuples. Takes 1 argument.
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

    def to_list(self):
        """

        :return: list
        """
        return list(self)

    def to_set(self):
        """

        :return: set
        """
        return set(self)

    def kvapply(self, func, *args, **kwargs):
        """
        maps function into each element of TupList with indexes

        :param function func: function to apply
        :return: new :py:class:`TupList`
        """
        return TupList(func(k, v, *args, **kwargs) for k, v in enumerate(self))

    def kapply(self, func, *args, **kwargs):
        """
        maps function into each key of TupList

        :param function func: function to apply
        :return: new :py:class:`TupList`
        """
        return TupList(func(k, *args, **kwargs) for k, _ in enumerate(self))

    def vapply(self, func, *args, **kwargs):
        """
        maps function into each element of TupList

        :param function func: function to apply
        :return: new :py:class:`TupList`
        """
        return TupList(func(v, *args, **kwargs) for v in self)

    def apply(self, *args, **kwargs):
        warnings.warn("use vapply instead of apply", DeprecationWarning)
        return self.vapply(*args, **kwargs)

    def to_df(self, **kwargs):
        try:
            import pandas as pd
            return pd.DataFrame(self.to_list(), **kwargs)
        except ImportError:
            raise ImportError('Pandas is not present in your system. Try: pip install pandas')


    def sorted(self, **kwargs):
        """
        Applies sorted function to elements and returns a TupList

        :param kwargs: arguments for sorted function
        :return: new :py:class:`TupList`
        """
        return TupList(sorted(self, **kwargs))
