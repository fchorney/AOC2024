from collections import defaultdict
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Self

from icecream import ic

from libaoc import solve
from libaoc.grid import Direction, Grid, Point


def solution1(input_path: Path) -> int:
    trail = parse_input(input_path)
    ic(trail.heads)
    return trail.find_hike_score()


def solution2(input_path: Path) -> int:
    trail = parse_input(input_path)
    ic(trail.heads)
    return trail.find_hike_score(unique=True)


@dataclass
class Hike:
    _hid: ClassVar[int] = 0

    start: Point
    curr: Point = None
    path: list[Point] = None

    def __post_init__(self):
        if self.curr is None:
            self.curr = self.start

        if self.path is None:
            self.path = []
        self.path.append(self.curr)

        self.hid = Hike._hid
        Hike._hid += 1

    def __eq__(self, other: Self) -> bool:
        return self.start == other.start and self.curr == other.curr and self.path == other.path

    def __repr__(self) -> str:
        return f'Hike(hid={self.hid}, start={self.start}, curr={self.curr}, path={self.path})'


class Trail[T](Grid[T]):
    def __init__(self, input: str, func: Callable = lambda v: int(v)) -> None:
        super().__init__(input, func)

        self.heads: list[Point] = [k for k, v in self.items if v == 0]

        self.cardinals: tuple[Direction, Direction, Direction, Direction] = (
            Direction.North,
            Direction.East,
            Direction.South,
            Direction.West,
        )

    def find_hike_score(self, unique=False) -> int:
        hikes: list[Hike] = [Hike(head) for head in self.heads]
        intersects: set[tuple[Point, Point]] = set()
        unique_hikes: dict[Point, set[tuple[Point, ...]]] = defaultdict(set)

        # Grab the first hike while hikes exist
        while hikes and (hike := hikes.pop()):
            if self[hike.curr] == 9:
                intersects.add((hike.start, hike.curr))
                unique_hikes[hike.start].add(tuple(hike.path))
                continue

            first_adjacent = True
            hike_copy = deepcopy(hike)
            next_points = [_next for dir in self.cardinals if (_next := hike.curr.adjacent(dir)) in self]
            for next in (_next for _next in next_points if _next not in hike.path):
                if self[next] == self[hike_copy.curr] + 1:
                    new_hike = hike

                    if first_adjacent:
                        hike.curr = next
                        hike.path.append(hike.curr)
                        first_adjacent = False
                    else:
                        new_hike = Hike(hike_copy.start, curr=next, path=deepcopy(hike_copy.path))

                    # Check if we already have this path
                    if new_hike not in hikes:
                        hikes.insert(0, new_hike)
                    continue

        score: dict[Point, int] = defaultdict(int)
        for a, _ in intersects:
            score[a] += 1

        if unique:
            return sum(len(x) for x in unique_hikes.values())
        return sum(score.values())


def parse_input(input_path: Path) -> Trail:
    with input_path.open() as f:
        return Trail[int](f.read())


if __name__ == '__main__':
    answer1 = 798
    answer2 = 1816
    solve(solution1, solution2, (answer1, answer2))
