import os
from unittest import TestCase

from m_pyutil.mtencent_map import TencentMap


class TestTencentMap(TestCase):

    def test_geocoder(self):
        tencent_map = TencentMap(os.environ.get('TENCENT_MAP_KEY'))

        response = tencent_map.geocoder(location=('104.101589', '30.655520'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 0)

        response = tencent_map.geocoder(address='黔东南州凯里经济开发区金源西大道37号')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 0)
