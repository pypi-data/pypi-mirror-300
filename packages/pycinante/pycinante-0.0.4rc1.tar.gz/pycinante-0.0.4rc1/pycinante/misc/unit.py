from __future__ import annotations
from enum import Enum
from typing import Any, Optional, Iterable, TypeVar, Generic
from types import MethodType
from functools import partial
from pycinante.utils import export

T_co = TypeVar("T_co", covariant=True)

@export
class uDefinition(Generic[T_co]):
    """
    A base class for defining a unit definition.
    """

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        """
        Returns the short name of the unit instance.
        """
        return self._name

    def n2u(self, value: T_co, **kwargs: Any) -> T_co:
        """
        Coverts the value of the crt unit into a new value of the base unit.
        """
        raise NotImplementedError(f"{self._name}'s n2u")

    def u2n(self, value: T_co, **kwargs: Any) -> T_co:
        """
        Coverts the value of the base unit into a new value of the crt unit.
        """
        raise NotImplementedError(f"{self._name}'s u2n")

@export
def unitify(value: T_co, nunit: Enum, tunit: Enum, strify: bool = False, **kwargs: Any) -> T_co | str:
    """
    Coverts a value of the nunit into a new value of the tunit.
    """
    assert isinstance(nunit, type(tunit)), "the target unit type must be same as the origin unit type"
    value = tunit.value.u2n(nunit.value.n2u(value, **kwargs), **kwargs)
    return f"{value} {tunit.value.name}" if strify else value

@export
class uWrapper(Generic[T_co]):
    """
    A wrapper class for wrapping a value with a unit, then the value can be easily converted into a new value of any
    unit via methods like `to_xxx`. It works well in python console env because the compiler can explicitly hint user
    what methods can be used.
    """

    def __init__(self, value: T_co, nunit: Enum) -> None:
        self._value = value
        self._nunit = nunit

        self.new_method_names = []
        for tunit in self._nunit.__class__:
            self.new_method_names.append(tunit.name.lower())

            # noinspection PyUnusedLocal
            def _wrapper(self, value: T_co, nunit: Enum, tunit: Enum, **kwargs: Any) -> uWrapper[T_co]:
                return uWrapper(unitify(value, nunit, tunit, **kwargs), tunit)

            setattr(self, f"to_{tunit.name.lower()}", MethodType(
                partial(_wrapper, value=self._value, nunit=self._nunit, tunit=tunit), self
            ))

    @property
    def value(self) -> T_co:
        """
        Returns the origin value object it wrapped.
        """
        return self._value

    def __str__(self) -> str:
        return self._value.__str__()

    def __repr__(self) -> str:
        return self._value.__repr__()

    def __dir__(self) -> Iterable[str]:
        return [*super(uWrapper, self).__dir__(), *self.new_method_names]

@export
def number_as_udef(name: str, unit: Optional[float] = None) -> uDefinition[float]:
    """
    Builds a uDef instance from a number type unit.
    """
    udef = uDefinition(name)
    if unit:
        udef.n2u = MethodType(lambda self, e, **kwargs: e * unit, udef)
        udef.u2n = MethodType(lambda self, e, **kwargs: e / unit, udef)
    return udef
