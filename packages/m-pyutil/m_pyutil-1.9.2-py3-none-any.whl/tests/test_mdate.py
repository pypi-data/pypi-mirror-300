import datetime
from unittest import TestCase

from m_pyutil import mdate


class Test(TestCase):

    def test_nowt(self):
        self.assertEqual(mdate.nowt(), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def test_nowd(self):
        self.assertEqual(mdate.nowd(), datetime.datetime.now().strftime('%Y-%m-%d'))

    def test_add_secs(self):
        self.assertEqual(mdate.add_secs('2021-01-01 00:00:00', 1), '2021-01-01 00:00:01')

    def test_add_mins(self):
        self.assertEqual(mdate.add_mins('2021-01-01 00:00:00', 1), '2021-01-01 00:01:00')

    def test_add_hours(self):
        self.assertEqual(mdate.add_hours('2021-01-01 00:00:00', 1), '2021-01-01 01:00:00')

    def test_add_days(self):
        self.assertEqual(mdate.add_days('2021-01-01 00:01', 1), '2021-01-02 00:01')

    def test_add_times(self):
        self.assertEqual(mdate.add_times('2021-01-01 00:00:00', 1, mdate.DeltaType.SEC), '2021-01-01 00:00:01')
        self.assertEqual(mdate.add_times('2021-01-01 00:00:00', 1, mdate.DeltaType.MIN), '2021-01-01 00:01:00')
        self.assertEqual(mdate.add_times('2021-01-01 00:00:00', 1, mdate.DeltaType.HOUR), '2021-01-01 01:00:00')
        self.assertEqual(mdate.add_times('2021-01-01 00:00:00', 1, mdate.DeltaType.DAY), '2021-01-02 00:00:00')
