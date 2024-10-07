from os import PathLike
from enum import Enum
from typing import Union, AnyStr
from typing_extensions import TypeAlias
from pycinante.misc.unit import number_as_udef
from pycinante.utils import export

__all__ = ["PathType"]

PathType: TypeAlias = Union[AnyStr, PathLike]

@export
class BinaryUnit(Enum):
    """
    Binary unit enum. It works with the utilities in 'pycinante.unit'.
    """
    BIT = number_as_udef(name="bit", unit=1 / 8)
    BYTE = number_as_udef(name="byte", unit=1)
    KILO_BYTE = number_as_udef(name="kb", unit=1024)
    MEGA_BYTE = number_as_udef(name="mb", unit=1024 ** 2)
    GIGA_BYTE = number_as_udef(name="gb", unit=1024 ** 3)
    TRILLION_BYTE = number_as_udef(name="tb", unit=1024 ** 4)
    PETA_BYTE = number_as_udef(name="pb", unit=1024 ** 5)
    EXA_BYTE = number_as_udef(name="eb", unit=1024 ** 6)
    ZETTA_BYTE = number_as_udef(name="zb", unit=1024 ** 7)
    YOTTA_BYTE = number_as_udef(name="yb", unit=1024 ** 8)
    BRONTO_BYTE = number_as_udef(name="bb", unit=1024 ** 9)
