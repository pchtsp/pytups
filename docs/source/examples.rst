Some examples
**************************

.. highlight:: python

SuperDict
=============================

These are dictionaries with additional methods based on the contents.

Example::

    import pytups as pt
    indent_dict = {'a': {'b': {'c': 'A'}}, 'b': {'t': {'d' : 'B'}}}
    my_superdict = pt.SuperDict.from_dict(indent_dict)
    my_superdict_dictup = my_superdict.to_dictup()
    # {('a', 'b', 'c'): 'A', ('b', 't', 'd'): 'B'}
    my_superdict_dictup.to_tuplist()
    # [('a', 'b', 'c', 'A'), ('b', 't', 'd', 'B')]
    my_superdict_dictup.kvapply(lambda k, v: v+'_1')
    # {('a', 'b', 'c'): 'A_1', ('b', 't', 'd'): 'B_1'}
    my_superdict_dictup.to_dictdict()
    # {'a': {'b': {'c': 'A'}}, 'b': {'t': {'d' : 'B'}}}


Normal operations
-----------------

Some operations have been oveloaded for dictionaries so they can be done between superdicts as if they were numbers:

Example data::

    import pytups as pt
    have = pt.SuperDict({'apples': 1, 'pears': 1, 'tomatoes': 0})
    need = pt.SuperDict({'apples': 1, 'pears': 2, 'tomatoes': 1})
    left_need = need - have
    # {'pears': 1, 'tomatoes': 1}


Filtering
-----------------

Example data::

    import pytups as pt
    indent_dict = {'aabb': 1, 'aacc': 2, 'bbaa': 1}
    my_superdict = pt.SuperDict.from_dict(indent_dict)

According to the value in the dictionary::

    my_superdict.vfilter(lambda v: v==1)
    # {'aabb': 1, 'bbaa': 1}

According to the key::

    my_superdict.kfilter(lambda k: k.startswith('aa'))
    # {'aabb': 1, 'aacc': 2}

Mutations
---------------------

Example data::

    import pytups as pt
    indent_dict = {'aabb': 1, 'aacc': 2, 'bbaa': 1}
    my_superdict = pt.SuperDict.from_dict(indent_dict)


Mutate using the value only::

    my_superdict.vapply(lambda v: v * 2)
    # {'aabb': 2, 'aacc': 4, 'bbaa': 2}

Mutate using the key only::

    my_superdict.kapply(lambda k: k[0])
    # {'aabb': 'a', 'aacc': 'a', 'bbaa': 'b'}

A combination of both::

    my_superdict.kvapply(lambda k, v: k[0] + str(v))
    # {'aabb': 'a1', 'aacc': 'a2', 'bbaa': 'b1'}


Setting and getting in nested dictionaries
-------------------------------------------------------

Example data::

    import pytups as pt
    indent_dict = {'a': {'b': {'c': 'A'}}, 'b': {'t': {'d' : 'B'}}}
    my_superdict = pt.SuperDict.from_dict(indent_dict)

Getting an path of values::

    my_superdict.get_m('a', 'b', 'c')
    # 'A'
    my_superdict.get_m('a', 'c')
    # None

Setting a path of values::

    my_superdict.set_m('a', 'c', value='R')
    # {'a': {'b': {'c': 'A'}, 'c': 'R'}, 'b': {'t': {'d': 'B'}}}


Aggregating
------------------------------------------

Aggregating a dictionary requires doing: `SuperDict` --> `TupList` --> `SuperDict`::

    import pytups as pt
    my_dict = pt.SuperDict({('a', 'b'): 1, ('a', 'c'): 2, ('f', 'c'): 3})

    my_dict.to_tuplist().to_dict(indices=0, result_col=2).vapply(sum)
    result = (
        my_dict
        # convert to TupList -> [('a', 'b', 1), ('a', 'c', 2), ('f', 'c', 3)]
        .to_tuplist()
        # convert to dict of lists -> {'a': [1, 2], 'f': [3]}
        .to_dict(indices=0, result_col=2).
        # sum each list -> {'a': 3, 'f': 3}
        vapply(sum)
    )
    # {'a': 3, 'f': 3}


