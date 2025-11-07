from enum import Enum


class MoveType(Enum):
    """Movement types that can be made in Paradux"""

    SWAP = 0
    """Swaps two adjacent tokens of opposite color"""

    SHIFT = 1
    """Shift two adjacent tokens in a single direction"""
