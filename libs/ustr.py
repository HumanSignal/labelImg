import sys
from libs.constants import DEFAULT_ENCODING


def ustr(x):
    """py2/py3 unicode helper"""

    if sys.version_info < (3, 0, 0):
        from PyQt4.QtCore import QString
        if type(x) == str:
            return x.decode(DEFAULT_ENCODING)
        if type(x) == QString:
            # https://blog.csdn.net/friendan/article/details/51088476
            # https://blog.csdn.net/xxm524/article/details/74937308
            return unicode(x.toUtf8(), DEFAULT_ENCODING, 'ignore')
        return x
    else:
        return x
