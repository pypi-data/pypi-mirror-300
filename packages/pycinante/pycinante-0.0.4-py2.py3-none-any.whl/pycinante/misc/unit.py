from __future__ import annotations
from enum import Enum
from types import MethodType
from functools import partial
from pycinante.utils import export

@export
class uDefinition:
    """
    A base class for defining a unit definition.
    """

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """
        Returns the short name of the unit instance.
        """
        return self._name

    def n2u(self, value, **kwargs):
        """
        Coverts the value of the crt unit into a new value of the base unit.
        """
        raise NotImplementedError(f"{self._name}'s n2u")

    def u2n(self, value, **kwargs):
        """
        Coverts the value of the base unit into a new value of the crt unit.
        """
        raise NotImplementedError(f"{self._name}'s u2n")

@export
def unitify(value, nunit, tunit, strify=False, **kwargs):
    """
    Coverts a value of the nunit into a new value of the tunit.
    """
    assert isinstance(nunit, type(tunit)), "the target unit type must be same as the origin unit type"
    value = tunit.value.u2n(nunit.value.n2u(value, **kwargs), **kwargs)
    return f"{value} {tunit.value.name}" if strify else value

@export
class uWrapper:
    """
    A wrapper class for wrapping a value with a unit, then the value can be easily converted into a new value of any
    unit via methods like `to_xxx`. It works well in python console env because the compiler can explicitly hint user
    what methods can be used.
    """

    def __init__(self, value, nunit):
        self._value = value
        self._nunit = nunit

        self._new_method_names = []
        for tunit in self._nunit.__class__:
            self._new_method_names.append(tunit.name.lower())

            def _wrapper(_self, value, nunit: Enum, tunit: Enum, **kwargs):
                return uWrapper(unitify(value, nunit, tunit, **kwargs), tunit)

            setattr(self, f"to_{tunit.name.lower()}", MethodType(
                partial(_wrapper, value=self._value, nunit=self._nunit, tunit=tunit), self
            ))

    @property
    def value(self):
        """
        Returns the origin value object it wrapped.
        """
        return self._value

    def __str__(self):
        return self._value.__str__()

    def __repr__(self):
        return self._value.__repr__()

    def __dir__(self):
        return [*super().__dir__(), *self._new_method_names]

@export
def number_as_udef(name, unit=None):
    """
    Builds a uDef instance from a number type unit.
    """
    udef = uDefinition(name)
    if unit:
        udef.n2u = MethodType(lambda self, e, **kwargs: e * unit, udef)
        udef.u2n = MethodType(lambda self, e, **kwargs: e / unit, udef)
    return udef
