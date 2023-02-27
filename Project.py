import sys
from random import randint, choice
from os import path, listdir, startfile
import pygame
from webbrowser import open as openweb
from sys import exit as exit_game
# Importing a libraries

pygame.mixer.pre_init()  # Initialization a mixer
pygame.init()  # Initialization a pygame


def load_image(name, colorkey=None, addpath=None):  # Load images to pygame
    if addpath:
        image = pygame.image.load(path.join(f'data/{addpath}', name))
    else:
        image = pygame.image.load(path.join(f'data', name))
    if not image:
        image = pygame.surface.Surface((200, 200), pygame.SRCALPHA)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def to_center(x: int = 0, y: int = 0):  # return a position where object be in center
    if not x:
        return (Y - y) // 2
    elif not y:
        return (X - x) // 2
    return (X - x) // 2, (Y - y) // 2


def to_coef(*n):  # Resizes to look the same on different screens
    if len(n) > 1:
        return tuple([int(q * coef) for q in n])
    return int(n[0] * coef)


def go_start():  # Starts a game
    global GAMEMODE, tm
    GAMEMODE = 12
    tm = FPS * 3


def start_game():  # Starting a game process
    global GAMEMODE, s, tb, score1, sprite_group_game, tm, img
    sprite_group_game = pygame.sprite.Group()
    GAMEMODE = 1
    tb = []
    s = 0
    score1 = 0
    img = pygame.transform.scale(load_image(list_targets[target], addpath='target'), to_coef(180, 180))
    for _ in range(objects):
        a = Target(to_coef(90))
        sprite_group_game.add(a)
    pygame.mouse.set_pos(to_center(1, 1))
    pygame.mixer.music.pause()


def go_menu():  # Return to menu
    global GAMEMODE, total
    stop_btn.change('stop.png')
    GAMEMODE = 0
    total = 50
    pygame.mixer.music.unpause()


def go_out():  # Exit the game
    global GAMEMODE
    GAMEMODE = -1


def go_help():  # Open a help window
    global GAMEMODE
    GAMEMODE = 2


def go_info():  # Open an information window
    global GAMEMODE
    GAMEMODE = 3


def to_hard():  # Start hard mode
    global total, objects
    total = 1000
    objects = 7
    go_start()


def pause():  # Pause the game
    global GAMEMODE
    if GAMEMODE == 1:
        GAMEMODE = 10
        stop_btn.change('start.png')
        pygame.mixer.music.unpause()
    else:
        GAMEMODE = 1
        stop_btn.change('stop.png')
        pygame.mixer.music.pause()


def random_site():  # For advertising
    pygame.mixer.music.set_volume(0)
    pygame.display.iconify()
    openweb(choice(['https://ya.ru', 'https://google.com', 'https://ya.ru', 'https://dzen.ru', 'https://ya.ru',
                    'https://store.steampowered.com/app/730', 'https://ya.ru',
                    'https://www.youtube.com/watch?v=dQw4w9WgXcQ']))


def add_target():  # Add a new target
    pygame.mixer.music.set_volume(0)
    pygame.display.iconify()
    t = sys.argv[0].rsplit('\\', maxsplit=1)[0]
    startfile(f'{t}/data/target')


def target_name():
    name = list_targets[target].rsplit('.', maxsplit=1)[0]
    if len(name) > 12:
        return name[:10] + '...'
    return name


def objects_count(n):  # Change an objects in game
    global objects
    objects = n
    for oc in range(1, 6):
        if oc != n:
            ocl[oc - 1].change(str(oc))
        else:
            ocl[oc - 1].change('#')


def create_tb(siz2):  # Create a game process
    while True:
        x1, y1 = randint(100, X - 100), randint(to_coef(300), Y - 100)
        fl = True
        for xy in tb:
            if (xy[0] - x1) ** 2 + (xy[1] - y1) ** 2 <= siz2 ** 2:
                fl = False
                break
        if fl:
            tb.append((x1, y1))
            return x1, y1


