from __future__ import annotations
import os
from os import PathLike
import os.path as osp
import shutil
from datetime import datetime
from pycinante.misc.unit import uWrapper
from pycinante.io.utils import BinaryUnit, get_filename, get_ext
from pycinante.io.accessor import match_file_accessor

__all__ = ["file"]

class File(PathLike):
    """
    Helper class to access a disk file for convenience.
    """

    def __init__(self, pathname):
        self._pathname = os.fspath(pathname)

    @property
    def path(self):
        """
        Returns the pathname associated with a disk file.
        """
        return self._pathname

    def is_file(self):
        """
        Return True if path is an existing regular file.
        """
        return osp.isfile(self)

    def is_link(self):
        """
        Return True if path refers to an existing directory entry that is a symbolic link.
        """
        return osp.islink(self)

    def is_samefile(self, pathname):
        """
        Return True if both pathname arguments refer to the same file.
        """
        return osp.samefile(self, pathname)

    def is_exists(self):
        """
        Return True if path refers to an existing file or an open file descriptor.
        """
        return osp.exists(self)

    def is_not_exists(self):
        """
        Return True if path refers to a non-existing path.
        """
        return not osp.exists(self)

    def basename(self):
        """
        Return the base name of pathname path. This is the second element of the pair returned by passing path to the
        function split().
        """
        return osp.basename(self)

    def filename(self):
        """
        Return the file name of pathname path. This is the string returned from basename() with striping the last extension.
        e.g. a pathname '/foo/bar/test.sh.__init__.py', the filename() function returns 'test.sh.c'.
        """
        return get_filename(self)

    def ext(self):
        """
        Return the extension of pathname path. It just returns the second element of the splitext().
        """
        return get_ext(self)

    def accessed_time(self):
        """
        Return the datetime of last access of file.
        """
        return datetime.fromtimestamp(osp.getatime(self))

    def modified_time(self):
        """
        Return the datetime of last modification of file.
        """
        return datetime.fromtimestamp(osp.getmtime(self))

    def size(self):
        """
        Return the size wrapped with uWrapper(), in bytes, of file.
        """
        return uWrapper(osp.getsize(self), BinaryUnit.BYTE)

    def touch(self):
        """
        Return a File and if the file doesn't exist, it is created with default permissions.
        """
        os.close(os.open(self, os.O_CREAT))
        return self

    def copy_to(self, dst, **kwargs):
        """
        Copy the file from self to dst. Return the destination File.
        """
        dst = dst if osp.isabs(dst) else osp.abspath(osp.join(self, dst))
        return File(shutil.copyfile(self, dst, **kwargs))

    def copy_from(self, src, **kwargs):
        """
        Copy the file from dst to self. Return the self File.
        """
        src = src if osp.isabs(src) else osp.abspath(osp.join(self, src))
        shutil.copyfile(src, self, **kwargs)
        return self

    def move_to(self, dst, **kwargs):
        """
        Move the self file to dst location. Return the destination File.
        """
        dst = dst if osp.isabs(dst) else osp.abspath(osp.join(self, dst))
        return File(shutil.move(self, dst, **kwargs))

    def move_from(self, src, **kwargs):
        """
        Move the src file to self location. Return the self File.
        """
        src = src if osp.isabs(src) else osp.abspath(osp.join(self, src))
        return File(shutil.move(src, self, **kwargs))

    def remove(self):
        """
        Remove (delete) the file path. If path is a directory, an OSError is raised.
        """
        os.remove(self)
        return self

    def rename(self, new_name):
        """
        Rename the file or directory src to dst. Note that there is not support move a file to another location and the
        argument new_name is only new name of the file. Return the destination File.
        """
        dst = osp.join(osp.dirname(self), new_name)
        os.rename(self, dst)
        return File(dst)

    def load(self, loader=None, **kwargs):
        """
        Load data from the file via the loader.
        """
        if loader is None:
            accessor = match_file_accessor(self.ext())
            assert accessor is not None, "there are none of file accessor to load the file"
            loader = accessor.load
        return loader(self, **kwargs)

    def dump(self, obj, dumper=None, **kwargs):
        """
        Dump data into the file via the dumper.
        """
        if dumper is None:
            accessor = match_file_accessor(self.ext())
            assert accessor is not None, "there are none of file accessor to load the file"
            dumper = accessor.dump
        return dumper(obj, self, **kwargs)

    def __fspath__(self):
        """
        Returns the pathname that works with PathLike.
        """
        return self._pathname

    def __repr__(self):
        """
        Return the pathname str.
        """
        return self._pathname

    def __str__(self):
        """
        Return the pathname str.
        """
        return self._pathname

file = File
