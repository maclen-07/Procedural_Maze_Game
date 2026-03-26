import pygame
from typing import Dict, List, Tuple


LEVELS = ["easy", "normal", "intermediate", "medium", "hard"]


def run(screen: pygame.Surface, available: Dict[str, List[dict]]) -> str:
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    selected = 0
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return "back"
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(LEVELS)
                elif ev.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(LEVELS)
                elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return LEVELS[selected]
                elif ev.key == pygame.K_ESCAPE:
                    return "back"
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos
                w, h = screen.get_size()
                for i, lvl in enumerate(LEVELS):
                    text = font.render(lvl.capitalize(), True, (0, 0, 0))
                    tx = w // 2 - text.get_width() // 2
                    ty = h // 2 - 120 + i * 50
                    rect = pygame.Rect(tx - 10, ty - 10, text.get_width() + 20, text.get_height() + 20)
                    if rect.collidepoint((mx, my)):
                        return lvl

        screen.fill((230, 230, 230))
        w, h = screen.get_size()
        title = font.render("Select Level", True, (10, 10, 10))
        screen.blit(title, (w // 2 - title.get_width() // 2, h // 2 - 220))

        for i, lvl in enumerate(LEVELS):
            color = (0, 0, 0)
            if i == selected:
                color = (255, 0, 0)
            available_mark = "(loaded)" if lvl in available else ""
            text = font.render(f"{lvl.capitalize()} {available_mark}", True, color)
            screen.blit(text, (w // 2 - text.get_width() // 2, h // 2 - 120 + i * 50))

        pygame.display.flip()
        clock.tick(30)
