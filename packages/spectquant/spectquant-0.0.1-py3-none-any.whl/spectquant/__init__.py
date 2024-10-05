# spectquant/__init__.py

"""
SpectQuant: \
    A Specialized Package for Extracting Image Features \
    for Cardiac Amyloidosis Quantification on SPECT.
"""

__version__ = "0.0.1"
__author__ = "Markus Köfler"
__all__ = [
    "SUV",
    "TBR",
    "SegmentVolume",
    "UptakeVol",
    "SeptumVol",
    "create_segs"
]

from .create_segs import create_segs
from .suv import SUV
from .tbr import TBR
from .volume import SegmentVolume
from .uptake import UptakeVol
from .septum import SeptumVol
