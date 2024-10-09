from __future__ import annotations
from functools import wraps
import inspect
import warnings
from types import FunctionType, MethodType
from pycinante.misc import version

__all__ = ["deprecated", "deprecated_arg", "deprecated_arg_default"]

class DeprecatedError(Exception):
    """
    A function or class was deprecated.
    """
    pass

def deprecated(since=None, removed=None, crt_version=None, msg_suffix="", warning_category=FutureWarning):
    """
    Marks a function or class as deprecated. If `since` is given this should be a version at or earlier than the current
    version and states at what version of the definition was marked as deprecated. If `removed` is given this can be any
    version and marks when the definition was removed.

    When the decorated definition is called, that is when the function is called or the class instantiated, a `warning_category`
    is issued if `since` is given and the current version is at or later than that given. a `DeprecatedError` exception
    is instead raised if `removed` is given and the current version is at or later than that, or if neither `since` nor
    `removed` is provided.

    Args:
        since: version at which the definition was marked deprecated but not removed.
        removed: version at which the definition was/will be removed and no longer usable.
        crt_version: version to compare since and removed against, default is current version.
        msg_suffix: message appended to warning/exception detailing reasons for deprecation and what to use instead.
        warning_category: a warning category class, defaults to `FutureWarning`.

    Returns:
        Decorated definition which warns or raises exception when used.
    """
    if since is not None and removed is not None and not version.leq(since, removed):
        raise ValueError(f"since must be less or equal to removed, got since={since}, removed={removed}.")

    is_deprecated, is_removed = True, False
    if crt_version is not None:
        # `crt_version` is smaller than `since`, do nothing
        if since is not None and not version.leq(since, crt_version):
            return lambda obj: obj

        # `crt_version` is greater than or equal to `removed`, raise a DeprecatedError
        if removed is not None and version.leq(removed, crt_version):
            is_removed = True

    # both `since` and `removed` are not specified, raise a DeprecatedError
    if since is None and removed is None:
        is_removed, is_deprecated = True, True

    def _decorator(obj):
        is_func = isinstance(obj, FunctionType)
        call_obj = obj if is_func else obj.__init__

        msg_prefix = f"{'Function' if is_func else 'Class'} `{obj.__qualname__}`"

        if is_removed and removed:
            msg_infix = f"was removed in version {removed}."
        elif is_deprecated and since:
            msg_infix = f"has been deprecated since version {since}."
            if removed is not None:
                msg_infix += f" It will be removed in version {removed}."
        else:
            msg_infix = "has been deprecated."

        msg = f"{msg_prefix} {msg_infix} {msg_suffix}".strip()

        @wraps(call_obj)
        def _wrapper(*args, **kwargs):
            if is_removed:
                raise DeprecatedError(msg)
            if is_deprecated:
                warnings.warn(message=f"{obj}: {msg}", category=warning_category, stacklevel=2)

            return call_obj(*args, **kwargs)

        if is_func:
            return _wrapper
        obj.__init__ = _wrapper
        return obj
    return _decorator

def deprecated_arg(name, since=None, removed=None, crt_version=None, msg_suffix="", new_name=None, warning_category=FutureWarning):
    """
    Marks a particular named argument of a callable as deprecated. The same conditions for `since` and `removed` as
    described in the `deprecated` decorator.

    When the decorated definition is called, that is when the function is called or the class instantiated with args, a
    `warning_category` is issued if `since` is given and the current version is at or later than that given. a `DeprecatedError`
    exception is instead raised if `removed` is given and the current version is at or later than that, or if neither `since`
    nor `removed` is provided.

    Args:
        name: name of position or keyword argument to mark as deprecated.
        since: version at which the argument was marked deprecated but not removed.
        removed: version at which the argument was/will be removed and no longer usable.
        crt_version: version to compare since and removed against, default is current version.
        msg_suffix: message appended to warning/exception detailing reasons for deprecation and what to use instead.
        new_name: name of position or keyword argument to replace the deprecated argument.
            if it is specified and the signature of the decorated function has a `kwargs`, the value to the
            deprecated argument `name` will be removed.
        warning_category: a warning category class, defaults to `FutureWarning`.

    Returns:
        Decorated callable which warns or raises exception when deprecated argument used.
    """
    if since is not None and removed is not None and not version.leq(since, removed):
        raise ValueError(f"since must be less or equal to removed, got since={since}, removed={removed}.")

    is_deprecated, is_removed = True, False
    if crt_version is not None:
        # `crt_version` is smaller than `since`, do nothing
        if since is not None and not version.leq(since, crt_version):
            return lambda obj: obj

        # `crt_version` is greater than or equal to `removed`, raise a DeprecatedError
        if removed is not None and version.leq(removed, crt_version):
            is_removed = True

    # both `since` and `removed` are not specified, raise a DeprecatedError
    if since is None and removed is None:
        is_removed, is_deprecated = True, True

    def _decorator(func: FunctionType | MethodType):
        arg_name = f"{func.__module__} {func.__qualname__}:{name}"
        sig = inspect.signature(func)

        msg_prefix = f"Argument `{name}`"

        if is_removed and removed:
            msg_infix = f"was removed in version {removed}."
        elif is_deprecated and since:
            msg_infix = f"has been deprecated since version {since}."
            if removed is not None:
                msg_infix += f" It will be removed in version {removed}."
        else:
            msg_infix = "has been deprecated."

        msg = f"{msg_prefix} {msg_infix} {msg_suffix}".strip()

        @wraps(func)
        def _wrapper(*args, **kwargs):
            if new_name is not None and name in kwargs and new_name not in kwargs:
                # replace the deprecated arg `name` with `new_name`
                kwargs[new_name] = kwargs[name]

                try:
                    sig.bind(*args, **kwargs).arguments
                except TypeError:  # multiple values for `new_name` using both `args` and `kwargs`
                    kwargs.pop(new_name, None)

            binding = sig.bind(*args, **kwargs).arguments
            positional_found = name in binding

            kw_found = False
            for k, param in sig.parameters.items():
                if param.kind == inspect.Parameter.VAR_KEYWORD and k in binding and name in binding[k]:
                    kw_found = True
                    # if the deprecated arg is found in the **kwargs, it should be removed
                    kwargs.pop(name, None)

            if positional_found or kw_found:
                if is_removed:
                    raise DeprecatedError(msg)
                if is_deprecated:
                    warnings.warn(message=f"{arg_name}: {msg}", category=warning_category, stacklevel=2)

            return func(*args, **kwargs)
        return _wrapper
    return _decorator

