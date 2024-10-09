"""Update Log

2024.10.07:
    - the interface previously exported by export() was changed to manually add the interface to __all__
    - removed the unused function unpacking_zip()
    - fixed the generic type, such as Predicate, to support any type of inputs
    - fixed flatten() only supports to flatten the builtins iterable and iterator
"""

from __future__ import annotations
import inspect
from functools import wraps
import warnings
import random
from itertools import groupby, product
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Iterable, Mapping, Callable, Iterator
from pycinante.utils import export

@export
def get_executor(max_workers=None, io_intensive=True, **kwargs):
    """
    Return an executor with up to max_workers pool size. If io_intensive is True, a ThreadPoolExecutor is returned,
    otherwise ProcessPoolExecutor.
    """
    executor = ThreadPoolExecutor if io_intensive else ProcessPoolExecutor
    return executor(max_workers=max_workers or cpu_count(), **kwargs)

@export
def concrt_map(func, iters, **kwargs):
    """
    Concurrent map function. An executor can be specified via `executor`, if none of executor was not specified, an io
    intensive executor will be used by default, and it will be shutdown when `concrt_map` finished.
    """
    user_executor = kwargs.pop("executor", None)
    executor = user_executor or get_executor(**kwargs)

    try:
        return executor.map(func, iters)
    finally:
        # if the executor is created by native, it will be shutdown
        if user_executor is None:
            executor.shutdown(wait=True)

@export
def concrt_filter(func, iters, **kwargs):
    """
    Concurrent filter function. An executor can be specified via `executor`, if none of executor was not specified, an
    io intensive executor will be used by default, and it will be shutdown when `concrt_filter` finished.
    """
    return (a for a, b in concrt_map(lambda e: (e, func(e)), iters=iters, **kwargs) if b)

@export
class MemoryBuffer(Iterable):
    """
    A helper class for holding a set of instances. It extends the properties of generator.
    """

    def __init__(self, element=None):
        if isinstance(element, (Iterable, Callable)):
            self._elements = element
        else:
            self._elements = [] if element is None else [element]

    def __iter__(self):
        """
        Return an iterator. All elements will be evaluated when the method has been calling.
        """
        yield from self._elements() if callable(self._elements) else self._elements

@export
def try_catch(ignored=Exception, val=None, name="_else"):
    """
    A wrapper for catching a or a group of exceptions and returns the failed results when one of the exception occurs.
    """
    def _wrapper(func):
        sig = inspect.signature(func)

        @wraps(func)
        def _decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ignored:
                for key, value in sig.bind(*args, **kwargs).arguments.items():
                    if key == name:
                        return value or val
                    elif isinstance(value, Mapping) and name in value:
                        return value.get(name) or val
                return val
        return _decorator
    return _wrapper

@export
def identity(*args, **kwargs):
    """
    Return the same arguments as the fed.
    """
    def _unwrap(e):
        return e[0] if len(e) == 1 else e

    if args and kwargs:
        return _unwrap(args), kwargs
    else:
        if args:
            return _unwrap(args)
        if kwargs:
            return kwargs
    return None

@export
def distinct(iterable, key):
    """
    Filters items from iterable and returns only distinct ones. Keeps order.
    """
    key, exist_keys = key or identity, set()
    for item in iterable:
        if (k := key(item)) not in exist_keys:
            exist_keys.add(k)
            yield item

STR_TRUE_SET = {"yes", "true", "t", "y", "1"}
STR_FALSE_SET = {"no", "false", "f", "n", "0"}

@export
def bool_plus(obj, default=bool):
    """
    Convert an obj as a bool. The default() could be fed into for specific type of objs.
    """
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, str):
        if obj.lower() in STR_TRUE_SET:
            return True
        if obj.lower() in STR_FALSE_SET:
            return False
    return default(obj)

@export
def flatten(iterable):
    """
    Generate each element of the given iterable. If the element is iterable and is not string, it yields each sub-element
    of the element recursively.
    """
    for item in iterable:
        if isinstance(item, (list, tuple, set, dict, Iterator)) and not isinstance(item, (str, bytes)):
            for sub_item in flatten(item):
                yield sub_item
        else:
            yield item

@export
def conditional_warning(condition, msg="", **kwargs):
    """
    If condition is True, then raise a warning with the msg.
    """
    if condition:
        warnings.warn(msg, **kwargs)

@export
def reorder(iterables, orders):
    """
    Return a new iterator with the new orders.
    """
    iterables = tuple(iterables)
    for index in orders:
        yield iterables[index]

@export
def shuffle(iterables):
    """
    Return a new iterator with the random orders.
    """
    iterables = tuple(iterables)
    orders = list(range(len(iterables)))
    random.shuffle(orders)
    yield from reorder(iterables, orders)

@export
def peek(element, func):
    """
    Does the same as `Java 8 peek. That is consuming the element and return itself.
    """
    func(element)
    return element

@export
def group_by(iterable, key=identity):
    """
    Make an iterator that returns consecutive keys and groups from the iterable.
    """
    return groupby(sorted(iterable, key=key), key=key)

@export
def parallel_warning(parallel, **kwargs):
    """
    A helper function used to raise a warning when the parallel is enabled but the method do not support.
    """
    if parallel or any((key in kwargs for key in ("executor", "io_intensive"))):
        co_name = inspect.currentframe().f_back.f_code.co_name
        warnings.warn(f"the {co_name}'s implementation is not supported for parallel.")

@export
def cartesian_product(iterable, repeat: int = 1):
    """
    Return a cartesian product of input iterables.
    """
    return product(*iterable) if repeat == 1 else product(iterable, repeat=repeat)

@export
def get_el_by_index(iterable, index: int):
    """
    Return the indexed element of the iterable.
    """
    if index >= 0:
        counter = 0
        iterable = iter(iterable)
        while counter < index:
            next(iterable)
            counter += 1
        return next(iterable)
    else:
        # for negative-indexed element
        return tuple(iterable)[index]

@export
def supress(supplier, ignored, handler):
    """
    Return the result of the func. Suppressing the specific exception when the func is running.
    """
    try:
        return supplier()
    except ignored as exc:
        if handler is not None:
            return handler(exc)

@export
def format(obj, template):
    """
    Return a string with filling the template with obj.
    """
    if isinstance(obj, Mapping):
        return template.format_map(obj)
    elif isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        return template.format(*obj)
    return template.format(obj)
