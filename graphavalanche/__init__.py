"""
GRAPHAVALANCHE - Citation Network Visualization Tool

A powerful Python tool for building and visualizing citation networks 
from academic paper metadata using OpenAlex API integration.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .network import CitationNetwork
from .loader import MetadataLoader

__all__ = ["CitationNetwork", "MetadataLoader", "__version__"]
