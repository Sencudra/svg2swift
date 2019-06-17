"""
Point class implementation.

Coordinate system enum implementation.
"""

from enum import Enum


class CoordinateSystem(Enum):
    """Coordinate system's type enum"""

    RELATIVE = 1
    ABSOLUTE = 2


class Point:
    """Point on a coordinate plane with x and y values"""

    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        else:
            raise TypeError

    def __rsub__(self, other):
        if isinstance(other, Point):
            return Point(other.x - self.x, other.y - self.y)
        else:
            raise TypeError

    def __mul__(self, other):
        if not isinstance(other, Point):
            return Point(self.x * other, self.y * other)
        else:
            raise TypeError

    def __rmul__(self, other):
        return self.__mul__(other)
