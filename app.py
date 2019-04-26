import pygame

from widgets import *
from map import Map, MapSpot


def update_screen():
    screen.fill((0, 51, 255))
    pygame.draw.rect(screen, (255, 204, 0), (0, 0, 600, 55))

    pygame.draw.line(screen, (184, 130, 31), (95, 0), (95, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (180, 0), (180, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (285, 0), (285, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (380, 0), (380, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (500, 0), (500, 55), 5)


def mainloop():
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and not search_field.active:
                mp.update(event)

        buttons = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        interface.update(events, buttons, keys)

        update_screen()
        mp.draw(screen)
        interface.draw(screen)

        pygame.display.flip()

        clock.tick(20)

    mp.sprite.remove_files()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 560))
    update_screen()

    # widget interface
    interface = PInterface()

    # search field
    search_field = PLineEdit(bg_color=(0, 0, 0), rect=(490, 35), interface=interface)
    search_field.set_font('data/font.ttf', 20)
    search_field.set_color((255, 204, 0))
    search_field.set_margin(10, 8)
    search_field.move(10, 515)
    search_field.update()

    # search button
    search_button = PButton('Find', bg_color=(255, 204, 0), rect=(80, 35), interface=interface)
    search_button.set_font('data/font.ttf', 22)
    search_button.move(510, 515)
    search_button.set_margin(12, 8)
    search_button.update()

    # help button
    help_button = PButton('Help', bg_color=(0, 51, 255), rect=(71, 35), interface=interface)
    help_button.set_font('data/font.ttf', 22)
    help_button.set_color((255, 204, 0))
    help_button.set_margin(8, 8)
    help_button.move(10, 10)
    help_button.update()

    # label for input mode switcher
    im_label = PLabel('Im:', rect=(35, 35), bg_color=(255, 204, 0), interface=interface)
    im_label.set_font('data/font.ttf', 22)
    im_label.set_margin(0, 8)
    im_label.move(110, 10)
    im_label.update()

    # input mode switcher
    images = [pygame.transform.scale(pygame.image.load(i).convert_alpha(), (40, 40))
              for i in ('data/im_1.png', 'data/im_2.png')]
    im_switcher = PCustomCheckbox(images, interface=interface)
    im_switcher.move(140, 10)
    im_switcher.update()

    # label for output mode switcher
    om_label = PLabel('Om:', rect=(40, 35), bg_color=(255, 204, 0), interface=interface)
    om_label.set_font('data/font.ttf', 22)
    om_label.set_margin(0, 8)
    om_label.move(195, 10)
    om_label.update()

    # output mode switcher
    images = [pygame.transform.scale(pygame.image.load(i).convert_alpha(), (40, 40))
              for i in ('data/om_1.png', 'data/om_2.png')]
    om_switcher = PCustomCheckbox(images, interface=interface)
    om_switcher.move(235, 10)
    om_switcher.update()

    # label for information type switcher
    irm_label = PLabel('IT:', rect=(35, 35), bg_color=(255, 204, 0), interface=interface)
    irm_label.set_font('data/font.ttf', 22)
    irm_label.set_margin(0, 8)
    irm_label.move(300, 10)
    irm_label.update()

    # information type switcher
    font = pygame.font.Font('data/font.ttf', 30)
    images = [font.render('A', True, (0, 51, 255)), font.render('O', True, (0, 51, 255))]
    om_switcher = PCustomCheckbox(images, interface=interface)
    om_switcher.move(345, 15)
    om_switcher.update()

    # reset button
    reset_button = PButton('Re', rect=(40, 35), bg_color=(255, 51, 0), interface=interface)
    reset_button.set_font('data/font.ttf', 20)
    reset_button.set_margin(6, 8)
    reset_button.set_color((0, 51, 255))
    reset_button.move(395, 10)
    reset_button.update()

    # home button
    home_button = PButton('Ho', rect=(40, 35), bg_color=(0, 255, 0), interface=interface)
    home_button.set_font('data/font.ttf', 20)
    home_button.set_margin(6, 8)
    home_button.set_color((0, 51, 255))
    home_button.move(445, 10)
    home_button.update()

    # info button
    info_button = PButton('Info', rect=(75, 35), bg_color=(0, 51, 255), interface=interface)
    info_button.set_font('data/font.ttf', 20)
    info_button.set_color((255, 204, 0))
    info_button.set_margin(12, 8)
    info_button.move(515, 10)
    info_button.update()

    # create map
    mp = pygame.sprite.GroupSingle(sprite=Map())
    mp.sprite.rect.y = 55

    # mainloop
    mainloop()
