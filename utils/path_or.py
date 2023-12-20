from functools import reduce
from typing import Any


def path_or(obj, keys: str, fallback: Any):
    """
    Returns first None of an attrchain
    """
    try:
        return reduce(getattr, keys.split('.'), obj)
    except AttributeError:
        return fallback
