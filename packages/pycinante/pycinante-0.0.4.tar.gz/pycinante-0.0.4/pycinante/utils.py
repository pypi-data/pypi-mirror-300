import sys
from functools import wraps
from importlib import import_module
import json

__all__ = ["export"]

def export(func_or_clz=None):
    """
    Exports a function/class definition into its module's `__all__`.
    """
    @wraps(func_or_clz)
    def _wrapper(func):
        return export(func)

    if func_or_clz is None:
        return _wrapper

    func_name = func_or_clz.__name__
    m = sys.modules[func_or_clz.__module__]
    if hasattr(m, "__all__"):
        if func_name not in m.__all__:
            m.__all__.append(func_name)
    else:
        m.__all__ = [func_name]

    return func_or_clz

@export
class OptionalImportError(ImportError):
    """
    Could not import APIs from an optional dependency.
    """

@export
def optional_import(module, name=""):
    """
    Imports an optional module specified by `module` string. Any importing related exceptions will be stored, and
    exceptions raise lazily when attempting to use the failed-to-import module.
    """
    try:
        the_module = import_module(module)
        the_module = getattr(the_module, name) if name else the_module
    except Exception as e:
        # any exceptions during import
        cmd = f"from {module} import {name}" if name else f"import {module}"
        exc = OptionalImportError(f"{str(cmd)} ({str(e)})").with_traceback(e.__traceback__)

        def wrapper(*_args, **_kwargs):
            raise exc

        return type("LazyRaise", (object,), {
            e: wrapper for e in ("__call__", "__getattr__", "__getitem__", "__iter__")
        })(), False
    else:  # found the module
        return the_module, True

@export
def prettify(obj, encoder=None, **kwargs):
    """Prettify a Python object into an easy-to-read string. Due to its backed by json serializer, if an object cannot
    be serialized, a plain string of the object will be returned. Or you can opt to implement a special json encoder to
    serialize the object and to set it to the `encoder` argument when calling `prettify`.

    Using cases:
        >>> import albumentations as T
        >>> class MyJsonEncoder(json.JSONEncoder):
        >>>     def default(self, obj):
        >>>         if isinstance(obj, (T.BaseCompose, T.BaseCompose)):
        >>>             return r(8) if (r := getattr(obj, "indented_repr", None)) else repr(obj)
        >>>         return super(MyJsonEncoder, self).default(obj)
        >>> transform = T.Compose([T.Resize(224, 224), T.Normalize()])
        >>> prettify(transform, encoder=MyJsonEncoder)
        Compose([
          Resize(p=1.0, height=224, width=224, interpolation=1),
          Normalize(p=1.0, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, normalization='standard'),
        ], p=1.0, bbox_params=None, keypoint_params=None, additional_targets={}, is_check_shapes=True)

        Here, we provide an example to illustrate how to use your customized JsonEncoder to serialize the object and to
        take the indent in json to get a more readable string.
    """
    try:
        return json.dumps(
            obj=obj,
            indent=kwargs.pop("indent", 4),
            cls=encoder or json.JSONEncoder,
            ensure_ascii=kwargs.pop("ensure_ascii", False),
            **kwargs
        )
    except TypeError:
        # if the obj cannot be serialized
        return repr(obj)
