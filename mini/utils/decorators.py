from time import time

from humanize import precisedelta
from loguru import logger

MINIMUM_UNIT = "milliseconds"


def howlong(func):
    def wrap(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        logger.debug(
            f"{func.__name__} took {precisedelta(time() - start, minimum_unit=MINIMUM_UNIT)}"
        )
        return result

    return wrap
