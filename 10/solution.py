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
    ic(trail.heads, trail.tails)

    trail.find_hikes()

    return -1


def solution2(input_path: Path) -> int:
    data = parse_input(input_path)
    ic(data)
    return -1

@dataclass
class Hike:
    _hid: ClassVar[int] = 0

    start: Point
    curr: Point = None
    path: list[Point] = None
    is_head: bool = True

    def __post_init__(self):
        if self.curr is None:
            self.curr = self.start

        if self.path is None:
            self.path = []
        self.path.append(self.curr)

        self.hid = Hike._hid
        Hike._hid += 1

    def __eq__(self, other: Self) -> bool:
        return self.start == other.start and self.curr == other.curr and self.is_head == other.is_head and self.path == other.path

    def __repr__(self) -> str:
        return f"Hike(hid={self.hid}, is_head={self.is_head}, start={self.start}, curr={self.curr}, path={self.path})"

class Trail[T](Grid[T]):
    def __init__(self, input: str, func: Callable = lambda v: int(v)) -> None:
        super().__init__(input, func)

        self.heads: list[Point] = [k for k, v in self.items if v == 0]
        self.tails: list[Point] = [k for k, v in self.items if v == 9]

        self.cardinals: tuple[Direction, Direction, Direction, Direction] = (
            Direction.North, Direction.East, Direction.South, Direction.West
        )

    def find_hikes(self) -> None:
        hikes: list[Hike] = []
        hikes.extend(Hike(tail, is_head=False) for tail in self.tails)
        hikes.extend(Hike(head) for head in self.heads)

        ic(hikes)

        done_h: list[Hike] = []
        done_t: list[Hike] = []

        intersects: set[tuple[Point, Point]] = set()

        # Grab the first hike while hikes exist
        while hikes and (hike := hikes.pop()):
            if hike.is_head and self[hike.curr] == 9:
                done_h.append(hike)
                continue

            if not hike.is_head and self[hike.curr] == 0:
                done_t.append(hike)
                continue

            first_adjacent = True
            hike_copy = deepcopy(hike)
            next_points = [_next for dir in self.cardinals if (_next :=  hike.curr.adjacent(dir)) in self]
            for next in (_next for _next in next_points if _next not in hike.path):
                if hike_copy.is_head and self[next] == self[hike_copy.curr] + 1:
                        # Gradual uphill
                        new_hike = hike

                        if first_adjacent:
                            hike.curr = next
                            hike.path.append(hike.curr)
                            first_adjacent = False
                        else:
                            new_hike = Hike(hike_copy.start, curr=next, path=deepcopy(hike_copy.path))

                        # Check if we already have this path
                        if new_hike not in hikes:
                            # Check if this path intersects any other paths
                            for idx in range(len(hikes)):
                                tail = hikes[idx]
                                if tail.is_head:
                                    continue
                                if self[tail.curr] == self[new_hike.curr] + 1:
                                    diff = abs(tail.curr - new_hike.curr)
                                    if (diff.row == 1 and diff.col == 0) or (diff.row == 0 and diff.col == 1):
                                        # These 2 hikes intersect
                                        intersects.add((new_hike.start, tail.start))
                                        del hikes[idx]
                                        break
                            else:
                                hikes.insert(0, new_hike)
                        continue

                if not hike_copy.is_head and self[next] == self[hike_copy.curr] - 1:
                    # Gradual downhill
                    new_hike = hike

                    if first_adjacent:
                        hike.curr = next
                        hike.path.append(hike.curr)
                        first_adjacent = False
                    else:
                        new_hike = Hike(hike_copy.start, is_head=False, curr=next, path=deepcopy(hike_copy.path))

                    # Check if we already have this path
                    if new_hike not in hikes:
                        # Check if this path intersects any other paths
                        for idx in range(len(hikes)):
                            head = hikes[idx]
                            if not head.is_head:
                                continue
                            if self[head.curr] == self[new_hike.curr] - 1:
                                diff = abs(head.curr - new_hike.curr)
                                if (diff.row == 1 and diff.col == 0) or (diff.row == 0 and diff.col == 1):
                                    # These 2 hikes intersect
                                    intersects.add((head.start, new_hike.start))
                                    del hikes[idx]
                                    break
                        else:
                            hikes.insert(0, new_hike)
                    continue

        for hike in sorted(done_h, key=lambda hike: hike.hid):
            ic(hike.is_head)
            ic(hike.hid, len(hike.path), hike.path)

        for hike in sorted(done_t, key=lambda hike: hike.hid):
            ic(hike.is_head)
            ic(hike.hid, len(hike.path), hike.path)

        ic(intersects)


def parse_input(input_path: Path) -> Trail:
    with input_path.open() as f:
        return Trail[int](f.read())


if __name__ == '__main__':
    answer1 = -999
    answer2 = -999
    solve(solution1, solution2, (answer1, answer2))
