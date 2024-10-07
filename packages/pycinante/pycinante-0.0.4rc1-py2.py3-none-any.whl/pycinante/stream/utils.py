from __future__ import annotations
import inspect
from functools import wraps
import warnings
import random
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor, Executor, ProcessPoolExecutor
from pycinante.utils import export
from typing import Optional, Any, TypeVar, Callable, Iterable, Union, Iterator, Type, Tuple, Dict

__all__ = [
    "Predicate", "Supplier", "Consumer", "BiConsumer", "Function", "BiFunction", "BinaryOperator", "Element", "Number"
]

T = TypeVar("T")
R = TypeVar("R")
U = TypeVar("U")

Predicate = Callable[[T], bool]
Supplier = Callable[[], T]
Consumer = Callable[[T], None]
BiConsumer = Callable[[T, R], None]
Function = Callable[[T], R]
BiFunction = Callable[[U, T], U]
BinaryOperator = Callable[[T, T], T]

Number = Union[int, float]
Element = Optional[Union[T, Iterable[T], Supplier[Iterable[T]]]]

@export
def get_executor(max_workers: Optional[int] = None, io_intensive: bool = True, **kwargs: Any) -> Executor:
    """
    Return an executor with up to max_workers pool size. If io_intensive is True, a ThreadPoolExecutor is returned,
    otherwise ProcessPoolExecutor.
    """
    executor = ThreadPoolExecutor if io_intensive else ProcessPoolExecutor
    return executor(max_workers=max_workers or cpu_count(), **kwargs)

@export
def concrt_map(func: Function[T, R], iters: Iterable[T], **kwargs: Any) -> Iterable[R]:
    """
    Concurrent map function. An executor can be specified via `executor`, if none of executor was not specified, an io
    intensive executor will be used by default, and it will be shutdown when `concrt_map` finished.
    """
    user_executor = kwargs.pop("executor", None)
    executor = user_executor or get_executor(**kwargs)

    try:
        return executor.map(func, iters)
    finally:
        if user_executor is None:
            executor.shutdown(wait=True)

@export
def concrt_filter(func: Predicate[T], iters: Iterable[T], **kwargs: Any) -> Iterable[T]:
    """
    Concurrent filter function. An executor can be specified via `executor`, if none of executor was not specified, an
    io intensive executor will be used by default, and it will be shutdown when `concrt_filter` finished.
    """
    return (a for a, b in concrt_map(lambda e: (e, func(e)), iters=iters, **kwargs) if b)

@export
class MemoryBuffer(Iterable[T]):
    """
    A helper class for holding a set of instances. It extends the properties of generator.
    """

    def __init__(self, element: Element[T] = None) -> None:
        if isinstance(element, (Iterable, Callable)):
            self._elements = element
        else:
            self._elements = [] if element is None else [element]

    def __iter__(self) -> Iterator[T]:
        """
        Return an iterator. All elements will be evaluated when the method has been calling.
        """
        yield from self._elements() if callable(self._elements) else self._elements

@export
def try_catch(
    ignored: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
    ret_val: Optional[T] = None,
    argname: str = "other",
) -> Callable[..., Optional[T]]:
    """
    A wrapper for catching a or a group of exceptions and returns the failed results when one of the exception occurs.
    """
    def _wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        sig = inspect.signature(func)

        @wraps(func)
        def _decorator(*args: Any, **kwargs: Any) -> Optional[T]:
            try:
                return func(*args, **kwargs)
            except ignored:
                bind = sig.bind(*args, **kwargs).arguments
                return bind.get(argname, None) or ret_val
        return _decorator
    return _wrapper

@export
def identity(*args: T, **kwargs: T) -> T | Tuple[T] | Dict[str, T]:
    """
    Return the same arguments as the fed.
    """
    def _unwrap(e: Tuple[T]) -> T:
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
def distinct(iterable: Iterable[T], key: Optional[Function[T, R]] = None) -> Iterator[T]:
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
def bool_plus(obj: Any, default: Callable[[Any], bool] = bool) -> bool:
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
def flatten(iterable: Iterable[T | Iterable[T]]) -> Iterator[T]:
    """
    Generate each element of the given iterable. If the element is iterable and is not string, it yields each sub-element
    of the element recursively.
    """
    for item in iterable:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            for sub_item in flatten(item):
                yield sub_item
        else:
            yield item

@export
def unpacking_zip(iterables: Iterable[Iterable[T]]) -> Iterator[Iterable[T]]:
    """
    unpacking_zip([[a, c], [b, d], ...]) works as same as zip(*[[a, c], [b, d], ...]).
    """
    iterators = (iter(e) for e in iterables)

    while True:
        ans = []
        for iterator in iterators:
            try:
                ans.append(next(iterator))
            except StopIteration:
                return
        yield tuple(ans)

@export
def conditional_warning(condition: bool, msg: str = "", **kwargs: Any) -> None:
    """
    If condition is True, then raise a warning with the msg.
    """
    if condition:
        warnings.warn(msg, **kwargs)

@export
def reorder(iterables: Iterable[T], orders: Iterable[int]) -> Iterator[T]:
    """
    Return a new iterator with the new orders.
    """
    iterables = tuple(iterables)
    for index in orders:
        yield iterables[index]

@export
def shuffle(iterables: Iterable[T]) -> Iterator[T]:
    """
    Return a new iterator with the random orders.
    """
    iterables = tuple(iterables)
    orders = list(range(len(iterables)))
    random.shuffle(orders)
    yield from reorder(iterables, orders)

@export
def peek(element: T, func: Consumer[T]) -> T:
    """
    Does the same as `Java 8 peek. That is consuming the element and return itself.
    """
    func(element)
    return element
