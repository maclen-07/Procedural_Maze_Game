import pygame
from game import menu, level_select, game_loop, highscore
import DFS


def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 700))
    pygame.display.set_caption("Maze Game")

    # Ensure mazes are generated/loaded once
    levels = DFS.generate_levels()

    state = "menu"
    while True:
        if state == "menu":
            action = menu.run(screen)
            if action == "play":
                state = "level_select"
            elif action == "highscore":
                _show_highscores(screen)
            elif action == "exit":
                break
        elif state == "level_select":
            choice = level_select.run(screen, levels)
            if choice == "back":
                state = "menu"
            else:
                # start game with selected maze
                maze = levels.get(choice)
                if maze:
                    game_loop.run(screen, maze, choice)
                state = "menu"

    pygame.quit()


def _show_highscores(screen):
    import pygame
    scores = highscore.sorted_scores()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    page = True
    while page:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                page = False

        screen.fill((240, 240, 240))
        w, h = screen.get_size()
        title = font.render("Highscores (Esc to return)", True, (0, 0, 0))
        screen.blit(title, (w // 2 - title.get_width() // 2, 20))
        y = 60
        for s in scores[:20]:
            line = font.render(f"{s.get('name')} - {s.get('level')} - {s.get('moves')}", True, (0, 0, 0))
            screen.blit(line, (40, y))
            y += 30

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
