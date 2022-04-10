"space_invaders.py: Space invader game using pygame"

import random
import math

import pygame
from pygame import mixer

pygame.init()

size = width, height = 800, 600

# create screen
screen = pygame.display.set_mode(size)

# background
background = pygame.image.load("./img/space.png")

# background sound
mixer.music.load("./audio/background.wav")
mixer.music.play(-1)


# title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("./img/space-invaders-32.png")
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load("./img/space-invaders-64.png")
player_x = 368
player_y = 480
player_x_change = 0
player_speed = 5

# enemies
n_enemy = 6
enemy_img = pygame.image.load("./img/ufo.png")
enemy_x = [random.randint(1, 735) for i in range(n_enemy)]
enemy_y = [random.randint(50, 150) for i in range(n_enemy)]
enemy_x_change = [4 for i in range(n_enemy)]
enemy_y_change = 40

# missile
# ready - you cannot see missile on screen
# fire - the missile is moving
missile_img = pygame.image.load("./img/missile.png")
missile_x = 0
missile_y = 480
missile_y_change = 13
missile_state = "ready"

# score
score_val = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

# game over text
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score():
    score = font.render(f"Score: {score_val}", True, (255, 255, 255))
    screen.blit(score, (text_x, text_y))


def game_over_text():
    text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y):
    screen.blit(enemy_img, (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missile_img, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, missile_x, missile_y):
    result = False
    distance = math.sqrt(
        math.pow(enemy_x - missile_x, 2) + math.pow(enemy_y - missile_y, 2)
    )
    if distance < 27:
        result = True
    return result


# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            elif event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            elif event.key == pygame.K_SPACE and missile_state == "ready":
                missile_sound = mixer.Sound("./audio/missile.wav")
                missile_sound.play()
                missile_x = player_x
                fire_missile(missile_x, missile_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_y_change = 0

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # player movement
    # keeps player in frame
    player_x += player_x_change
    if player_x < 0:
        player_x = 0
    elif player_x > 736:
        player_x = 736

    for i in range(n_enemy):

        # game over
        if enemy_y[i] > 430:
            for j in range(n_enemy):
                enemy_y[j] = 1000
            game_over_text()
            break

        # enemy movement
        # makes the enemy come closer when it reaches the end of a line
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= 736:
            enemy_x_change[i] = -enemy_x_change[i]
            enemy_y[i] += enemy_y_change

        # collision
        if is_collision(enemy_x[i], enemy_y[i], missile_x, missile_y):
            explosion_sound = mixer.Sound("./audio/explosion2.wav")
            explosion_sound.play()
            missile_y = 480
            missile_state = "ready"
            score_val += 1
            enemy_x[i] = random.randint(1, 735)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i])

    # missile movement
    if missile_y <= 0:
        missile_y = 480
        missile_state = "ready"
    elif missile_state == "fire":
        fire_missile(missile_x, missile_y)
        missile_y -= missile_y_change

    player(player_x, player_y)
    show_score()

    pygame.display.update()
