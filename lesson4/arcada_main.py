import pygame

from constants import *
from level import *
from level_config import *

from game_sprites import *
from gamesingle import game


game.start()
hero = game.start_level(1)

game.show_menu()

key_a = pygame.K_a
key_d = pygame.K_d
key_h = pygame.K_h

# Настройки кнопки выхода с пиктограммой
exit_icon = pygame.transform.scale(pygame.image.load("exit.png"), (32, 32))
button_rect = pygame.Rect(win_width - 50, 10, 40, 40)

while game.run:
    for event in pygame.event.get():
        # Закрытие окна
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT)):
            game.stop()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                hero.move_left(HERO_STEP)
            elif event.unicode == 'a':
                hero.move_left(HERO_STEP)
                key_a = event.key
            elif event.key == pygame.K_RIGHT:
                hero.move_right(HERO_STEP)
            elif event.unicode == 'd':
                hero.move_right(HERO_STEP)
                key_d = event.key
            elif event.key == pygame.K_UP or event.unicode == 'w':
                hero.jump(HERO_JUMP)
            elif event.unicode == 'h':
                key_h = event.key
            elif event.unicode == 'm':
                game.music.change()
            elif event.unicode == 'u':
                game.music.volume_up()
            elif event.unicode == 'j':
                game.music.volume_down()
            elif event.key == pygame.K_SPACE:
                game.music.good_fire()
                hero.fire()
        elif event.type == pygame.KEYUP:
            if game.is_help:
                game.resume()
            else:
                if event.key == pygame.K_LEFT or event.key == key_a:
                    hero.stop()
                elif event.key == pygame.K_RIGHT or event.key == key_d:
                    hero.stop()
                elif event.key == key_h:
                    game.show_menu()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                game.stop()

    if game.in_game():
        game.all_sprites.update()
        if hero.rect.left < win_leftbound or hero.rect.right > win_rightbound:
            offset_x = game.hero_pos.x - hero.rect.x
            game.camera.move(offset_x, 0, game.all_sprites)
        game.hero_pos.x = hero.rect.x
        game.hero_pos.y = hero.rect.y

        game.draw_back_with_shift()
        game.window.blit(game.help.line(points=game.points, lives=game.lives), (0, 10))
        pygame.draw.rect(game.window, C_DARK, button_rect)
        game.window.blit(exit_icon, (button_rect.x + 4, button_rect.y + 4))
        game.all_sprites.draw(game.window)

    pygame.display.update()
    if game.goal_touched(hero):
        game.next_level()

    if hero not in game.all_sprites:
        if game.lives > 0:
            game.timer.tick(1)
            hero = game.restart_level()
        else:
            game.lose()

    game.timer.tick(FPS)
