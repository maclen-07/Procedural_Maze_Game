import random

def add_multiple_paths(grid, rows, cols, extra_paths=20):
    for _ in range(extra_paths):
        x = random.randint(0, cols - 1)
        y = random.randint(0, rows - 1)

        current = grid[x + y * cols]

        directions = []

        if x > 0:
            directions.append(("left", (x - 1, y)))
        if x < cols - 1:
            directions.append(("right", (x + 1, y)))
        if y > 0:
            directions.append(("top", (x, y - 1)))
        if y < rows - 1:
            directions.append(("bottom", (x, y + 1)))

        if not directions:
            continue

        direction, (nx, ny) = random.choice(directions)
        neighbor = grid[nx + ny * cols]

        if direction == "top":
            current.walls["top"] = False
            neighbor.walls["bottom"] = False
        elif direction == "bottom":
            current.walls["bottom"] = False
            neighbor.walls["top"] = False
        elif direction == "left":
            current.walls["left"] = False
            neighbor.walls["right"] = False
        elif direction == "right":
            current.walls["right"] = False
            neighbor.walls["left"] = False