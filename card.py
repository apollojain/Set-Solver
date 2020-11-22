from enum import Enum


class Number(Enum):
    ONE = 1
    TWO = 2
    THREE = 3

    def get_value(self):
        if self == ONE:
            return 1
        elif self == TWO:
            return 2
        elif self == THREE:
            return 3


class Shape(Enum):
    DIAMOND = 1
    SQUIGGLE = 2
    OVAL = 3


class Shading(Enum):
    SOLID = 1
    STRIPED = 2
    OPEN = 3


class Color(Enum):
    RED = 1
    GREEN = 2
    PURPLE = 3


class Card(object):
    def __init__(self, number: Number, shape: Shape, shading: Shading, color: Color):
        self.number = number
        self.shape = shape
        self.shading = shading
        self.color = color

    def __repr__(self):
        return "Card(number={number}, shape={shape}, shading={shading}, color={color})".format(
            number=self.number, shape=self.shape, shading=self.shading, color=self.color
        )

    def __hash__(self):
        return hash((self.number, self.shape, self.shading, self.color))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.number == other.number
                and self.shape == other.shape
                and self.shading == other.shading
                and self.color == other.color
            )
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
