# encoding: utf-8

from __future__ import print_function
from types import NoneType

__author__ = "Shamim Hasnath"
__copyright__ = "Copyright 2013, Shamim Hasnath"
__license__ = "BSD License"
__version__ = "1.0.1"


TAB_SIZE = 4



def display(o, space, num, key, typ):
    st = ""
    l = []
    if key:
        if typ is dict:
            st += " " * space + "['%s'] => "
        else:
            st += " " * space + "%s => "
        l.append(key)
    elif space > 0:
        st += " " * space + "[%d] => "
        l.append(num)
    else:  # at the very start
        st += "#%d "
        l.append(num)

    if type(o) in (tuple, list, dict, int, str, float, long, bool, NoneType, unicode):
        if type(o) == NoneType:
            st += "%s "
            l.append("None")
        else:
            st += "%s(%s) "
            l.append(type(o).__name__)

            if type(o) in (int, float, long, bool, NoneType):
                l.append(o)
            else:
                l.append(len(o))

            if type(o) in (str, unicode):
                st += '"%s"'
                l.append(o)

    elif isinstance(o, object):
        st += "object(%s) (%d)"
        class_name = o.__class__.__name__
        class_module = o.__class__.__module__
        if class_module != "__builtin__":
            class_name = class_module + "." + class_name
        l.append(class_name)
        l.append(len(getattr(o, '__dict__', {})))

    print(st % tuple(l))


def dump(o, space, num, key, typ, depth=0, max_depth=None):

    if type(o) in (str, int, float, long, bool, NoneType, unicode):
        display(o, space, num, key, typ)

    elif isinstance(o, object):
        display(o, space, num, key, typ)
        num = 0
        if type(o) in (tuple, list, dict):
            typ = type(o)  # type of the container of str, int, long, float etc
        elif isinstance(o, object):
            o = getattr(o, '__dict__', {})
            typ = object
        for i in o:
            space += TAB_SIZE
            if not max_depth or depth < max_depth:
                if type(o) is dict:
                    dump(o[i], space, num, i, typ, depth + 1, max_depth)
                else:
                    dump(i, space, num, '', typ, depth + 1, max_depth)
                num += 1
            space -= TAB_SIZE


def var_dump(*args, **kwargs):
    """
      shows structured information of a object, list, tuple etc
    """
    i = 0
    if not 'max_depth' in kwargs:
        kwargs['max_depth'] = 12
    for x in args:
        dump(x, 0, i, '', object, **kwargs)
        i += 1


def inject():
    import __builtin__
    __builtin__.var_dump = var_dump
