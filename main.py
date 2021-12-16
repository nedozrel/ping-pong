import pygame
import sys
import random

WIDTH, HEIGHT = 1000, 700
FPS = 60
platform_y_pos = 20
WHITE = (255, 255, 255)
player_pos = 280
ball_direction_x = random.randrange(-1, 2, 2)
ball_direction_y = random.randrange(-1, 2, 2)
ball_x_speed = 3 * ball_direction_x
ball_y_speed = 3 * ball_direction_y
player_speed = 0
enemy_speed = 7
player_score = 0
enemy_score = 0
game_active_status = 'game start'

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

font = pygame.font.Font('20051.ttf', 20)
game_end_font = pygame.font.Font('20051.ttf', 100)

ball = pygame.Rect(WIDTH / 2 - 15, HEIGHT / 2 - 15, 20, 20)
player = pygame.Rect(20, player_pos, 10, 100)
enemy = pygame.Rect(WIDTH - 20, HEIGHT / 2 - 70, 10, 100)

SPEED_UP = pygame.USEREVENT
pygame.time.set_timer(SPEED_UP, 15000)
speed_booster = 1


def check_collision():
    if ball.colliderect(player):
        return True
    if ball.colliderect(enemy):
        return True
    return False


def display_score():
    player_score_surface = font.render(f'{player_score}', True, WHITE)
    enemy_score_surface = font.render(f'{enemy_score}', True, WHITE)
    player_score_rect = player_score_surface.get_rect(center=(WIDTH / 4, 15))
    enemy_score_rect = player_score_surface.get_rect(center=(WIDTH - WIDTH / 4, 15))
    screen.blit(enemy_score_surface, enemy_score_rect)
    screen.blit(player_score_surface, player_score_rect)


def display_game_status(game_active_status):
    if game_active_status == 'game over':
        game_end_surface = game_end_font.render('Game over', True, WHITE)
        game_end_rect = game_end_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 100))
        press_space_surface = font.render('Press space to continue.', True, WHITE)
        press_space_rect = press_space_surface.get_rect(center=(WIDTH / 2, HEIGHT - HEIGHT / 4 - 100))
        screen.blit(press_space_surface, press_space_rect)
        screen.blit(game_end_surface, game_end_rect)

    if game_active_status == 'game win':
        game_end_surface = game_end_font.render('You win', True, WHITE)
        game_end_rect = game_end_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 100))
        press_space_surface = font.render('Press space to continue.', True, WHITE)
        press_space_rect = press_space_surface.get_rect(center=(WIDTH / 2, HEIGHT - HEIGHT / 4 - 100))
        screen.blit(press_space_surface, press_space_rect)
        screen.blit(game_end_surface, game_end_rect)

    if game_active_status == 'game start':
        press_space_surface = font.render('Press space to continue.', True, WHITE)
        press_space_rect = press_space_surface.get_rect(center=(WIDTH / 2, HEIGHT - HEIGHT / 2))
        screen.blit(press_space_surface, press_space_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPEED_UP:
            if ball_y_speed < 0:
                ball_y_speed -= speed_booster
            if ball_y_speed > 0:
                ball_y_speed += speed_booster
            if ball_x_speed < 0:
                ball_x_speed -= speed_booster
            if ball_x_speed > 0:
                ball_x_speed += speed_booster
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active_status == 'game over':
                enemy_score = 0
                player_score = 0
                ball.centery = HEIGHT / 2
                ball.centerx = WIDTH / 2
                ball_y_speed = 3 * ball_direction_y
                ball_x_speed = 3 * ball_direction_x
                game_active_status = True
            if event.key == pygame.K_SPACE and game_active_status == 'game win':
                enemy_score = 0
                player_score = 0
                ball.centery = HEIGHT / 2
                ball.centerx = WIDTH / 2
                ball_y_speed = 3 * ball_direction_y
                ball_x_speed = 3 * ball_direction_x
                game_active_status = True
            if event.key == pygame.K_SPACE and game_active_status == 'game start':
                game_active_status = True
            if event.key == pygame.K_w:
                player_speed -= 6
            if event.key == pygame.K_s:
                player_speed += 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_speed += 6
            if event.key == pygame.K_s:
                player_speed -= 6
    if game_active_status == 'game start':
        display_game_status('game start')

    if game_active_status is True:
        if enemy.centery < ball.centery:
            enemy.y += enemy_speed
        if enemy.centery > ball.centery:
            enemy.y -= enemy_speed

        if player.top <= 0:
            player.top = 0
        if player.bottom >= HEIGHT:
            player.bottom = HEIGHT

        if enemy.top <= 0:
            enemy.top = 0
        if enemy.bottom >= HEIGHT:
            enemy.bottom = HEIGHT

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_y_speed *= -1
        if ball.left <= 0:
            ball_x_speed *= -1
            enemy_score += 1
        if ball.right >= WIDTH:
            ball_x_speed *= -1
            player_score += 1

        if check_collision():
            ball_x_speed *= -1

        if enemy_score >= 5:
            game_active_status = 'game over'
        if player_score >= 5:
            game_active_status = 'game win'

        player.y += player_speed
        ball.x += ball_x_speed
        ball.y += ball_y_speed

        screen.fill((0, 0, 0))
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.rect(screen, WHITE, player)
        pygame.draw.rect(screen, WHITE, enemy)
        display_score()

    if game_active_status == 'game over':
        display_game_status('game over')

    if game_active_status == 'game win':
        display_game_status('game win')

    pygame.display.update()
    clock.tick(FPS)
