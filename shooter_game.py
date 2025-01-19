#Создай собственный Шутер!
from time import time as timer
from pygame import *
from random import randint
window = display.set_mode((700,500))
display.set_caption('Шутер')
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
bullet_sound = mixer.Sound('fire.ogg')
mixer.music.set_volume(0)
bullet_sound.set_volume(0)
background = transform.scale(image.load('galaxy.jpg'), (700,500))
bcount = 0
gcount = 0
life = 3
num_fire = 0
game = True
finish = False
rel_time = False
clock = time.Clock()
FPS = 60
class GameSprite(sprite.Sprite):
    def __init__(self, qimage, x, y, qspeed, qx, qy):
        super().__init__()
        self.image = transform.scale(image.load(qimage), (qx,qy))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = qspeed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 15,20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        direction = 'down'
        global bcount
        if self.rect.y >= -70:
            self.rect.y += self.speed
        if self.rect.y >= 550:
            self.rect.y = -70            
            self.rect.x = randint(5,630)
            bcount += 1

class Bullet(GameSprite):
    def update(self):
        direction = 'up'
        self.rect.y -= self.speed
        if self.rect.y <= -70:
            self.kill()

font.init()
font2 = font.SysFont('Arial',80)
font1 = font.SysFont("Arial", 36)
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png',randint(200,500),-70,randint(1,3),80,50)
    asteroids.add(asteroid)

for i in range(5):
    monster = Enemy('ufo.png',randint(200,500),-70,randint(1,3),80,50)
    monsters.add(monster)
player = Player('rocket.png',350,430,5,65,65)

win = font2.render('YOU WIN',1,(255,255,0)) 
lose = font2.render('YOU LOSE', 1, (255,0,0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    bullet_sound.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start = timer()

    if finish != True:
        window.blit(background, (0,0))

        player.update()
        bullets.update()
        asteroids.update()
        monsters.draw(window)
        player.reset()
        monsters.update()
        bullets.draw(window)
        asteroids.draw(window)

        sprite_list = sprite.groupcollide(monsters,bullets, True, True)
        for i in sprite_list:
            gcount += 1
            monster = Enemy('ufo.png',randint(200,500),-70,randint(1,5),80,50)
            monsters.add(monster)

        text_lose = font1.render('Пропущенно: ' + str(bcount), 1, (255,255,255))

        if gcount == 100:
            finish = True
            window.blit(win, (200,250))
        
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life = life - 1

        if bcount >= 7 or life == 0:
            finish = True
            window.blit(lose, (200,250))

        if rel_time == True:
            end = timer()

            if end - start < 3:
                text_reload = font1.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(text_reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False 

        text_win = font1.render('Счёт: ' + str(gcount), 1, (255,255,255))
        text_life = font2.render(str(life), 1, (150, 0, 0))
        window.blit(text_life, (650, 10))
        window.blit(text_lose, (10,40))
        window.blit(text_win, (10,20))
        

    display.update()
    clock.tick(FPS)

