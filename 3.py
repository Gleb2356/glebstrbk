import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Аркада")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Класс для фона
class Background:
    def __init__(self):
        self.image = pygame.image.load("car4.png")
        self.rect = self.image.get_rect()
        self.speed = 5
        self.offset = 0

    def update(self, direction):
        if direction == "left":
            self.offset += self.speed
            if self.offset > WIDTH:
                self.offset -= WIDTH
        elif direction == "right":
            self.offset -= self.speed
            if self.offset < -WIDTH:
                self.offset += WIDTH

    def draw(self, surface):
        surface.blit(self.image, (self.offset, 0))
        surface.blit(self.image, (self.offset + WIDTH, 0))


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5

    def update(self, keys, background):
        # Движение игрока
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.left < 100:  # Граница для движения фона вправо
                background.update("right")
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.right > WIDTH - 100:  # Граница для движения фона влево
                background.update("left")
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Ограничение движения по вертикали
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))


# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(1, 3)
        self.direction = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.direction *= -1


# Класс стрелы
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speed = 10
        self.lifetime = WIDTH // self.speed

    def update(self):
        self.rect.x += self.speed
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()


# Создание объектов
background = Background()
player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
arrows = pygame.sprite.Group()

# Создание врагов
for i in range(5):
    enemy = Enemy(random.randint(0, WIDTH - 40), random.randint(0, HEIGHT - 40))
    enemies.add(enemy)
    all_sprites.add(enemy)

# Основной цикл
clock = pygame.time.Clock()
running = True

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Создание стрелы
                arrow = Arrow(player.rect.right, player.rect.centery)
                arrows.add(arrow)
                all_sprites.add(arrow)

    # Обновление объектов
    keys = pygame.key.get_pressed()
    player.update(keys, background)
    enemies.update()
    arrows.update()

    # Проверка коллизий
    hits = pygame.sprite.groupcollide(arrows, enemies, True, True)
    for hit in hits:
        all_sprites.remove(hit)
        for enemy in hits[hit]:
            all_sprites.remove(enemy)

    # Отрисовка
    background.draw(screen)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()