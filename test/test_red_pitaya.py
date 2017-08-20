from unittest import TestCase
from spectroscopypy import RedPitaya

class RedPitayaTest(TestCase):
    DEFAULT_PORT = 5000
    
    def test_red_pitaya_creation_hostname(self):
        HOST = 'rp-f0060c.local'
        red_pitaya = RedPitaya(HOST)

        self.assertEqual(HOST, red_pitaya.host)
        self.assertEqual(self.DEFAULT_PORT, red_pitaya.port)

    def test_red_pitaya_creation_ip(self):
        HOST = '192.168.1.35'
        red_pitaya = RedPitaya(HOST)

        self.assertEqual(HOST, red_pitaya.host)
        self.assertEqual(self.DEFAULT_PORT, red_pitaya.port)

    def test_red_pitaya_creation_with_non_default_port(self):
        HOST = 'rp-f0060c.local'
        PORT = 9999
        red_pitaya = RedPitaya(HOST, PORT)

        self.assertEqual(HOST, red_pitaya.host)
        self.assertEqual(PORT, red_pitaya.port)

    def test_get_generator_channel_with_invalid_id(self):
        red_pitaya = RedPitaya('rp-f0060c.local')

        INVALID_CHANNEL_ID = 3
        with self.assertRaises(ValueError):
            generator_channel = red_pitaya.get_generator_channel(INVALID_CHANNEL_ID)

    def test_get_generator_channel(self):
        red_pitaya = RedPitaya('rp-f0060c.local')

        CHANNEL_ID = 1
        channel = red_pitaya.get_generator_channel(CHANNEL_ID)

        self.assertEqual(CHANNEL_ID, channel.channel_id)
        

    def test_get_oscilloscope_channel_with_invalid_id(self):
        red_pitaya = RedPitaya('rp-f0060c.local')

        INVALID_CHANNEL_ID = 3
        with self.assertRaises(ValueError):
            red_pitaya.get_oscilloscope_channel(INVALID_CHANNEL_ID)

    def test_get_oscilloscope_channel_with_valid_id(self):
        red_pitaya = RedPitaya('host')

        CHANNEL_ID = 1
        channel = red_pitaya.get_oscilloscope_channel(CHANNEL_ID)

        self.assertEqual(CHANNEL_ID, channel.channel_id)
