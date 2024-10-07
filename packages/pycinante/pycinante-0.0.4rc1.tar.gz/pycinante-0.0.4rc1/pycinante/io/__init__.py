from __future__ import annotations
import os
from os import PathLike
from os import path as osp
from glob import iglob
import shutil
from pycinante.io.file import File
from pycinante.io.utils import PathType
from typing import Any, List
from typing_extensions import Self

__all__ = ["osp", "file", "path"]

class Path(PathLike):
    """Helper class to operate on path in convenience.

    Using cases:
        >>> root = Path("log", "unet").mkdir()
        >>> checkpoints = root / "checkpoints"
        >>> last_ckpt = checkpoints + "last.ckpt"

        As shown above, if the path root "log/unet" is not exists, PathBuilder will automatically create it when mkdir
        was set True. After that you can continue to build new paths via `/`, e.g. "log/unet/checkpoints", and final
        pathnames by `+`, e.g. "log/unet/checkpoints/last.ckpt".
    """

    def __init__(self, *pathnames: PathType) -> None:
        self._pathname = os.fspath(osp.join(*(pathnames or (".",))))

    @property
    def path(self) -> str:
        """
        Returns the pathname associated with a disk folder.
        """
        return self._pathname

    def parent(self) -> Path:
        """
        Return the directory name of pathname path. This is the first element of the pair returned by passing path to
        the function split().
        """
        return Path(osp.dirname(self))

    def glob(self, pattern: str, **kwargs: Any) -> List[File | Path]:
        """
        Returns all Files or Paths matching with the pattern.
        """
        return [File(e) if osp.isfile(e) else Path(e) for e in iglob(osp.join(self, pattern), **kwargs)]

    def is_dir(self) -> bool:
        """
        Return True if path is an existing directory.
        """
        return osp.isdir(self)

    def is_link(self) -> bool:
        """
        Return True if path refers to an existing directory entry that is a symbolic link.
        """
        return osp.islink(self)

    def is_mount(self) -> bool:
        """
        Return True if pathname path is a mount point.
        """
        return osp.ismount(self)

    def is_empty(self) -> bool:
        """
        Return True if the folder not contains any folder or file.
        """
        return len(os.listdir(self)) == 0

    def is_exists(self) -> bool:
        """
        Return True if path refers to an existing path.
        """
        return osp.exists(self)

    def is_not_exists(self) -> bool:
        """
        Return True if path refers to a non-existing path.
        """
        return osp.exists(self)

    def join(self, *pathnames: PathType) -> Path:
        """
        Join one or more path segments intelligently.
        """
        return Path(*(self, *pathnames))

    def abs(self) -> Self:
        """
        Return a Path with the normalized absolutized version of the pathname path.
        """
        self._pathname = osp.abspath(self)
        return self

    def normcase(self) -> Self:
        """
        Normalize the case of a pathname.
        """
        self._pathname = osp.normcase(self)
        return self

    def normpath(self) -> Self:
        """
        Normalize a pathname by collapsing redundant separators and up-level references so that A//B, A/B/, A/./B and
        A/foo/../B all become A/B.
        """
        self._pathname = osp.normpath(self)
        return self

    def expand_vars(self) -> Self:
        """
        Return a Path with the argument with environment variables expanded.
        """
        self._pathname = osp.expandvars(self)
        return self

    def expand_user(self) -> Self:
        """
        Return a Path with the argument with an initial component of ~ replaced by that user's home directory.
        """
        self._pathname = osp.expanduser(self)
        return self

    def relpath(self, start: PathType = os.curdir) -> Self:
        """
        Return a relative filepath to path either from the current directory or from an optional start directory.
        """
        self._pathname = osp.relpath(self, start)
        return self

    def cd(self, dst: PathType) -> Path:
        """
        Return a Path with changing the current directory to dst.
        """
        return Path(dst if osp.isabs(dst) else osp.abspath(osp.join(self._pathname, dst)))

    def mkdir(self) -> Self:
        """
        Create a directory recursively. Return its self instance.
        """
        os.makedirs(self, exist_ok=True)
        return self

    def remove(self, **kwargs: Any) -> Self:
        """
        Recursively delete a directory tree.
        """
        shutil.rmtree(self, **kwargs)
        return self

    def __truediv__(self, pathname: PathType) -> Path:
        """
        Join path with new pathname.
        """
        return Path(osp.join(self, pathname))

    def __add__(self, name: PathType) -> File:
        """
        Join file with new filename.
        """
        return File(osp.join(self, name))

    def __fspath__(self) -> str:
        """
        Returns the pathname that works with PathLike.
        """
        return self._pathname

    def __repr__(self) -> str:
        """
        Return the pathname str.
        """
        return self._pathname

    def __str__(self) -> str:
        """
        Return the pathname str.
        """
        return self._pathname

path = Path
file = File
