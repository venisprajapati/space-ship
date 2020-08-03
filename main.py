import pygame
import math
import random
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create the screen(display) ( length, width ) -> tuple; so it is required to write inside another bracket
screen = pygame.display.set_mode((800, 600))  # ( width, height )
# screen starts from left-up corner as (0,0) there is left -> right : 0 -> 800
# top -> bottom : 0 -> 600

# Background
# background = pygame.image.load('space.png')

# title and icon
pygame.display.set_caption("Space Ship")  # display caption
icon = pygame.image.load('ufo.png')  # make image variable and load image
pygame.display.set_icon(icon)  # set image as icon

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player img, co-ordinates
playerimg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemies
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

# Enemy img, co-ordinates
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet img, co-ordinates
bulletimg = []
bulletX = []
bulletY = []
bulletX_change = []
bulletY_change = []
bullet_state = []
num_of_bullets = 3

bullet_ready = True

# ready - you cant see the bullet on screen
# fire - bullet is currently moving
for i in range(num_of_bullets):
    bulletimg.append(pygame.image.load('bullet.png'))
    bulletX.append(0)
    bulletY.append(480)
    bulletX_change.append(0)
    bulletY_change.append(1.2)
    bullet_state.append('Ready')

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 72)

# Play again font
again_font = pygame.font.Font('freesansbold.ttf', 22)

# Exit text font
exit_font = pygame.font.Font('freesansbold.ttf', 32)

# Game Life font
life_font = pygame.font.Font('freesansbold.ttf', 32)

# Game is running or not
game_run = True


# Game Life TExt
def game_life_fun():
    life_text = life_font.render("LIFE : " + str(game_life), True, (25, 255, 50))
    screen.blit(life_text, (620, 10))


# Play Again
def play_again(cnt):
    if cnt % 2 == 0:
        set_color = (255, 25, 25)
    else:
        set_color = (180, 185, 195)
    again = again_font.render("Press Enter key to continue again..", True, set_color)
    screen.blit(again, (235, 320))


# Show score
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game Over Text
def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 24, 24))
    screen.blit(over_text, (200, 150))
    show_score(321, 250)
    mixer.music.stop()


# Exit now
def exit_text():
    exit_text = exit_font.render("Press Enter to exit game", True, (255, 255, 255))
    screen.blit(exit_text, (220, 325))
    show_score(321, 250)


# Creating(drawing) playerimg on surface
def player(x, y):
    screen.blit(playerimg, (x, y))  # draw img


def enemy(enemyX, enemyY, i):
    screen.blit(enemyimg[i], (enemyX, enemyY))


# Bullet mechanism
def fire_bullet(x, y, i):
    global bullet_state
    bullet_state[i] = 'Fire'
    screen.blit(bulletimg[i], (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


count = 0

game_life = 2

# pass is null statement,It complies nothing (happens nothing) and used to The pass statement is useful when you don’t
# write the implementation of a function but you want to implement it in the future.
# if there is only pass without any condition, -> Screen hangs. it never ends, i.e. loop.
# Game Loop.
running = True
while running:  # running infinite while loop

    # Display screen (above everything)
    # Anything that is persistent into your window continuously
    screen.fill((10, 10, 10))  # (R,G,B) values

    # background image
    # screen.blit(background, (0,0))

    for event in pygame.event.get():  # see all the events happening in game window
        if event.type == pygame.QUIT:  # must write event type to check type of events and it is QUIT /=not quit,() :
            running = False  # break loop

    count += 1

    # if key is pressed whether right or left.
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -0.7
        if event.key == pygame.K_RIGHT:
            playerX_change = 0.7

    # Bullet Algorithm
    for b in range(num_of_bullets):
        if bulletY[b] <= 380:
            bullet_ready = True
        if bullet_ready == True:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if bullet_state[b] is 'Ready':
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        # Get the current x co-ordinates of spaceship and stores inside bulletX
                        bulletX[b] = playerX
                        fire_bullet(bulletX[b], bulletY[b], b)
                        bullet_ready = False


    # key is released
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
            playerX_change = 0

    # boundries for player ship
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 1000
            game_over_text()
            if game_run == True:
                game_life -= 1
            if game_life > 0:
                play_again(count)
                game_life_update = False
            elif game_life == 0:
                exit_text()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER:
                        exit()
            game_run = False

        # restarting game
        if game_run == False:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_KP_ENTER:
                    game_run = True
                    mixer.music.play(-1)
                    # print(game_life, "after restart")
                    for j in range(num_of_enemies):
                        enemyX[j] = random.randint(0, 736)
                        enemyY[j] = random.randint(50, 150)
                        enemyX_change[j] = 2
                        enemyY_change[j] = 40

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        for b in range(num_of_bullets):
            collision = isCollision(enemyX[i], enemyY[i], bulletX[b], bulletY[b])
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bulletY[b] = 480
                bullet_state[b] = 'Ready'
                score_value += 5
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    for i in range(num_of_bullets):
        if bulletY[i] <= 0:
            bulletY[i] = 480
            bullet_state[i] = 'Ready'
        if bullet_state[i] is 'Fire':
            fire_bullet(bulletX[i], bulletY[i], i)
            bulletY[i] -= bulletY_change[i]

    # shows us the Score
    if game_run == True:
        show_score(textX, textY)

    player(playerX, playerY)

    game_life_fun()

    pygame.display.update()  # update screen, if something new is added

# Completed.
