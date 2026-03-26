import os
import json
import random
from typing import List, Dict

from multi_path import add_multiple_paths

class Cell:
    """Grid cell for maze generation. No rendering responsibilities."""

    def __init__(self, x: int, y: int, cols: int, rows: int):
        self.x = x
        self.y = y
        self.cols = cols
        self.rows = rows
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

    def _index(self, x: int, y: int):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return x + y * self.cols
        return None

    def unvisited_neighbors(self, grid: List["Cell"]) -> List["Cell"]:
        neighbors = []
        coords = [("left", (self.x - 1, self.y)), ("right", (self.x + 1, self.y)),
                  ("top", (self.x, self.y - 1)), ("bottom", (self.x, self.y + 1))]
        for _name, (nx, ny) in coords:
            idx = self._index(nx, ny)
            if idx is not None:
                nbr = grid[idx]
                if not nbr.visited:
                    neighbors.append(nbr)
        return neighbors


def _remove_walls(a: Cell, b: Cell) -> None:
    dx = a.x - b.x
    dy = a.y - b.y
    if dx == 1:  # b is left of a
        a.walls["left"] = False
        b.walls["right"] = False
    elif dx == -1:  # b is right of a
        a.walls["right"] = False
        b.walls["left"] = False
    if dy == 1:  # b is above a
        a.walls["top"] = False
        b.walls["bottom"] = False
    elif dy == -1:  # b is below a
        a.walls["bottom"] = False
        b.walls["top"] = False


def generate_maze(cols: int, rows: int) -> List[Dict]:
    """Generate a maze using DFS (stack-based backtracking).

    Returns a list of cell dictionaries with x, y and walls.
    """
    grid: List[Cell] = [Cell(x, y, cols, rows) for y in range(rows) for x in range(cols)]

    stack: List[Cell] = []
    current = grid[0]
    current.visited = True

    while True:
        neighbors = current.unvisited_neighbors(grid)
        if neighbors:
            chosen = random.choice(neighbors)
            chosen.visited = True
            stack.append(current)
            _remove_walls(current, chosen)
            current = chosen
        elif stack:
            current = stack.pop()
        else:
            break

    add_multiple_paths(grid, rows, cols, extra_paths=30)
      
    # Convert to serializable data
    maze_data: List[Dict] = []
    for cell in grid:
        maze_data.append({
            "x": cell.x,
            "y": cell.y,
            "walls": {
                "top": bool(cell.walls["top"]),
                "right": bool(cell.walls["right"]),
                "bottom": bool(cell.walls["bottom"]),
                "left": bool(cell.walls["left"]),
            },
        })
    return maze_data


def save_maze(filename: str, data: List[Dict]) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_maze(filename: str) -> List[Dict]:
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_levels() -> Dict[str, List[Dict]]:
    """Generate or load five difficulty level mazes and return them.

    Files are stored under a `mazes` directory next to this module.
    """
    base_dir = os.path.join(os.path.dirname(__file__), "mazes")
    os.makedirs(base_dir, exist_ok=True)

    levels = {
        "easy": (10, "maze_easy.json"),
        "normal": (15, "maze_normal.json"),
        "intermediate": (20, "maze_intermediate.json"),
        "medium": (25, "maze_medium.json"),
        "hard": (30, "maze_hard.json"),
    }

    result: Dict[str, List[Dict]] = {}
    for name, (size, filename) in levels.items():
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            data = load_maze(path)
        else:
            data = generate_maze(size, size)
            save_maze(path, data)
        result[name] = data

    return result


if __name__ == "__main__":
    levels = generate_levels()
    for k, maze in levels.items():
        print(f"Level {k}: {len(maze)} cells")
