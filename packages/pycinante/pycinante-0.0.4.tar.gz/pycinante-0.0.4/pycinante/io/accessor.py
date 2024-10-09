from abc import ABC, abstractmethod
import os
import sys
import pickle
import re
from pycinante.utils import optional_import, export

@export
class FileAccessor(ABC):
    """
    A helper class for providing unified interfaces to access various type of file.
    """

    # specify what type of file the file accessor can be accessed
    supported_types = []

    @property
    @abstractmethod
    def loader(self):
        """
        Return a loader used for loading the specific type file from path.
        """
        pass

    @property
    @abstractmethod
    def dumper(self):
        """
        Return a dumper used for storing data into the specific file.
        """
        pass

    @property
    def order(self):
        """
        Return a priority number where a higher priority can be first considered as FileAccessor. The priority is -1 by
        default. A larger value indicates a higher priority.
        """
        return -1

    def load(self, path, **kwargs):
        """
        Load data from the specific path through loader().
        """
        return self.loader(path, **kwargs)

    def dump(self, obj, path, **kwargs):
        """
        Dump data to the specific file through dumper().
        """
        self.dumper(obj, path, **kwargs)

@export
def load_text(path, **kwargs):
    """
    Load text from the path file.
    """
    with open(path, "r", encoding=kwargs.pop("encoding", sys.getdefaultencoding())) as fp:
        return fp.read()

@export
def dump_text(obj, path, **kwargs):
    """
    Dump obj into the text file.
    """
    with open(path, "w", encoding=kwargs.pop("encoding", sys.getdefaultencoding())) as fp:
        fp.write(obj)

@export
class TextFileAccessor(FileAccessor):
    """
    A helper class for accessing files of text type (.txt).
    """

    supported_types = [".txt"]

    @property
    def loader(self):
        return load_text

    @property
    def dumper(self):
        return dump_text

@export
def load_bytes(path, **kwargs):
    """
    Load bytes from the path file.
    """
    with open(path, "rb", **kwargs) as fp:
        return fp.read()

@export
def dump_bytes(obj, path, **kwargs):
    """
    Dump obj into the bytes file.
    """
    with open(path, "wb", **kwargs) as fp:
        fp.write(obj)

@export
class BytesFileAccessor(FileAccessor):
    """
    A helper class for accessing files of binary type. The accessor can read all type of file.
    """

    supported_types = [".*"]

    @property
    def loader(self):
        return load_bytes

    @property
    def dumper(self):
        return dump_bytes

    @property
    def order(self):
        return -2147483648

try:
    import simplejson as json
except ImportError:
    import json

@export
def load_json(path, **kwargs):
    """
    Load json from the path file.
    """
    with open(path, "r", encoding=kwargs.pop("encoding", sys.getdefaultencoding())) as fp:
        return json.load(fp, **kwargs)

@export
def dump_json(obj, path, **kwargs):
    """
    Dump obj into the json file.
    """
    with open(path, "w", encoding=kwargs.pop("encoding", sys.getdefaultencoding())) as fp:
        json.dump(obj, fp, **kwargs)

@export
class JsonFileAccessor(FileAccessor):
    """
    A helper class for accessing files of json type (.json).
    """

    supported_types = [".json"]

    @property
    def loader(self):
        return load_json

    @property
    def dumper(self):
        return dump_json

@export
def load_pickle(path, **kwargs):
    """
    Load pickle from the path file.
    """
    with open(path, "rb") as fp:
        return pickle.load(fp, **kwargs)

@export
def dump_pickle(obj, path, **kwargs):
    """
    Dump obj into the pickle file.
    """
    with open(path, "wb") as fp:
        pickle.dump(obj, fp, **kwargs)

@export
class PickleFileAccessor(FileAccessor):
    """
    A helper class for accessing files of pickle type (.pkl).
    """

    supported_types = [".pkl"]

    @property
    def loader(self):
        return load_pickle

    @property
    def dumper(self):
        return dump_pickle

cv2, _ = optional_import("cv2")

@export
def load_cv2(path, **kwargs):
    """
    Load image from the path file via opencv.
    """
    return cv2.imread(os.fspath(path), **kwargs)

@export
def dump_cv2(obj, path, **kwargs):
    """
    Dump obj into the image file via opencv.
    """
    assert cv2.imwrite(os.fspath(path), obj, **kwargs)

@export
class OpenCVImageFileAccessor(FileAccessor):
    """
    A helper class for accessing files of image type via opencv.
    """

    supported_types = [
        ".bmp", ".dib", ".jpeg", ".jpg", ".jpe", ".jp2", ".png", ".webp", ".pbm", ".pgm", ".ppm", ".sr", ".ras", "tiff",
        ".tif", ".exr", ".hdr", ".pic"
    ]

    @property
    def loader(self):
        return load_cv2

    @property
    def dumper(self):
        return dump_cv2

    @property
    def order(self):
        # higher priority than PIL accessor
        return 100

