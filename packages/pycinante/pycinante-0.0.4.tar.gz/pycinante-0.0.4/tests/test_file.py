from pathlib import PurePath
from pycinante.io import file

def test_path():
    assert file("file.log").path == "file.log"
    assert file(PurePath("file.log")).path == "file.log"

def test_is_file():
    assert file("file.log").is_file()
    assert not file("no_exists.log").is_file()

def test_is_exists():
    assert file("file.log").is_exists()
    assert not file("no_exists.log").is_exists()

def test_basename():
    assert file("./file.log").basename() == "file.log"

def test_filename():
    assert file("./file.log").filename() == "file"

def test_ext():
    assert file("./file.log").ext() == ".log"

def test_accessed_time():
    print(file("./file.log").accessed_time())

def test_modified_time():
    print(file("./file.log").modified_time())

def test_size():
    print(file("./test.log").size().value)

def test_rename():
    print(file("./file.log").rename("test.log"))
