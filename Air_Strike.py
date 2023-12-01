import pygame
import random
import time
import math
from pygame import mixer
#initialize pygame
pygame.init()

#make screen
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('images/sky.png')

#sound
mixer.music.load('images/lovesosa.mp3')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("AIR STRIKE")
icon = pygame.image.load('images/planeicon.png')
pygame.display.set_icon(icon)

#player and coordinates
playerimg = pygame.image.load('images/space ship.png')
playerX = 370
playerY = 480
playerX_change = 0

#enemy
enemyimg = []
enemyX = []
enemyY = [] 
enemyX_change = []
enemyY_change = []
numberenemy = 8

for i in range(numberenemy):
    #enemy
    enemyimg.append(pygame.image.load('images/enemyjet.png'))
    enemyX.append(random.randint(0, 746))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(15)
    enemyY_change.append(40)

#bullet 
#ready - u cant see bullet
#fire - the bullet is moving
bulletimg = pygame.image.load('images/missile.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 30
bullet_state = "ready"

#score

score_value = 0
font = pygame.font.Font('images/ARCADE.TTF', 40)

textX = 10
textY = 10

#game over
over_font = pygame.font.Font('images/ARCADE.TTF', 100)
def game_over_text(x,y):
    over_text = over_font.render( "GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (180, 250))


#score 
def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))


#bullet function
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

# enemy function
def enemy(x,y,i):
    screen.blit(enemyimg[i], (x, y))

#function to draw the player on to the screen
def player(x,y):
    screen.blit(playerimg,(x, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 50:
        return True
    else:
        return False

clock = pygame.time.Clock()
#game loop, keeps game continuous
running = True
while running:

    screen.fill((0, 150, 200))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                    playerX_change = -15
            if event.key == pygame.K_RIGHT:
                    playerX_change = 15
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('images/laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                   playerX_change = 0
            
    

    # movement player
    playerX += playerX_change

    if playerX <= 10:
        playerX = 10
    elif playerX >=736:
        playerX = 736

    #movement enemy
    for i in range(numberenemy):

        #game over

        if enemyY[i] > 440:
            for j in range(numberenemy):
                enemyY[j] = 2000
            game_over_text(180, 250)
            break        
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 15
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -15
            enemyY[i] += enemyY_change[i]

        #collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('images/explosions.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 746)
            enemyY[i] = random.randint(50, 150)
            
        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    clock.tick(35)
    #player remains on screen
    player(playerX, playerY)
    #score
    show_score(textX, textY)
    #update the new things we add to display
    pygame.display.update()

