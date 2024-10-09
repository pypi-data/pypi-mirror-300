"""Update Log

2023.10.08:
    - added type hints on attrdict

2024.10.07:
    - completely tested attrdict and attrify()'s functionalities provided already
    - added the generic supports for any type of inputs
    - fixed the __dir__() method returning duplicate attributes
    - fixed a bug where the __getitem__() method do not raise a KeyError when accessing no-exists keys
    - added a feature to pop() method that allows elements to be pop via chain keys
    - added the supports to other methods in dict (and not in attrdict before)
"""

from __future__ import annotations
import contextlib

__all__ = ["attrdict", "attrify"]

class AttrDict(dict):
    """Attribute dictionary, allowing access to dict values as if they were class attributes.

    Using cases:
        >>> net = attrdict({"name": "unet", "cfg": {"in_channels": 3, "num_classes": 9}})
        >>> net.cfg.num_classes
        9
        >>> net["cfg.decoder.depths"] = [2, 2, 2, 2]
        >>> net["cfg.decoder.depths"][0]
        2

        As shown above, you first need to covert an existing dict into AttrDict, and then you can access its value as
        you access a class/instance's properties. Moreover, you can get/set the value in `[]` via cascaded strings.
    """
    def __init__(self, seq=None, **kwargs):
        super().__init__()
        self.update(seq, **kwargs)

    def clear(self):
        """
        Remove all items from the dictionary. Return itself. Note that the clear() function only deletes references to
        currently held instances.
        """
        _ = [delattr(self, key) for key in self.keys()]
        super().clear()
        return self

    def copy(self):
        """
        Return a shallow copy of the current instance.
        """
        return AttrDict(super().copy())

    @staticmethod
    def fromkeys(iterable, values=None, **_kwargs):
        """
        Create a new dictionary with keys from iterable and values set to value.
        """
        return AttrDict(dict.fromkeys(iterable, values))

    def get(self, key, default=None):
        """
        Return the value for key if key is in the dictionary, else default.
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def items(self):
        """
        Return a new view of the dictionary’s items ((key, value) pairs).
        """
        return super().items()

    def keys(self):
        """
        Return a new view of the dictionary’s keys.
        """
        return super().keys()

    def pop(self, key, default=None):
        """
        If key is in the dictionary, remove it and return its value, else return default. If default is not given and
        key is not in the dictionary, a KeyError is raised.
        """
        if "." in key:
            prefix, key = key.rsplit(sep=".", maxsplit=1)
            parent = self.__getitem__(prefix)
        else:
            parent = self

        with contextlib.suppress(AttributeError):
            delattr(parent, key)
        return super(AttrDict, parent).pop(key, default)

    def popitem(self):
        """
        Remove and return a (key, value) pair from the dictionary. Pairs are returned in LIFO order.
        """
        ret = super().popitem()
        with contextlib.suppress(AttributeError):
            delattr(self, ret[0])
        return ret

    def setdefault(self, key, default=None):
        """
        If key is in the dictionary, return its value. If not, insert key with a value of default and return default.
        default defaults to None.
        """
        if self.__contains__(key):
            return self.__getitem__(key)
        self.__setitem__(key, default)
        return default

    def update(self, seq=None, **kwargs):
        """
        Update the dictionary with the key/value pairs from other, overwriting existing keys. Return itself.
        """
        for key, value in dict(seq or {}, **kwargs).items():
            self.__setattr__(key, value)
        return self

    def values(self):
        """
        Return a new view of the dictionary’s values.
        """
        return super().values()

    def __contains__(self, key: str):
        """
        Return True if the dictionary has the specified key, else False.
        """
        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False

    def __delitem__(self, key: str):
        """
        Delete self[key]. It is implemented by pop().
        """
        self.pop(key)

    def __setattr__(self, key: str, value):
        """
        Set d[key]=value and at same time set d.key=value.
        """
        def _covert_recursively(obj):
            if isinstance(obj, dict) and not isinstance(obj, AttrDict):
                return self.__class__(obj)
            if isinstance(obj, (tuple, list, set)):
                return type(obj)((_covert_recursively(e) for e in obj))
            return obj

        value = _covert_recursively(value)
        super().__setattr__(key, value)
        super().__setitem__(key, value)

    def __getattr__(self, key: str):
        """
        Return the value for key if key is in the dictionary, else raise a KeyError.
        """
        return super().__getitem__(key)

    def __setitem__(self, key: str, value):
        """
        It works similar to __setattr__(), and you can set key/value pair in str chain way like d["a.b.c.d"]=value.
        """
        if "." in key:
            key, suffix = key.split(sep=".", maxsplit=1)
            self.__setattr__(key, value={}) if key not in self else None
            self.__getattr__(key).__setitem__(suffix, value)
        else:
            self.__setattr__(key, value)

    def __getitem__(self, key: str):
        """
        It works similar to __getattr__(), and you can get key/value pair in str chain way like d["a.b.c.d"].
        """
        if "." in key:
            prefix, key = key.rsplit(sep=".", maxsplit=1)
            d = self.__getitem__(prefix)
            if not isinstance(d, AttrDict):
                raise KeyError(".".join((prefix, key)))
            return d[key]
        return self.__getattr__(key)

    def __dir__(self):
        """
        Return all method/attribute names of the instance.
        """
        return super().__dir__()

def attrify(seq=None, **kwargs):
    """
    Covert a dict/iterable into a AttrDict.
    """
    return AttrDict(seq, **kwargs)

attrdict = AttrDict
