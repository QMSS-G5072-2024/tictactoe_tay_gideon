# read version from installed package
from importlib.metadata import version
__version__ = version("tictactoe_gt2528")

# import all functions
from .tictactoe_gt2528 import *