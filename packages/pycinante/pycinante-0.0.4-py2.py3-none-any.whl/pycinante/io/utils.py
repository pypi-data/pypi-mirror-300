import os.path as osp
from enum import Enum
from pycinante.misc.unit import number_as_udef
from pycinante.utils import export

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

@export
def get_ext(path):
    """
    Return the extension of a given path.
    """
    return osp.splitext(osp.basename(path))[1]

@export
def get_filename(path):
    """
    Return the file name of pathname path. This is the string returned from basename() with striping the last extension.
    e.g. a pathname '/foo/bar/test.sh.__init__.py', the filename() function returns 'test.sh.c'.
    """
    return osp.splitext(osp.basename(path))[0]
