from dataclasses import dataclass
import random
import time
from pycinante.stream import stream
from pycinante.stream.utils import identity

def test_map():
    # assert list(stream([1, 2, 3]).map(identity)._element) == [1, 2, 3]
    assert list(stream([1, 2, 3]).map(lambda e: e ** 2)._element) == [1, 4, 9]
    print(stream([1, 2, 3]).map(lambda e: e ** 2).listify())
    # assert list(stream(range(10000)).map(lambda e: e ** 2, parallel=True)._element) == [e ** 2 for e in range(10000)]
    #
    # def f1(e):
    #     time.sleep(random.randint(0, 5))
    #     return e ** 2
    #
    # assert list(stream(range(10)).map(f1, parallel=True)._element) == [e ** 2 for e in range(10)]

def test_map_by_index():
    assert list(stream([[1, 2], [2, 3], [3, 4]]).map_by_index(0, identity)._element) == [[1, 2], [2, 3], [3, 4]]
    assert list(stream([[1, 2], [2, 3], [3, 4]]).map_by_index(1, lambda e: e + 1)._element) == [[1, 3], [2, 4], [3, 5]]

def test_enumerate():
    assert list(stream(range(10000)).enumerate()._element) == list(enumerate(range(10000)))

def test_flatten():
    assert list(stream([[[[[1]], 2, [3], [4]], [5], [6]]]).flatten()._element) == list(range(1, 7))
    print(stream([[1], [2, [3, [4]]]]).flatten().listify())

    @dataclass
    class Person:
        name: str
        age: int

    (stream
     .range(10)
     .map(lambda e: Person(str(e), e + 1))
     .group_by(lambda e: e.age % 2 == 0)
     .values()
     .flatten()
     .foreach(print))

def test_group_by():
    print([(a, list(b)) for a, b in stream(["123", "456", "224", "778"]).group_by(lambda e: int(e[0]) % 2 == 0)])

def test_zip():
    print(stream([[1, 2, 3], [4, 5, 6]]).zip().listify())

def test_product():
    print(stream([[1, 2, 3], [4, 5, 6]]).product().listify())

def test_int():
    print(stream(["1", "2", "3"]).int().listify())

def test_filter():
    assert stream(range(10000)).filter(lambda e: e % 2 == 0).listify() == [e for e in range(10000) if e % 2 == 0]
    assert stream(range(10000)).filter(lambda e: e % 2 == 0, parallel=True).listify() == [e for e in range(10000) if e % 2 == 0]

    def f(e):
        time.sleep(random.randint(0, 2))
        return e % 2 == 0

    assert stream(range(10)).filter(f, parallel=False).listify() == [e for e in range(10) if e % 2 == 0]
    assert stream(range(10)).filter(f, parallel=True).listify() == [e for e in range(10) if e % 2 == 0]

def test_keys():
    print(stream([(e, e ** 2) for e in range(10)]).keys().listify())

def test_values():
    print(stream([(e, e ** 2) for e in range(10)]).values().listify())

def test_distinct():
    print(stream([random.randint(0, 10) for _ in range(100)]).distinct().listify())

def test_instance_of():
    print(stream([1, 2, True, "123", [], (), {}, set()]).instance_of(dict).listify())

def test_limit():
    print(stream(range(100)).limit(5).listify())

def test___getitem__():
    print(stream(range(100))[5])
    print(stream(range(100))[5:10].listify())

def test_skip():
    print(stream(range(10)).skip(1).listify())

def test_first():
    print(stream().first(_else=10))
    print(stream([1, 2, 3, 4]).first(_else=10))

def test_last():
    print(stream().last(_else=10))
    print(stream([1, 2, 3, 4]).last(_else=10))

def test_collect():
    print(stream(range(10)).collect(list, lambda a, b: a.append(b)))

def test_tuplify():
    print(stream(range(10)).tuplify())

def test_listify():
    print(stream(range(10)).listify())

def test_setify():
    print(stream(range(10)).setify())

def test_dictify():
    print(stream(enumerate(range(10))).dictify())

def test_reduce():
    print(stream(range(10)).reduce(lambda a, b: a + b))
    print(stream().reduce(lambda a, b: a + b))

def test_any():
    print(stream([True, True, False]).any(bool))

def test_all():
    print(stream([True, True, False]).all(bool))

def test_count():
    print(stream(range(10)).count())

def test_sum():
    print(stream(range(10)).sum())
    print(stream().sum())

def test_mean():
    print(stream(range(10)).mean())

def test_min():
    print(stream(range(10)).min())
    print(stream([]).min())

def test_max():
    print(stream(range(10)).max())
    print(stream([]).max())

def test_join():
    print(stream(range(10)).join(","))
    print(stream().join(","))

def test_reorder():
    print(stream(range(10)).reorder(range(9, -1, -1)).tuplify())

def test_sort():
    print(stream([random.randint(0, 100) for _ in range(10)]).sort(ascending=False).tuplify())

def test_reverse():
    print(stream(range(10)).reverse().tuplify())

def test_shuffle():
    print(stream(range(10)).shuffle().tuplify())

def test_peek():
    print(stream(range(10)).peek(print).listify())

def test_foreach():
    stream(range(10)).foreach(print)

def test_get():
    print()
    (stream
     .range(1, 3)
     .format("https://wallhaven.cc/latest?page={}")
     .get(ignored=TimeoutError)
     .soup()
     .map(lambda e: e.select("#thumbs > section > ul > li > figure > a"))
     .flatten()
     .map(lambda e: e["href"])
     .foreach(print))
