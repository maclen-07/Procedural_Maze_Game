import pygame
from typing import Tuple


OPTIONS = ["Play", "Highscore", "Exit"]


def run(screen: pygame.Surface) -> str:
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    selected = 0
    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return "exit"
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(OPTIONS)
                elif ev.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(OPTIONS)
                elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return OPTIONS[selected].lower()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos
                # check clicks
                w, h = screen.get_size()
                for i, opt in enumerate(OPTIONS):
                    text = font.render(opt, True, (0, 0, 0))
                    tx = w // 2 - text.get_width() // 2
                    ty = h // 2 - 60 + i * 60
                    rect = pygame.Rect(tx - 10, ty - 10, text.get_width() + 20, text.get_height() + 20)
                    if rect.collidepoint((mx, my)):
                        return opt.lower()

        screen.fill((200, 200, 200))
        w, h = screen.get_size()
        title = font.render("Maze Game", True, (10, 10, 10))
        screen.blit(title, (w // 2 - title.get_width() // 2, h // 2 - 160))

        for i, opt in enumerate(OPTIONS):
            color = (0, 0, 0)
            if i == selected:
                color = (255, 0, 0)
            text = font.render(opt, True, color)
            screen.blit(text, (w // 2 - text.get_width() // 2, h // 2 - 60 + i * 60))

        pygame.display.flip()
        clock.tick(30)

    return "exit"
