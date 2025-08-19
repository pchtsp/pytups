Philisophy
**************************

Working with 1-dimensional data
=======================================

Just like in R, vectors are just expected everywhere, it would be nice to work with dictionaries and lists just as if they were vectors. In this way, we could just apply functions to them, sum them, etc. without too much thinking on what happens inside. Python has list comprehensions and that is already very good. Also, numpy has fairly good support for vectorized operations.

Sadly, I usually use dictionaries to manipulate my data. And there is not a very good way to work with dictionaries and numpy. And, after using list comprehensions for a long time, I find that they take a lot of space and time to write and I *usually* have very simple needs for my dictionary operations.

For cases when multidimensional data is needed, I usually like to think of lists of tuples. This is the closest to a table (dataframe) that one can get without having to use pandas.

Chaining operations
=============================

I really like `dplyr`, `magrittr` and `tidyverse` libraries in R. They provide a light, concise series of steps to show the process in the data manipulation. Pandas can, sometimes, provide this. But pandas sometimes is too heavy for small, fast operations and tables sometimes do not provide the good data format for some situations.

Most functions available in `pytups` return an object instead of changing it 'in place'. So, for example if a function is applies to a dictionary::

    import pytups as pt
    original = pt.SuperDict({'a': 1, 'b': 2, 'f': 3})
    new = original.vapply(lambda: x: x**2)
    print(original)
    # {'a': 1, 'b': 2, 'f': 3}
    print(new)
    # {'a': 1, 'b': 4, 'f': 9}

This can lead to several chaining operations::

    import pytups as pt
    pt.SuperDict({'a': 1, 'b': 2, 'f': 3}).
        vapply(lambda x: x**2).\
        clean(1).\
        fill_with_default(['a', 'b', 'c', 'd', 'e', 'f']).\
        to_tuplist()
    # [('a', 0), ('b', 4), ('c', 0), ('d', 0), ('e', 0), ('f', 9)]


Interoperability of types
===========================================

There are two main data types that are tightly related via two functions: :py:func:`pytups.superdict.SuperDict.to_tuplist` for :py:class:`pytups.superdict.SuperDict` and :py:func:`pytups.tuplist.TupList.to_dict` for :py:class:`pytups.tuplist.TupList`.


Going from dictionaries to tuple lists
---------------------------------------------

If one has a single-level dictionary, one can get a tuple 'fairly' easily by 'just' appending the value of the dictionary into the keys. It's almost equivalent to using the `items` function of a dictionary but applies the `TupList` type.

::

    import pytups as pt
    pt.SuperDict({'a': 1, 'b': 2, 'f': 3}).to_tuplist()
    # [('a', 1), ('b', 2), ('f', 3)]
    pt.SuperDict({'a': 1, 'b': 2, 'f': 3}).items()
    # dict_items([('a', 1), ('b', 2), ('f', 3)])

In some, cases this function takes some liberties to interpret the content so as to make the TupList flat::

    import pytups as pt
    pt.SuperDict({'a': [1, 2, 5], 'b': 2, 'f': 3}).to_tuplist()
    # [('a', 1), ('a', 2), ('a', 5), ('b', 2), ('f', 3)]
    pt.SuperDict({'a': [1, 2, 5], 'b': 2, 'f': 3}).items()
    # dict_items([('a', [1, 2, 5]), ('b', 2), ('f', 3)])

So, if it finds some list, it iterates over it. Using the regular `items` function would not do that.

Sometimes, we start with a nested dictionary. If we want to get a tuple from this, we need to first convert it into a flat dictionary and then get a tuple list::

    import pytups as pt
    indent_dict = {'a': {'b': {'c': 'A'}}, 'b': {'t': {'d' : 'B'}}}
    supdict = pt.SuperDict.from_dict(indent_dict)
    supdict_dictup = supdict.to_dictup()
    # {('a', 'b', 'c'): 'A', ('b', 't', 'd'): 'B'}
    tuplist = supdict_dictup.to_tuplist()
    print(tuplist)
    # [('a', 'b', 'c', 'A'), ('b', 't', 'd', 'B')]
    type(tuplist)
    # <class 'pytups.tuplist.TupList'>


Going from tuple lists to dictionaries
---------------------------------------------

If one has a list of tuples, one can obtain a dictionary indexed in some way over part of the tuple. In a way, is like creating a key in a database table or a :meth:`pandas.DataFrame.groupby` function in :py:mod:`pandas` with the difference that it creates a new variable with the modifications.

Starting with the previous example one can reverse the tuplist quite easily::

    import pytups as pt
    tuplist = pt.TupList([('a', 'b', 'c', 'A'), ('b', 't', 'd', 'B')])
    tuplist.to_dict(3, is_list=False)
    # {('a', 'b', 'c'): 'A', ('b', 't', 'd'): 'B'}

This function assumes by default that the result will be a list. One can enforce only the last value by using `is_list=False`. But, now that we are starting with the flatten tuple list, we can choose a different way to index it::

    tuplist.to_dict(0, is_list=False)
    # {('b', 'c', 'A'): 'a', ('t', 'd', 'B'): 'b'}

We can also give a list as a resulting column, so::

    tuplist.to_dict([0, 3], is_list=False)
    # {('b', 'c'): ('a', 'A'), ('t', 'd'): ('b', 'B')}

By default, we assume that the index will be the complement of the resulting column. But we can also give an explicit index for the dictionary if we want to drop some of the values or we want to change the order of the key::

    tuplist.to_dict([0, 3], is_list=False, indices=[2, 1])
    # {('c', 'b'): ('a', 'A'), ('d', 't'): ('b', 'B')}
    tuplist.to_dict([0, 3], is_list=False, indices=[2])
    # {'c': ('a', 'A'), 'd': ('b', 'B')}

