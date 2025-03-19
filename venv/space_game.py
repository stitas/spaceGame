import pygame, random

pygame.init()

width = 1024
height = 1024

win = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

blue = (52,204,255)
green = (0,255,0)
white = (255,255,255)
red = (255,0,0)

lifes_pos = [920,5]
level_pos = [920,20]
title_pos = [214,128]
play_pos = [433,363]
controls_pos = [353,463]
quit_game_pos = [433,563]
controls_title_pos = [355,128]
up_pos = [134,250]
down_pos = [134,350]
left_pos = [134,450]
right_pos = [134,550]
lctrl_pos = [134,650]
back_pos = [433,800]
game_over_pos = [334,128]
play_again_pos = [314,250]
main_menu_pos = [434,350]
quit_pos = [434,450]

play_button_rect = [288,350,447,60]
controls_button_rect = [288,450,447,60]
quit_game_button_rect = [288,550,447,60]
controls_rect = [124,240,775,450]
back_rect = [420,787,182,60]
play_again_rect = [288,237,447,60]
main_menu_rect = [288,337,447,60]
quit_rect = [288,437,447,60]
title_rect1 = [214, 165, 596, 20]
title_rect2 = [262, 186, 500, 20]
title_rect3 = [310, 207, 404, 20]
title_rect4 = [358, 228, 308, 20]
title_rect5 = [406, 249, 212, 20]
title_rect6 = [454, 270, 116, 20]
title_rect7 = [502, 291, 20, 20]


player_ship = pygame.image.load(r'assets\starship.png')
asteroid_img = pygame.image.load(r'assets\asteroid.png')
laser_blue = pygame.image.load(r'assets\projectileblue.png')
bg = pygame.image.load(r'assets\space.png')

explosions = [pygame.image.load(r'assets\regularExplosion00.png'),pygame.image.load(r'assets\regularExplosion01.png'),
              pygame.image.load(r'assets\regularExplosion02.png'),pygame.image.load(r'assets\regularExplosion03.png'),
              pygame.image.load(r'assets\regularExplosion04.png'),pygame.image.load(r'assets\regularExplosion05.png'),
              pygame.image.load(r'assets\regularExplosion06.png'),pygame.image.load(r'assets\regularExplosion07.png'),
              pygame.image.load(r'assets\regularExplosion08.png')]

pygame.font.init()
font_small = pygame.font.Font(r'assets\font.ttf',15)
font_big = pygame.font.Font(r'assets\font.ttf',40)

ship_pos = []
life = 3
eleminations = 0
health_bar = 100

class Asteroid(pygame.sprite.Sprite):
    def __init__(self,x,y,image,vel):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.vel = vel
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args, **kwargs) -> None:
        global life
        self.rect.center = [self.x,self.y]
        self.y += self.vel
        if self.y in range(1050,1500):
            self.kill()
            health.get_damage()

