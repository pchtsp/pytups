## Pytups
[![Build Status](https://travis-ci.org/pchtsp/pytups.svg?branch=master)](https://travis-ci.org/pchtsp/pytups)

## What and why

I grew used to the chained operations `dplyr` in R. Also, although not a great fan myself, `pandas`. The thing is in python I find myself using dictionary and list comprehensions all the time to pass from one data format to the other efficiently. But after doing it for the Nth time, I thought of automaticing it.

In my case, it helps me construct optimisation models with `pulp`. I see other possible uses not related to OR.

I've just implemented some additional methos to regular dictionaries, lists and ordered dictionaries to come up with interesting methos that somewhat quickly pass from one to the other and help with data wrangling.

In order for the operations to make any sense, the assumption that is done is that whatever you are running functions in, has the same structure. For examplem, if you a have a list of tuples: every element of the list is a tuple with the same type and the same types of elements inside the tuple, e.g. `[(1, 'red', 'b', '2018-01'), (10, 'ccc', 'ttt', 'ff')]`. Note that both tuples have four elements and the first one is a number, not a string. We do not check that this is consistent.

The're made to always return a new object, so no "in-place" editing.

Right now there are three classes to use. 

## Quick example

```python
    import pytups as pt
```

## Installing

    pip install pytups

or, for the development version:

    pip install https://github.com/pchtsp/pytups/archive/master.zip

## Testing

Run the command 
    
    python -m unittest test

 if the output says OK, all tests were passed.

## Reference

### Superdicts

These are just dictionaries with additional methods based on the contents.

```python
    import pytups as pt
    some_dict = {'a': 1, }
    some_dict = pl.Superdict(some_dict)
    some_dict.to_tup()  #  [('a', 1)]
    some_dict_plus_one = some_dict.apply(lambda k, v: v+1)  #  {'a': 2}
```

### tuplists

Lists of tuples of any size.

```python
    import orloge as ol
    ol.get_info_log_solver(path_to_solver_log, solver_name)
```

This returns a python dictionary with a lot of information from the log (see *Examples* below).

### ordered sets

This was somewhat copied from other libraries (inspired by `pyomo`). It seems to be a list but in fact is an instance of an ordered dictionary. We have just implemented the most common list operations to use it as a list.

The purpose is mainly to use it as a sequence of things in order to ask for the position, the next element and the previous one.

Specially useful for a list of dates, months, etc.