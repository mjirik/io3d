#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Deprecation decorator, taken from https://gist.github.com/kgriffs/8202106"""

import functools
import inspect
import warnings


# NOTE: We don't want our deprecations to be ignored by default, so create our own type.
class DeprecatedWarning(UserWarning):
    pass


def deprecated(instructions):
    """
    Flags a method as deprecated.

    :param instructions: A human-friendly string of instructions, such as: 'Please migrate to add_proxy() ASAP.'
    :return: DeprecatedWarning
    """
    def decorator(func):
        """This is a decorator which can be used to mark functions as deprecated.

        It will result in a warning being emitted when the function is used.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            message = 'Call to deprecated function {}. {}'.format(func.__name__,
                                                                  instructions)
            frame = inspect.currentframe().f_back
            warnings.warn_explicit(message,
                                   category=DeprecatedWarning,
                                   filename=inspect.getfile(frame.f_code),
                                   lineno=frame.f_lineno)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def main():
    pass


if __name__ == '__main__':
    main()
