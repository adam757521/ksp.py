from typing import Iterable, Any, Optional


__all__ = ("get",)


def get(iterable: Iterable[Any], **kwargs) -> Optional[Any]:
    """
    Returns the first object that matches the kwargs arguments.
    Used in caching.

    :param Iterable iterable: The iterable.
    :param kwargs: The key arguments.
    :return: The first object that matches the kwargs arguments.
    :rtype: Optional[Any]
    """

    for elem in iterable:
        for key, value in kwargs.items():
            if getattr(elem, key) == value:
                return elem
