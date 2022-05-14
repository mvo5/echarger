#!/usr/bin/python3

import mock
import datetime
import unittest

import eloader


class TestEloader(unittest.TestCase):
    def setUp(self):
        self.el = eloader.EloaderController()
        self.el.goe = mock.Mock(eloader.goeapi.GoeAPI)
        self.el.smax = mock.Mock(eloader.smaxsmt.SolarmaxSmt)
        self.el.log = mock.Mock()
        self.el.now = mock.Mock()
        # mock mid-day
        self.el.now.return_value = datetime.time(12, 0, 0)

    def test_eloader_will_pause_when_not_enough_power(self):
        # pretent we are at 6kw at the loader
        self.el.goe.power = 6
        self.el.goe.phases = 1
        self.el.goe.amere = 6
        # pretent 1kw from solar
        self.el.smax.current_power = 1.0
        self.assertEqual(self.el.tick(), 360)
        self.assertTrue(self.el.goe.force_pause)
        self.el.log.assert_called_with("not enough power, forcing pause")

    def test_eloader_manual_overriden(self):
        test_cases = [
            # paused or no car, divergence does not matter
            {"pau": True, "con": True, "cur_amp": 10, "goe_amp": 16, "exp": False},
            {"pau": False, "con": False, "cur_amp": 10, "goe_amp": 16, "exp": False},
            {"pau": True, "con": False, "cur_amp": 10, "goe_amp": 16, "exp": False},
            # manual overriden by user
            {"pau": False, "con": True, "cur_amp": 10, "goe_amp": 16, "exp": True},
        ]
        for t in test_cases:
            self.el.goe.force_pause = t["pau"]
            self.el.goe.car_connected = t["con"]
            self.el.current_ampere = t["cur_amp"]
            self.el.goe.ampere = t["goe_amp"]
            self.el.current_phases = 1
            self.el.goe.phases = 1
            self.assertEqual(self.el.manual_overriden(), t["exp"], msg=t)
