"""Enums and the Tile class."""

from __future__ import annotations
from enum import Enum, IntEnum
from typing import Union

__all__ = [
    "ORDER",
    "BonusTile",
    "Bonuses",
    "Dragon",
    "Flower",
    "Honors",
    "Misc",
    "Number",
    "Season",
    "Simples",
    "Suit",
    "Tile",
    "Wind",
]


class Suit(Enum):
    """Base enum class for suits."""

    pass


class Simples(Suit):
    """Enum for simples suits (numbered from 1-9)"""

    ZHU = "zhu"
    TONG = "tong"
    WAN = "wan"


class Honors(Suit):
    """Enum for honors suits (tiles that cannot Chow)"""

    FENG = "feng"  # value is instance of Wind
    LONG = "long"  # value is instance of Dragon


class Bonuses(Suit):
    """Enum for bonus suits (tiles that only count when you win)"""

    HUA = "hua"
    GUI = "gui"


class Misc(Suit):
    """Enum for special case suits"""

    UNKNOWN = "?"
    HIDDEN = "k"
    MISSING = " "


class Wind(IntEnum):
    """Represents a wind direction"""

    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3


class Dragon(IntEnum):
    """Represents a dragon"""

    RED = 0  # hong zhong
    GREEN = 1  # fa cai
    WHITE = 2  # bai ban


class Flower(IntEnum):
    """Represents a Flowers tile"""

    MEI = Wind.EAST.value
    LAN = Wind.SOUTH.value
    JU = Wind.WEST.value
    ZHU = Wind.NORTH.value


class Season(IntEnum):
    """Represents a Seasons tile"""

    SPRING = Wind.EAST.value
    SUMMER = Wind.SOUTH.value
    AUTUMN = Wind.WEST.value
    WINTER = Wind.NORTH.value


ORDER = {"wan": 0, "tong": 1, "zhu": 2, "feng": 3, "long": 4}

Number = Union[int, Wind, Dragon]


class Tile:
    """Data class for tiles."""

    suit: Suit
    number: Number

    def __init__(self, suit: Suit, number: Number):
        """Initialize Tile."""
        self.suit = suit
        self.number = number
        if self.suit in Simples:
            self.number = int(number)
        elif self.suit == Honors.FENG:
            self.number = Wind(number)
        elif self.suit == Honors.LONG:
            self.number = Dragon(number)
        elif self.suit in Bonuses:
            raise ValueError("Please use the BonusTile class for bonus tiles.")
        else:
            raise ValueError(f"Invalid suit: {self.suit!r}")

    @classmethod
    def from_str(cls, s: str) -> Tile:
        """Create a Tile object from a string representation.

        Args:
            s (str): The string representation of the tile in the format "suit/number".

        Returns:
            Tile: The created Tile object.

        Raises:
            ValueError: If the suit is invalid or the number is not in the range [1, 9].
        """
        suit_s, number_s = s.split("/")
        suit: Suit = Misc.UNKNOWN
        for num in (Simples, Honors, Bonuses, Misc):
            try:
                suit = num(suit_s)
            except ValueError:
                continue
            else:
                break
        else:
            raise ValueError("Invalid suit")
        number: int = int(number_s) - 1
        if not (0 <= number < 9):
            raise ValueError(f"Number {number_s} not in range [1, 9]")
        if suit == Honors.FENG:
            number = Wind(number)
        if suit == Honors.LONG:
            number = Dragon(number)
        return cls(suit, number)

    def __str__(self) -> str:
        """str(tile) -> 'suit/number'"""
        return f"{self.suit.value}/{self.number}"

    __repr__ = __str__

    def __hash__(self):
        """Calculate the hash value of the tile.

        Returns:
            int: The hash value of the tile.
        """
        return hash((self.suit, self.number))

    def __eq__(self, other: Tile) -> bool:
        """Tiles are equal when their suits and numbers are equal.

        Args:
            other (Tile): The other tile to compare with.

        Returns:
            bool: True if the tiles are equal, False otherwise.
        """
        if not (isinstance(other, type(self)) or isinstance(self, type(other))):
            return NotImplemented
        return hash(self) == hash(other)

    def __lt__(self, other: Tile) -> bool:
        """Compare two Tile objects based on their suit and number.

        Args:
            other (Tile): The other Tile object to compare with.

        Returns:
            bool: True if self is less than other, False otherwise.
        """
        if not (isinstance(other, type(self)) or isinstance(self, type(other))):
            return NotImplemented
        if self.suit == other.suit:
            return self.number < other.number
        if self.suit.value not in ORDER or other.suit.value not in ORDER:
            return False
        return ORDER[self.suit.value] < ORDER[other.suit.value]


class BonusTile(Tile):
    suit: Bonuses
    number: Union[int, Flower, Season]

    def __init__(self, suit: Bonuses, number: Union[int, Flower, Season]):
        """Initialize Tile."""
        self.suit = suit
        if self.suit == Bonuses.HUA:
            self.number = Flower(number)
        elif self.suit == Bonuses.GUI:
            self.number = Season(number)
        else:
            raise ValueError(f"Invalid BonusTile suit: {self.suit!r}")
