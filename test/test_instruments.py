from mock import Mock
from unittest import TestCase
from spectroscopypy.instruments import RedPitayaOscilloscope, OscilloscopeDriver, ScpiOscilloscopeDriver
from spectroscopypy import Pulse, Sample

class RedPitayaOscilloscopeTest(TestCase):

    def test_can_create_red_pitaya_oscilloscope(self):
        scope = RedPitayaOscilloscope(driver=Mock(OscilloscopeDriver))
    
    def test_acquire(self):
        driver = Mock(OscilloscopeDriver)
        driver.acquire = Mock(return_value=([0.0, 0.1, 0.2], [0.0, 0.3, 0.6]))
        scope = RedPitayaOscilloscope(driver)
        
        pulse = scope.acquire(channel=1)

        self.assertEqual(Pulse((Sample(0.0, 0.0),
                                Sample(0.1, 0.3),
                                Sample(0.2, 0.6))), pulse)


class ScpiOscilloscopeDriverTest(TestCase):

    def test_can_create_scpi_oscilloscope_driver(self):
        driver = ScpiOscilloscopeDriver(address='rp-f0060c.local')

    def test_open(self):
        driver = ScpiOscilloscopeDriver(address='rp-f0060c.local')
        driver.open()

    def test_close(self):
        driver = ScpiOscilloscopeDriver(address='rp-f0060c.local')
        driver.open()
        driver.close()

    def test_acquire(self):
        driver = ScpiOscilloscopeDriver(address='rp-f0060c.local')
        driver.open()
        result = driver.acquire(channel=1)
        driver.close()
