
from mysqlsh.plugin_manager import plugin, plugin_function

from check import trx
from check import queries
from check import locks
from check import schema
from check import other

@plugin
class check:
    """
    Check management and utilities.

    A collection of tools and utilities to perform checks on your
    MySQL Database Server.
    """
