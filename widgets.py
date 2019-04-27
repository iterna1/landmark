import pygame


class PInterface(pygame.sprite.Group):
    def mouse_click(self, event):
        for s in self.sprites():
            if s.itself == 'PLineEdit':
                if s.rect.collidepoint(*event.pos) or s.active:
                    s.switch()
                    s.update()
            elif s.itself == 'PButton':
                if event.button != 1:
                    continue
                if s.rect.collidepoint(*event.pos):
                    s.on()
                    s.update()
            elif s.itself == 'PCheckbox':
                if event.button != 1:
                    continue
                if s.rect.collidepoint(*event.pos):
                    s.switch()
                    s.update()

    def mouse_unclench(self, event):
        for s in self.sprites():
            if s.itself == 'PButton' and event.button == 1:
                if s.pressed:
                    s.off()
                    s.update()

    def key_click(self, event):
        for s in self.sprites():
            if s.itself == 'PLineEdit':
                if not s.active:
                    continue
                letter = pygame.key.name(event.key)
                if letter in '1234567890-=qwertyuiop[]asdfghjkl;\'zxcvbnm,./\\':
                    s += letter
                    s.update()
                elif event.key == pygame.K_SPACE:
                    s += ' '
                    s.update()

    def mouse_press(self, buttons):
        pass

    def key_press(self, keys):
        if not any(keys):
            return
        for s in self.sprites():
            if s.itself == 'PLineEdit':
                if not s.active:
                    continue
                if keys[pygame.K_BACKSPACE]:
                    s -= 1
                    s.update()

    def update(self, events, buttons, keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_click(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_unclench(event)
            elif event.type == pygame.KEYDOWN:
                self.key_click(event)

        self.mouse_press(buttons)
        self.key_press(keys)


class PLineWidgetTemplate(pygame.sprite.Sprite):
    def __init__(self, text, rect=None, bg_color=(255, 255, 255), interface=None):
        if interface is not None:
            super().__init__(interface)
        else:
            super().__init__()

        self.font = pygame.font.Font(None, 28)
        self.text = text

        self.bg_color = pygame.Color(*bg_color)
        self.color = pygame.Color(0, 0, 0)

        self.margin_x = 0
        self.margin_y = 0

        if rect:
            self.rect = pygame.Rect((0, 0, *rect))
        else:
            self.rect = self.font.render(self.text, True, self.color).get_rect()

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        if self.bg_color:
            self.image.fill(self.bg_color)
        self.image.blit(self.font.render(self.text, True, self.color),
                        (self.margin_x, self.margin_y))

    def set_text(self, text):
        self.text = text

    def set_color(self, color):
        if color is tuple:
            color = pygame.Color(*color)
        self.color = color

    def set_colorkey(self, color):
        self.image.set_colorkey(color)

    def set_bg_color(self, color):
        self.bg_color = color

    def set_font(self, file, size):
        self.font = pygame.font.Font(file, size)

    def set_margin(self, x, y):
        self.margin_x = x
        self.margin_y = y

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.image.fill(self.bg_color)
        self.image.blit(self.font.render(self.text, True, self.color),
                        (self.margin_x, self.margin_y))


class PLabel(PLineWidgetTemplate):
    itself = 'PLabel'


class PLineEdit(PLineWidgetTemplate):
    itself = 'PLineEdit'

    def __init__(self, placeholder='', rect=(150, 24), bg_color=(214, 214, 214), interface=None):
        self.active = False
        super().__init__(placeholder, rect=rect, bg_color=bg_color, interface=interface)

        self.set_margin(7, 1)

    def switch(self):
        self.active = ~self.active

    def __add__(self, other):
        new = self
        new.text += other
        return new

    def __sub__(self, other):
        new = self
        new.text = new.text[:-other]
        return new

    def update(self):
        self.image.fill(self.bg_color)

        txt = self.text
        if self.active:
            txt += '|'

        self.image.blit(self.font.render(txt, True, self.color),
                        (self.margin_x, self.margin_y))


class PButton(PLineWidgetTemplate):
    itself = 'PButton'

    def __init__(self, text, rect=None, bg_color=(228, 228, 228), interface=None):
        super().__init__(text, rect=rect, bg_color=bg_color, interface=interface)
        self.pressed = False

        hsva = self.bg_color.hsva
        self.s_color = pygame.Color(0, 0, 0)
        self.s_color.hsva = (hsva[0], hsva[1], hsva[2] - 30, hsva[3])

    def on(self):
        self.pressed = True

    def off(self):
        self.pressed = False

    def set_color(self, color):
        super().set_color(color)
        hsva = self.bg_color.hsva
        self.s_color = pygame.Color(0, 0, 0)
        self.s_color.hsva = (hsva[0], hsva[1], hsva[2] - 30, hsva[3])

    def update(self):
        if self.pressed:
            self.image.fill(self.s_color)
        else:
            self.image.fill(self.bg_color)

        self.image.blit(self.font.render(self.text, True, self.color),
                        (self.margin_x, self.margin_y))


class PCheckbox(pygame.sprite.Sprite):
    itself = 'PCheckbox'

    def __init__(self, rect=(15, 15), bg_color=(255, 0, 105), s_color=None, interface=None):
        if interface is not None:
            super().__init__(interface)
        else:
            super().__init__()

        self.bg_color = pygame.Color(*bg_color)
        self.margin_x = 0
        self.margin_y = 0

        self.rect = pygame.Rect((0, 0, *rect))
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.bg_color)

        self.checked = False

        if s_color is None:
            self.s_color = tuple(map(lambda x: 255 - x, self.bg_color))
        else:
            self.s_color = s_color

    def switch(self):
        self.checked = ~self.checked

    def set_bg_color(self, color):
        self.bg_color = color

    def set_s_color(self, color):
        self.s_color = color

    def set_margin(self, x, y):
        self.margin_x = x
        self.margin_y = y

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.checked:
            self.image.fill(self.s_color)
        else:
            self.image.fill(self.bg_color)


class PCustomCheckbox(pygame.sprite.Sprite):
    itself = 'PCheckbox'

    def __init__(self, images, interface=None):
        if interface is not None:
            super().__init__(interface)
        else:
            super().__init__()

        self.images = images

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.checked = False

    def switch(self):
        self.checked = ~self.checked

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.image = self.images[self.checked]