def deprecated_arg_default(name, new_default, since=None, replaced=None, crt_version=None, msg_suffix="", warning_category=FutureWarning):
    """
    Marks a particular arguments default of a callable as deprecated. It is changed from `old_default` to `new_default`
    in version `changed`.

    When the decorated definition is called, a `warning_category` is issued if `since` is given, the default is not explicitly
    set by the caller and the current version is at or later than that given. Another warning with the same category is
    issued if `changed` is given and the current version is at or later.

    Args:
        name: name of position or keyword argument where the default is deprecated/changed.
        new_default: name of the new default.
            It is validated that this value is not present as the default before version `replaced`.
            This means, that you can also use this if the actual default value is `None` and set later in the function.
            You can also set this to any string representation, e.g. `"calculate_default_value()"`
            if the default is calculated from another function.
        since: version at which the argument default was marked deprecated but not replaced.
        replaced: version at which the argument default was/will be replaced.
        crt_version: version to compare since and removed against, default is current version.
        msg_suffix: message appended to warning/exception detailing reasons for deprecation.
        warning_category: a warning category class, defaults to `FutureWarning`.

    Returns:
        Decorated callable which warns when deprecated default argument is not explicitly specified.
    """
    if since is not None and replaced is not None and not version.leq(since, replaced):
        raise ValueError(f"since must be less or equal to replaced, got since={since}, replaced={replaced}.")

    is_deprecated, is_replaced = True, False
    if crt_version is not None:
        # `crt_version` is smaller than `since`, do nothing
        if since is not None and not version.leq(since, crt_version):
            return lambda obj: obj

        # `crt_version` is greater than or equal to `replaced`, raise a DeprecatedError
        if replaced is not None and version.leq(replaced, crt_version):
            is_replaced = True

    # both `since` and `removed` are not specified, raise a DeprecatedError
    if since is None and replaced is None:
        is_replaced, is_deprecated = True, True

    def _decorator(func: FunctionType | MethodType):
        arg_name = f"{func.__module__} {func.__qualname__}:{name}"

        if name not in (sig := inspect.signature(func)).parameters:
            raise ValueError(f"Argument `{name}` not found in signature of {func.__qualname__}.")

        if (old_default := sig.parameters[name].default) is inspect.Parameter.empty:
            raise ValueError(f"Argument `{name}` has no default value.")

        if old_default == new_default and not is_replaced:
            raise ValueError(f"Argument `{name}` was replaced to the new default value `{new_default}` before the specified version {replaced}.")

        msg_prefix = f" Current default value of argument `{name}={old_default}`"

        if is_replaced and replaced:
            msg_infix = f"was changed in version {replaced} from `{name}={old_default}` to `{name}={new_default}`."
        elif is_deprecated and since:
            msg_infix = f"has been deprecated since version {since}."
            if replaced is not None:
                msg_infix += f" It will be changed to `{name}={new_default}` in version {replaced}."
        else:
            msg_infix = f"has been deprecated from `{name}={old_default}` to `{name}={new_default}`."

        msg = f"{msg_prefix} {msg_infix} {msg_suffix}".strip()

        @wraps(func)
        def _wrapper(*args, **kwargs):
            if name not in sig.bind(*args, **kwargs).arguments and is_deprecated:
                # arg was not found so the default value is used
                warnings.warn(message=f"{arg_name}: {msg}", category=warning_category, stacklevel=2)
            return func(*args, **kwargs)
        return _wrapper
    return _decorator
