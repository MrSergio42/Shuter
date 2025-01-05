from pygame import *
from random import randint

init()

W = 500
H = 700
fps = 60

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
        if self.rect.y > H - self.height:
            self.rect.x = randint(0, W - self.weight)
            self.rect.y = 0

player = Player(W / 2, H - 140, 5, "images/51fQqBomGhL-removebg-preview.png", 130, 140)
enemis = sprite.Group()
for i in range(5):
    enemy = Enemy(randint(0, W - 70), randint(-35, 0), randint(1, 5), "images/ufo.png", 70, 35)
    enemis.add(enemy)

venom1 = Venom(randint(0, W - 70), randint(-35, 0), randint(1, 5), "images/asteroid.png", 70, 35)

life = 3
kill = 0
skiped = 0

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(bg, (0, 0))

    player.draw()
    player.move()

    enemis.draw(window)
    enemis.update()

    venom1.draw()
    venom1.update()


    display.flip()
    clock.tick(fps)      