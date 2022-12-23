import functools
import logging
from logging import Logger
from pathlib import Path

LOGGER = logging.getLogger("toodle")


def attach(level=logging.INFO):
    LOGGER.setLevel(level)
    LOGGER.addHandler(logging.StreamHandler())


def log_tree(msg: str, root: Path, current: Path, logger=LOGGER):
    indent = " " * 4 * (len(current.parts) - len(root.parts))
    logger.info(indent + msg)


def log(msg, level=logging.INFO):
    LOGGER.log(level, msg)


def log_call(
        logger: Logger = LOGGER,
        level=logging.INFO,
        on_enter: str = None,
        on_exit: str = None
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if on_enter is not None:
                logger.log(level, on_enter.format(*args, **kwargs))
            result = func(*args, **kwargs)
            if on_exit is not None:
                logger.log(level, on_exit.format(*args, **kwargs))
            return result

        return wrapper

    return decorator
