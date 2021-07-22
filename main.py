import pygame
import sys
from station import Station
import pygame.mixer
import random
from enemy import Enemy
from bullet import Bullet

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 487
STATION_HEIGHT = 380
BULLET_SPEED = 10
ENEMY_SPEED = 7

# Screen settings
(width, height) = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()

# Station
station_file = open("assets/textures/iss.png")
station_texture = pygame.image.load(station_file)
station = Station(200, STATION_HEIGHT, station_texture)

# Time sec
start_time = 250
clock = pygame.time.Clock()

# Enemy
enemy_file = open("assets/textures/stone_2.png")
enemy_texture = pygame.image.load(enemy_file)
enemies: list[Enemy] = []


# Bullets
bullet_file = open("assets/textures/bullet.png")
bullet_texture = pygame.image.load("assets/textures/bullet.png")
bullets: list[Bullet] = []
bulletX = 90

# Caption
pygame.display.set_caption("ISS Escape")

# Background
background_texture = pygame.image.load("assets/textures/bg.jpg")

# Shot sound
shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")

# Main loop
running = True
while running:
    all_event = pygame.event.get()
    for event in all_event:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            shot_sound.play()
            bullet = Bullet(
                bulletX + station.pos_x,
                STATION_HEIGHT + 10,
                bullet_texture,
                BULLET_SPEED,
            )

            bullets.append(bullet)

    # Enemies moves
    for enemy in enemies:
            enemy.move()

    for i in range(1):
        if start_time > 200:
            enemy = Enemy(random.randrange(0 + i * 100, 600), -30, enemy_texture, ENEMY_SPEED)
            enemies.append(enemy)

    # Station moves
    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_LEFT]:
        station.pos_x -= 10
    elif all_keys[pygame.K_RIGHT]:
        station.pos_x += 10

    my, mx = pygame.mouse.get_pos()

    for bullet in bullets:
        bullet.move()

    # Iterate over a slice copy if you want to mutate a list.
    for bullet in bullets[:]:
        if bullet.pos_x < 0:
            bullets.remove(bullet)

    # Keeping player on screen
    if station.pos_x < 0:
        station.pos_x = 0
    if station.pos_x > SCREEN_WIDTH:
        station.pos_x = SCREEN_WIDTH

    screen.blit(background_texture, (0, 0))

    for bullet in bullets:
        screen.blit(bullet_texture, pygame.Rect(bullet.pos_x, bullet.pos_y, 0, 0))

    for enemy in enemies:
        screen.blit(enemy.texture, (enemy.pos_x, enemy.pos_y))
        
    screen.blit(station.texture, (station.pos_x, station.pos_y))
    pygame.display.flip()
    clock.tick(60)