"""MCNParse

Package for parsing MCNP output files and saving data to JSON format.

Data can be either compressed or uncompressed. Currently unable to parse tallies
that have more than one bin technique (or tallies that contain multiple
surfaces, cells, or detector points) or tallies which are unbinned.

"""

from .core import mcnparse, find_regions
from .utils.deserialization import deserialize

__all__ = ["mcnparse", "find_regions", "deserialize"]
