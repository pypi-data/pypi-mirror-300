from unittest import TestCase

from m_pyutil.mip import get_ip, get_netmask, get_broadcast


class Test(TestCase):

    def test_get_ip(self):
        ip = get_ip()
        regexp = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        self.assertRegex(ip, regexp)

    def test_get_netmask(self):
        netmask = get_netmask()
        regexp = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        self.assertRegex(netmask, regexp)

    def test_get_broadcast(self):
        broadcast = get_broadcast()
        regexp = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        self.assertRegex(broadcast, regexp)
