import pygame

from widgets import *
from map import Map, MapSpot, lonlat_distance
from speaker import Jarvis


def update_screen():
    screen.fill((0, 51, 255))
    pygame.draw.rect(screen, (255, 204, 0), (0, 0, 600, 55))

    pygame.draw.line(screen, (184, 130, 31), (95, 0), (95, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (180, 0), (180, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (285, 0), (285, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (380, 0), (380, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (500, 0), (500, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (0, 55), (600, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (0, 0), (600, 0), 5)


def mainloop():
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and not search_field.active:
                mp.update(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and mp.sprite.rect.collidepoint(event.pos):
                if event.button == 1:
                    point = mp.sprite.xy_into_ll(event.pos)

                    spot = MapSpot()
                    ll = '%f,%f' % point

                    if it_switcher.checked:
                        spot.find_organization(text=ll, ll=ll)
                    else:
                        spot.find_toponym(geocode=ll, ll=ll)

                    if spot.point and lonlat_distance(spot.point, point) <= 50:
                        mp.sprite.set_spot(spot, focus=False)
                        mp.sprite.update_image()

        buttons = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        interface.update(events, buttons, keys)

        update_screen()
        mp.draw(screen)
        interface.draw(screen)

        pygame.display.flip()

        # input mode switcher
        if im_switcher.checked:
            interface.add(rt_label)
            interface.add(record_button)

            search_field.set_text('')
            interface.remove(search_field)
            interface.remove(search_button)
        else:
            interface.add(search_field)
            interface.add(search_button)

            rt_label.set_text('')
            rt_label.update()
            interface.remove(rt_label)
            interface.remove(record_button)

        # on search button click
        if search_button.pressed:
            request_text = search_field.text
            if request_text:
                spot = MapSpot()

                if it_switcher.checked:
                    spot.find_organization(text=request_text)
                else:
                    spot.find_toponym(geocode=request_text)
                if spot.point:
                    # setting this spot on map
                    mp.sprite.set_spot(spot, focus=True)
                    mp.sprite.update_image()

        # on record button click
        if record_button.pressed:
            request_text = jarvis.listen()

            if request_text:
                spot = MapSpot()

                if it_switcher.checked:
                    spot.find_organization(text=request_text)
                else:
                    spot.find_toponym(geocode=request_text)
                if spot.point:
                    rt_label.set_text(request_text)
                    rt_label.update()
                    # setting this spot on map
                    mp.sprite.set_spot(spot, focus=True)
                    mp.sprite.update_image()

        # on reset button click
        elif reset_button.pressed:
            mp.sprite.set_spot(None)
            mp.sprite.update_image()

        # on home button click
        elif home_button.pressed:
            mp.sprite.set_spot(mp.sprite.spot, focus=True)
            mp.sprite.update_image()

        elif info_button.pressed:
            pass

        clock.tick(20)

    mp.sprite.remove_files()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 560))
    update_screen()

    # speaker
    jarvis = Jarvis()

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

    # text recognizer label
    rt_label = PLabel('', bg_color=(0, 0, 0), rect=(490, 35))
    rt_label.set_font('data/font.ttf', 20)
    rt_label.set_color((255, 204, 0))
    rt_label.set_margin(10, 8)
    rt_label.move(10, 515)
    rt_label.update()

    # record voice button
    record_button = PButton('Rec', bg_color=(255, 204, 0), rect=(80, 35))
    record_button.set_font('data/font.ttf', 24)
    record_button.move(510, 515)
    record_button.set_margin(14, 8)
    record_button.update()

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
    it_label = PLabel('IT:', rect=(35, 35), bg_color=(255, 204, 0), interface=interface)
    it_label.set_font('data/font.ttf', 22)
    it_label.set_margin(0, 8)
    it_label.move(300, 10)
    it_label.update()

    # information type switcher
    font = pygame.font.Font('data/font.ttf', 30)
    images = [font.render('A', True, (0, 51, 255)), font.render('O', True, (0, 51, 255))]
    it_switcher = PCustomCheckbox(images, interface=interface)
    it_switcher.move(345, 15)
    it_switcher.update()

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
