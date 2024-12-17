from collections import defaultdict
from dataclasses import dataclass
from itertools import groupby
from operator import itemgetter
from pathlib import Path

from icecream import ic

from libaoc import solve
from libaoc.grid import Direction, Grid, Point


def solution1(input_path: Path) -> int:
    garden = parse_input(input_path)
    garden.find_plots()
    return garden.plot_cost


def solution2(input_path: Path) -> int:
    garden = parse_input(input_path)
    ic(garden)
    garden.find_plots()
    return garden.discount_plot_cost


@dataclass
class Plot:
    name: str
    area: int = 0
    perimeter: int = 0
    points: list[Point] = None

    def __post_init__(self):
        self.points = []

    def __repr__(self) -> str:
        return f"Plot(name='{self.name}', area={self.area}, perimeter={self.perimeter}, points={self.points})"


class Garden(Grid):
    CARDINALS = Direction.cardinals()

    def __init__(self, input: str) -> None:
        super().__init__(input)

        self.plots: dict[str, Plot] = {}
        self.plot_idx: dict[str, int] = defaultdict(int)

    @property
    def plot_cost(self) -> int:
        return sum(p.area * p.perimeter for p in self.plots.values())

    @property
    def discount_plot_cost(self) -> int:
        cost = 0

        for plot in self.plots.values():
            sides = 0

            ic(plot)
            rows = defaultdict(
                lambda: {Direction.North: [], Direction.South: [], Direction.East: [], Direction.West: []}
            )
            cols = defaultdict(
                lambda: {Direction.North: [], Direction.South: [], Direction.East: [], Direction.West: []}
            )

            for point in plot.points:
                for dir in self.CARDINALS:
                    adj = point.adjacent(dir)
                    if adj not in self or not self[adj] == self[point]:
                        rows[point.row][dir].append(point)
                        cols[point.col][dir].append(point)

            v_con = []
            h_con = []
            for values in rows.values():
                # Find contiguous paths
                north = [x.col for x in sorted(values[Direction.North])]
                south = [x.col for x in sorted(values[Direction.South])]

                for _cols in [north, south]:
                    for _, g in groupby(enumerate(_cols), lambda ix: ix[0] - ix[1]):
                        thing = list(map(itemgetter(1), g))
                        v_con.append(thing)
                        sides += 1

            for values in cols.values():
                # Find contiguous paths
                east = [x.row for x in sorted(values[Direction.East])]
                west = [x.row for x in sorted(values[Direction.West])]

                for _rows in [east, west]:
                    for _, g in groupby(enumerate(_rows), lambda ix: ix[0] - ix[1]):
                        thing = list(map(itemgetter(1), g))
                        h_con.append(thing)
                        sides += 1
            ic(v_con, h_con)
            cost += plot.area * sides

        return cost

    def get_plot_index(self, name: str) -> str:
        self.plot_idx[name] += 1
        return str(self.plot_idx[name])

    def neighbours(self, point: Point, name: str) -> list[Point]:
        return sorted([p for dir in self.CARDINALS if (p := point.adjacent(dir)) in self and self[p] == name])

    def find_plots(self) -> None:
        # For each point in the garden, find all adjacent points of the same name
        _pm = {p: self.neighbours(p, n) for p, n in self.items}

        # Grab the first item from _pm, and concatenate all touching points to make a plot
        while _pm:
            key = list(_pm.keys())[0]
            name = self[key]
            plot = Plot(name + self.get_plot_index(name))

            visited = {key}
            get = set()
            p = key

            try:
                while z := {x for x, y in _pm.items() if p in y}:
                    get = get | z - visited
                    visited |= z
                    p = get.pop()
            except KeyError as _:
                pass

            for v in visited:
                plot.area += 1
                plot.perimeter += 4 - len(self.neighbours(v, self[v]))
                plot.points.append(v)
                del _pm[v]

            plot.points.sort()
            self.plots[plot.name] = plot


def parse_input(input_path: Path) -> Garden:
    with input_path.open() as f:
        return Garden(f.read())


if __name__ == '__main__':
    answer1 = 1377008
    answer2 = 815788
    solve(solution1, solution2, (answer1, answer2))
