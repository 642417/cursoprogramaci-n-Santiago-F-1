#sudo dkpg --configure -a
#sudo apt-get install python3-pygame


import math
import random
import pygame 

from pygame import mixer

# Inicio del juego
pygame.init()

# Crear el fondo de pantalla
screen = pygame.display.set_mode((1000, 800))

# Fondo de pantalla
background = pygame.image.load('/media/pc11/FONSECA 10-3/Juego 1/Fondo.png')

# Sound
mixer.music.load("/media/pc11/FONSECA 10-3/Juego 1/UTF-8background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Marte busca mamás")
icon = pygame.image.load('/media/pc11/FONSECA 10-3/Juego 1/enemigo-removebg-preview.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('/media/pc11/FONSECA 10-3/Juego 1/Cohete-removebg-preview.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 42

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemigo_2-removebg-preview.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#disparo, proyectil, bala

armaImg = pygame.image.load('/media/pc11/FONSECA 10-3/Juego 1/bala-removebg-preview.png')
armaX = 0
armaY = 480
armaX_change = 0
armaY_change = 10
arma_estado = "ready"

# Puntaje

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Juego terminado
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_puntaje(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def iniciar_disparo (x, y):
    global arma_estado
    arma_estado = "Fire"
    screen.blit(armaImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    # imagen de fondo
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.quit:
            running = False

        # si presiona
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()