PIL, _ = optional_import(module="PIL", name="Image")

@export
def load_pil(path, **kwargs):
    """
    Load image from the path file via Pillow.
    """
    return PIL.open(os.fspath(path), **kwargs)

@export
def dump_pil(obj, path, **kwargs):
    """
    Dump obj into the image file via Pillow.
    """
    obj.save(os.fspath(path), **kwargs)

@export
class PILImageFileAccessor(FileAccessor):
    """
    A helper class for accessing files of image type via Pillow.
    """

    supported_types = [
        ".blp", ".bmp", ".dds", ".dib", ".eps", ".gif", ".icns", ".ico", ".im", ".jpeg", ".jp2", ".msp", ".pcx", ".png",
        ".ppm", ".sgi", ".spider", ".tga", ".tiff", ".webp", ".xbm", ".cur", ".dcx", ".fits", ".flc", ".fpx", ".ftex",
        ".gbr", ".gb", ".imt", ".iptc", ".naa", ".mcidas", ".mic", ".mpo", ".pcd", ".pixar", ".psd", ".qoi", ".sun", "wal",
        ".wmf", ".emf", ".xpm", ".palm", ".pdf", ".xvt", ".bufr", ".grib", ".hdf5", ".mepg"
    ]

    @property
    def loader(self):
        return load_pil

    @property
    def dumper(self):
        return dump_pil

pandas, _ = optional_import("pandas")

@export
def load_csv(path, **kwargs):
    """
    Load csv from the path file.
    """
    return pandas.read_csv(path, **kwargs)

@export
def dump_csv(obj, path, **kwargs):
    """
    Load obj into the csv file.
    """
    obj.to_csv(path, **kwargs)

@export
class CsvFileAccessor(FileAccessor):
    """
    A helper class for accessing files of csv type (.csv).
    """

    supported_types = [".csv"]

    @property
    def loader(self):
        return load_csv

    @property
    def dumper(self):
        return dump_csv

@export
def load_excel(path, **kwargs):
    """
    Load Excel from the path file.
    """
    return pandas.read_excel(path, **kwargs)

@export
def dump_excel(obj, path, **kwargs):
    """
    Load obj into the Excel file.
    """
    obj.to_excel(path, **kwargs)

@export
class XlsxFileAccessor(FileAccessor):
    """
    A helper class for accessing files of xlsx type (.xlsx).
    """

    supported_types = [".xlsx"]

    @property
    def loader(self):
        return load_excel

    @property
    def dumper(self):
        return dump_excel

numpy, _ = optional_import("numpy")

@export
def load_numpy(path, **kwargs):
    """
    Load numpy from the path file.
    """
    return numpy.load(path, allow_pickle=kwargs.pop("allow_pickle", True), **kwargs)

@export
def dump_numpy(obj, path, **kwargs):
    """
    Dump obj into the numpy file.
    """
    numpy.save(path, obj, **kwargs)

@export
class NumpyFileAccessor(FileAccessor):
    """
    A helper class for accessing files of numpy type (.npy, .npz).
    """

    supported_types = [".npy", ".npz"]

    @property
    def loader(self):
        return load_numpy

    @property
    def dumper(self):
        return dump_numpy

torch, _ = optional_import("torch")

@export
def load_torch(path, **kwargs):
    """
    Load torch from the path file.
    """
    return torch.load(path, **kwargs)

@export
def dump_torch(obj, path, **kwargs):
    """
    Dump obj into the torch file.
    """
    torch.save(obj, path, **kwargs)

@export
class TorchFileAccessor(FileAccessor):
    """
    A helper class for accessing files of torch type (.pt, .pth).
    """

    supported_types = [".pt", ".pth"]

    @property
    def loader(self):
        return load_torch

    @property
    def dumper(self):
        return dump_torch

archive, _ = optional_import("archive")

@export
def extract_archive(src, dst, **kwargs):
    """
    Extract the archive file src into the folder dst.
    """
    archive.extract(os.fspath(src), os.fspath(dst), **kwargs)

@export
class ArchiveFileAccessor(FileAccessor):
    """
    A helper class for extracting an archive into a folder (.zip, .tar, ...).
    """

    supported_types = [
        ".docx", ".egg", ".jar", ".odg", ".odp", ".ods", ".odt", ".pptx", ".tar", ".tar.bz2", ".tar.gz", ".tgz", ".tz2",
        ".xlsx", ".zip"
    ]

    @property
    def loader(self):
        raise NotImplementedError("the archive file accessor only extract method can be called.")

    @property
    def dumper(self):
        raise NotImplementedError("the archive file accessor only extract method can be called.")

    # noinspection PyMethodMayBeStatic
    def extract(self, src, dst, **kwargs):
        """
        Extract the archive file src into the folder dst.
        """
        extract_archive(src, dst, **kwargs)

