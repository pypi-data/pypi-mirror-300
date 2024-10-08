"""
Cortado package
================

A brief description of the package.
"""

__version__ = '0.1.1'
__author__ = 'Musaddiq K Lodi'
__license__ = 'MIT'

from .data import *
from .marker_genes import *
from .hill_climbing import *
from .evaluate import *
from .utils import *

# Optional: initialization code
def init():
    # Code to be executed when the package is imported
    print("Cortado package initialized!")
    pass

init()