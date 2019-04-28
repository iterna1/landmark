import requests
import pygame
import sys

from webbrowser import open as openweb

from widgets import *
from map import Map, MapSpot, lonlat_distance
from speaker import Jarvis


def terminate():
    mp.sprite.remove_files()
    pygame.quit()
    sys.exit(1)


def dialog_window():
    dialog = PInterface()

    window = pygame.sprite.Sprite()
    window.itself = None
    window.image = pygame.Surface((300, 225))
    window.image.fill((255, 204, 0))
    window.rect = (150, 112, 300, 225)
    dialog.add(window)

    more_information = PButton('More info', rect=(135, 50), bg_color=(0, 51, 255), interface=dialog)
    more_information.set_font('data/font.ttf', 20)
    more_information.set_margin(10, 14)
    more_information.set_color((255, 51, 0))
    more_information.move(305, 277)
    more_information.update()

    no_thanks = PButton('No, thanks', rect=(135, 50), bg_color=(255, 51, 0), interface=dialog)
    no_thanks.set_font('data/font.ttf', 20)
    no_thanks.set_margin(5, 14)
    no_thanks.set_color((0, 51, 255))
    no_thanks.move(160, 277)
    no_thanks.update()

    while True:
        events = pygame.event.get()
        if pygame.QUIT in [e.type for e in events]:
            terminate()

        buttons = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        dialog.update(events, buttons, keys)
        dialog.draw(screen)
        pygame.display.flip()

        if more_information.pressed:
            return True
        elif no_thanks.pressed:
            return False
        clock.tick(20)


def update_screen():
    screen.fill((0, 51, 255))
    pygame.draw.rect(screen, (255, 204, 0), (0, 0, 600, 55))

    pygame.draw.line(screen, (184, 130, 31), (95, 0), (95, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (180, 0), (180, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (380, 0), (380, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (500, 0), (500, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (0, 55), (600, 55), 5)
    pygame.draw.line(screen, (184, 130, 31), (0, 0), (600, 0), 5)


def mainloop():
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and not search_field.active:
                mp.update(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and mp.sprite.rect.collidepoint(event.pos):
                if event.button == 1:
                    point = mp.sprite.xy_into_ll(event.pos)

                    spot = MapSpot()
                    lonlat = '%f,%f' % point
                    spot.find_toponym(geocode=lonlat, ll=lonlat)

                    if api_switcher.checked:
                        api_switcher.switch()
                        api_switcher.update()

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

                if api_switcher.checked:
                    spot.find_organization(text=request_text, type='biz')
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

                if api_switcher.checked:
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
            record_button.pressed = False
            record_button.update()
            mp.sprite.set_spot(None)
            mp.sprite.update_image()

        # on home button click
        elif home_button.pressed:
            home_button.pressed = False
            home_button.update()
            mp.sprite.set_spot(mp.sprite.spot, focus=True)
            mp.sprite.update_image()

        # on help button click
        elif help_button.pressed:
            help_button.pressed = False
            help_button.update()
            openweb('http://localhost:8080/help')

        # on info button click
        elif info_button.pressed:
            info_button.pressed = False
            info_button.update()
            if mp.sprite.spot:
                text = 'No address found.'
                if mp.sprite.spot.toponym:
                    text_base = mp.sprite.spot.toponym
                    text = text_base['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
                elif mp.sprite.spot.organization:
                    text_base = mp.sprite.spot.organization
                    text = text_base['properties']['CompanyMetaData']['address']
                jarvis.say(text)

                if dialog_window():
                    response = None
                    if mp.sprite.spot.toponym:
                        response = requests.get('http://localhost:8080/index',
                                                json={'api': 'geocoder', 'response': mp.sprite.spot.toponym})
                    elif mp.sprite.spot.organization:
                        response = requests.get('http://localhost:8080/index',
                                                json={'api': 'geocoder', 'response': mp.sprite.spot.organization})
                    with open('templates/info.html', 'w') as file:
                        file.write(response.text)
                    openweb('http://localhost:8080/information')

        clock.tick(20)


if __name__ == 'app':
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

    # label for api switcher
    api_label = PLabel('Api:', rect=(45, 35), bg_color=(255, 204, 0), interface=interface)
    api_label.set_font('data/font.ttf', 22)
    api_label.set_margin(0, 8)
    api_label.move(195, 10)
    api_label.update()

    # api switcher
    font = pygame.font.Font('data/font.ttf', 18)
    images = [font.render('geocoder', True, (0, 51, 255)), font.render('geosearch', True, (0, 51, 255))]
    api_switcher = PCustomCheckbox(images, interface=interface)
    api_switcher.move(248, 20)
    api_switcher.update()

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
