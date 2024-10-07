from functools import partial, update_wrapper as wraps
from pycinante.utils import optional_import, prettify
from typing import Any

__all__ = ["logger", "log"]

loguru, _ = optional_import(module="loguru", name="logger")

def log(msg: Any, *msgs: Any, level: str, sep: str = " ", pretty: bool = False, **kwargs: Any) -> None:
    getattr(loguru, level)(sep.join(((pretty and prettify) or str)(m) for m in (msg, *msgs)), **kwargs)

class logger:
    """Helper class for convenience to record log with loguru.

    Using cases:
        >>> from datetime import datetime
        >>> logger.add(f"training-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.log")
        >>> loss = ...
        >>> logger.info("train loss", loss.item())

        Here, the syntax is very similar to `print`, where you can send multiple inputs which later will be output. And
        the input can be any type, finally all inputs will automatically be converted to strings. Moreover, we also define
        aliases for the methods that exist in `loguru.logger` for the class. You can access these methods as you would
        in `loguru.logger`.
    """

    add = loguru.add
    bind = loguru.bind
    catch = loguru.catch
    complete = loguru.complete
    configure = loguru.configure
    contextualize = loguru.contextualize
    disable = loguru.disable
    enable = loguru.enable
    level = loguru.level
    opt = loguru.opt
    parse = loguru.parse
    patch = loguru.patch
    remove = loguru.remove
    start = loguru.start
    stop = loguru.stop

    critical = wraps(partial(log, level="critical"), log)
    debug = wraps(partial(log, level="debug"), log)
    info = wraps(partial(log, level="info"), log)
    warning = wraps(partial(log, level="warning"), log)
    error = wraps(partial(log, level="error"), log)
    exception = wraps(partial(log, level="exception"), log)
    success = wraps(partial(log, level="success"), log)
    trace = wraps(partial(log, level="trace"), log)
    log = loguru.log
