## Pytups
[![Build Status](https://travis-ci.org/pchtsp/pytups.svg?branch=master)](https://travis-ci.org/pchtsp/pytups)

## What and why

I grew used to the chained operations in R's `tidyverse` packages or, although not a great fan myself, python's `pandas`. I find myself using dictionary and list comprehensions all the time to pass from one data format to the other efficiently. But after doing it for the Nth time, I thought of automaticing it.

In my case, it helps me construct optimisation models with [PuLP](https://github.com/coin-or/pulp). I see other possible uses not related to OR.

I've implemented some additional methods to regular dictionaries, lists and sets to come up with interesting methods that somewhat quickly pass from one to the other and help with data wrangling.

In order for the operations to make any sense, the assumption that is done is that whatever you are using has the same 'structure'. For example, if you a have a list of tuples: every element of the list is a tuple with the same size and the Nth element of the tuple has the same type, e.g. `[(1, 'red', 'b', '2018-01'), (10, 'ccc', 'ttt', 'ff')]`. Note that both tuples have four elements and the first one is a number, not a string. We do not check that this is consistent.

They're made to always return a new object, so no "in-place" editing, hopefully.

Right now there are three classes to use. 

## Quick example

We reverse a nested dictionary to take the deepest key outside while keeping the same final values. This chain of operations uses both `superdict` and `tuplist` at different points.

```python
    import pytups as pt
    some_dict = {'a': {'b': {'c': 'A'}}, 'b': {'t': {'c' : 'B'}}}
    pt.SuperDict.from_dict(some_dict).\
        to_dictup().\
        to_tuplist().\
        filter([2, 0, 1, 3]).\
        to_dict(result_col=3, is_list=False).\
        to_dictdict()
    # {'c': {'a': {'b': 'A'}, 'b': {'t': 'B'}}}
```

## Installing

    pip install pytups

or, for the development version:

    pip install https://github.com/pchtsp/pytups/archive/master.zip

## Testing

Run the command 
    
    python -m unittest discover -s tests

 if the output says OK, all tests were passed.

## Reference

### Superdicts

These are dictionaries with additional methods based on the contents.

Example:

```python
    import pytups as pt
    indent_dict = {'a': {'b': {'c': 'A'}}, 'b': {'t': {'d' : 'B'}}}
    supdict = pl.Superdict.from_dict(indent_dict)
    supdict_dictup = supdict.to_dictup()
    # {('a', 'b', 'c'): 'A', ('b', 't', 'd'): 'B'}
    supdict_dictup.to_tup()
    # [('a', 'b', 'c', 'A'), ('b', 't', 'd', 'B')]
    supdict_dictup.apply(lambda k, v: v+'_1')
    # {('a', 'b', 'c'): 'A_1', ('b', 't', 'd'): 'B_1'}
    supdict_dictup.to_dictdict()
    # {'a': {'b': {'c': 'A'}}, 'b': {'t': {'d' : 'B'}}}
```

### tuplists

Lists of tuples of any size.
Example:

```python
    _list = [('a', 'b', 'c', 1), ('a', 'b', 'c', 2), ('a', 'b', 'c', 3),
            ('r', 'b', 'c', 1), ('r', 'b', 'c', 2), ('r', 'b', 'c', 3)]
    tuplist = pt.TupList(_list)
    tuplist.filter([0, 2]).unique()
    # [('a', 'c'), ('r', 'c')]
    tuplist.to_dict(result_col=3, is_list=True)
    # {('a', 'b', 'c'): [1, 2, 3], ('r', 'b', 'c'): [1, 2, 3]}
    tuplist.test_filter_list_f(lambda x: x[0] <= 'a')
    # [('a', 'b', 'c', 1), ('a', 'b', 'c', 2), ('a', 'b', 'c', 3)]
```

### ordered sets

We have implemented the most common list operations to use it as a list. The purpose is mainly to use it as a sequence of things in order to ask for the position, the next element and the previous one and X elements from it.

Specially useful for a list of dates, months, when you want fast lookup speeds.

As a set, it can only take as element hashable objects (lists are not ok: tuples are).