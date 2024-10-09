import pytest
from pycinante.dict.attrdict import *

def test___init__():
    assert attrdict() == {}
    assert attrdict({}) == {}
    assert attrdict([]) == {}
    assert attrdict(()) == {}
    assert attrdict(set()) == {}
    assert attrdict({"a": 1}) == {"a": 1}
    assert attrdict({"a": 1, "b": 2}) == {"a": 1, "b": 2}
    assert attrdict({"a": 1, "b": {"c": 3}}) == {"a": 1, "b": {"c": 3}}
    assert attrdict(a=1, b=2, c=dict(d=3)) == {"a": 1, "b": 2, "c": {"d": 3}}
    assert attrdict([("a", 1), ("b", 2)]) == {"a": 1, "b": 2}

def test___setattr__and___getattr__():
    t = attrdict()

    t["a.b.c.d"] = 1
    assert t.a.b.c._d == 1

    t["a.b.c.e"] = {"k": [2, {"j": [3, 4, 5]}]}
    assert t.a.b.c.e.k[1].j[0] == 3

def test_clear():
    t = attrdict()
    t["a.b.c.d"] = [1, 2, {"e": 3}]
    t["a.b.c.g"] = 4
    t["a.b.f"] = [5, 6]

    g = t.a.b.c.d[-1]

    assert isinstance(g, attrdict)
    t.clear()
    assert "a" not in dir(t)
    assert g == {"e": 3}

def test_copy():
    t = attrdict()
    t["a.b.c.d"] = [1, 2, {"e": 3}]

    assert id(t.copy().a.b.c.d) == id(t.a.b.c.d)

def test_fromkeys():
    assert attrdict.fromkeys(iterable=["a", "b"], values=[1, 2, 3]).a[0] == 1

def test_get():
    assert attrdict({"a": 1}).get("a") == 1
    assert attrdict({"a": 1}).get("a.b.c") is None

def test_items():
    assert list(attrdict({"a": 1}).items()) == [("a", 1)]

def test_keys():
    assert list(attrdict({"a": 1, "b": 2}).keys()) == ["a", "b"]

def test_pop():
    t = attrdict()
    t["a.b.c.d"] = [1, 2, {"e": 3}]
    t["a.b.c.g"] = 4
    t["a.b.f"] = [5, 6]

    assert t.pop("a.b.c.g") == 4
    assert t.a.b.c.d[-1].e == 3

def test_popitem():
    assert attrdict({"a": "b"}).popitem() == ("a", "b")

def test_setdefault():
    assert attrdict().setdefault("a") is None
    assert attrdict().setdefault("a", [1]) == [1]
    assert attrdict(a=2).setdefault("a", [1]) == 2

def test_update():
    assert attrdict({"a": 1, "b": 2}).a == 1
    assert attrdict({"a": 1, "b": {"c": 3}}).b.c == 3
    assert attrdict({"a": 1, "b": {"c": [4, {"d": 5}]}}).b.c[1].d == 5
    with pytest.raises(KeyError):
        assert attrdict({"a": 1, "b": 2}).c

def test_values():
    assert list(attrdict({"a": 1, "b": 2}).values()) == [1, 2]

def test___contains__():
    assert "a" in attrdict({"a": 1})
    assert "a.b.c" not in attrdict({"a": 1})

def test___delitem__():
    t = attrdict()
    t["a.b.c.d"] = [1, 2, {"e": 3}]

    del t["a"]

    print(t)

def test_attrify():
    assert attrify() == {}
    assert attrify({}) == {}
    assert attrify([]) == {}
    assert attrify(()) == {}
    assert attrify(set()) == {}
    assert attrify({"a": 1}) == {"a": 1}
    assert attrify({"a": 1, "b": 2}) == {"a": 1, "b": 2}
    assert attrify({"a": 1, "b": {"c": 3}}) == {"a": 1, "b": {"c": 3}}
    assert attrify(a=1, b=2, c=dict(d=3)) == {"a": 1, "b": 2, "c": {"d": 3}}
    assert attrify([("a", 1), ("b", 2)]) == {"a": 1, "b": 2}
