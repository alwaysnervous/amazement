import pygame
import sys


def end_screen(screen, score, level, font_name='freesansbold.ttf', font_size=32):
    # Создание шрифта и текста
    font = pygame.font.Font(font_name, font_size)
    score_text = font.render('Очки: ' + str(score), True, (255, 255, 255))
    level_text = font.render('Уровень: ' + str(level), True, (255, 255, 255))

    # Определение позиции текста
    score_rect = score_text.get_rect()
    score_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 50)
    level_rect = level_text.get_rect()
    level_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

    # Отображение текста на экране
    screen.blit(score_text, score_rect)
    screen.blit(level_text, level_rect)

    # Обновление экрана
    pygame.display.flip()

    # Создание кнопки возврата в главное меню
    button_color = (0, 255, 0)  # Зеленый цвет
    button_rect = pygame.Rect(0, 0, 250, 50)  # Размеры кнопки
    button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 100)  # Позиция кнопки

    # Отображение кнопки на экране
    pygame.draw.rect(screen, button_color, button_rect)

    # Создание текста для кнопки
    button_font = pygame.font.Font(font_name, font_size)
    button_text = button_font.render('Главное меню', True, (0, 0, 0))  # Черный цвет текста
    button_text_rect = button_text.get_rect()
    button_text_rect.center = button_rect.center

    # Отображение текста кнопки на экране
    screen.blit(button_text, button_text_rect)

    # Обновление экрана
    pygame.display.flip()

    # Ожидание нажатия кнопки
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    return False
