from mock import Mock
from unittest import TestCase, skip
from spectroscopypy.instruments import *
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


class RedPitayaGeneratorTest(TestCase):

    def test_can_create_generator(self):
        generator = RedPitayaGenerator(commander=Mock(GeneratorCommander))

    def test_open_generator(self):
        commander = Mock(GeneratorCommander)
        generator = RedPitayaGenerator(commander)

        generator.open()
        
        commander.open.assert_called_once_with()

    def test_close_generator(self):
        commander = Mock(GeneratorCommander)
        generator = RedPitayaGenerator(commander)

        generator.close()

        commander.close.assert_called_once_with()

    def test_write(self):
        commander = Mock(GeneratorCommander)
        generator = RedPitayaGenerator(commander)

        pulse = Pulse((
                Sample(0.0, 0.0),
                Sample(0.1, 0.3),
                Sample(0.2, 0.6),))
        channel = 1
        
        generator.write(pulse, channel)

        commander.write.assert_called_once_with(pulse, channel)
    
        
class ScpiOscilloscopeDriverTest(TestCase):

    def test_can_create_scpi_oscilloscope_driver(self):
        driver = ScpiOscilloscopeDriver(address='rp-f0060c.local')

    @skip('WIP')
    def test_open(self):
        driver = ScpiOscilloscopeDriver(address='rp-f0060c.local')
        driver.open()

    @skip('WIP')
    def test_close(self):
        driver = ScpiOscilloscopeDriver(address='rp-f0060c.local')
        driver.open()
        driver.close()

    @skip('WIP')
    def test_acquire(self):
        driver = ScpiOscilloscopeDriver(address='rp-f0060c.local')
        driver.open()
        result = driver.acquire(channel=1)
        driver.close()

        
class ScpiGeneratorCommanderTest(TestCase):

    def test_can_create_scpi_generator_commander(self):
        commander = ScpiGeneratorCommander(host='rp-f0060c.local')

    def test_open(self):
        commander = ScpiGeneratorCommander(host='rp-f0060c.local', connection=Mock(scpipy.ScpiConnection))
        commander.open()
        
