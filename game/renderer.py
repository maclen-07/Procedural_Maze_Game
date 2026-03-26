import pygame
from typing import List, Dict, Tuple


def infer_size(maze_data: List[Dict]) -> Tuple[int, int]:
    cols = max(cell["x"] for cell in maze_data) + 1
    rows = max(cell["y"] for cell in maze_data) + 1
    return cols, rows


def draw_maze(surface: pygame.Surface, maze_data: List[Dict]):
    cols, rows = infer_size(maze_data)
    sw, sh = surface.get_size()
    # compute tile size to fit
    tile = max(1, min(sw // cols, sh // rows))
    maze_w = tile * cols
    maze_h = tile * rows
    x_off = (sw - maze_w) // 2
    y_off = (sh - maze_h) // 2

    bg_color = (255, 255, 255)
    line_color = (0, 0, 0)

    # fill maze background
    pygame.draw.rect(surface, bg_color, (x_off, y_off, maze_w, maze_h))

    # debug: optionally fill cells lightly to check alignment
    cell_fill = (245, 245, 245)
    for cell in maze_data:
        x = cell["x"]
        y = cell["y"]
        px = x_off + x * tile
        py = y_off + y * tile
        pygame.draw.rect(surface, cell_fill, (px + 1, py + 1, tile - 2, tile - 2))

    # draw walls
    for cell in maze_data:
        x = cell["x"]
        y = cell["y"]
        walls = cell["walls"]
        px = x_off + x * tile
        py = y_off + y * tile
        if walls.get("top", True):
            pygame.draw.line(surface, line_color, (px, py), (px + tile, py), 2)
        if walls.get("right", True):
            pygame.draw.line(surface, line_color, (px + tile, py), (px + tile, py + tile), 2)
        if walls.get("bottom", True):
            pygame.draw.line(surface, line_color, (px + tile, py + tile), (px, py + tile), 2)
        if walls.get("left", True):
            pygame.draw.line(surface, line_color, (px, py + tile), (px, py), 2)

    # outer border (ensure clean edges)
    pygame.draw.rect(surface, line_color, (x_off, y_off, maze_w, maze_h), 2)


def cell_to_pixels(surface: pygame.Surface, maze_data: List[Dict], cx: int, cy: int):
    cols, rows = infer_size(maze_data)
    sw, sh = surface.get_size()
    tile = max(1, min(sw // cols, sh // rows))
    maze_w = tile * cols
    maze_h = tile * rows
    x_off = (sw - maze_w) // 2
    y_off = (sh - maze_h) // 2
    px = x_off + cx * tile
    py = y_off + cy * tile
    return px, py, tile, tile
