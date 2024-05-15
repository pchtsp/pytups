Pytups
**************************
.. image:: https://img.shields.io/pypi/v/pytups.svg
    :target: https://pypi.org/project/pytups/
.. image:: https://img.shields.io/pypi/l/pytups.svg
    :target: https://pypi.org/project/pytups/
.. image:: https://img.shields.io/pypi/pyversions/pytups.svg
    :target: https://pypi.org/project/pytups/
.. image:: https://travis-ci.org/pchtsp/pytups.svg?branch=master
    :target: https://travis-ci.org/pchtsp/pytups

What and why
================

The idea is to allow sparse operations to be executed in matrix data.

I grew used to the chained operations in R's `tidyverse <https://www.tidyverse.org/>`_  packages or, although not a great fan myself, python's `pandas <https://pandas.pydata.org/>`_ . I find myself using dictionary and list comprehensions all the time to pass from one data format to the other efficiently. But after doing it for the Nth time, I thought of automaticing it.

In my case, it helps me construct optimisation models with  `PuLP <https://github.com/coin-or/pulp>`_. I see other possible uses not related to OR.

I've implemented some additional methods to regular dictionaries, lists and sets to come up with interesting methods that somewhat quickly pass from one to the other and help with data wrangling.

In order for the operations to make any sense, the assumption that is done is that whatever you are using has the same 'structure'. For example, if you a have a list of tuples: every element of the list is a tuple with the same size and the Nth element of the tuple has the same type, e.g. ``[(1, 'red', 'b', '2018-01'), (10, 'ccc', 'ttt', 'ff')]``. Note that both tuples have four elements and the first one is a number, not a string. We do not check that this is consistent.

They're made to always return a new object, so no "in-place" editing, hopefully.

Right now there are three classes to use: dictionaries, tuple lists and ordered sets.

Python versions
================

Python 3.8 and up.


Quick example
================

We index a tuple list according to some index positions.::

    import pytups as pt
    some_list_of_tuples = [('a', 'b', 'c', 1), ('a', 'b', 'c', 2), ('a', 'b', 'c', 45)]
    tp_list = pt.TupList(some_list_of_tuples)
    tp_list.to_dict(result_col=3)
    # {('a', 'b', 'c'): [1, 2, 45]}
    tp_list.to_dict(result_col=3).to_dictdict()
    # {'a': {'b': {'c': [1, 2, 45]}}}
    tp_list.to_dict(result_col=[2, 3])
    # {('a', 'b'): [('c', 1), ('c', 2), ('c', 45)]}

We do some operations on dictionaries with common keys.::

    import pytups as pt
    some_dict = pt.SuperDict(a=1, b=2, c=3, d=5)
    some_other_dict = pt.SuperDict(a=5, b=7, c=1)
    some_other_dict + some_dict
    # {'a': 6, 'b': 9, 'c': 4}
    some_other_dict.vapply(lambda v: v**2)
    # {'a': 25, 'b': 49, 'c': 1}
    some_other_dict.kvapply(lambda k, v: v/some_dict[k])
    # {'a': 5.0, 'b': 3.5, 'c': 0.3333333333333333}

Installing
================

::

    pip install pytups

or, for the development version::

    pip install https://github.com/pchtsp/pytups/archive/master.zip

Testing
================

Run the command::
    
    python -m unittest discover -s tests

if the output says OK, all tests were passed.