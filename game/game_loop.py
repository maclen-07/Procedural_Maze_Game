import pygame
from typing import List, Dict
from .renderer import draw_maze, cell_to_pixels, infer_size
from .player import Player
from .highscore import add_score


def run(screen: pygame.Surface, maze_data: List[Dict], level_name: str) -> None:
    clock = pygame.time.Clock()
    player = Player(0, 0)
    cols, rows = infer_size(maze_data)
    running = True
    font = pygame.font.SysFont(None, 28)

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_ESCAPE,):
                    return
                moved = False
                if ev.key in (pygame.K_UP, pygame.K_w):
                    moved = player.try_move("up", maze_data)
                elif ev.key in (pygame.K_DOWN, pygame.K_s):
                    moved = player.try_move("down", maze_data)
                elif ev.key in (pygame.K_LEFT, pygame.K_a):
                    moved = player.try_move("left", maze_data)
                elif ev.key in (pygame.K_RIGHT, pygame.K_d):
                    moved = player.try_move("right", maze_data)
                # check win
                if player.x == cols - 1 and player.y == rows - 1:
                    # show level complete and prompt for name
                    name = _prompt_name(screen, player.moves)
                    if name:
                        add_score(name, player.moves, level_name)
                    return

        screen.fill((180, 180, 180))
        draw_maze(screen, maze_data)

        px, py, cw, ch = cell_to_pixels(screen, maze_data, player.x, player.y)
        # draw player as circle
        cx = px + cw // 2
        cy = py + ch // 2
        pygame.draw.circle(screen, (0, 100, 255), (cx, cy), min(cw, ch) // 3)

        moves_text = font.render(f"Moves: {player.moves}", True, (0, 0, 0))
        screen.blit(moves_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)


def _prompt_name(screen: pygame.Surface, moves: int) -> str:
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    input_text = ""
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return ""
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    return input_text.strip() or "Player"
                elif ev.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if ev.unicode.isprintable():
                        input_text += ev.unicode

        screen.fill((220, 220, 220))
        w, h = screen.get_size()
        title = font.render("Level Complete!", True, (0, 0, 0))
        txt = font.render(f"Moves: {moves}", True, (0, 0, 0))
        prompt = font.render("Enter name and press Enter:", True, (0, 0, 0))
        name_surf = font.render(input_text, True, (0, 0, 0))
        screen.blit(title, (w // 2 - title.get_width() // 2, h // 2 - 80))
        screen.blit(txt, (w // 2 - txt.get_width() // 2, h // 2 - 40))
        screen.blit(prompt, (w // 2 - prompt.get_width() // 2, h // 2))
        screen.blit(name_surf, (w // 2 - name_surf.get_width() // 2, h // 2 + 40))

        pygame.display.flip()
        clock.tick(30)
