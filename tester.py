import pygame as pg
import math
import pygame
import os
from random import randint

# setup
caption = "cargo run"
pygame.display.set_caption(caption)
winWidth = 600
winHeight = 480
spritesList = pygame.sprite.Group()
shipList = pygame.sprite.Group()
enemyFighterList = []
enemyFighterGroup = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()

# main variables
clock = pygame.time.Clock()
enemyFighterSpeed = 1.5

# colors
WHITE = 255, 255, 255
RED = 255, 0, 0

# loading images
images = [os.path.join('background.png'),
          os.path.join('player_ship_laser.png'),
          os.path.join('player.png'),
          os.path.join('player_blue.png'),
          os.path.join('player_green.png'),
          os.path.join('enemy_fighter.png'),
          os.path.join('enemy_heavy.png'),]

# background setup
bkgs = []

class Background(pygame.sprite.Sprite):
    x = 0
    y = 0
    maxY = 0

    def __init__(self, texture, x=0, y=0, width=1, height=1):
        super(Background, self).__init__()
        self.image = texture
        self.x = y
        self.y = x
        self.width = width
        self.height = height
        pygame.draw.rect(self.image, (0, 0, 0), [self.x, self.y, width, height])
        self.rect = self.image.get_rect()

    def scroll(self, speed):
        self.y += (speed)
        if self.y > winHeight:
            self.y = -winHeight

    def update(self):
        self.scroll(5)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

def enemy_image_load():
    image = pg.image.load('enemy_fighter.png').convert()
    image.set_colorkey((255, 0, 255))
    transformed_image = pg.transform.rotate(image, 180)
    orig_image = pg.transform.scale(transformed_image, (40, 80))
    return orig_image


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, screen_rect):
        super(Enemy, self).__init__()
        self.screen_rect = screen_rect
        self.image = image
        start_buffer = 0
        self.rect = self.image.get_rect(center=(screen_rect.centerx, screen_rect.centery + start_buffer))
        self.distance_above_player = 100
        self.speed = 2

    def pos_towards_player(self, player_rect):
        c = math.sqrt((player_rect.x - self.rect.x) ** 2 + (player_rect.y - self.distance_above_player - self.rect.y) ** 2)
        try:
            x = (player_rect.x - self.rect.x) / c
            y = ((player_rect.y - self.distance_above_player) - self.rect.y) / c
        except ZeroDivisionError:
            return False
        return (x, y)

    # moves the enemy towards player
    def update(self, player):
        new_pos = self.pos_towards_player(player.rect)
        if new_pos:
            self.rect.x = self.rect.x + new_pos[0] * self.speed
            self.rect.y = self.rect.y + new_pos[1] * self.speed

    def draw(self, surf):
        surf.blit(self.image, self.rect)

class Laser:
    def __init__(self, loc, screen_rect, x, y):
        self.screen_rect = screen_rect
        self.image = pg.image.load(images[1]).convert()
        self.rect = self.image.get_rect(center=loc)
        self.speed = 7
        self.x = x
        self.y = y

    def update(self):
        self.rect.y -= self.speed

    def render(self, surf):
        surf.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen_rect):
        super(Player, self).__init__()
        self.screen_rect = screen_rect
        self.image = pg.image.load('player_blue.png').convert()
        self.image.set_colorkey((255, 0, 255))
        playerX = 0
        playerY = 0
        self.x = playerX
        self.y = playerY
        self.width = winWidth
        self.height = winHeight
        self.transformed_image = pg.transform.rotate(self.image, 180)
        start_buffer = 300
        self.rect = self.image.get_rect(
            center=(screen_rect.centerx, screen_rect.centery + start_buffer)
        )
        self.dx = 300
        self.dy = 300
        self.lasers = []
        self.timer = 0.0
        self.laser_delay = 500
        self.add_laser = False

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if self.add_laser:
                    self.lasers.append(Laser(self.rect.center, self.screen_rect, 0, 0))
                    self.add_laser = False

    def update(self, keys, dt):
        self.rect.clamp_ip(self.screen_rect)
        if keys[pg.K_LEFT]:
            self.rect.x -= self.dx * dt
        if keys[pg.K_RIGHT]:
            self.rect.x += self.dx * dt
        if keys[pg.K_UP]:
            self.rect.y -= self.dy * dt
        if keys[pg.K_DOWN]:
            self.rect.y += self.dy * dt
        for laser in self.lasers:
            laser.update()
        if pg.time.get_ticks() - self.timer > self.laser_delay:
            self.timer = pg.time.get_ticks()
            self.add_laser = True

    def draw(self, surf):
        for laser in self.lasers:
            laser.render(surf)
        surf.blit(self.transformed_image, self.rect)

class fallingEnemy(pygame.sprite.Sprite):
    def __init__(self, screen_rect, position, game):
        super(fallingEnemy, self).__init__()
        super(fallingEnemy, self).__init__()
        self.screen_rect = screen_rect
        self.image = pygame.image.load('enemy_fighter.png')
        fallingEnemyX = randint(0, 600)
        fallingEnemyY = 0
        self.x = fallingEnemyX
        self.y = fallingEnemyY
        self.width = winWidth
        self.height = winHeight
        self.rect = self.image.get_rect()
        position -= randint(0, 10000)
        self.position = position
        self.game = game

    def checkCollision(self, game):
        for rocket in game.rockets:
            if rocket.x < self.x + self.rect and Laser.x > self.x - self.rect and Laser.y < self.y + self.rect and Laser.y > self.y - self.rect:
                return True

    def fall(self, enemyFighterSpeed):
        self.position += enemyFighterSpeed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.position))

if __name__ == "__main__":
    pygame.init()
    Game_Window = pygame.display.set_mode((winWidth, winHeight))
    bkg_texture = pygame.transform.scale((pygame.image.load(images[0])), (winWidth, winHeight))
    BkgSprite1 = Background(bkg_texture, winWidth * (-1), 0)
    BkgSprite2 = Background(bkg_texture, 0, 0)
    BkgSprite3 = Background(bkg_texture, winWidth, 0)

    spritesList.add(BkgSprite1)
    spritesList.add(BkgSprite2)
    spritesList.add(BkgSprite3)

screen = pg.display.set_mode((600, 480))
screen_rect = screen.get_rect()
player = Player(screen_rect)
playerGroup.add(player)
ENEMY_IMAGE = enemy_image_load()

for i in range(100):
    enemyFighter = fallingEnemy(screen_rect, 20, (480, 600))
    enemyFighterList.append(enemyFighter)

enemy = Enemy(ENEMY_IMAGE, screen_rect)

clock = pg.time.Clock()

done = False
while not done:
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        player.get_event(event)
    delta_time = clock.tick(60) / 1000.0
    player.update(keys, delta_time)
    enemy.update(player)
    spritesList.update()
    BkgSprite1.draw(Game_Window)
    BkgSprite2.draw(Game_Window)
    BkgSprite3.draw(Game_Window)
    player.draw(screen)
    enemy.draw(screen)
    for enemyFighter in enemyFighterList:
        enemyFighter.draw(screen)
        enemyFighter.fall(enemyFighterSpeed)
        enemyFighterGroup.add(enemyFighter)
    check1 = enemyFighter.checkCollision()
    if check1 == True:
        print('collision')
    pg.display.update()
