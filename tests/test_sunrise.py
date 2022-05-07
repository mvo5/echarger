#!/usr/bin/python3

import datetime
import unittest

from eloader import get_sunrise_sunset


class TestSunsetDawn(unittest.TestCase):
    def test_sunrise_sunset_fuzzy(self):
        sunrise, sunset = get_sunrise_sunset("Berlin")
        # just basic sanity test for Germany
        self.assertTrue(sunrise < sunset)
        # sunrise
        self.assertTrue(datetime.time(4, 30, 0) < sunrise)
        self.assertTrue(datetime.time(7, 31, 0) > sunrise)
        # sunset
        self.assertTrue(datetime.time(17, 30, 0) < sunset)
        self.assertTrue(datetime.time(22, 0, 0) > sunset)

    def test_sunrise_sunset_precise(self):
        sunrise, sunset = get_sunrise_sunset("Berlin", date=datetime.date(2022, 5, 7))

        self.assertEqual("05:24", sunrise.strftime("%H:%M"))
        self.assertEqual("20:41", sunset.strftime("%H:%M"))
