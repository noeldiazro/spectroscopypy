from mock import Mock
from unittest import TestCase
from spectroscopypy import *

class UseCasesTest(TestCase):

    def test_generate_pulse(self):
        pulse = Pulse((
            Sample(0.0, 0.0),
            Sample(0.1, 0.2),
            Sample(0.2, 0.4),))
        channel = 1
        generator = Mock(Generator)
        generate_pulse(pulse, channel, generator)

        generator.open.assert_called_once_with()
        generator.write.assert_called_once_with(pulse, channel)
        generator.close.assert_called_once_with()

