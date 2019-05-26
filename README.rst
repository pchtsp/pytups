Pytups
**************************
.. image:: https://travis-ci.org/pchtsp/pytups.svg?branch=master
    :target: https://travis-ci.org/pchtsp/pytups

.. highlight:: python

What and why
================

I grew used to the chained operations in R's `tidyverse <https://www.tidyverse.org/>`_  packages or, although not a great fan myself, python's `pandas <https://pandas.pydata.org/>`_ . I find myself using dictionary and list comprehensions all the time to pass from one data format to the other efficiently. But after doing it for the Nth time, I thought of automaticing it.

In my case, it helps me construct optimisation models with  `PuLP <https://github.com/coin-or/pulp>`_. I see other possible uses not related to OR.

I've implemented some additional methods to regular dictionaries, lists and sets to come up with interesting methods that somewhat quickly pass from one to the other and help with data wrangling.

In order for the operations to make any sense, the assumption that is done is that whatever you are using has the same 'structure'. For example, if you a have a list of tuples: every element of the list is a tuple with the same size and the Nth element of the tuple has the same type, e.g. ``[(1, 'red', 'b', '2018-01'), (10, 'ccc', 'ttt', 'ff')]``. Note that both tuples have four elements and the first one is a number, not a string. We do not check that this is consistent.

They're made to always return a new object, so no "in-place" editing, hopefully.

Right now there are three classes to use: dictionaries, tuple lists and ordered sets.

Quick example
================

We reverse a nested dictionary to take the deepest key outside while keeping the same final values. This chain of operations uses both `superdict` and `tuplist` objects at different points.::

    import pytups as pt
    some_dict = {'a': {'b': {'c': 'A'}}, 'b': {'t': {'c' : 'B'}}}
    pt.SuperDict.from_dict(some_dict).\
        to_dictup().\
        to_tuplist().\
        filter([2, 0, 1, 3]).\
        to_dict(result_col=3, is_list=False).\
        to_dictdict()
    # {'c': {'a': {'b': 'A'}, 'b': {'t': 'B'}}}

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