TupLists
=============================

Lists of tuples of any size.

Example::

    import pytups as pt
    _list = [('a', 'b', 'c', 1), ('a', 'b', 'c', 2), ('a', 'b', 'c', 3),
            ('r', 'b', 'c', 1), ('r', 'b', 'c', 2), ('r', 'b', 'c', 3)]
    tuplist = pt.TupList(_list)
    tuplist.filter([0, 2]).unique()
    # [('a', 'c'), ('r', 'c')]
    tuplist.to_dict(result_col=3, is_list=True)
    # {('a', 'b', 'c'): [1, 2, 3], ('r', 'b', 'c'): [1, 2, 3]}
    tuplist.filter_list_f(lambda x: x[0] <= 'a')
    # [('a', 'b', 'c', 1), ('a', 'b', 'c', 2), ('a', 'b', 'c', 3)]

Compress using start-stop
----------------------------

A specific use case of tuplists is reducing combinations of possibilities to start-stop combinations.

In the following example we have tuples and we use the first column as index and the second as the position. We get that index `a` has values from `1` to `3`. Index `r`, on the other hand, has consecutive elements `3` to `4`, but has one element without consecutive `1`. So, we pass from having six tuples to only three that retain the same information. In this example `compare_tups` is just a function that asks whether the key is the same or the positions are consecutive::

    import pytups as pt
    _list = [('a', 1), ('a', 2), ('a', 3), ('r', 1), ('r', 3), ('r', 4)]

    compare_tups = lambda x, y, p: x[0] != y[0] or x[p] -1 != y[p]
    pt.TupList(_list).to_start_finish(compare_tups, pp=1)
    # [('a', 1, 3), ('r', 1, 1), ('r', 3, 4)]

A somewhat similar but more complex example follows. Instead of using values to retain the position, we use dates. So, in order to compare dates we have to define some auxiliary function to be able to tell if two dates are consecutive or not. The result is similar.::

    import pytups as pt
    import datetime as dt
    _list = [('a', '2019-01-01'), ('a', '2019-01-02'), ('a', '2019-01-03'),
                ('r', '2019-01-01'), ('r', '2019-01-03'), ('r', '2019-01-04')]

    def prev_date(date):
        return (dt.datetime.strptime(date, '%Y-%m-%d') - dt.timedelta(days=1)).strftime('%Y-%m-%d')

    compare_tups = lambda x, y, p: x[0] != y[0] or prev_date(x[p]) != y[p]
    pt.TupList(_list).to_start_finish(compare_tups, pp=1)
    # [('a', '2019-01-01', '2019-01-03'), ('r', '2019-01-01', '2019-01-01'), ('r', '2019-01-03', '2019-01-04')]


Ordered sets
=============================

We have implemented the most common list operations to use it as a list. The purpose is mainly to use it as a sequence of things in order to ask for the position, the next element and the previous one and X elements from it.

Specially useful for a list of dates, months, when you want fast lookup speeds.

As a set, it can only take as element hashable objects (lists are not ok: tuples are).

Coming from R
=========================

In R, you have the `apply` family of function, that apply a function over some list or vector.

The closest to this function would be the `vapply` functions in both dictionaries and tuplists.

In R one can do the following::

    sapply(c(1, 2, 5, 7, 11), as.character)
    # "1"  "2"  "5"  "7"  "11"

Or, using the chaining magic and without actually using the `sapply` given that R works vectorized by default::

    library(magrittr)
    c(1, 2, 5, 7, 11) %>% as.character
    # "1"  "2"  "5"  "7"  "11"

With pytups one would do::

    import pytups as pt
    pt.TupList([1, 2, 5, 7, 11]).vapply(str)
    # ['1', '2', '5', '7', '11']

A better example could be replacing `sapply` in the following R situation::
    
    lll <- list(c(1, 2, 5, 7, 5), c(5, 6, 7))
    sapply(lll, length)
    # 5 3

We would do the following in pytups::
    
    import pytups as pt
    pt.TupList([(1, 2, 5, 7, 5), (5, 6, 7)]).vapply(len)
    # [5, 3]