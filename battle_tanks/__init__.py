""" Commons """
import os.path
import sys


def resolve_route(rute,relative = '.'):
    """resolve_route"""
    if hasattr(sys,'_MEIPASS'):
        return os.path.join(sys._MEIPASS,rute)
    return os.path.join(os.path.abspath(relative),rute)


ROUTE = lambda route: os.path.join(os.path.abspath("."), route)
