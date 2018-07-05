#!/usr/bin/env python
"""functions around regex Expression which are used in multiple files"""

import os,re


def reglob(path, exp, invert=False):
    """
    glob.glob() style searching which uses regex

    Parameters
    ----------
    path : str
        path to search in
    exp : str
        Regex expression for filename
    invert: bool
        Invert match to non matching files (Default is `True`)

    Returns
    -------

    """

    m = re.compile(exp)

    if invert is False:
        res = [f for f in os.listdir(path) if m.search(f)]
    else:
        res = [f for f in os.listdir(path) if not m.search(f)]

    res = map(lambda x: "%s/%s" % ( path, x, ), res)
    return res