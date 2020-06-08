import pygame
import random
import math
import sys
from random import randint
from pygame import mixer

# setup
pygame.init()
screen = pygame.display.set_mode((600, 480))
score = 0
highscore = 0
coins = 0
lives = 3
winWidth = 600
winHeight = 480
color_CYAN = (0, 255, 255)
color_BLACK = (0, 0, 0)
all_sprites_list = pygame.sprite.Group()
running = False
click = False

pygame.display.set_caption("cargo run")
icon = pygame.image.load('icon1.png')
pygame.display.set_icon(icon)

# background
bkgs=[]
bkg_texture_str="background.png"

# background sound

class Background(pygame.sprite.Sprite):
    x = 0
    y = 0
    maxY=0
    def __init__(self, texture,x=0,y=0, width = 1, height = 1):
        super(Background,self).__init__()
        self.image=texture
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        pygame.draw.rect(self.image,(0,0,0), [self.x, self.y, width, height])
        self.rect = self.image.get_rect()

    def scroll(self,speed):
        self.y+=(speed)
        if self.y>winHeight:
            self.y=-winHeight

    def update(self):
        self.scroll(10)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

# player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, changeX):
        super().__init__()
        self.image = pygame.image.load('player.png')
        self.x = x
        self.y = y
        self.changeX = changeX
        self.rect = (self.x, self.y)

playerX = 268
playerY = 350
playerXChange = 0
player = Player(playerX, playerY, playerXChange)

# Enemy
enemyImgList = []
enemyXList = []
enemyYList = []
enemyXChangeList = []
enemyYChangeList = []

def enemy(x, y, i):
    screen.blit(enemyImgList[i], (x, y))

for i in range(4):
    enemyImgList.append(pygame.image.load('enemyFighter.png'))
    enemyXList.append(randint(64, 416))
    enemyYList.append(randint(-300, -50))
    enemyXChangeList.append(1)
    enemyYChangeList.append(2)

# explosion setup
explosionGroup = pygame.sprite.Group()
def explode(x, y):
    explosion = pygame.image.load('explosion.png')
    screen.blit(explosion, (x, y))

# Player laser
playerLaserImg = pygame.image.load('player_ship_laser.png')
playerLaserX = 0
playerLaserY = playerY
playerLaserXChange = playerX
playerLaserYChange = 10
playerLaserState = "ready"
# this is the trail behind the player
particlesL = []
particlesR = []
def randomParticles(): # randomizes particle colors
    select = randint(1, 2)
    if select == 1:
        return (0, 255, 255)
    if select == 2:
        return (0, 128, 128)

def playerLaserFire(x, y):
    global playerLaserState
    playerLaserState = "fire"
    screen.blit(playerLaserImg, (x + 28, y + 10))

def collisionCheck(enemyFighterX, enemyFighterY, playerLaserX, playerLaserY):
    distance = math.sqrt(math.pow(playerLaserX - enemyFighterX, 2) + math.pow(playerLaserY - enemyFighterY, 2))
    if distance < 27:
        return True
    else:
        return False

