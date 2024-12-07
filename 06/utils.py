from dataclasses import dataclass
from enum import IntEnum

from icecream import ic


@dataclass
class Point:
    row: int
    col: int

    def __hash__(self) -> int:
        return hash((self.row, self.col))


class Direction(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


class Map:
    def __init__(self, data: str) -> None:
        self._guard_chars = ('^', '<', '>', 'v')
        self._obstruction_chars = ('#',)
        self._visit_char = '!'

        self._grid: list[list[str]] = []
        self._original_loc: Point | None = None
        self._parse_map(data)
        self._init()
        
    def _init(self) -> None:
        self._guard_on_map = True
        self._guard_loc: Point | None = self._original_loc
        self._guard_dir: Direction = Direction.N

        self._visited: set[tuple[Point, Direction]] = set()
        self.has_loop = False

    def _parse_map(self, map_data: str) -> None:
        for r_idx, line in enumerate(map_data.splitlines()):
            row = list(line)
            self._grid.append(row)

            for c_idx, item in enumerate(row):
                if item in self._guard_chars:
                    self._original_loc = Point(r_idx, c_idx)


    def _direction_char(self) -> str:
        match self._guard_dir:
            case Direction.N:
                return '^'
            case Direction.E:
                return '>'
            case Direction.S:
                return 'v'
            case Direction.W:
                return '<'

    def _is_on_map(self, point: Point) -> bool:
        return not (point.row < 0 or point.row >= len(self._grid) or point.col < 0 or point.col >= len(self._grid[0]))

    @staticmethod
    def _get_step_point(point: Point, direction: Direction) -> Point:
        match direction:
            case Direction.N:
                return Point(point.row - 1, point.col)
            case Direction.E:
                return Point(point.row, point.col + 1)
            case Direction.S:
                return Point(point.row + 1, point.col)
            case Direction.W:
                return Point(point.row, point.col - 1)

    def __getitem__(self, item: Point) -> str:
        return self._grid[item.row][item.col]

    def __setitem__(self, item: Point, value: str) -> None:
        self._grid[item.row][item.col] = value

    @staticmethod
    def _turn_90(direction: Direction) -> Direction:
        return Direction((direction + 1) % 4)

    def _move(self, next_step: Point, direction: Direction) -> None:
        # Mark that we have visited our current location
        self[self._guard_loc] = self._visit_char
        self._visited.add((self._guard_loc, self._guard_dir))

        # Move to the next location
        self._guard_dir = direction
        self._guard_loc = next_step

        # If the next location is on the map, move our guard marker there
        if on_map := self._is_on_map(next_step):
            self[self._guard_loc] = self._direction_char()

        # Keep track of being on the map
        self._guard_on_map = on_map

    def _is_obstructed(self, next_step: Point, obstacle: Point | None) -> bool:
        # If the next step is on the map, check if we're obstructed
        return self._is_on_map(next_step) and self[next_step] in self._obstruction_chars or next_step == obstacle

    def _find_next_step(self, point: Point, direction: Direction, obstacle: Point | None) -> tuple[Point, Direction]:
        # Get our next step
        next_step = self._get_step_point(point, direction)
        curr_direction = direction

        # Keep checking our next step until it is unobstructed
        while self._is_obstructed(next_step, obstacle):
            curr_direction = self._turn_90(curr_direction)
            next_step = self._get_step_point(point, curr_direction)

        return next_step, curr_direction

    def _step(self, obstacle: Point | None) -> None:
        # Show the current location
        # ic('Guard')
        # self.show_grid(self._guard_loc)

        # Get our next step
        next_step, next_direction = self._find_next_step(self._guard_loc, self._guard_dir, obstacle)

        if (next_step, next_direction) in self._visited:
            self.has_loop = True
            return

        # Move to the next step
        self._move(next_step, next_direction)
            

    def get_path(self, obstacle: Point | None = None) -> set[Point]:
        self._init()
        
        path: set[Point] = set()
        while self._guard_on_map and not self.has_loop:
            path.add(self._guard_loc)
            self._step(obstacle)
            
        return path

    def display(self) -> None:
        ic(self._guard_dir, self._guard_loc, len(self._visited))
        ic(self._grid)

    def show_grid(self, point: Point, square_size: int = 2) -> None:
        left = point.col - square_size
        top = point.row - square_size
        right = point.col + square_size
        bottom = point.row + square_size

        rows = len(self._grid)
        cols = len(self._grid[0])

        if left < 0:
            right += abs(left)
            left = 0
        if top < 0:
            bottom += abs(top)
            top = 0
        if right >= cols:
            left -= right - (cols - 1)
            right = cols - 1
        if bottom >= rows:
            top -= bottom - (rows - 1)
            bottom = rows - 1

        # Grab sub grid
        orig_char = self._grid[point.row][point.col]
        self._grid[point.row][point.col] = '@'

        subgrid: list[list[str]] = []
        for row in range(top, bottom + 1):
            subgrid.append(self._grid[row][left : right + 1])

        ic(subgrid)

        self._grid[point.row][point.col] = orig_char
