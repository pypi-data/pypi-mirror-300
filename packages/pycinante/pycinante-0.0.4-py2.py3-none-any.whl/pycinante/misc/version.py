import re
import warnings
from pycinante.utils import export

@export
def str2tuple(version):
    """
    Covert a version_str into a version_tuple.
    """
    def _try_cast(val):
        try:
            m = re.match(pattern="(\\d+)(.*)", string=val.strip())
            return int(m.groups()[0]) if m else val
        except ValueError:
            return val

    return tuple(map(_try_cast, version.split(sep="+", maxsplit=1)[0].split(".")))

@export
def tuple2str(version):
    """
    Covert a version tuple into a version_str.
    """
    return ".".join(str(e) for e in version)

@export
def leq(lhs, rhs):
    """
    Returns True if version `lhs` is earlier or equal to `rhs`.
    """
    for l, r in zip(str2tuple(str(lhs)), str2tuple(str(rhs))):
        if l != r:
            if isinstance(l, int) and isinstance(r, int):
                return l < r
            return f"{l}" < f"{r}"
    return True

@export
def min_version(module, min_version_str=""):
    """
    Returns True if the module's version is greater or equal to the 'min_version'. When min_version_str is not provided,
    it always returns True.
    """
    if not min_version_str or not hasattr(module, "__version__"):
        return True  # always valid version
    return str2tuple(module.__version__)[:2] >= str2tuple(min_version_str)[:2]

@export
def exact_version(module, version_str=""):
    """
    Returns True if the module's __version__ matches version_str.
    """
    if not hasattr(module, "__version__"):
        warnings.warn(f"{module} has no attribute __version__ in exact_version check.")
        return False
    return bool(module.__version__ == version_str)