if __name__=="__main__":
    pygame.init()

    screen=pygame.display.set_mode((winWidth,winHeight))
    clock = pygame.time.Clock()
    screen.fill(color_CYAN)

    bkg_texture=pygame.transform.scale((pygame.image.load(bkg_texture_str)),(winWidth,winHeight))
    BkgSprite1 = Background(bkg_texture,0,winHeight*(-1))
    BkgSprite2 = Background(bkg_texture,0,0)
    BkgSprite3 = Background(bkg_texture,0,winHeight)

    all_sprites_list.add(BkgSprite1)
    all_sprites_list.add(BkgSprite2)
    all_sprites_list.add(BkgSprite3)

    # text setup
    texts = ['Play!', 'score = ', 'lives = ', 'highscore = ',
             'how to play', 'paused', 'back']
    def callText(call, variable, color, default, fontSize):
        font = pygame.font.Font('freesansbold.ttf', int(fontSize))
        if variable == 'no variable':
            whichText = texts[call]
        else:
            whichText = (texts[call] + str(variable))
        text = font.render(whichText, True, (color))
        textRect = text.get_rect()
        if default == 'default':
            textRect.center = (winWidth // 2, winHeight // 2)
        else:
            textRect.center = default
        return screen.blit(text, textRect)

reset = False
paused = False
def mainGame():
    global running, playerLaserState, playerX, playerLaserY
    global playerXChange, playerLaserX, score, lives, highscore
    global coins, paused, reset

    mixer.music.load('background music.wav')
    mixer.music.play(-1)
    enemyChange = 0

    while not running:
        all_sprites_list.update()
        screen.fill(color_CYAN)
        BkgSprite1.draw(screen)
        BkgSprite2.draw(screen)
        BkgSprite3.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerXChange = -6
                if event.key == pygame.K_RIGHT:
                    playerXChange = 6
                if event.key == pygame.K_SPACE:
                    if playerLaserState == "ready":
                        laserFireSound = mixer.Sound('laser.wav')
                        laserFireSound.play()
                        playerLaserX = playerX
                        playerLaserFire(playerX, playerLaserY)
                if event.key == pygame.K_p:
                    paused = not paused
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerXChange = 0
        if paused == True:
            continue

        playerX += playerXChange
        if playerX <= 0:
            playerX = 0
        elif playerX >= 536:
            playerX = 536

        # player laser movement
        if playerLaserY <= 0:
            playerLaserY = playerY
            playerLaserState = "ready"
        if playerLaserState == "fire":
            playerLaserFire(playerLaserX, playerLaserY)
            playerLaserY -= playerLaserYChange

        # draw player and particles
        particlesL.append([[playerX + 10, playerY + 70], [random.randint(0, 20) / 10 - 1, 2], random.randint(4, 6)])
        particlesR.append([[playerX + 54, playerY + 70], [random.randint(0, 20) / 10 - 1, 2], random.randint(4, 6)])

        for particle in particlesL:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            particle[1][1] += 0.1
            pygame.draw.circle(screen, randomParticles(), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                particlesL.remove(particle)
        for particle in particlesR:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            particle[1][1] += 0.1
            pygame.draw.circle(screen, randomParticles(), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                particlesR.remove(particle)

        # draw player
        screen.blit(player.image, (playerX, playerY))

        # enemy movement and collision check one
        for i in range(4):
            if enemyYList[i] > 600:
                enemyYList[i] = randint(-300, -50)
                enemyXList[i] = randint(64, 416)
                score -= 1
                if score <= 0:
                    score = 0
            collisionOneCheck = collisionCheck(enemyXList[i], enemyYList[i], playerLaserX, playerLaserY)
            collisionTwoCheck = collisionCheck(enemyXList[i], enemyYList[i], playerX, playerY)
            if collisionOneCheck:
                playerLaserY = 200
                playerLaserState = "ready"
                laserHitSound = mixer.Sound('laser hit sound.wav')
                laserHitSound.play()
                score += 1
                enemyXList[i] = randint(0, 200)
                enemyYList[i] = randint(-300, 50)
            enemy(enemyXList[i], enemyYList[i], i)
            enemyYList[i] += 2
            if collisionTwoCheck:
                lives -= 1
                shock1 = pygame.image.load('shock1.png')
                shock2 = pygame.image.load('shock2.png')
                screen.blit(shock1, (playerX, 350))
                screen.blit(shock2, (playerX, 350))
                enemyXList[i] = randint(0, 200)
                enemyYList[i] = randint(-300, 50)
                if lives == 0:
                    if score >= highscore:
                        highscore = score
                    running = True
                    coins += score
                    break

        # draw score and lives
        callText(1, score, (255, 255, 255), (525, 25), 20)
        callText(2, lives, (255, 255, 255), (425, 25), 20)

        enemyChange += 0.0005
        changeValue = -1
        for i in range(4):
            changeValue += 1
            enemyYList[changeValue] += enemyChange

        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)

# game menu
class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

logo = pygame.image.load('Cargo Run Logo.png')
def mainMenu():
    global running, playerLaserState, playerX, playerLaserY
    global playerXChange, playerLaserX, score, lives, highscore
    global coins, paused, reset

    all_sprites_list.update()
    screen.fill(color_CYAN)
    BkgSprite1.draw(screen)
    BkgSprite2.draw(screen)
    BkgSprite3.draw(screen)

    screen.blit(logo, (50, 20))
    button1 = button((0, 0, 0), 70, 200, 200, 30, texts[0])

    pygame.display.update()

    while True:
        event = pygame.event.poll()
        pos = pygame.mouse.get_pos()

        button1.draw(screen, (0, 0, 0))
        callText(3, highscore, (255, 255, 255), (170, 300), 30)
        callText(1, score, (255, 255, 255), (170, 340), 30)
        screen.blit((pygame.image.load("how to play.png")), (280, 150))
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1.isOver(pos):
                score = 0
                mainGame()
                all_sprites_list.update()
                screen.fill(color_CYAN)
                BkgSprite1.draw(screen)
                BkgSprite2.draw(screen)
                BkgSprite3.draw(screen)

                screen.blit(logo, (50, 20))
                button1 = button((0, 0, 0), 70, 200, 200, 30, texts[0])

                pygame.display.update()

                running = False
                lives = 3
                reset = True

        if event.type == pygame.MOUSEMOTION:
            if button1.isOver(pos):
                button1.color = (192, 192, 192)
            else:
                button1.color = (255, 255, 255)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                pygame.quit()
                sys.exit()

mainMenu()
