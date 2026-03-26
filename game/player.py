from typing import List, Dict


class Player:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
        self.moves = 0

    def try_move(self, direction: str, maze: List[Dict]) -> bool:
        idx = self.x + self.y * (max(c["x"] for c in maze) + 1)
        cell = maze[idx]
        walls = cell["walls"]
        nx, ny = self.x, self.y
        if direction == "up":
            if walls.get("top"):
                return False
            ny -= 1
        elif direction == "down":
            if walls.get("bottom"):
                return False
            ny += 1
        elif direction == "left":
            if walls.get("left"):
                return False
            nx -= 1
        elif direction == "right":
            if walls.get("right"):
                return False
            nx += 1
        # bounds check
        cols = max(c["x"] for c in maze) + 1
        rows = max(c["y"] for c in maze) + 1
        if nx < 0 or ny < 0 or nx >= cols or ny >= rows:
            return False
        self.x, self.y = nx, ny
        self.moves += 1
        return True
