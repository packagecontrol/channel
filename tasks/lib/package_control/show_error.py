# Not shared with Package Control

from . import text


def show_error(string, params=None, strip=True, indent=None):
    """
    Sends an error message to rollbar after running the string through
    text.format()

    :param string:
        The error to display

    :param params:
        Params to interpolate into the string

    :param strip:
        If the last newline in the string should be removed

    :param indent:
        If all lines should be indented by a set indent after being dedented
    """

    print(text.format(string, params, strip=strip, indent=indent))
