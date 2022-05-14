#!/usr/bin/python3

import mock
import unittest

import eloader


class TestEloader(unittest.TestCase):
    def setUp(self):
        self.el = eloader.EloaderController()
        self.el.goe = mock.Mock(eloader.goeapi.GoeAPI)
        self.el.smax = mock.Mock(eloader.smaxsmt.SolarmaxSmt)
        self.el.log = mock.Mock()

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
