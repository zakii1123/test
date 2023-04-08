from pygame import *
import pygame
from random import *
pygame.init()

mixer.init()

 

width, height = 800, 500
window = display.set_mode((width, height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (width, height))

hp1 = transform.scale(image.load("hp1.png"), (125, 70))
hp2 = transform.scale(image.load("hp2.png"), (125, 70))
hp3 = transform.scale(image.load("hp3.png"), (125, 70))
num_hp = 3



class GameSprite(sprite.Sprite):  
    def __init__(self, player_image, player_x, player_y, w_sprite, h_sprite, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w_sprite, h_sprite))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 1:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 750:
            self.rect.x += self.speed
    def shot(self):
        bullet = Bullets("bullet.png", self.rect.centerx, self.rect.top, 10, 15, 10)
        bullets.add(bullet)
        
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y = self.rect.y + self.speed
        global lost
        global num_hp
        if self.rect.y > height:
            self.rect.x = randint(0, width - 30)
            self.rect.y = -30
            lost += 1 
            num_hp -= 1  

class Bullets(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()



# class Bonus_Of_Damage(GameSprite):
#     global bonus_spawn
#     bonus_spawn = choice([0,1])
#     def update(self):
#         if bonus_spawn == 1:
#             self.rect.y += self.speed
#             if self.rect.y < 0:
#                 self.kill()
              

global game

def pause():
    
    paused = True
    while paused: 
         for e in event.get():
            if e.type == QUIT:
                game = False
    
            pause = font.render("Нажмите Esc, что бы продолжить", 5, (255, 255, 255))
            window.blit(pause, (width//2 - 150, height//2))
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                paused = False


            pygame.display.update()
            clock.tick(FPS)            


font = pygame.font.SysFont("calibri", 20) 
font2 = pygame.font.SysFont("calibri", 35) 

# killall = Bonus_Of_Damage("chmo.jpg", randint(0, width - 80), 0, 50, 50, 3)

bonuses = sprite.Group()
# killall.add(bonuses)
player = Player("rocket.png", 350, 425, 50, 50, 10)
monsters = sprite.Group()
random_enemy = ["ufo.png", "asteroid.png"]
for i in range(6):  
    monster = Enemy(choice(random_enemy)  , randint(0, width - 80), -40, 50, 50, randint(1, 3))
    monsters.add(monster)

bullets = sprite.Group()
score = 0
clock = time.Clock()
FPS = 55
finish = True 
game = True


while game:
    if num_hp >= 0:

        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN and e.key == K_SPACE:
                player.shot()
            if   lost >= 10:
                game = False    
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                pause()



        collide = sprite.groupcollide(monsters, bullets, True, True)
        for c in collide:
            score += 1 
            bonus_spawn = choice([0,1])
            monster = Enemy(choice(random_enemy),randint(0, width - 80), -40, 50, 50, randint(1, 5))
            monsters.add(monster)
        # collide2 = sprite.spritecollide(player, bonuses, True)
        # for c in collide2:
        #     for i in monsters:
        #         i.kill()  
        #         for i in range(1):  
        #             monster = Enemy(choice(random_enemy)  , randint(0, width - 80), -40, 50, 50, randint(1, 3))
        #             monsters.add(monster)
          

        pattern_lost_scores = font.render("Промахи: " +  str(lost), 0, (255, 255, 255))
        player_scores = font.render("Очки: " + str(score), 0, (255, 255, 255))

        window.blit(background,(0,0))
        window.blit(pattern_lost_scores,(10,10))
        window.blit(player_scores,(730,10))
        if num_hp == 3:
            window.blit(hp3, (0, 20)) 
        if num_hp == 2:
            window.blit(hp2, (0, 20)) 
        if num_hp == 1:
            window.blit(hp1, (0, 20))
        monsters.update()
        monsters.draw(window)
        player.update()
        player.reset()
        bullets.update()
        bullets.draw(window)
        
        bonuses.update()
        bonuses.draw(window)
        display.update()
        clock.tick(FPS)
    

    
    else:
        window.fill((0,0,0))
        num = font2.render("Ты проиграл ", 0, (255, 255, 255))
        window.blit(num, (width//2 - 100, height//2))
        m_x, m_y = pygame.mouse.get_pos()
        btn = pygame.Rect(100, 200, 100, 100)
        pygame.draw.rect(window, (255,255,255), btn)
        for e in event.get():
            if e.type == QUIT:
                game = False
            if btn.collidepoint(m_x, m_y) and e.type == MOUSEBUTTONDOWN:
                num_hp = 3

            display.update()

            # mixer.music.load('kak.mp3')
            # mixer.music.play()    
            