"""Update Log

2024.10.07:
    - added logging level constants in logger for more convenience when accessing logging level
    - added a useful function console() that supports reconfig console logging handler in one line code
    - re-implemented the function remove() where you not only can remove a handler by its id but its filename or stream
    - added a function for loading configuration files to config the logger
"""

from __future__ import annotations
import sys
import os.path as osp
import logging
from functools import partial
from loguru import _defaults
from loguru import logger as loguru
from pycinante.io.accessor import match_file_accessor
from pycinante.log.utils import eval_valexp

__all__ = ["logger"]

def log(msg, *msgs, sep=" ", prettify=str, level, **kwargs) -> None:
    """
    An updated version of loguru.log(), and you can use it like the print() function.
    """
    getattr(loguru, level)(sep.join((prettify(m) for m in (msg, *msgs))), **kwargs)

class logger:
    """
    Helper classes to facilitate logging using loguru.

    Using cases:
        >>> from datetime import datetime
        >>> logger.add(f"training-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.log")
        >>> loss = ...
        >>> logger.info("train loss", loss.item())

        Here, the syntax is very similar to `print`, where you can send multiple inputs which later will be output. And
        the input can be any type, finally all inputs will automatically be converted to strings. Moreover, we also define
        aliases for the methods that exist in `loguru.logger` for the class. You can access these methods as you would
        in `loguru.logger`.

    Note that the loguru package is an optional package. Before you use the logger, you need first ensure that the loguru
    have installed in your environment (e.g. pip install loguru, here all version of loguru works well.).
    """

    # the severity levels
    # refer https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add
    TRACE = 5
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    SUCCESS = 25
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    # the enhanced log functions
    trace = partial(log, level="trace")
    debug = partial(log, level="debug")
    info = partial(log, level="info")
    success = partial(log, level="success")
    warning = partial(log, level="warning")
    error = partial(log, level="error")
    critical = partial(log, level="critical")

    # the other interface exposed in loguru.logger
    # https://loguru.readthedocs.io/en/stable/api/logger.html
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
    start = loguru.start
    stop = loguru.stop
    log = loguru.log
    exception = loguru.exception

    @staticmethod
    def remove(handler_id=None):
        """
        Remove a previously added handler and stop sending logs to its sink. It has a little different from loguru.logger.remove(),
        the remove() removes a handler by the handler id, filename, or stream.
        """
        if handler_id is None or isinstance(handler_id, int):
            loguru.remove(handler_id)
            return

        if isinstance(handler_id, str):
            # remove all handlers whose filename is matched with handler_id
            def _is_matching_handler(handler) -> bool:
                return getattr(getattr(handler[1], "_sink"), "_path", None) == handler_id
        elif isinstance(handler_id, type(sys.stderr)):
            # remove all handlers whose stream is matched with handler_id
            def _is_matching_handler(handler) -> bool:
                return getattr(getattr(handler[1], "_sink"), "_stream", None) == handler_id
        else:
            raise ValueError(f"Cannot handle handler_id type: {type(handler_id)}")

        handlers = getattr(loguru, "_core").handlers.items()
        for handler in filter(_is_matching_handler, handlers):
            loguru.remove(handler[0])

    @staticmethod
    def console(level=None, format=None, **kwargs) -> None:
        """
        A helper function for reconfiguring the logging outputting to the console. It only re-configs the default console
        logging handler, that is a handler whose handler id is equal to 0.
        """
        logger.remove(0)
        level, format = level or _defaults.LOGURU_LEVEL, format or _defaults.LOGURU_FORMAT
        logger.add(sys.stderr, level=level, format=format, **kwargs)

    @staticmethod
    def load_cfg(path, context=None) -> None:
        """
        Load the logging configs in the file (.json, .toml, .yaml, ...) and config the logger with it.

        An example config file (json case as an example):
            config = {
                "handlers": [
                    {"sink": "{sys.stdout}", "format": "{time} - {message}"},
                    {"sink": "file.log", "serialize": True},
                ],
                "extra": {"user": "someone"}
            }
        As shown above, for file handler it's same as in configure(). Note that when configuring a stream handler where
        the sink is a stream object, but in json file it cannot be config-ed directly. Here we use the value expression
        to solve the problem, that is you need to config the object with its name as "{sys.stdout}", and until the config
        be loaded the value expression will be evaluated and the expression will be replaced with the evaluated value.
        In same cases, evaluating the value expression needs a special context to support, the context can be set in k/v
        pair as same as in eval() to provide a context env. the sys env is provided by default.
        """
        cfg = match_file_accessor(osp.splitext(osp.basename(path))[1]).load(path)
        assert isinstance(cfg, dict), f"the configuration file must be dict type, not {type(cfg)}"

        context = {**{"sys": sys}, **(context or {})}
        for handler in cfg.get("handlers", []):
            # for re-writing objects into the config with those braces style sink
            handler["sink"] = eval_valexp(handler["sink"], context)

        logger.configure(**cfg)
