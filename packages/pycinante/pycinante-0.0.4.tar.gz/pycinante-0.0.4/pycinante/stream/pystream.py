"""Update Log

2024.10.08:
    - completely tested stream's functionalities provided already
    - fixed some known bugs
    - added the support for requests
"""

from functools import partial, reduce
from itertools import islice, tee, chain
import re
import sys
from decimal import Decimal
from operator import add
import requests
from pycinante.stream.utils import *
from pycinante.io.accessor import match_file_accessor
from pycinante.io.utils import get_ext
from pycinante.utils import optional_import
from typing import Iterable

__all__ = ["stream"]

class Stream(Iterable):
    """
    A sequence of elements supporting sequential and parallel aggregate operations.
    """

    @staticmethod
    def of(element=None, **kwargs):
        """
        Returns a sequential ordered stream whose elements are the specified values.
        """
        return Stream(element, **kwargs)

    @staticmethod
    def range(*args, **kwargs):
        """
        Returns a sequential ordered stream whose elements are generated from the range.
        """
        return Stream(range(*args), **kwargs)

    @staticmethod
    def concat(*streams, **kwargs):
        """
        Return a union stream of concatenating a set of streams.
        """
        return Stream(lambda: chain.from_iterable(streams), **kwargs)

    @staticmethod
    def load(path, loader, **kwargs):
        """
        Return a stream of consisting of elements which is loaded from a path file.
        """
        return Stream((loader or match_file_accessor(get_ext(path)).load)(path), **kwargs)

    def __init__(self, element=None, executor=None, **kwargs):
        """
        Construct a stream from the given element.
        """
        self._element = MemoryBuffer(element)
        self._executor = executor

    @property
    def _copy_element(self):
        """
        Return a copy version of the current element iterator.
        """
        self._element, element = tee(self._element)
        return element

    # map #

    def map(self, mapper, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of applying the given function to the elements of this stream.
        """
        if mapper != identity:
            # for exception handling
            new_mapper = None
            if (ignored := kwargs.pop("ignored", None)) is not None:
                new_mapper = lambda e: supress(
                    lambda: mapper(e),
                    ignored=ignored,
                    handler=kwargs.pop("handler", None)
                )

            # for concurrent executing
            kwargs["executor"] = kwargs.pop("executor", self._executor)
            func = (parallel and partial(concrt_map, **kwargs)) or map
            return Stream(lambda: func(new_mapper or mapper, self._copy_element), executor=self._executor)
        return self

    def map_by_index(self, index: int, mapper, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of applying the given function to the indexed elements of this stream.
        """
        def _mapper(e):
            assert isinstance(e, list), "only list element can be applied with map_by_index()"
            e[index] = mapper(e[index])
            return e

        return self.map(_mapper, parallel, **kwargs)

    def map_key(self, mapper, default_index: int = 0, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of mapping only key in [key, value] pair.
        """
        return self.map_by_index(index=default_index, mapper=mapper, parallel=parallel, **kwargs)

    def map_value(self, mapper, default_index: int = 1, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of mapping only value in [key, value] pair.
        """
        return self.map_by_index(index=default_index, mapper=mapper, parallel=parallel, **kwargs)

    def keys(self, default_index: int = 0, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of only key in [key, value] pair.
        """
        return self.map(lambda e: e[default_index], parallel, **kwargs)

    def values(self, default_index: int = 1, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of only value in [key, value] pair.
        """
        return self.map(lambda e: e[default_index], parallel, **kwargs)

    def enumerate(self, start: int = 0, parallel=False, **kwargs):
        """
        Return a stream consisting of the element of (index, element) pairs.
        """
        parallel_warning(parallel, **kwargs)
        return Stream(zip(range(start, sys.maxsize), self._copy_element), executor=self._executor)

    def flatten(self, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of replacing each element of this stream with its flatten elements.
        """
        parallel_warning(parallel, **kwargs)
        return Stream(flatten(self._copy_element), executor=self._executor)

    def group_by(self, key=identity, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of grouping by the key(element) of this stream.
        """
        parallel_warning(parallel, **kwargs)
        return Stream(group_by(self._copy_element, key=key), executor=self._executor)

    def zip(self, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of zipping element of this stream.
        """
        parallel_warning(parallel, **kwargs)
        return Stream(lambda: zip(*self._copy_element), executor=self._executor)

    def product(self, repeat: int = 1, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of the Cartesian Product of stream, similar with itertools.product.
        """
        parallel_warning(parallel, **kwargs)
        return Stream(partial(cartesian_product, iterable=self._copy_element, repeat=repeat), executor=self._executor)

    def int(self, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of applying the int function to the elements of this stream.
        """
        return self.map(int, parallel, **kwargs)

    def float(self, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of applying the float function to the elements of this stream.
        """
        return self.map(float, parallel, **kwargs)

    def decimal(self, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of applying the Decimal function to the elements of this stream.
        """
        return self.map(Decimal, parallel, **kwargs)

    def str(self, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of applying the str function to the elements of this stream.
        """
        return self.map(str, parallel, **kwargs)

    def format(self, template: str, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of applying the format function to the elements of this stream.
        """
        return self.map(partial(format, template=template), parallel, **kwargs)

    # # map / requests

    def request(self, method: str, parallel=False, ignored=None, handler=None, session=None, **kwargs):
        """
        Return a stream consisting of the results of sending a request. Note that if you want set the executor argument
        there are a need of the new exc_params dict for this purpose.
        """
        def _request(url):
            func = (session is not None and session.request) or requests.request
            return func(method=method, url=url, **kwargs)

        exc_params = kwargs.pop("exc_params", {})
        return self.map(_request, parallel, ignored=ignored, handler=handler, **exc_params)

    def get(self, params=None, parallel=False, ignored=None, handler=None, session=None, **kwargs):
        """
        Return a stream consisting of the results of sending a get request.
        """
        kwargs = dict(parallel=parallel, ignored=ignored, handler=handler, session=session, **kwargs)
        return self.request(method="get", params=params, **kwargs)

    def post(self, data=None, json=None, parallel=False, ignored=None, handler=None, session=None, **kwargs):
        """
        Return a stream consisting of the results of sending a post request.
        """
        kwargs = dict(parallel=parallel, ignored=ignored, handler=handler, session=session, **kwargs)
        return self.request(method="post", data=data, json=json, parallel=parallel, **kwargs)

    def json(self, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of a json response.
        """
        return self.map(lambda e: e.json(), parallel, **kwargs)

    def soup(self, parallel=False, **kwargs):
        """
        Return a stream consisting of the results of a BeautifulSoup response.
        """
        def _get_text(item):
            if isinstance(item, (str, bytes)):
                return item
            if isinstance(item, requests.Response):
                return item.text
            raise ValueError(f"unknown type {type(item)} to parse html")

        bs4, _ = optional_import(module="bs4", name="BeautifulSoup")
        return self.map(lambda e: bs4(_get_text(e)), parallel, **kwargs)

    # filter #

    def filter(self, predicate, parallel=False, **kwargs):
        """
        Return a stream consisting of the elements of this stream that match the given predicate.
        """
        # for exception handling
        new_predicate = None
        if (ignored := kwargs.pop("ignored", None)) is not None:
            new_predicate = lambda e: supress(
                lambda: predicate(e),
                ignored=ignored,
                handler=kwargs.pop("handler", None)
            )

        # for concurrent executing
        kwargs["executor"] = kwargs.pop("executor", self._executor)
        func = (parallel and partial(concrt_filter, **kwargs)) or filter
        return Stream(lambda: func(new_predicate or predicate, self._copy_element), self._executor)

    def include(self, predicate, parallel=False, **kwargs):
        """
        An alias of Stream.filter(predicate, kwargs).
        """
        return self.filter(predicate, parallel, **kwargs)

    def exclude(self, predicate, parallel=False, **kwargs):
        """
        Return a stream consisting of the elements of this stream that don't match the given predicate.
        """
        return self.filter(lambda e: not predicate(e), parallel, **kwargs)

    def regexp(self, pattern: str, parallel=False, **kwargs):
        """
        Return a stream consisting of the elements which is matched with the regexp pattern.
        """
        return self.filter(lambda e: bool(re.match(pattern, str(e))), parallel, **kwargs)

    def even(self, parallel=False, **kwargs):
        """
        Return a stream consisting of the elements where e is an even.
        """
        return self.filter(lambda e: float(e) % 2 == 0, parallel, **kwargs)

    def odd(self, parallel=False, **kwargs):
        """
        Return a stream consisting of the elements where e is an odd.
        """
        return self.filter(lambda e: float(e) % 2 != 0, parallel, **kwargs)

    def divisible_by(self, number, parallel=False, **kwargs):
        """
        Return a stream consisting of the elements where e is divisible by the given one.
        """
        return self.filter(lambda e: float(e) % number == 0, parallel, **kwargs)

    def distinct(self, key=identity, parallel=False, **kwargs):
        """
        Return a stream consisting of the distinct elements (according to __eq__) of this stream.
        """
        parallel_warning(parallel, **kwargs)
        return Stream(distinct(self._copy_element, key=key))

    def instance_of(self, types, parallel=False, **kwargs):
        """
        Return a stream consisting of the elements where e is instance of given type or types.
        """
        return self.filter(lambda e: isinstance(e, types), parallel, **kwargs)

    def no_none(self, parallel=False, **kwargs):
        """
        Return a stream consisting of the elements where e is not None.
        """
        return self.filter(lambda e: e is not None, parallel, **kwargs)

    def no_false(self, default=bool, parallel=False, **kwargs):
        """
        Return a stream consisting of the elements where bool_plus(e) == True.
        """
        return self.filter(lambda e: bool_plus(e, default), parallel, **kwargs)

    def limit(self, max_size: int, parallel=False, **kwargs):
        """
        Return a stream consisting of the elements of this stream, truncated to be no longer than max_size in length.
        """
        parallel_warning(parallel, **kwargs)
        return self.__class__(islice(self._copy_element, max_size))

    def skip(self, n: int, parallel=False, **kwargs):
        """
        Return a stream consisting of the remaining elements of this stream after discarding the first n elements.
        """
        parallel_warning(parallel, **kwargs)
        return self.__class__(islice(self._copy_element, n, None))

    def first(self, parallel=False, **kwargs):
        """
        Return the first element of this stream, or an `_else` if the stream is empty.
        """
        return self.take(index=0, parallel=parallel, **kwargs)

    def last(self, parallel=False, **kwargs):
        """
        Return the last element of this stream, or an `_else` if the stream is empty.
        """
        return self.take(index=-1, parallel=parallel, **kwargs)

    @try_catch(ignored=(StopIteration, IndexError), name="_else")
    def take(self, index: int, parallel=False, **kwargs):
        """
        Return the element indexed by index of this stream.
        """
        parallel_warning(parallel, **kwargs)
        return get_el_by_index(self._copy_element, index)

    # collect #

    def collect(self, supplier, accumulator, finisher=identity, parallel=False, **kwargs):
        """
        Performs a reduction operation on the elements of this stream using a Collector.
        """
        container = supplier()
        _ = tuple(self.map(lambda e: accumulator(container, e), parallel, **kwargs))
        return finisher(container)

    def tuplify(self, parallel=False, **kwargs):
        """
        Performs a reduction operation on the elements of this stream using a tuple.
        """
        parallel_warning(parallel, **kwargs)
        return tuple(self._copy_element)

    def listify(self, parallel=False, **kwargs):
        """
        Performs a reduction operation on the elements of this stream using a list.
        """
        parallel_warning(parallel, **kwargs)
        return list(self._copy_element)

    def setify(self, parallel=False, **kwargs):
        """
        Performs a reduction operation on the elements of this stream using a set.
        """
        parallel_warning(parallel, **kwargs)
        return set(self._copy_element)

    def dictify(self, parallel=False, **kwargs):
        """
        Performs a mapping operation on the elements of this stream using a dict.
        """
        parallel_warning(parallel, **kwargs)
        return dict(self._copy_element)

    # reduce #

    @try_catch(ignored=(StopIteration, TypeError), name="e")
    def reduce(self, accumulator, e=None, parallel=False, **kwargs):
        """
        Performs a reduction on the elements of this stream, using an associative accumulation function, and returns an
        Optional describing the reduced value, if any.
        """
        parallel_warning(parallel, **kwargs)
        return reduce(accumulator, self._copy_element, e) if e is not None \
            else reduce(accumulator, self._copy_element)

    def any(self, predicate, parallel=False, **kwargs):
        """
        Return whether any elements of this stream match the provided predicate.
        """
        return any(self.map(predicate, parallel, **kwargs))

    def all(self, predicate, parallel=False, **kwargs):
        """
        Return whether all elements of this stream match the provided predicate.
        """
        return all(self.map(predicate, parallel, **kwargs))

    def count(self, parallel=False, **kwargs):
        """
        Return the count of elements in this stream.
        """
        parallel_warning(parallel, **kwargs)
        return len(tuple(self._copy_element))

    def sum(self, parallel=False, **kwargs):
        """
        Return the sum of elements in this stream.
        """
        parallel_warning(parallel, **kwargs)
        return self.reduce(add)

    def mean(self, parallel=False, **kwargs):
        """
        Return the mean of elements in this stream.
        """
        return (self.sum(parallel, **kwargs) or 0) / (self.count(parallel, **kwargs) + 1e-8)

    @try_catch(ignored=(ValueError, StopIteration), name="_else")
    def min(self, key=None, parallel=False, **kwargs):
        """
        Return the minimum element of this stream according to the provided key.
        """
        parallel_warning(parallel, **kwargs)
        return min(self, key=key)

    @try_catch(ignored=(ValueError, StopIteration), name="_else")
    def max(self, key=None, parallel=False, **kwargs):
        """
        Return the maximum element of this stream according to the provided key.
        """
        parallel_warning(parallel, **kwargs)
        return max(self, key=key)

    def join(self, sep: str = "", parallel=False, **kwargs):
        """
        Return a joining string of this stream by sep.
        """
        return sep.join(self.str(parallel, **kwargs))

    # order #

    def reorder(self, orders: Iterable[int], parallel=False, **kwargs):
        """
        Return a stream consisting of the reordered elements.
        """
        parallel_warning(parallel, **kwargs)
        return Stream(reorder(self._copy_element, orders), executor=self._executor)

    def sort(self, key=None, ascending=True, parallel=False, **kwargs):
        """
        Returns a stream consisting of the elements of this stream, sorted according to key.
        """
        parallel_warning(parallel, **kwargs)
        return Stream(lambda: sorted(self._copy_element, key=key, reverse=not ascending))

    def reverse(self, parallel=False, **kwargs):
        """
        Returns a stream consisting of the reversed order elements of this stream.
        """
        parallel_warning(parallel, **kwargs)
        return Stream(reversed(tuple(self._copy_element)), executor=self._executor)

    def shuffle(self, parallel=False, **kwargs):
        """
        Returns a stream consisting of the random order elements of this stream.
        """
        parallel_warning(parallel, **kwargs)
        return self.__class__(shuffle(self._copy_element), executor=self._executor)

    # traverse #

    def peek(self, action, parallel=False, **kwargs):
        """
        Returns a stream consisting of the elements of this stream, additionally performing the provided action on each
        element as elements are consumed from the resulting stream.
        """
        return self.map(lambda e: peek(e, action), parallel, **kwargs)

    def foreach(self, action, parallel=False, **kwargs):
        """
        Performs an action for each element of this stream.
        """
        for _ in self.map(action, parallel, **kwargs): ...

    # magic #

    def __len__(self):
        """
        Return the count of elements in this stream.
        """
        return self.count()

    def __getitem__(self, index):
        """
        Return the element indexed by index of this stream.
        """
        if isinstance(index, int):
            return self.take(index)
        return Stream(lambda: islice(self._copy_element, index.start, index.stop, index.step))

    def __iter__(self):
        """
        Return an iterator. All elements will be evaluated when the method has been calling.
        """
        return self._element.__iter__()

stream = Stream
