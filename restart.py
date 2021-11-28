from pygame import *
'''Необходимые классы'''

#класс-родитель для спрайтов 
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys [K_a]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if (keys[K_UP] or keys[K_w]) and self.rect.y > 5:
            self.rect.y -= self.speed
        if (keys[K_DOWN] or keys[K_s])and self.rect.y < win_height -80:
            self.rect.y += self.speed













#класс-наследник для спрайта-врага (перемещается сам)
class Enemy(GameSprite):
    side = "left"
    def update(self):
        if self.rect.x <= 470:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

#класс для спрайтов-препятствий
class Wall(sprite.Sprite):
    """Делай шо хош"""
    def __init__(self, **args):
        super().__init__()
        if args.get('color') == None:
            self.color = (255, 0, 0)
        else:
            self.color = args['color']
        self.width = args['size'][0]
        self.height = args['size'][1]
 
        self.image = Surface([self.width, self.height])
        self.image.fill(self.color)
 
        self.rect = self.image.get_rect()
        self.rect.x = args['position'][0]
        self.rect.y = args['position'][1]
 
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        #draw.rect(window, self.color, self.rect)

'''Описание игры'''

#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

w1 = Wall(color = (154, 205, 50), position = (100, 20), size = (450, 10))
w2 = Wall(color = (154, 205, 50), position = (100, 480), size = (350, 10))
w3 = Wall(color = (154, 205, 50), position = (100, 20), size = (10, 380))
w4 = Wall(color = (154, 205, 50), position = (200, 130), size = (10, 350))
w5 = Wall(color = (154, 205, 50), position = (450, 130), size = (10, 360))
w6 = Wall(color = (154, 205, 50), position = (300, 20), size = (10, 350))
w7 = Wall(color = (154, 205, 50), position = (390, 120), size = (130, 10))

#Персонажи игры:
packman = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

game = True
finish = False
clock = time.Clock()

font.init()
font_basic = font.SysFont('Corbel', 50, True, True)
font_attempts = font.SysFont('Corbel', 17, True)
win = font_basic.render('Ты выиграл! +1 попытка', True, (255, 215, 0))
lose = font_basic.render('Ты проиграл! -1 попытка', True, (180, 0, 0), (0,0,0)) ## !!!
restart = font_basic.render('Нажми R для перезапуска', True, (180, 0, 0))
exit_text = font_basic.render('Нажми Q для выхода', True, (180, 0, 0))
attempts = 5
attempts_text = font_attempts.render(f'Осталось {attempts} попыток', True, (255, 255, 255))

#музыка
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.set_volume(.3)
mixer.music.play(-1)

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

def collide(is_win = True):
    global attempts, finish, attempts_text
    finish = True
    if is_win:
        attempts+=1
        window.blit(win, (50, 200))
        window.blit(restart, (40, 250))
    else:
        attempts-=1
        window.blit(lose, (50, 200))
        if attempts != 0:
            window.blit(restart, (40, 250))
        else:
            window.blit(exit_text, (80, 250))
    attempts_text = font_attempts.render(f'Осталось {attempts} попыток', True, (255, 255, 255))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_r and finish and attempts > 0:
                packman = Player('hero.png', 5, win_height - 80, 4)
                finish = False
            if e.key == K_q:
                game = False

    if not finish:
        window.blit(background,(0, 0))
        
        packman.update()
        monster.update()
        #sdagsfdgsfdg
        packman.reset()
        monster.reset()
        final.reset() 
        
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()
        
        #Ситуация "Проигрыш" asdfsdfasdfasdfasdf
        if (sprite.collide_rect(packman, monster) or 
        sprite.collide_rect(packman, w1) or 
        sprite.collide_rect(packman, w2) or 
        sprite.collide_rect(packman, w2) or 
        sprite.collide_rect(packman, w3) or 
        sprite.collide_rect(packman, w4) or 
        sprite.collide_rect(packman, w5) or 
        sprite.collide_rect(packman, w6) or 
        sprite.collide_rect(packman, w7)):
            collide(False)
            kick.play()

        #Ситуация "Выигрыш"
        if sprite.collide_rect(packman, final):
            collide(True)
            money.play()
        window.blit(attempts_text, (5,5))
        display.update()
    clock.tick(60)