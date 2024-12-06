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
    def __init__(self):
        self._guard_chars = ('^', '<', '>', 'v')
        self._obstruction_chars = ("#",)
        self._visit_char = "!"
        
        self._grid: list[list[str]] = []
        
        self._guard_loc: Point | None = None
        self._guard_dir: Direction | None = None
        
        self.guard_on_map = True
        self._visited: set[Point] = set()
        self._obstacles: set[Point] = set()
    
    @property
    def visited(self) -> int:
        return len(self._visited)
    
    @property
    def obstacles(self) -> int:
        return len(self._obstacles)
    
    def parse_map(self, map_data: str) -> None:
        for r_idx, line in enumerate(map_data.splitlines()):
            row = list(line)
            self._grid.append(row)
            
            for c_idx, item in enumerate(row):
                if item in self._guard_chars:
                    self._guard_loc = Point(r_idx, c_idx)
            
        self._find_direction()
        
    def _find_direction(self) -> None:
        match self[self._guard_loc]:
            case '^':
                self._guard_dir = Direction.N
            case '>':
                self._guard_dir = Direction.E
            case 'v':
                self._guard_dir = Direction.S
            case '<':
                self._guard_dir = Direction.W

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
    
    def _get_step_point(self, point: Point, direction: Direction) -> Point:
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
            
    
    def _turn_90(self, direction: Direction) -> Direction:
        return Direction((direction + 1) % 4)
    
    def _move(self, next: Point, direction: Direction) -> None:
        # Mark that we have visited our current location
        self[self._guard_loc] = self._visit_char
        self._visited.add(self._guard_loc)
        
        # Move to the next location
        self._guard_dir = direction
        self._guard_loc = next
        
        # If the next location is on the map, move our guard marker there
        if on_map := self._is_on_map(next):
            self[self._guard_loc] = self._direction_char()
            
        # Keep track of being on the map
        self.guard_on_map = on_map
        
    def _is_obstructed(self, next: Point) -> bool:
        # If the next step is on the map, check if we're obstructed
        return self._is_on_map(next) and self[next] in self._obstruction_chars
    
    def _find_next_step(self, point: Point, direction: Direction) -> tuple[Point, Direction]:
        # Get our next step
        next_step = self._get_step_point(point, direction)
        curr_direction = direction

        # Keep checking our next step until it is unobstructed
        while self._is_obstructed(next_step):
            curr_direction = self._turn_90(curr_direction)
            next_step = self._get_step_point(point, curr_direction)
            
        return next_step, curr_direction
    
    def _find_loop_obstacles(self) -> None:
        # If we're already right in front of an obstacle, we don't need to check this
        next_guard_step = self._get_step_point(self._guard_loc, self._guard_dir)
        if self._is_obstructed(next_guard_step) or not self._is_on_map(next_guard_step):
            return

        # Cast out a ray to your right, and see if we hit an obstacle we've previously hit
        ray_dir = self._turn_90(self._guard_dir)
        curr_step = self._guard_loc

        # Walk the path until we hit an obstacle
        next_step = self._get_step_point(curr_step, ray_dir)
        
        # The case where your immediate right is an obstacle, we still want to check what would happen
        # if we got turned around
        if self._is_obstructed(next_step):
            ray_dir = self._turn_90(ray_dir)
            next_step = self._get_step_point(curr_step, ray_dir)
        
        while True:
            if not self._is_on_map(next_step):
                # We've walked off the map, no loops here
                return
            elif self._is_obstructed(next_step):
                if curr_step not in self._visited:
                    return
                break
            curr_step = next_step
            next_step = self._get_step_point(curr_step, ray_dir)

        # We've potentially found a loop, and the next step isn't already an obstacle
        self._obstacles.add(next_guard_step)
    
    def step(self, find_loop_obstacles: bool = False) -> None:
        # TODO: Find Loop Obstacles
        # For each step, if you were to turn right and follow the path...
        # If you hit an obstacle you've already hit before then it's a loop
        # else it's not a loop
        
        if find_loop_obstacles:
            self._find_loop_obstacles()       
        
        # Get our next step
        next_step, next_direction = self._find_next_step(self._guard_loc, self._guard_dir)

        # Move to the next step
        self._move(next_step, next_direction)

    def display(self) -> None:
        ic(self._guard_dir, self._guard_loc, len(self._visited))
        ic(self._grid)
