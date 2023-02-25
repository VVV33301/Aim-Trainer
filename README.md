# Aim Trainer
Created by _Vladimir Varenik_ and _Dilyara Ismagilova_

<h1 align="center"> <img src="https://user-images.githubusercontent.com/117539159/211195258-fff078c7-2e7b-4ded-a176-e5645c314f18.png" /> </h1>

## Description
***"Aim Trainer"*** is a game for training the player's reaction speed. Recommended for fans and pro players of shooters like Counter Strike and others to improve speed and accuracy. The game is a set of targets that appear in turn in random places, and as soon as a certain number is destroyed, the results are displayed to the user. The game has several windows - *menu*, *game*, *help* and *information*, as well as *pause* and *exit* windows.

### Advertising
There is an advertisement in the game, when clicked, the source opens with a probability of 50%

## Screenshots
![Menu](https://user-images.githubusercontent.com/117539159/221351484-10b83ec0-6f78-4de7-b377-fc075b1e7d3c.png)
![Game](https://user-images.githubusercontent.com/117539159/212554964-37c44631-ed81-4fe4-a7bf-0ec162e83791.png)

# Project
This project created by `Python 3.9`. The main module is `pygame`. There are also some parts of the `random`, `os`, `sys` and `webbrowser` modules. The project consists of one executable file and the data folder, where the images and musics for the buttons are stored. 

## New technologies
Especially for this project, classes of unusual buttons for *pygame* were developed.
```python
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
```
## License
The project uses a license GNU LGPL
