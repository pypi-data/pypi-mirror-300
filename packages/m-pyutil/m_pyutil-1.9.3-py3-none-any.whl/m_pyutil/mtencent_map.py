from urllib.parse import quote

import requests


class TencentMap:

    def __init__(self, key: str):
        self.key = quote(key or '')

    def geocoder(self, location: tuple = None, address: str = None):
        url = 'https://apis.map.qq.com/ws/geocoder/v1'
        if location:
            lng = quote(location[0])
            lat = quote(location[1])
            location = quote(f'{lat},{lng}')
            url = f'{url}?location={location}&key={self.key}'
        elif address:
            address = quote(address)
            url = f'{url}?address={address}&key={self.key}'
        else:
            raise ValueError('location or address is required')
        return requests.get(url)
