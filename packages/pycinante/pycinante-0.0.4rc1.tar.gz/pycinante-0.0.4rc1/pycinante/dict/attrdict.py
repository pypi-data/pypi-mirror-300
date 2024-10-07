from __future__ import annotations
from typing import TypeVar, Dict, Optional, Iterable, Union
from typing_extensions import Self

__all__ = ["attrdict", "attrify"]

T = TypeVar("T")
E = TypeVar("E")

Element = Optional[Union[Dict[str, T], Iterable[Iterable]]]

class AttrDict(Dict[str, E]):
    """Attribute dictionary, allowing access to dict values as if they were class attributes.

    Using cases:
        >>> d = AttrDict({"name": "unet", "cfg": {"in_channels": 3, "num_classes": 9}})
        >>> d.cfg.num_classes
        9
        >>> d["cfg.decoder.depths"] = [2, 2, 2, 2]
        >>> d["cfg.decoder.depths"][0]
        2

        As shown above, you first need to covert an existing dict into AttrDict, and then you can access its value as
        you access a class/instance's properties. Moreover, you can get/set the value in `[]` via cascaded strings.
    """
    def __init__(self, seq: Element[E] = None, **kwargs: E) -> None:
        super(AttrDict, self).__init__()
        self.update(seq, **kwargs)

    def update(self, seq: Element[E] = None, **kwargs: E) -> Self:
        """
        Update the dictionary with the key/value pairs from other, overwriting existing keys. Return itself.
        """
        for key, value in dict(seq or {}, **kwargs).items():
            self.__setattr__(key, value)
        return self

    def pop(self, key: str, default: Optional[E] = None) -> E:
        """
        If key is in the dictionary, remove it and return its value, else return default. If default is not given and
        key is not in the dictionary, a KeyError is raised.
        """
        delattr(self, key)
        return super(AttrDict, self).pop(key, default)

    def __setattr__(self, key: str, value: E) -> None:
        """
        Set d[key]=value and at same time set d.key=value.
        """
        def _covert_recursively(obj: E) -> E:
            if isinstance(obj, dict) and not isinstance(obj, AttrDict):
                return self.__class__(obj)
            if isinstance(obj, (tuple, list, set)):
                return type(obj)((_covert_recursively(e) for e in obj))
            return obj

        value = _covert_recursively(value)
        super(AttrDict, self).__setattr__(key, value)
        super(AttrDict, self).__setitem__(key, value)

    def __getattr__(self, key: str) -> E:
        """
        Return the value for key if key is in the dictionary, else raise a KeyError.
        """
        return super(AttrDict, self).__getitem__(key)

    def __setitem__(self, key: str, value: E) -> None:
        """
        It works similar to __setattr__(), and you can set key/value pair in str chain way like d["a.b.c.d"]=value.
        """
        if "." in key:
            key, suffix = key.split(sep=".", maxsplit=1)
            self.__setattr__(key, value={}) if key not in self else None
            self.__getattr__(key).__setitem__(suffix, value)
        else:
            self.__setattr__(key, value)

    def __getitem__(self, k: str) -> E:
        """
        It works similar to __getattr__(), and you can get key/value pair in str chain way like d["a.b.c.d"].
        """
        if "." in k:
            prefix, k = k.rsplit(sep=".", maxsplit=1)
            return self.__getitem__(prefix)[k]
        return self.__getattr__(k)

    def __dir__(self) -> Iterable[str]:
        """
        Return all method/attribute names of the instance.
        """
        return [*super(AttrDict, self).__dir__(), *self.keys()]

def attrify(seq: Element[T] = None, **kwargs: T) -> AttrDict[T]:
    """
    Covert a dict/iterable into a AttrDict.
    """
    return AttrDict(seq, **kwargs)

attrdict = AttrDict
