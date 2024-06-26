"""This module is a continuation of the BPNeurode module."""

from FFNeurode import FFNeurode
from BPNeurode import BPNeurode


class FFBPNeurode(BPNeurode, FFNeurode):
    """Implement the FFBPNeurode class."""
    # code below is optional
    def __init__(self):
        super().__init__()

    # this is optional as well
    # pass