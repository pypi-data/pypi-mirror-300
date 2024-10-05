from collections import abc
from itertools import repeat
from numbers import Number
from typing import List
import numpy as np


def _ntuple(n):
    """From PyTorch internals."""

    def parse(x):
        """Parse bounding boxes format between XYWH and LTWH."""
        return x if isinstance(x, abc.Iterable) else tuple(repeat(x, n))

    return parse


to_2tuple = _ntuple(2)