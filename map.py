import request
import pygame
from os import remove

from math import pow, cos, radians


class Map(pygame.sprite.Sprite):
    dlon = 0.02
    dlat = 0.008
    k = 0.0000428

    def __init__(self, ll=(0, 0), zoom=10, type='map'):
        super().__init__()

        # default params
        self.lon, self.lat = ll
        self.zoom = zoom
        self.type = type
        self.spot = None

        # sprite attrs
        self.image = pygame.Surface((600, 450))
        self.update_image()

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def set_spot(self, spot, focus=False):
        self.spot = spot
        if focus:
            self.lon, self.lat = spot.point

    def update_image(self):
        # request params
        params = {'ll': '%s,%s' % (self.lon, self.lat),
                  'z': self.zoom,
                  'l': self.type}
        if self.spot:
            ll = ','.join(map(str, self.spot.point))
            params['pt'] = '%s,pm2wtm' % ll

        # request
        try:
            data = request.static_maps(**params)
        except request.BadRequest as br:
            print(br)
            return

        # setting map image
        ext = '.jpg' if self.type == 'sat' else '.png'
        with open('map' + ext, 'wb') as file:
            file.write(data)

        self.image = pygame.image.load('map' + ext)

    def xy_into_ll(self, pos):
        dy = 225 - pos[1]
        dx = pos[0] - 300
        lon = self.lon + dx * Map.k * pow(2, 15 - self.zoom)
        lat = self.lat + dy * Map.k * cos(radians(self.lat)) * pow(2, 15 - self.zoom)

        return lon, lat

    def scale(self, dz):
        if 0 <= self.zoom + dz <= 17:
            self.zoom += dz

    def update(self, event):
        # event handler
        if event.key == pygame.K_PAGEUP:
            self.scale(1)
        elif event.key == pygame.K_PAGEDOWN:
            self.scale(-1)
        elif event.key == pygame.K_UP:
            self.lat += Map.dlat * pow(2, 15 - self.zoom)
        elif event.key == pygame.K_DOWN:
            self.lat -= Map.dlat * pow(2, 15 - self.zoom)
        elif event.key == pygame.K_RIGHT:
            self.lon += Map.dlon * pow(2, 15 - self.zoom)
        elif event.key == pygame.K_LEFT:
            self.lon -= Map.dlon * pow(2, 15 - self.zoom)
        elif event.key == pygame.K_F1:
            self.type = 'map'
        elif event.key == pygame.K_F2:
            self.type = 'sat'
        elif event.key == pygame.K_F3:
            self.type = 'skl'
        elif event.key == pygame.K_F4:
            self.type = 'trf'

        if self.lon > 180:
            self.lon -= 360
        elif self.lon < -180:
            self.lon += 360
        if self.lat > 90:
            self.lat -= 180
        elif self.lat < -90:
            self.lat += 180

        # update map image
        self.update_image()

    def remove_files(self):
        try:
            remove('map.png')
        except FileNotFoundError:
            pass
        try:
            remove('map.jpg')
        except FileNotFoundError:
            pass


class MapSpot:
    def __init__(self, point=None):
        self.info = dict()
        self.point = point

        self.organization = None
        self.toponym = None
        self.address = None
        self.postcode = None

        if point:
            self.find_toponym(geocode=','.join(map(str, self.point)))
            self.find_organization(text=','.join(map(str, self.point)))

    def find_organization(self, **kwargs):
        try:
            self.organization = request.geosearch(**kwargs)[0]
        except IndexError:
            print('No organizations found')
        else:
            if not self.point:
                self.point = self.organization['geometry']['coordinates']
            if not self.address:
                self.address = self.organization['properties']['CompanyMetaData'].get('address')

    def find_toponym(self, **kwargs):
        try:
            self.toponym = request.geocoder(**kwargs)[0]
        except IndexError:
            print('No toponyms found')
        else:
            if not self.point:
                self.point = [float(i) for i in self.toponym['Point']['pos'].split()]
            if not self.address:
                self.address = self.toponym['metaDataProperty']['GeocoderMetaData'].get('Address')['formatted']
            if not self.postcode:
                self.postcode = self.toponym['metaDataProperty']['GeocoderMetaData'].get('Address').get('postal_code')
