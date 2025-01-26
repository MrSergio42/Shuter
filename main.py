from pygame import *
from random import randint

init()

W = 500
H = 700
FPS = 60

life = 3
kill = 0
skiped = 0

mixer.init()
mixer.music.load("sounds/space.ogg")
mixer.music.set_volume(0.3)
mixer.music.play()

fire_snd = mixer.Sound("sounds/fire.ogg")

font.init()
font1 = font.SysFont("fonts/Bebas_Neue_Cyrillic.ttf", 35, bold=True)
font2 = font.SysFont("fonts/Bebas_Neue_Cyrillic.ttf", 20, bold=True)

window = display.set_mode((W, H))
display.set_caption("Shoter")

bg = transform.scale(image.load("images/galaxy.jpg"), (W, H))

clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, speed, img, weight, height):
        super().__init__()
        self.speed = speed
        self.image = transform.scale(image.load(img), (weight, height))
        self.weight = weight
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys_presed = key.get_pressed()
        if keys_presed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_presed[K_d] and self.rect.x < W -  self.weight:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 20, "images/bullet.png", 15, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global kill
        self.rect.y += self.speed
        if self.rect.y > H - self.height:
            self.rect.x = randint(0, W - self.weight)
            self.rect.y = 0
            kill += 1

class Venom(GameSprite):
    def __init__(self, x, y, speed, img, weight, height):
        super().__init__(x, y, speed, img, weight, height)
        self.angel = 0
        self.original_image = self.image

    def update(self):
        self.rect.y += self.speed
        self.angel += 2
        self.image = transform.rotate(self.original_image, self.angel)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.y > H - self.height:
            self.rect.x = randint(0, W - self.weight)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Buff(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > H - self.height:
            self.rect.x = randint(0, W - self.weight)
            self.rect.y = -100

player = Player(W / 2, H - 140, 5, "images/51fQqBomGhL-removebg-preview.png", 130, 140)

life_boost = Buff(randint(0, W - 50), -100, randint(2, 5), "images/hell_box.png", 50, 50)
armo_boost = Buff(randint(0, W - 50), -100, randint(2, 5), "images/bull_box.png", 50, 50)

enemis = sprite.Group()
for i in range(5):
    enemy = Enemy(randint(0, W - 70), randint(-35, 0), randint(1, 5), "images/ufo.png", 70, 35)
    enemis.add(enemy)

venom1 = Venom(randint(0, W - 70), randint(-35, 0), randint(1, 5), "images/asteroid.png", 70, 35)

venoms = sprite.Group()
for i in range(3):
    venom1 = Venom(randint(0, W - 70), randint(-35, 10), randint(1, 3), "images/asteroid.png", 70, 35)
    venoms.add(venom1)

bullets = sprite.Group() 

game = True
finish = False
shut_count = 30
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if shut_count > 0:
                    fire_snd.play()
                    player.fire()
                    shut_count -= 1
            if e.key == K_ESCAPE:
                finish = False
    if not finish:
        window.blit(bg, (0, 0))

        player.draw()
        player.move()

        enemis.draw(window)
        enemis.update()

        venom1.draw()
        venom1.update()

        bullets.draw(window)
        bullets.update()

        life_boost.draw()
        life_boost.update()

        armo_boost.draw()
        armo_boost.update()

        if sprite.groupcollide(bullets, enemis, True, True):
            kill += 1
            enemy = Enemy(randint(0, W - 70), randint(-35, 10), randint(1, 3), "images/ufo.png", 70, 35)
            enemis.add(enemy)

        if sprite.groupcollide(bullets, venoms, True, False):
            pass

        if sprite.spritecollide(player, venoms, True):
            life -= 1
            venom = Venom(randint(0, W - 70), randint(-35, 10), randint(1, 3), "images/asteroid.png", 70, 35)
            venoms.add(venom)

        if sprite.spritecollide(player, enemis, True):
            life -= 1
            enemy = Enemy(randint(0, W - 70), randint(-35, 10), randint(1, 3), "images/ufo.png", 70, 35)
            enemis.add(enemy)

        if life == 0:
            finish = True

        skiped_txt = font1.render(f"Пропущено: {skiped}", True, (255, 255, 255))
        kill_txt = font1.render(f"Вбито: {kill}", True, (255, 255, 255))
        life_txt = font1.render(f"Життя: {life}", True, (255, 255, 255))
        shut_count_txt = font1.render(f"Боеприпаси: {shut_count}", True, (255, 255, 255))

        window.blit(skiped_txt, (10, 10))
        window.blit(kill_txt, (10, 35))
        window.blit(life_txt, (10, 60))
        window.blit(shut_count_txt, (10, 85))
    else:
        life = 3
        skiped = 0
        kill = 0
        shut_count = 30
        for enemy in enemis:
            enemy.kill()
            for venom in venoms:
                venom.kill()
            for bullet in bullets:
                bullet.kill()

        for i in range(3):
            venom1 = Venom(randint(0, W - 70), randint(-35, 10), randint(1, 3), "images/asteroid.png", 70, 35)
            venoms.add(venom1)

        for i in range(5):
            enemy = Enemy(randint(0, W - 70), randint(-35, 0), randint(1, 5), "images/ufo.png", 70, 35)
            enemis.add(enemy)

    display.update()
    clock.tick(FPS)