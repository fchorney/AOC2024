from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum
from typing import Self, TypeVar

T = TypeVar('T', default=str)


class Direction(IntEnum):
    North = 1
    East = 2
    South = 3
    West = 4

    @classmethod
    def cardinals(cls) -> tuple[Self, Self, Self, Self]:
        return (Direction.North, Direction.East, Direction.South, Direction.West)


@dataclass
class Point:
    row: int
    col: int

    @property
    def x(self) -> int:
        return self.col

    @x.setter
    def x(self, value: int) -> None:
        self.col = value

    @property
    def y(self) -> int:
        return self.row

    @y.setter
    def y(self, value: int) -> None:
        self.row = value

    def adjacent(self, dir: Direction) -> Self:
        match dir:
            case Direction.North:
                return Point(self.row - 1, self.col)
            case Direction.East:
                return Point(self.row, self.col + 1)
            case Direction.South:
                return Point(self.row + 1, self.col)
            case Direction.West:
                return Point(self.row, self.col - 1)

    def __sub__(self, other: Self) -> Self:
        return Point(self.row - other.row, self.col - other.col)

    def __add__(self, other: Self) -> Self:
        return Point(self.row + other.row, self.col + other.col)

    def __mul__(self, other: Self | int) -> Self:
        if isinstance(other, int):
            return Point(self.row * other, self.col * other)
        return Point(self.row * other.row, self.col * other.col)

    def __abs__(self) -> Self:
        return Point(abs(self.row), abs(self.col))

    def __eq__(self, other: Self) -> bool:
        return self.row == other.row and self.col == other.col

    def __lt__(self, other: Self) -> bool:
        return self.row < other.row or (self.row == other.row and self.col < other.col)

    def __hash__(self) -> int:
        return hash((self.row, self.col))


# A good chunk of this class was "borrowed" from
# https://github.com/brass75/AdventOfCode/blob/cfac8bd4e69e0b0cf0ab0f4b8fbd5d040f0e53ae/aoc_lib/grid.py
# Thanks Dan!
class Grid[T]:
    def __init__(self, input: str, func: Callable = lambda v: v) -> None:
        self._input = input
        lines = input.splitlines()
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.grid: dict[Point, T] = {
            Point(row, col): func(v) for row, line in enumerate(lines) for col, v in enumerate(line)
        }

    @property
    def values(self):
        return self.grid.values()

    @property
    def items(self):
        return self.grid.items()

    @property
    def coordinates(self):
        return self.grid.keys()

    @property
    def end(self) -> Point:
        return Point(self.rows - 1, self.cols - 1)

    def __hash__(self) -> int:
        return hash(self.grid)

    def __getitem__(self, point: Point) -> T:
        return self.grid[point]

    def __contains__(self, point: Point) -> bool:
        return point in self.grid

    def __repr__(self) -> str:
        return '\n'.join(''.join(str(self[(Point(row, col))]) for col in range(self.cols)) for row in range(self.rows))
