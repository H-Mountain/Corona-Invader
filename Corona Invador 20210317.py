import pygame
import random
import math
from pygame import mixer
import pygame_menu

# Initialize the pygame
pygame.init()

# creates the screen
screen = pygame.display.set_mode((800, 600))

# Menu
def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    # Do the job here !
    pass



# background
background = pygame.image.load("background3.jpg")

# Background sound
mixer.music.load("bensound-scifi2.mp3")
mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Game over sound
game_over_sound = mixer.Sound("gameover_sound.wav")

# Title and Icon
pygame.display.set_caption("Pandemic Invader")
icon = pygame.image.load("enemy.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player_spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy2.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("syringe.png")
bulletX = 0
bulletY = 480
bulletX_change = 0.2
bulletY_change = 1
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("Space Quest.ttf", 32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font("Space Quest.ttf", 64)
over_2nd_line_font = pygame.font.Font("Space Quest.ttf", 16)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    over_text_2nd_line = over_2nd_line_font.render("The pandemic is here. Enjoy COVID-19, looser.", True,
                                                   (255, 255, 255))
    screen.blit(over_text_2nd_line, (185, 335))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False


# Game Loop, makes sure the game window is running
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))

    # background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        # if keystroke is pressed, check if its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:

                # Checks if bullet is on the screen or not
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    # Gets the current X coordinate of the spaceship
                    fire_bullet(playerX, bulletY)
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)




        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change

    # Makes sure player can't move outside game window
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
            game_over_text(200, 250)

            if game_over_sound:
                game_over_sound.play()
                game_over_sound = False

            break

        enemyX[i] += enemyX_change[i]
        # Makes sure enemy can't move outside game window
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("boop-dead.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Makes player visible at all times
    player(playerX, playerY)

    # Shows score
    show_score(textX, textY)

    # Updates screen
    pygame.display.update()