class Cursor:
    """Change a cursor in game"""
    def __init__(self, cur, size):
        pygame.mouse.set_visible(False)
        self.cursor = pygame.transform.scale(load_image(cur), size)
        self.x, self.y = map(lambda p: p // 4, size)

    def update(self, scr, pos_x, pos_y):
        scr.blit(self.cursor, (pos_x - self.x, pos_y - self.y))


class Button(pygame.sprite.Sprite):
    """This is a base class of buttons"""

    def __init__(self):
        """Initialization a new button"""
        pygame.sprite.Sprite.__init__(self)

    def update(self):
        """Update buttons"""
        if event.type == pygame.MOUSEMOTION:
            if self.fl and self.x - self.sx < event.pos[0] < self.x + self.sx and \
                    self.y - self.sy < event.pos[1] < self.y + self.sy:
                self.image = self.image2
            else:
                self.image = self.image1
        global is_press
        if event.type == pygame.MOUSEBUTTONDOWN and not is_press and self.timer > 10:
            if self.x - self.sx < event.pos[0] < self.x + self.sx and \
                    self.y - self.sy < event.pos[1] < self.y + self.sy:
                self.timer = 0
                self.func()
                is_press = True
        self.timer += 1


class ImageButton(Button):
    """This is a class of button with image"""

    def __init__(self, im: str, func, center: tuple = (0, 0), size: tuple = (100, 100),
                 border_color: pygame.Color = pygame.SRCALPHA, hover: str = None):
        super(ImageButton, self).__init__()

        self.image1 = pygame.transform.scale(load_image(im), size)
        self.image1.convert_alpha()
        pygame.draw.rect(self.image1, border_color, [(0, 0), size], 2)
        self.fl = True if hover else False
        if self.fl:
            self.image2 = pygame.transform.scale(load_image(hover), size)
            self.image2.convert_alpha()
            pygame.draw.rect(self.image2, border_color, [(0, 0), size], 2)
        self.func = func

        self.image = self.image1

        self.rect = self.image.get_rect()
        self.x, self.y = center
        self.sx, self.sy = map(lambda n_: n_ // 2, size)
        self.rect.center = center
        self.size = size
        self.bc = border_color

        self.timer = 5

    def change(self, new_im: str, new_hover: str = None):
        """Change an old image to new"""
        self.image1 = pygame.transform.scale(load_image(new_im), self.size)
        self.image1.convert_alpha()
        pygame.draw.rect(self.image1, self.bc, [(0, 0), self.size], 2)
        if self.fl and new_hover:
            self.image2 = pygame.transform.scale(load_image(new_hover), self.size)
            self.image2.convert_alpha()
            pygame.draw.rect(self.image2, self.bc, [(0, 0), self.size], 2)

        self.image = self.image1


class TextButton(Button):
    """This is a class of button with text"""

    def __init__(self, text: str, fontb: int, func, center: tuple = (0, 0), size: tuple = (100, 100),
                 color: pygame.Color = pygame.Color('white'), back_color: pygame.Color = pygame.SRCALPHA,
                 border_color: pygame.Color = pygame.SRCALPHA, hover_color: pygame.Color = pygame.SRCALPHA,
                 hover_back_color: pygame.Color = pygame.SRCALPHA):
        super(TextButton, self).__init__()

        self.fontb = pygame.font.Font(None, fontb)
        self.x, self.y = center
        self.sx, self.sy = map(lambda n_: n_ // 2, size)
        self.size = size
        self.color = color
        self.ec = back_color
        self.bc = border_color
        self.hc = hover_color
        self.hbc = hover_back_color

        t = self.fontb.render(text, True, color)
        ts = t.get_size()
        self.image1 = pygame.Surface(size)
        self.image1.fill(back_color)
        self.image1.blit(t, (self.sx - ts[0] // 2, self.sy - ts[1] // 2))
        self.image1.convert_alpha()
        pygame.draw.rect(self.image1, border_color, [(0, 0), size], 2)
        self.fl = True if hover_color != 65536 or hover_back_color != 65536 else False
        if self.fl:
            t1 = self.fontb.render(text, True, hover_color)
            self.image2 = pygame.Surface(size)
            self.image2.fill(hover_back_color)
            self.image2.blit(t1, (self.sx - ts[0] // 2, self.sy - ts[1] // 2))
            self.image2.convert_alpha()
            pygame.draw.rect(self.image2, border_color, [(0, 0), size], 2)
        self.func = func

        self.image = self.image1

        self.rect = self.image.get_rect()
        self.rect.center = center

        self.timer = 5

    def change(self, new_text: str):
        """Change an old text to new"""
        t = self.fontb.render(new_text, True, self.color)
        ts = t.get_size()
        self.image1 = pygame.Surface(self.size)
        self.image1.fill(self.ec)
        self.image1.blit(t, (self.sx - ts[0] // 2, self.sy - ts[1] // 2))
        self.image1.convert_alpha()
        pygame.draw.rect(self.image1, self.bc, [(0, 0), self.size], 2)
        self.fl = True if self.hc != self.hbc != 65536 else False
        if self.fl:
            t1 = self.fontb.render(new_text, True, self.hc)
            self.image2 = pygame.Surface(self.size)
            self.image2.fill(self.hbc)
            self.image2.blit(t1, (self.sx - ts[0] // 2, self.sy - ts[1] // 2))
            self.image2.convert_alpha()
            pygame.draw.rect(self.image2, self.bc, [(0, 0), self.size], 2)

        self.image = self.image1


class Target(pygame.sprite.Sprite):
    """This is class of game target objects"""
    effect = pygame.mixer.Sound('data/effect.wav')

    def __init__(self, size):
        self.size = size
        sz = size * 2
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.x, self.y = create_tb(sz)
        self.rect.center = (self.x, self.y)
        self.s = s

    def update(self):
        """Update an object"""
        global is_press, score1, tb
        if event.type == pygame.MOUSEBUTTONDOWN and not is_press:
            if (self.x - event.pos[0]) ** 2 + (self.y - event.pos[1]) ** 2 <= self.size ** 2:
                self.effect.play()
                score1 += 1
                del tb[tb.index((self.x, self.y))]
                if score1 <= total - objects:
                    a = Target(self.size)
                    sprite_group_game.add(a)
                is_press = True
                self.kill()


if __name__ == '__main__':  # Run a game
    FPS = 60  # Fps
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Window of game
    pygame.display.set_caption('Aim trainer')  # Caption of window
    pygame.display.set_icon(load_image('LOGO.png'))  # Icon of window
    X, Y = screen.get_size()  # Size of window
    GAMEMODE = 0  # Game window
    is_press = False  # Check is pressed mouse buttons
    coef = X / 2560  # Coefficient of window
    list_targets = listdir('data/target')
    target = 0

    cursor = Cursor('cursor.png', to_coef(45, 50))  # Set cursor

    pygame.mixer.music.load('data/sound.mp3')  # Background music
    pygame.mixer.music.play(-1)

    # Groups of sprites
    sprite_group_0 = pygame.sprite.Group()
    sprite_group_1 = pygame.sprite.Group()
    sprite_group_game = pygame.sprite.Group()
    sprite_group_exit = pygame.sprite.Group()
    sprite_group_help = pygame.sprite.Group()
    sprite_group_info = pygame.sprite.Group()

    # Other parameters to game
    total = 50
    objects = 3
    tb = []
    s = 0
    score1 = 0
    font = pygame.font.Font(None, to_coef(180))
    fonttar = pygame.font.Font(None, to_coef(80))
    img = None
    curr_target = pygame.transform.scale(load_image(list_targets[target], addpath='target'), to_coef(360, 360))

    # Close button
    close = ImageButton('exit_static.png', go_out, to_coef(100, 100), to_coef(150, 150), hover='exit_active.png')
    sprite_group_0.add(close)
    sprite_group_1.add(close)
    sprite_group_help.add(close)
    sprite_group_info.add(close)

    # Exit button
    exit_btn = TextButton('Exit', to_coef(250), exit_game, (X // 2 - to_coef(300), Y // 2), to_coef(550, 200),
                          pygame.Color('white'), pygame.Color(255, 151, 61), pygame.Color(255, 223, 51),
                          pygame.Color('red'), pygame.Color(45, 45, 45))
    sprite_group_exit.add(exit_btn)

    # Stop exit button
    no_exit_btn = TextButton('Menu', to_coef(250), go_menu, (X // 2 + to_coef(300), Y // 2), to_coef(550, 200),
                             pygame.Color('white'), pygame.Color(255, 151, 61), pygame.Color(255, 223, 51),
                             pygame.Color('red'), pygame.Color(45, 45, 45))
    sprite_group_exit.add(no_exit_btn)

    # Pauses a game
    stop_btn = ImageButton('stop.png', pause, (X - to_coef(100), to_coef(100)), to_coef(150, 150))
    sprite_group_1.add(stop_btn)

    # Select objects button
    x_res = to_center(to_coef(790)) + to_coef(75)
    ocl = []
    for i in range(1, 6):
        btn = TextButton(str(i), to_coef(235), lambda n=i: objects_count(n), (x_res, Y // 2 - to_coef(150)),
                         to_coef(150, 150), pygame.Color('green'), pygame.Color('grey'), pygame.Color('red'),
                         pygame.Color('red'), pygame.Color(100, 100, 100))
        ocl.append(btn)
        sprite_group_0.add(btn)
        x_res += to_coef(160)
    ocl[2].change('#')

    # Start button
    start_btn = TextButton('START', to_coef(235), go_start, (X // 2, Y // 2 + 100), to_coef(600, 240),
                           back_color=pygame.Color(255, 223, 51), border_color=pygame.Color('red'),
                           hover_color=pygame.Color(255, 223, 51), hover_back_color=pygame.Color('grey'))
    sprite_group_0.add(start_btn)

    # Help window
    fonth = pygame.font.Font(None, to_coef(120))
    shs = (X - to_coef(400), Y - to_coef(400))
    surf_help = pygame.surface.Surface(shs)
    surf_help.fill(pygame.Color(50, 50, 111))
    pygame.draw.rect(surf_help, pygame.Color('red'), [(0, 0), shs], 5)
    y_res = 50

    # Information window
    with open('data/help') as help_file:
        for ln in help_file.read().split('\n'):
            txh = fonth.render(ln, True, (255, 255, 255))
            surf_help.blit(txh, (to_center(txh.get_size()[0]) - to_coef(200), to_coef(y_res)))
            y_res += 100
    surf_help_sprite = pygame.sprite.Sprite()
    surf_help_sprite.image = surf_help
    surf_help_sprite.rect = to_center(*shs)
    sprite_group_help.add(surf_help_sprite)
    surf_info = pygame.surface.Surface(shs)
    surf_info.fill(pygame.Color(50, 50, 111))
    pygame.draw.rect(surf_info, pygame.Color('red'), [(0, 0), shs], 5)
    surf_info.blit(pygame.transform.scale(load_image('LOGO.png'), to_coef(256, 256)), (shs[0] // 2 - to_coef(128), 20))
    txa = fonth.render('AIM TRAINER', True, (255, 255, 255))
    surf_info.blit(txa, (to_center(txa.get_size()[0]) - to_coef(200), to_coef(300)))
    fontv = pygame.font.Font(None, to_coef(100))
    txav = fontv.render('Version: 0.3.0', True, (255, 255, 255))
    surf_info.blit(txav, to_coef(50, 400))
    txal = fontv.render('License: GNU LESSER GENERAL PUBLIC LICENSE', True, (255, 255, 255))
    surf_info.blit(txal, to_coef(50, 500))
    txal = fontv.render('Copyright (C) 2023', True, (255, 255, 255))
    surf_info.blit(txal, to_coef(50, 600))
    txal = fontv.render('Vladimir Varenik & Dilyara Ismagilova', True, (255, 255, 255))
    surf_info.blit(txal, to_coef(50, 700))
    surf_info_sprite = pygame.sprite.Sprite()
    surf_info_sprite.image = surf_info
    surf_info_sprite.rect = to_center(*shs)
    sprite_group_info.add(surf_info_sprite)

    # Exit of help and info windows
    menu_btn = TextButton('Menu', to_coef(150), go_menu, (X - to_coef(200), to_coef(100)), to_coef(300, 150),
                          pygame.Color('purple'), border_color=pygame.Color('red'), hover_color=pygame.Color('yellow'))
    sprite_group_help.add(menu_btn)
    sprite_group_info.add(menu_btn)

    # Open a help window
    help_btn = TextButton('Help', to_coef(150), go_help, (to_coef(200), Y - to_coef(500)), to_coef(350, 150),
                          pygame.Color('purple'), border_color=pygame.Color('red'),
                          hover_color=pygame.Color(112, 20, 112))
    sprite_group_0.add(help_btn)

    # Open an information window
    info_btn = TextButton('Info', to_coef(150), go_info, (to_coef(200), Y - to_coef(300)), to_coef(350, 150),
                          pygame.Color('purple'), border_color=pygame.Color('red'),
                          hover_color=pygame.Color(112, 20, 112))
    sprite_group_0.add(info_btn)

    # Start game in hard mode
    hard_btn = TextButton('Easy?', to_coef(150), to_hard, (to_coef(200), Y - to_coef(100)), to_coef(350, 150),
                          pygame.Color(220, 120, 180), pygame.Color(127, 0, 255), pygame.Color('red'),
                          hover_color=pygame.Color('red'))
    sprite_group_0.add(hard_btn)

    # Advertising
    ad_btn = TextButton('Site', to_coef(120), random_site, (X - to_coef(150), to_coef(105)), to_coef(200, 120),
                        pygame.Color(220, 120, 180), pygame.Color(127, 0, 255), pygame.Color('red'),
                        hover_color=pygame.Color('red'))
    sprite_group_0.add(ad_btn)

    # Add a new target
    add_btn = TextButton('Add', to_coef(100), add_target, (X - to_coef(220), Y - to_coef(100)), to_coef(200, 100),
                         pygame.Color(220, 120, 180), pygame.Color(127, 0, 255), pygame.Color('red'),
                         hover_color=pygame.Color('red'))
    sprite_group_0.add(add_btn)

    # Game settings
    clock = pygame.time.Clock()
    tm = 0
    s_color = pygame.Color(255, 0, 0)

    while True:  # Game process
        clock.tick(FPS)  # Next frame timer
        for event in pygame.event.get():  # Events
            if event.type == pygame.QUIT:  # Exit
                exit_game()
            if event.type == pygame.KEYDOWN:  # Press a button in keyboard
                if event.key == pygame.K_ESCAPE:
                    GAMEMODE = -1
                elif event.key == pygame.K_F1:
                    GAMEMODE = 2 if GAMEMODE != 2 else 0
                elif event.key == pygame.K_F2:
                    mv = pygame.mixer.music.get_volume()
                    if mv > 0:
                        pygame.mixer.music.set_volume(mv - 0.1)
                elif event.key == pygame.K_F3:
                    mv = pygame.mixer.music.get_volume()
                    if mv < 1:
                        pygame.mixer.music.set_volume(mv + 0.1)
                elif event.key == pygame.K_F4:
                    pygame.mixer.music.set_volume(0)
                elif event.key == pygame.K_SPACE:
                    if GAMEMODE == 1 or GAMEMODE == 10:
                        pause()
                elif GAMEMODE == 0 and event.key == pygame.K_UP:
                    total += 5
                elif GAMEMODE == 0 and event.key == pygame.K_DOWN and total > 24:
                    total -= 5
                elif GAMEMODE == 0 and event.key == pygame.K_LEFT:
                    target = target - 1 if target > 0 else len(list_targets) - 1
                    curr_target = pygame.transform.scale(load_image(list_targets[target], addpath='target'),
                                                         to_coef(360, 360))
                elif GAMEMODE == 0 and event.key == pygame.K_RIGHT:
                    target = target + 1 if target < len(list_targets) - 1 else 0
                    curr_target = pygame.transform.scale(load_image(list_targets[target], addpath='target'),
                                                         to_coef(360, 360))
                elif GAMEMODE == 11:
                    go_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Press a button in mouse
                if GAMEMODE == 1 and event.pos[1] > to_coef(200):
                    s += 1
                elif GAMEMODE == 11:
                    go_menu()
                    is_press = True
                elif GAMEMODE == 0 and event.button == 4:
                    total += 1
                elif GAMEMODE == 0 and event.button == 5 and total > 20:
                    total -= 1
            if event.type == pygame.MOUSEBUTTONUP:  # Stop press a button in mouse
                is_press = False

        if GAMEMODE == 1:  # Game
            sprite_group_1.update()
            sprite_group_game.update()
            screen.fill(pygame.Color('black'))
            s_color.hsva = (tm % 360, 100, 100)
            text1 = font.render(str(score1), True, s_color)
            text1t = font.render(str(round(tm / FPS, 1)), True, (s_color.b, s_color.r, s_color.g))
            screen.blit(text1, to_coef(500, 50))
            screen.blit(text1t, to_coef(750, 50))
            sprite_group_game.draw(screen)
            sprite_group_1.draw(screen)
            if score1 == total:
                GAMEMODE = 11
                pygame.mixer.music.play(-1)
            tm += 1
        elif GAMEMODE == 12:  # Start a game
            screen.fill(pygame.Color('black'))
            text1t = font.render(str(tm // FPS + 1), False, s_color)
            screen.blit(text1t, to_center(*text1t.get_size()))
            tm -= 1
            if tm <= 0:
                start_game()
        elif GAMEMODE == 10:  # Pause
            sprite_group_1.update()
            screen.fill(pygame.Color('black'))
            text1 = font.render(str(score1), True, s_color)
            text1t = font.render(str(round(tm / FPS, 1)), True, (s_color.b, s_color.r, s_color.g))
            screen.blit(text1, to_coef(500, 50))
            screen.blit(text1t, to_coef(650, 50))
            text10 = font.render('PAUSE', True, (255, 10, 10))
            sprite_group_game.draw(screen)
            screen.blit(text10, to_center(*text10.get_size()))
            sprite_group_1.draw(screen)
        elif GAMEMODE == 11:  # Finish a game
            screen.fill(pygame.Color('black'))
            res1 = round(score1 / s * 100, 2)
            res2 = round(tm / FPS, 2)
            if res1 > 99 and res2 < total * 0.5:
                textc = font.render('Who are you!?', True, (255, 0, 0))
            elif res1 > 95 and res2 < total * 0.8:
                textc = font.render('Fantastic!', True, (255, 40, 40))
            elif res1 > 90 and res2 < total:
                textc = font.render('Very good!', True, (255, 50, 50))
            elif res1 > 80 and res2 < total * 1.2:
                textc = font.render('Good!', True, (255, 50, 50))
            elif res1 > 60 and res2 < total * 1.4:
                textc = font.render('Fine!', True, (255, 50, 50))
            elif res1 > 50 and res2 < total * 1.6:
                textc = font.render('Not bad!', True, (255, 50, 50))
            elif res1 > 40 and res2 < total * 1.8:
                textc = font.render('Bad!', True, (255, 100, 100))
            elif res1 > 25 and res2 < total * 2:
                textc = font.render('Very bad!', True, (255, 150, 150))
            else:
                textc = font.render('Noob!', True, (255, 250, 250))
            text0 = font.render(f'{res1}%, {res2} sec', True, (100, 255, 100))
            screen.blit(textc, (to_center(textc.get_size()[0]), 200))
            screen.blit(text0, to_center(*text0.get_size()))
        elif GAMEMODE == 0:  # Menu
            list_targets = listdir('data/target')
            sprite_group_0.update()
            screen.fill(pygame.Color(25, 25, 85))
            texti = font.render(f'Objects: {total}', True, (255, 127, 0))
            screen.blit(texti, (to_center(texti.get_size()[0], texti.get_size()[1] + to_coef(600))))
            pygame.draw.rect(screen, (255, 0, 0), [(X - to_coef(400), Y - to_coef(600)), to_coef(360, 360)], 1)
            screen.blit(curr_target, (X - to_coef(400), Y - to_coef(600)))
            textt = fonttar.render(target_name(), True, (127, 127, 127))
            screen.blit(textt, (X - to_coef(400) + to_coef(180 - textt.get_size()[0] // 2), Y - to_coef(240)))
            sprite_group_0.draw(screen)
        elif GAMEMODE == -1:  # Exit
            sprite_group_exit.update()
            screen.fill(pygame.Color('black'))
            sprite_group_exit.draw(screen)
        elif GAMEMODE == 2:  # Help window
            sprite_group_help.update()
            screen.fill(pygame.Color(25, 25, 85))
            sprite_group_help.draw(screen)
        elif GAMEMODE == 3:  # Information window
            sprite_group_info.update()
            screen.fill(pygame.Color(25, 25, 85))
            sprite_group_info.draw(screen)
        else:  # For emergency exit
            exit_game()

        cursor.update(screen, *pygame.mouse.get_pos())  # Update a cursor
        pygame.display.flip()  # Go to next frame