class Laser(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [-100,-100]

    def update(self, *args, **kwargs) -> None:
        self.rect.center = [self.x, self.y]
        self.mask = pygame.mask.from_surface(self.image)
        self.keys = pygame.key.get_pressed()
        self.y -= 20
        if self.y <= -100:
            self.kill()
        for laser in laser_group:
            if pygame.sprite.spritecollide(laser,asteroid_group,True,pygame.sprite.collide_mask):
                global eleminations
                eleminations += 1
                explosion.get_pos(self.x, self.y)
                self.kill()

class Ship(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.vel = 15
        self.rect = self.image.get_rect()

    def create_laser(self):
        return Laser(self.x,self.y,laser_blue)

    def update(self, *args, **kwargs) -> None:
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = [self.x, self.y]
        if len(ship_pos) >= 2:
            for pos in range(0,len(ship_pos)-1):
                ship_pos.pop(0)
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_UP] and self.rect.center[1] != 51:
            self.y -= self.vel
        if self.keys[pygame.K_DOWN] and self.rect.center[1] != 966:
            self.y += self.vel
        if self.keys[pygame.K_LEFT] and self.rect.center[0] != 46:
            self.x -= self.vel
        if self.keys[pygame.K_RIGHT] and self.rect.center[0] != 976:
            self.x += self.vel
        ship_pos.append(self.rect.center)
        if pygame.sprite.spritecollide(ship,asteroid_group,True,pygame.sprite.collide_mask):
            explosion.get_pos(self.x,self.y)
            health.get_damage()

class Health(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = health_bar
        self.height = height
        self.width_border = width + 2
        self.xr = x
        self.yr = y
        self.widthr = width
        self.heightr = height
        self.image = pygame.Surface([self.width,self.height])
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_damage(self):
        global health_bar
        global life
        self.damage = random.randrange(15, 20)
        if health_bar > 0:
            health_bar -= self.damage
            self.width -= self.damage
        if health_bar <= 0:
            life -= 1
            health_bar = 100
            self.width = health_bar

    def update(self, *args, **kwargs) -> None:
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect1 = pygame.Rect(self.x-1,self.y-1,self.width_border,self.height+2)
        self.rect2 = pygame.Rect(self.xr, self.yr, self.widthr, self.heightr)
        pygame.draw.rect(win,white,self.rect1,1)
        pygame.draw.rect(win,red,self.rect2)
        pygame.draw.rect(win,green,self.rect)

class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.explode = False
        self.index = 0
        self.image = explosions[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [-100,-100]

    def get_pos(self,x,y):
        self.x = x
        self.y = y
        self.explode = True

    def update(self, *args, **kwargs) -> None:
        global explosions
        if self.explode:
            self.index += 0.5
            self.rect.center = [self.x,self.y]
            if self.index < len(explosions) and self.index % 1 == 0:
                self.image = explosions[int(self.index)]
            elif self.index > len(explosions):
                self.index = 0
                self.explode = False

def lifes(lifes):
    value = font_small.render('LIFES:' + str(lifes),True,blue)
    win.blit(value,lifes_pos)

def lvl(level):
    value = font_small.render('LEVEL:' + str(level),True,blue)
    win.blit(value,level_pos)

def title():
    value = font_big.render('ASTEROID ATTACK',True,blue)
    win.blit(value,title_pos)
    pygame.draw.rect(win,blue,title_rect1)
    pygame.draw.rect(win,blue,title_rect2)
    pygame.draw.rect(win,blue,title_rect3)
    pygame.draw.rect(win,blue,title_rect4)
    pygame.draw.rect(win,blue,title_rect5)
    pygame.draw.rect(win,blue,title_rect6)

def play_button():
    pygame.draw.rect(win,blue,play_button_rect,1)
    value = font_big.render('PLAY',True,blue)
    win.blit(value,play_pos)
    if pygame.mouse.get_pos()[0] in range(288,736):
        if pygame.mouse.get_pos()[1] in range(350,411):
            pygame.draw.rect(win,white,play_button_rect)
            pygame.draw.rect(win,blue,play_button_rect,3)
            win.blit(value,play_pos)


def controls_button():
    pygame.draw.rect(win,blue,controls_button_rect,1)
    value = font_big.render('CONTROLS',True,blue)
    win.blit(value,controls_pos)
    if pygame.mouse.get_pos()[0] in range(288,736):
        if pygame.mouse.get_pos()[1] in range(450,511):
            pygame.draw.rect(win,white,controls_button_rect)
            pygame.draw.rect(win,blue,controls_button_rect,3)
            win.blit(value,controls_pos)

def quit_game():
    pygame.draw.rect(win,blue,quit_game_button_rect,1)
    value = font_big.render('QUIT',True,blue)
    win.blit(value,quit_game_pos)
    if pygame.mouse.get_pos()[0] in range(288,736):
        if pygame.mouse.get_pos()[1] in range(550,611):
            pygame.draw.rect(win,white,quit_game_button_rect)
            pygame.draw.rect(win,blue,quit_game_button_rect,3)
            win.blit(value,quit_game_pos)

def controls_win():
    title_value = font_big.render('CONTROLS',True,blue)
    up_value = font_big.render('UP: MOVE FORWARD',True,blue)
    down_value = font_big.render('DOWN: MOVE DOWNWARD', True, blue)
    left_value = font_big.render('LEFT: MOVE LEFT', True, blue)
    right_value = font_big.render('RIGHT: MOVE RIGHT', True, blue)
    lctrl_value = font_big.render('LCTRL: SHOOT LASER', True, blue)
    back_value = font_big.render('BACK',True,blue)
    win.blit(title_value,controls_title_pos)
    win.blit(up_value,up_pos)
    win.blit(down_value,down_pos)
    win.blit(left_value,left_pos)
    win.blit(right_value,right_pos)
    win.blit(lctrl_value,lctrl_pos)
    win.blit(back_value,back_pos)
    pygame.draw.rect(win,blue,controls_rect,1)
    pygame.draw.rect(win,blue,back_rect,1)
    if pygame.mouse.get_pos()[0] in range(420,603):
        if pygame.mouse.get_pos()[1] in range(787,848):
            pygame.draw.rect(win,white,back_rect)
            pygame.draw.rect(win,blue,back_rect,3)
            win.blit(back_value,back_pos)

def game_over_win():
    title_value = font_big.render('GAME OVER',True,blue)
    play_again_value = font_big.render('PLAY AGAIN',True,blue)
    main_menu_value = font_big.render('MENU',True,blue)
    quit_value = font_big.render('QUIT',True,blue)
    win.blit(title_value,game_over_pos)
    win.blit(play_again_value,play_again_pos)
    win.blit(main_menu_value,main_menu_pos)
    win.blit(quit_value,quit_pos)
    pygame.draw.rect(win,blue,play_again_rect,1)
    pygame.draw.rect(win,blue,main_menu_rect,1)
    pygame.draw.rect(win,blue,quit_rect,1)
    if pygame.mouse.get_pos()[0] in range(288,735):
        if pygame.mouse.get_pos()[1] in range(237,297):
            pygame.draw.rect(win,white,play_again_rect)
            pygame.draw.rect(win,white,play_again_rect,1)
            win.blit(play_again_value,play_again_pos)
    if pygame.mouse.get_pos()[0] in range(288,735):
        if pygame.mouse.get_pos()[1] in range(337,397):
            pygame.draw.rect(win,white,main_menu_rect)
            pygame.draw.rect(win,white,main_menu_rect,1)
            win.blit(main_menu_value,main_menu_pos)
    if pygame.mouse.get_pos()[0] in range(288,735):
        if pygame.mouse.get_pos()[1] in range(437,497):
            pygame.draw.rect(win,white,quit_rect)
            pygame.draw.rect(win,white,quit_rect,1)
            win.blit(quit_value,quit_pos)


def levels():
    global level
    if eleminations <= 30:
        level = 1
        if len(asteroid_group) < 2:
            asteroid = Asteroid(random.randrange(51, 966), random.randrange(-50, -10), asteroid_img, random.randrange(1, 2))
            asteroid_group.add(asteroid)
            asteroid.update()
    elif 30 <= eleminations <= 60:
        level = 2
        if len(asteroid_group) < 3:
            asteroid = Asteroid(random.randrange(51, 966), random.randrange(-50, -10), asteroid_img, random.randrange(1, 3))
            asteroid_group.add(asteroid)
            asteroid.update()
    elif 60 <= eleminations <= 90:
        level = 3
        if len(asteroid_group) < 4:
            asteroid = Asteroid(random.randrange(51, 966), random.randrange(-50, -10), asteroid_img, random.randrange(1, 3))
            asteroid_group.add(asteroid)
            asteroid.update()
    elif 90 <= eleminations <= 120:
        level = 4
        if len(asteroid_group) < 5:
            asteroid = Asteroid(random.randrange(51, 966), random.randrange(-50, -10), asteroid_img, random.randrange(1, 4))
            asteroid_group.add(asteroid)
            asteroid.update()
    elif 120 <= eleminations <= 150:
        level = 5
        if len(asteroid_group) < 6:
            asteroid = Asteroid(random.randrange(51, 966), random.randrange(-50, -10), asteroid_img, random.randrange(1, 5))
            asteroid_group.add(asteroid)
            asteroid.update()
    elif eleminations > 150:
        level = 'You Win'

ship = Ship(526,726,player_ship)
ship_group = pygame.sprite.Group()
ship_group.add(ship)

laser_group = pygame.sprite.Group()

health = Health(10,10,100,10)
health_group = pygame.sprite.Group()
health_group.add(health)

explosion = Explosion()
explosion_group = pygame.sprite.Group()
explosion_group.add(explosion)

asteroid = Asteroid(0,0,asteroid_img,0)
asteroid_group = pygame.sprite.Group()

def game_over():
    run = True
    while run:
        print(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] in range(288,735):
                    if pygame.mouse.get_pos()[1] in range(237,297):
                        main()
                        run = False
                if pygame.mouse.get_pos()[0] in range(288,735):
                    if pygame.mouse.get_pos()[1] in range(337,397):
                        menu()
                        run = False
                if pygame.mouse.get_pos()[0] in range(288,735):
                    if pygame.mouse.get_pos()[1] in range(437,497):
                        quit()

        win.blit(bg,(0,0))

        game_over_win()

        pygame.display.update()
        clock.tick(60)

def controls_menu():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] in range(420, 603):
                    if pygame.mouse.get_pos()[1] in range(787, 848):
                        menu()

        win.blit(bg,(0,0))

        controls_win()

        pygame.display.update()
        clock.tick(60)

def menu():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] in range(288, 736):
                    if pygame.mouse.get_pos()[1] in range(350, 411):
                        main()
                if pygame.mouse.get_pos()[0] in range(288, 736):
                    if pygame.mouse.get_pos()[1] in range(450, 511):
                        controls_menu()
                if pygame.mouse.get_pos()[0] in range(288, 736):
                    if pygame.mouse.get_pos()[1] in range(550, 611):
                        quit()

        win.blit(bg,(0,0))

        title()
        play_button()
        controls_button()
        quit_game()

        pygame.display.update()
        clock.tick(60)

def main():
    global life
    global level
    global laser_group
    global asteroid_group
    global ship_group
    global health_group
    global explosion_group
    run=True
    while run:
        levels()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    laser_group.add(ship.create_laser())

        if life == 0:
            run = False
            life = 3
            game_over()
            ship_group = pygame.sprite.Group()

            laser_group = pygame.sprite.Group()

            health_group = pygame.sprite.Group()

            explosion_group = pygame.sprite.Group()

            asteroid_group = pygame.sprite.Group()

            eleminations = 0

            level = 1

        win.blit(bg,(0,0))

        laser_group.draw(win)
        laser_group.update()

        asteroid_group.draw(win)
        asteroid_group.update()

        ship_group.draw(win)
        ship_group.update()

        health_group.draw(win)
        health_group.update()

        explosion_group.draw(win)
        explosion_group.update()

        lifes(life)
        lvl(level)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    menu()
