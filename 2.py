import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Анимация фигур")

# Цвета
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255),
    (128, 0, 0), (0, 128, 0), (0, 0, 128)
]


# Класс для анимированной фигуры
class Shape:
    def __init__(self, shape_type, x, y, size, speed, color):
        self.shape_type = shape_type  # 'square', 'rectangle', 'circle', 'triangle'
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.direction = 1  # 1 - вправо, -1 - влево

        # Особые параметры для разных фигур
        if shape_type == 'rectangle':
            self.width = size * 2
            self.height = size
        else:
            self.width = size
            self.height = size

    def move(self):
        self.x += self.speed * self.direction

        # Проверка столкновения с границами
        if self.x + self.width > WIDTH or self.x < 0:
            self.direction *= -1
            self.color = random.choice(COLORS)

        # Корректировка позиции, чтобы не выходить за границы
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > WIDTH:
            self.x = WIDTH - self.width

    def draw(self, surface):
        if self.shape_type == 'square':
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
        elif self.shape_type == 'rectangle':
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        elif self.shape_type == 'circle':
            pygame.draw.circle(surface, self.color, (int(self.x + self.size / 2), int(self.y + self.size / 2)),
                               self.size // 2)
        elif self.shape_type == 'triangle':
            points = [
                (self.x + self.size // 2, self.y),
                (self.x, self.y + self.size),
                (self.x + self.size, self.y + self.size)
            ]
            pygame.draw.polygon(surface, self.color, points)

    def is_clicked(self, pos):
        x, y = pos
        if self.shape_type == 'circle':
            center_x = self.x + self.size / 2
            center_y = self.y + self.size / 2
            distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            return distance <= self.size / 2
        else:
            return (self.x <= x <= self.x + self.width and
                    self.y <= y <= self.y + self.height)


# Создание фигур
shapes = [
    Shape('square', 100, 100, 50, 3, random.choice(COLORS)),
    Shape('rectangle', 100, 200, 40, 4, random.choice(COLORS)),
    Shape('circle', 100, 300, 60, 2, random.choice(COLORS)),
    Shape('triangle', 100, 400, 70, 5, random.choice(COLORS))
]

# Основной цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                for shape in shapes:
                    if shape.is_clicked(event.pos):
                        shape.color = random.choice(COLORS)
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # Очистка экрана
    screen.fill((240, 240, 240))

    # Обновление и отрисовка фигур
    for shape in shapes:
        shape.move()
        shape.draw(screen)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()