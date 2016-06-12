"""
# HACK: Workaround MySQLdb import error
# http://stackoverflow.com/questions/30893734/no-module-named-mysql-google-app-engine-django
"""

import pkg_resources
import imp


def __bootstrap__():
    global __bootstrap__, __loader__, __file__
    __file__ = pkg_resources.resource_filename(__name__, '/lib/_mysql.so')
    # __loader__ = None; del __bootstrap__, __loader__
    imp.load_dynamic(__name__, __file__)

__bootstrap__()
