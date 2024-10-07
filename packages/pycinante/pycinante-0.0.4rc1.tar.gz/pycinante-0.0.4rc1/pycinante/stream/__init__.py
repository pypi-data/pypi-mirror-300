from __future__ import annotations
from functools import partial, reduce
from itertools import islice, groupby, product
import re
from concurrent.futures import Executor
import sys
from decimal import Decimal
from operator import add
from pycinante.stream.utils import *
from typing import Iterable, TypeVar, Optional, Iterator, Any, Type, Tuple, Callable, List, Set, Dict
from typing_extensions import Self

__all__ = ["stream"]

E = TypeVar("E")
R = TypeVar("R")
A = TypeVar("A")

class Stream(Iterable[E]):
    """
    A sequence of elements supporting sequential and parallel aggregate operations.
    """

    def __init__(self, element: Element[E] = None, executor: Optional[Executor] = None) -> None:
        self._element = MemoryBuffer(element)
        self._executor = executor

    # map #

    def map(self, mapper: Function[E, R], parallel: bool = False, **kwargs: Any) -> Stream[R]:
        """
        Return a stream consisting of the results of applying the given function to the elements of this stream.
        """
        if mapper != identity:
            func = (parallel and partial(concrt_map, executor=kwargs.pop("executor", self._executor), **kwargs)) or map
            return self.__class__(lambda: func(mapper, self), executor=self._executor)
        return self

    def map_by_index(self, index: int, mapper: Function[E, E], parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the results of applying the given function to the indexed elements of this stream.
        """
        def _mapper(e: E) -> E:
            assert isinstance(e, list), "only list element can be applied with map_by_index()"
            e[index] = mapper(e[index])
            return e
        return self.map(_mapper, parallel, **kwargs)

    def map_key(self, mapper: Function[E, E], default_index: int = 0, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the results of mapping only key in [key, value] pair.
        """
        return self.map_by_index(index=default_index, mapper=mapper, parallel=parallel, **kwargs)

    def map_value(self, mapper: Function[E, E], default_index: int = 1, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the results of mapping only value in [key, value] pair.
        """
        return self.map_by_index(index=default_index, mapper=mapper, parallel=parallel, **kwargs)

    def enumerate(self, start: int = 0, parallel: bool = False, **kwargs: Any) -> Stream[Tuple[int, E]]:
        """
        Return a stream consisting of the element of (index, element) pairs.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return self.__class__(zip(range(start, sys.maxsize), self), executor=self._executor)

    def flatten(self, parallel: bool = False, **kwargs: Any) -> Stream[R]:
        """
        Return a stream consisting of the results of replacing each element of this stream with its flatten elements.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return self.__class__(flatten(self), executor=self._executor)

    # TODO: sort() need call local and is a generator
    def group_by(self, key: Callable[[E], R] = identity, parallel: bool = False, **kwargs: Any) -> Stream[Tuple[R, Iterable[E]]]:
        """
        Return a stream consisting of the results of grouping by the key(element) of this stream.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return self.__class__(groupby(sorted(self, key=key), key=key), executor=self._executor)

    def zip(self, parallel: bool = False, **kwargs: Any) -> Stream[Iterable[E]]:
        """
        Return a stream consisting of the results of zipping element of this stream.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        # noinspection PyTypeChecker
        return self.__class__(lambda: zip(*self), executor=self._executor)

    def product(self, repeat: Optional[int] = None, parallel: bool = False, **kwargs: Any) -> Stream[Iterable[E]]:
        """
        Return a stream consisting of the results of the Cartesian Product of stream, similar with itertools.product.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        e = (repeat and (lambda: product(self, repeat=repeat))) or (lambda: product(*self))
        # noinspection PyTypeChecker
        return self.__class__(e, executor=self._executor)

    def int(self, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the results of applying the int function to the elements of this stream.
        """
        return self.map(lambda e: int(e), parallel, **kwargs)

    def float(self, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the results of applying the float function to the elements of this stream.
        """
        return self.map(lambda e: float(e), parallel, **kwargs)

    def decimal(self, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the results of applying the Decimal function to the elements of this stream.
        """
        return self.map(lambda e: Decimal(e), parallel, **kwargs)

    def str(self, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the results of applying the str function to the elements of this stream.
        """
        return self.map(lambda e: str(e), parallel, **kwargs)

    # filter #

    def filter(self, predicate: Predicate[E], parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the elements of this stream that match the given predicate.
        """
        func = partial(concrt_filter, executor=kwargs.pop("executor", self._executor), **kwargs) if parallel else filter
        return self.__class__(func(predicate, self), self._executor)

    def filter_by_index(self, index: int, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the results of only indexed elements.
        """
        return self.filter(lambda e: e[index], parallel, **kwargs)

    def keys(self, default_index: int = 0, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the results of only key in [key, value] pair.
        """
        return self.filter_by_index(default_index, parallel, **kwargs)

    def values(self, default_index: int = 1, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the results of only value in [key, value] pair.
        """
        return self.filter_by_index(default_index, parallel, **kwargs)

    def include(self, predicate: Predicate[E], parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        An alias of Stream.filter(predicate, kwargs).
        """
        return self.filter(predicate, parallel, **kwargs)

    def exclude(self, predicate: Predicate[E], parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the elements of this stream that don't match the given predicate.
        """
        return self.filter(lambda e: not predicate(e), parallel, **kwargs)

    def regexp(self, pattern: str, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the elements which is matched with the regexp pattern.
        """
        return self.filter(lambda e: bool(re.match(pattern, str(e))), parallel, **kwargs)

    def even(self, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the elements where e is an even.
        """
        return self.filter(lambda e: float(e) % 2 == 0, parallel, **kwargs)

    def odd(self, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the elements where e is an odd.
        """
        return self.filter(lambda e: float(e) % 2 != 0, parallel, **kwargs)

    def divisible_by(self, number: Number, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the elements where e is divisible by the given one.
        """
        return self.filter(lambda e: float(e) % number == 0, parallel, **kwargs)

    def distinct(self, key: Optional[Function[E, R]] = None, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the distinct elements (according to __eq__) of this stream.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return Stream(distinct(self, key))

    def instance_of(self, types: Type | Tuple[Type], parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the elements where e is instance of given type or types.
        """
        return self.filter(lambda e: isinstance(e, types), parallel, **kwargs)

    def no_none(self, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the elements where e is not None.
        """
        return self.filter(lambda e: e is not None, parallel, **kwargs)

    def no_false(self, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the elements where bool_plus(e) == True.
        """
        return self.filter(lambda e: bool_plus(e), parallel, **kwargs)

    def limit(self, max_size: int, parallel: bool = False, **kwargs: Any) -> Self:
        """
        Return a stream consisting of the elements of this stream, truncated to be no longer than max_size in length.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return self.__class__(islice(self, max_size))

    def skip(self, n: int, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the remaining elements of this stream after discarding the first n elements.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return self.__class__(islice(self, n, None))

    @try_catch(ignored=StopIteration, argname="_else")
    def first(self, _else: Optional[E] = None, parallel: bool = False, **kwargs: Any) -> Optional[E]:
        """
        Return the first element of this stream, or an `_else` if the stream is empty.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return next(iter(self))

    @try_catch(ignored=StopIteration, argname="_else")
    def last(self, _else: Optional[E] = None, parallel: bool = False, **kwargs: Any) -> Optional[E]:
        """
        Return the last element of this stream, or an `_else` if the stream is empty.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return next(reversed(tuple(self)))

    @try_catch(ignored=IndexError, argname="_else")
    def take(self, index: int, _else: Optional[E] = None, parallel: bool = False, **kwargs: Any) -> Optional[E]:
        """
        Return the element indexed by index of this stream.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return tuple(self)[index]

    # collect #

    def collect(
        self,
        supplier: Supplier[A],
        accumulator: BiConsumer[A, E],
        finisher: Function[A, R] = identity,
        parallel: bool = False,
        **kwargs: Any
    ) -> R:
        """
        Performs a reduction operation on the elements of this stream using a Collector.
        """
        container = supplier()
        func = (parallel and partial(concrt_map, executor=kwargs.pop("executor", self._executor), **kwargs)) or map
        _ = tuple(func(lambda e: accumulator(container, e), parallel, **kwargs))
        return finisher(container)

    def tuplify(self, parallel: bool = False, **kwargs: Any) -> Tuple[E]:
        """
        Performs a reduction operation on the elements of this stream using a tuple.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return tuple(self)

    def listify(self, parallel: bool = False, **kwargs: Any) -> List[E]:
        """
        Performs a reduction operation on the elements of this stream using a list.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return list(self)

    def setify(self, parallel: bool = False, **kwargs: Any) -> Set[E]:
        """
        Performs a reduction operation on the elements of this stream using a set.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return set(self)

    def dictify(self, parallel: bool = False, **kwargs: Any) -> Stream[Dict]:
        """
        Performs a mapping operation on the elements of this stream using a dict.
        """
        return self.map(lambda e: dict(e), parallel, **kwargs)

    # reduce #

    @try_catch(ignored=(TypeError, StopIteration), argname="e")
    def reduce(self, accumulator: BinaryOperator[E], e: Optional[E] = None, parallel: bool = False, **kwargs: Any) -> Optional[E]:
        """
        Performs a reduction on the elements of this stream, using an associative accumulation function, and returns an
        Optional describing the reduced value, if any.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return reduce(accumulator, self, initial=e or object())

    def any(self, predicate: Predicate[E], parallel: bool = False, **kwargs: Any) -> bool:
        """
        Return whether any elements of this stream match the provided predicate.
        """
        return any(self.map(predicate, parallel, **kwargs))

    def all(self, predicate: Predicate[E], parallel: bool = False, **kwargs: Any) -> bool:
        """
        Return whether all elements of this stream match the provided predicate.
        """
        return all(self.map(predicate, parallel, **kwargs))

    def count(self, parallel: bool = False, **kwargs: Any) -> int:
        """
        Return the count of elements in this stream.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return len(tuple(self))

    def sum(self, parallel: bool = False, **kwargs: Any) -> Optional[E]:
        """
        Return the sum of elements in this stream.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return self.reduce(add)

    def mean(self, parallel: bool = False, **kwargs: Any) -> Optional[E]:
        """
        Return the mean of elements in this stream.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        ans = self.reduce(lambda e1, e2: (add(e1[0], e2[0]), add(e1[1], e2[1])))
        return ans[0] / (ans[1] + 1e-8)

    @try_catch(ignored=(ValueError, StopIteration), argname="_else")
    def min(self, key: Function[E, R] = None, _else: E = None, parallel: bool = False, **kwargs: Any) -> Optional[E]:
        """
        Return the minimum element of this stream according to the provided key.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return min(self, key=key)

    @try_catch(ignored=(ValueError, StopIteration), argname="_else")
    def max(self, key: Function[E, R] = None, _else: E = None, parallel: bool = False, **kwargs: Any) -> Optional[E]:
        """
        Return the maximum element of this stream according to the provided key.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return max(self, key=key)

    def join(self, sep: str = "", parallel: bool = False, **kwargs: Any) -> E:
        """
        Return a joining string of this stream by sep.
        """
        return sep.join(self.str(parallel, **kwargs))

    # order #

    def reorder(self, orders: Iterable[int], parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Return a stream consisting of the reordered elements.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return self.__class__(reorder(self, orders), executor=self._executor)

    def sort(self, key: Function[E, R] = None, ascending: bool = True, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Returns a stream consisting of the elements of this stream, sorted according to key.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return self.__class__(lambda: sorted(self, key=key, reverse=not ascending))

    def reverse(self, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Returns a stream consisting of the reversed order elements of this stream.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return self.__class__(reversed(tuple(self)), executor=self._executor)

    def shuffle(self, parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Returns a stream consisting of the random order elements of this stream.
        """
        conditional_warning(parallel or kwargs, msg="this method's implementation is not supported for parallel.")
        return self.__class__(shuffle(self), executor=self._executor)

    # traverse #

    def peek(self, action: Consumer[E], parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Returns a stream consisting of the elements of this stream, additionally performing the provided action on each
        element as elements are consumed from the resulting stream.
        """
        return self.map(lambda e: peek(e, action), parallel, **kwargs)

    def foreach(self, action: Consumer[E], parallel: bool = False, **kwargs: Any) -> None:
        """
        Performs an action for each element of this stream.
        """
        _ = tuple(self.map(action, parallel, **kwargs))

    # misc #

    def __len__(self) -> int:
        """
        Return the count of elements in this stream.
        """
        return self.count()

    def __getitem__(self, index: int) -> E:
        """
        Return the element indexed by index of this stream.
        """
        return self.take(index)

    def __iter__(self) -> Iterator[E]:
        """
        Return an iterator. All elements will be evaluated when the method has been calling.
        """
        return self._element.__iter__()

stream = Stream
