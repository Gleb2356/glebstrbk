import pygame
from constants import *

class Help():
    def __init__(self):
        big_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 28)

        # Загрузка пиктограмм управления
        self.icon_left = pygame.transform.scale(pygame.image.load("left.png"), (32, 32))
        self.icon_right = pygame.transform.scale(pygame.image.load("right.png"), (32, 32))
        self.icon_jump = pygame.transform.scale(pygame.image.load("jump.png"), (32, 32))
        self.icon_shoot = pygame.transform.scale(pygame.image.load("shoot.png"), (32, 32))
        self.icon_music = pygame.transform.scale(pygame.image.load("music.png"), (32, 32))
        self.icon_help = pygame.transform.scale(pygame.image.load("help.png"), (32, 32))

        # Подготовка текста
        text1 = big_font.render("Управление", True, C_YELLOW)
        controls = [
            (self.icon_left, "Влево: 'a' или стрелка влево"),
            (self.icon_right, "Вправо: 'd' или стрелка вправо"),
            (self.icon_jump, "Прыжок: 'w' или стрелка вверх"),
            (self.icon_shoot, "Выстрел: пробел"),
            (self.icon_music, "Музыка вкл/выкл: 'm', громче: 'u', тише: 'j'"),
            (self.icon_help, "Подсказка вкл/выкл (пауза): 'h'")
        ]

        # Фон и рамка
        img = pygame.Surface([round(3 * win_width / 4), round(3 * win_height / 4)], pygame.SRCALPHA)
        img.fill((0, 0, 0, 180))
        pygame.draw.rect(img, C_YELLOW, img.get_rect(), 3, border_radius=15)

        # Отображение текста с пиктограммами
        w, h = round(win_width / 8), round(win_height / 12)
        img.blit(text1, (w, h))
        for index, (icon, line) in enumerate(controls):
            img.blit(icon, (w, h * (index + 2)))
            text = self.small_font.render(line, True, C_YELLOW)
            img.blit(text, (w + 40, h * (index + 2)))

        self.img = img

        # Строка состояния
        self.text_points = self.small_font.render("Очков: ", True, C_DARK)
        self.text_lives = self.small_font.render("Жизней: ", True, C_DARK)
        self.text_help = self.small_font.render("Пауза/подсказка: 'h'", True, C_DARK)
        self.text_height = self.text_help.get_height()

    def line(self, points=0, lives=1):
        tab = 50
        img = pygame.Surface([win_width, self.text_height], pygame.SRCALPHA)
        img.blit(self.text_lives, (0, 0))
        img.blit(self.small_font.render(str(lives), True, C_YELLOW), (self.text_lives.get_width(), 0))
        img.blit(self.text_points, (self.text_lives.get_width() + tab, 0))
        img.blit(self.small_font.render(str(points), True, C_YELLOW), (self.text_lives.get_width() + tab + self.text_points.get_width(), 0))
        img.blit(self.text_help, (self.text_lives.get_width() + tab * 2 + self.text_points.get_width(), 0))
        return img
