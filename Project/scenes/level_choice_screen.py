import pygame
import sys


def level_choice_screen(screen):
    pygame.display.set_caption("Выбор уровня")

    font = pygame.font.Font(None, 36)

    levels = ["Уровень 1", "Уровень 2", "Уровень 3", "Случайная генерация уровней"]

    selected_level = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_level = (selected_level - 1) % len(levels)
                elif event.key == pygame.K_DOWN:
                    selected_level = (selected_level + 1) % len(levels)
                elif event.key == pygame.K_RETURN:
                    return selected_level

        screen.fill((0, 0, 0))

        for i, level in enumerate(levels):
            text = font.render(level, True, (0, 0, 255) if i == selected_level else (255, 255, 255))
            screen.blit(text, (100, 100 + i * 40))

        pygame.display.flip()
