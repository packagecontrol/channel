# Not shared with Package Control

import os
import sys

PREFIX = '\\\\?\\' if sys.platform == 'win32' else ''

__cache_path = os.path.join(os.path.expanduser('~'), '.package_control')


def set_cache_dir(cache_path):
    global __cache_path
    __cache_path = cache_path


def pc_cache_dir():
    return __cache_path


def user_config_dir():
    return pc_cache_dir()


def longpath(path):
    """
    Normalize path, eliminating double slashes, etc.

    This is a patched version of ntpath.normpath(), which

    1. replaces `/` by `\\` on Windows, even if the absolute path specified is
       already prefixed by \\\\?\\ or \\\\.\\ to make sure to avoid WinError 123
       when calling functions like ntpath.realpath().

    2. always prepends \\\\?\\ on Windows to enable long paths support.

    This is to workaround some shortcomings of python stdlib.

    :param path:
        The absolute path to normalize

    :returns:
        A normalized path string
    """

    if PREFIX:
        special_prefixes = (PREFIX, '\\\\.\\')
        if path.startswith(special_prefixes):
            return os.path.normpath(path.replace('/', '\\'))
        return PREFIX + os.path.normpath(path)
    return os.path.normpath(path)


def shortpath(path):
    """
    Return unprefixed absolute path

    :param path:
        The absolute path to remove prefix from

    :returns:
        An unprefixed path string
    """
    return path[len(PREFIX):] if path.startswith(PREFIX) else path