yaml, _ = optional_import("yaml")

@export
def load_yaml(path, **_kwargs):
    """
    Load yaml from the path file.
    """
    with open(path, "r") as fp:
        return yaml.safe_load(fp.read())

@export
def dump_yaml(obj, path, **kwargs):
    """
    Dump obj into the yaml file.
    """
    with open(path, "w") as fp:
        yaml.safe_dump(obj, fp, allow_unicode=True, **kwargs)

@export
class YamlFileAccessor(FileAccessor):
    """
    A helper class for accessing files of yaml type (.yml, .yaml).
    """

    supported_types = [".yml", ".yaml"]

    @property
    def loader(self):
        return load_yaml

    @property
    def dumper(self):
        return dump_yaml

toml, _ = optional_import("toml")

@export
def load_toml(path, **kwargs):
    """
    Load toml from the path file.
    """
    return toml.load(path, **kwargs)

@export
def dump_toml(obj, path, **kwargs):
    """
    Dump obj into the toml file.
    """
    with open(path, "w") as fp:
        toml.dump(obj, fp, **kwargs)

@export
class TomlFileAccessor(FileAccessor):
    """
    A helper class for accessing files of toml type (.toml).
    """

    supported_types = [".toml"]

    @property
    def loader(self):
        return load_toml

    @property
    def dumper(self):
        return dump_toml

ElementTree, _ = optional_import(module="xml.etree", name="ElementTree")

@export
def load_xml(path, **kwargs):
    """
    Load xml from the path file.
    """
    return ElementTree.parse(path, **kwargs)

@export
def dump_xml(obj, path, **kwargs):
    """
    Dump obj into the xml file.
    """
    obj.write(path, **kwargs)

@export
class XmlFileAccessor(FileAccessor):
    """
    A helper class for accessing files of xml type (.xml).
    """

    supported_types = [".xml"]

    @property
    def loader(self):
        return load_xml

    @property
    def dumper(self):
        return dump_xml

BeautifulSoup, _ = optional_import(module="bs4", name="BeautifulSoup")

@export
def load_html(path, **kwargs):
    """
    Load html from the path file.
    """
    return BeautifulSoup(load_text(path, **kwargs), parser=kwargs.pop("parser", "lxml"))

@export
def dump_html(obj, path, **kwargs):
    """
    Dump obj into the html file.
    """
    dump_text(obj.prettify(), path, **kwargs)

@export
class HtmlFileAccessor(FileAccessor):
    """
    A helper class for accessing files of html type (.xml).
    """

    supported_types = [".html"]

    @property
    def loader(self):
        return load_html

    @property
    def dumper(self):
        return dump_html

soundfile, _ = optional_import("soundfile")

@export
def load_sound(path, **kwargs):
    """
    Load sound from the path file.
    """
    return soundfile.read(os.fspath(path), **kwargs)[0]

@export
def dump_sound(obj, path, **kwargs):
    """
    Dump obj into the sound file.
    """
    soundfile.write(os.fspath(path), obj, **kwargs)

@export
class SoundFileAccessor(FileAccessor):
    """
    A helper class for accessing files of sound type (.mp3, .raw, ...).
    """

    supported_types = [".raw", ".flac", ".ogg", ".mp3"]

    @property
    def loader(self):
        return load_sound

    @property
    def dumper(self):
        return dump_sound

# Note that the native list is thread-safe supported by GIL
_file_accessors = [
    module() for name, module in globals().items()
    if name.endswith("FileAccessor") and name != "FileAccessor"
]

@export
def add_file_accessor(accessor):
    """
    Add a FileAccessor into global file accessor pool. Note that the pool only allows one instance type has one accessor.
    If multiple times adding same instance type accessors into the pool, the newest accessor will be retained.
    """
    try:
        old = next(filter(lambda e: isinstance(e, type(accessor)), _file_accessors))
        _file_accessors.remove(old)
    except StopIteration:
        pass

    _file_accessors.append(accessor)

@export
def match_file_accessor(ext, accessor_type=None):
    """
    Return a FileAccessor that it can access the ext type file. If there are none of FileAccessor matching with ext,
    then None will be returned.
    """
    candidates = [e for e in _file_accessors if any([bool(re.match(t, ext)) for t in e.supported_types])]

    # none of matching
    if len(candidates) == 0:
        return None

    # by type
    if accessor_type is not None:
        return next(filter(lambda e: isinstance(e, accessor_type), candidates))

    # by order
    candidates = sorted(candidates, key=lambda e: e.order, reverse=True)
    return candidates[0]
