import itertools
from collections import defaultdict
from pathlib import Path

from icecream import ic

from libaoc import solve
from libaoc.grid import Grid, Point


def solution1(input_path: Path) -> int:
    grid = parse_input(input_path)
    return grid.find_antinodes()


def solution2(input_path: Path) -> int:
    grid = parse_input(input_path)
    return grid.find_antinodes(echo=True)


class RadioGrid[T](Grid[T]):
    def __init__(self, input: str) -> None:
        super().__init__(input)

        self.antennas: dict[str, list[Point]] = defaultdict(list)
        self.antinodes: set[Point] = set()
        self._find_antennas()

    def find_antinodes(self, echo: bool = False) -> int:
        for coords in self.antennas.values():
            for a, b in itertools.combinations(coords, 2):
                diff = a - b

                if not echo:
                    for new_coord in (a + diff, b - diff):
                        if new_coord in self:
                            self.antinodes.add(new_coord)
                else:
                    # Add both nodes to the anti-nodes
                    self.antinodes.add(a)
                    self.antinodes.add(b)

                    new_coord = a
                    while (new_coord := new_coord + diff) in self:
                        self.antinodes.add(new_coord)

                    new_coord = b
                    while (new_coord := new_coord - diff) in self:
                        self.antinodes.add(new_coord)

        return len(self.antinodes)

    def _find_antennas(self) -> None:
        for k, v in self.items:
            # Ignore blank spaces
            if v == '.':
                continue
            ic(k, v)
            self.antennas[v].append(k)


def parse_input(input_path: Path) -> RadioGrid:
    with input_path.open() as f:
        return RadioGrid[str](f.read())


if __name__ == '__main__':
    answer1 = 398
    answer2 = 1333
    solve(solution1, solution2, (answer1, answer2))
