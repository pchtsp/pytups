import numpy as np

class TupList(list):

    # TODO: test following method:
    def __getitem__(self, key):
        if isinstance(key, slice):
            return TupList(self[i] for i in range(key.start, key.stop, key.step))
        return list.__getitem__(self, key)

    def filter(self, indices):
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

    def filter_list_f(self, function):
        """
        returns new list with only tuples for which `function` returns True

        :param function function: function to apply to each element
        :return: new :py:class:`TupList`
        """
        return TupList([i for i in self if function(i)])

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

    def to_start_finish(self, compare_tups, pp=1, sort=True):
        """
        Takes a calendar tuple list of the form: (id, month) and
        returns a tuple list of the form (id, start_month, end_month)
        it works with a bigger tuple too.

        :param function compare_tups: function to decide two tups are not consecutive. Takes 3 arguments
        :param int pp: the position in the tuple where the period is
        :return: new :py:class:`TupList`
        """
        if sort:
            self.sort(key=lambda x: (x[0], x[pp]))
        res_start_finish = []
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

        for list_tup in all_periods:
            res_start_finish.append(tuple(list(list_tup[0]) + [list_tup[-1][pp]]))
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


    def apply(self, func, *args, **kwargs):
        """
        maps function into each element of TupList

        :param function func: function to apply
        :return: new :py:class:`TupList`
        """
        return TupList(func(v, *args, **kwargs) for v in self)

    def kapply(self, func, *args, **kwargs):
        """
        maps function into each element of TupList

        :param function func: function to apply
        :return: new :py:class:`TupList`
        """
        return TupList(func(k, v, *args, **kwargs) for k, v in enumerate(self))


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
