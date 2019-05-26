Some examples
**************************

.. highlight:: python

Coming from R
=========================

In R, you have the `apply` family of function, that apply a function over some list or vector.

The closest to this function would be the `apply` and `vapply` functions in both dictionaries and tuplists.

In R one can do the following::

    sapply(c(1, 2, 5, 7, 11), as.character)
    # "1"  "2"  "5"  "7"  "11"

Or, using the chaining magic::

    library(magrittr)
    c(1, 2, 5, 7, 11) %>% as.character

In fact, R already assumes vectorized functions, so one could use::

    c(1, 2, 5, 7, 11) %>% as.character

With pytups one would do::

    import pytups as pt
    pt.TupList([1, 2, 5, 7, 11]).apply(str)
    # ['1', '2', '5', '7', '11']

SuperDict
=============================

These are dictionaries with additional methods based on the contents.

Example::

    import pytups as pt
    indent_dict = {'a': {'b': {'c': 'A'}}, 'b': {'t': {'d' : 'B'}}}
    supdict = pt.SuperDict.from_dict(indent_dict)
    supdict_dictup = supdict.to_dictup()
    # {('a', 'b', 'c'): 'A', ('b', 't', 'd'): 'B'}
    supdict_dictup.to_tuplist()
    # [('a', 'b', 'c', 'A'), ('b', 't', 'd', 'B')]
    supdict_dictup.apply(lambda k, v: v+'_1')
    # {('a', 'b', 'c'): 'A_1', ('b', 't', 'd'): 'B_1'}
    supdict_dictup.to_dictdict()
    # {'a': {'b': {'c': 'A'}}, 'b': {'t': {'d' : 'B'}}}

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

Ordered sets
=============================

We have implemented the most common list operations to use it as a list. The purpose is mainly to use it as a sequence of things in order to ask for the position, the next element and the previous one and X elements from it.

Specially useful for a list of dates, months, when you want fast lookup speeds.

As a set, it can only take as element hashable objects (lists are not ok: tuples are).