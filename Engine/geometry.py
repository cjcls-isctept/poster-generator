"""
engine.geometry
===============

Geometria utilizada pelo motor de composição.

Todo o projeto deve utilizar Rect em vez de tuplas
(x0, y0, x1, y1).

Autor: Cláudio Lopes + ChatGPT
"""

from __future__ import annotations

from dataclasses import dataclass


# ----------------------------------------------------------------------
# Point
# ----------------------------------------------------------------------

@dataclass(slots=True)
class Point:
    x: int
    y: int

    def move(self, dx: int, dy: int) -> "Point":
        return Point(self.x + dx, self.y + dy)


# ----------------------------------------------------------------------
# Size
# ----------------------------------------------------------------------

@dataclass(slots=True)
class Size:
    width: int
    height: int


# ----------------------------------------------------------------------
# Rect
# ----------------------------------------------------------------------

@dataclass(slots=True)
class Rect:
    """
    Retângulo definido por:

        left
        top
        right
        bottom
    """

    left: int
    top: int
    right: int
    bottom: int

    # --------------------------------------------------------------

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top

    @property
    def size(self) -> Size:
        return Size(self.width, self.height)

    # --------------------------------------------------------------

    @property
    def center_x(self) -> int:
        return self.left + self.width // 2

    @property
    def center_y(self) -> int:
        return self.top + self.height // 2

    @property
    def center(self) -> Point:
        return Point(
            self.center_x,
            self.center_y,
        )

    # --------------------------------------------------------------

    @property
    def top_left(self) -> Point:
        return Point(self.left, self.top)

    @property
    def top_right(self) -> Point:
        return Point(self.right, self.top)

    @property
    def bottom_left(self) -> Point:
        return Point(self.left, self.bottom)

    @property
    def bottom_right(self) -> Point:
        return Point(self.right, self.bottom)

    # --------------------------------------------------------------

    @property
    def aspect_ratio(self) -> float:
        if self.height == 0:
            return 0.0

        return self.width / self.height

    # --------------------------------------------------------------

    def as_tuple(self) -> tuple[int, int, int, int]:
        return (
            self.left,
            self.top,
            self.right,
            self.bottom,
        )

    # --------------------------------------------------------------

    def move(self, dx: int, dy: int) -> "Rect":

        return Rect(
            self.left + dx,
            self.top + dy,
            self.right + dx,
            self.bottom + dy,
        )

    # --------------------------------------------------------------

    def inflate(self, value: int) -> "Rect":
        """
        Aumenta o retângulo.
        """

        return Rect(
            self.left - value,
            self.top - value,
            self.right + value,
            self.bottom + value,
        )

    # --------------------------------------------------------------

    def deflate(self, value: int) -> "Rect":
        """
        Diminui o retângulo.
        """

        return Rect(
            self.left + value,
            self.top + value,
            self.right - value,
            self.bottom - value,
        )

    # --------------------------------------------------------------

    def padding(
        self,
        left: int = 0,
        top: int = 0,
        right: int = 0,
        bottom: int = 0,
    ) -> "Rect":

        return Rect(
            self.left + left,
            self.top + top,
            self.right - right,
            self.bottom - bottom,
        )

    # --------------------------------------------------------------

    def contains(self, point: Point) -> bool:

        return (
            self.left <= point.x <= self.right
            and
            self.top <= point.y <= self.bottom
        )

    # --------------------------------------------------------------

    def intersects(self, other: "Rect") -> bool:

        return not (

            self.right < other.left

            or

            self.left > other.right

            or

            self.bottom < other.top

            or

            self.top > other.bottom

        )

    # --------------------------------------------------------------

    @classmethod
    def from_xywh(
        cls,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> "Rect":

        return cls(
            x,
            y,
            x + width,
            y + height,
        )

    # --------------------------------------------------------------

    @classmethod
    def from_center(
        cls,
        center_x: int,
        center_y: int,
        width: int,
        height: int,
    ) -> "Rect":

        half_w = width // 2
        half_h = height // 2

        return cls(

            center_x - half_w,

            center_y - half_h,

            center_x + half_w,

            center_y + half_h,

        )

    # --------------------------------------------------------------

    def __iter__(self):

        yield self.left
        yield self.top
        yield self.right
        yield self.bottom

    # --------------------------------------------------------------

    def __repr__(self):

        return (
            f"Rect("
            f"{self.left}, "
            f"{self.top}, "
            f"{self.right}, "
            f"{self.bottom})"
        )