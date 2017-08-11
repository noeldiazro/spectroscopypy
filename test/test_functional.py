from unittest import TestCase
from scpipy import TcpIpAddress, TcpIpLink, ScpiConnection, Oscilloscope
from spectroscopypy import Commander, RedPitayaOscilloscopeChannel, PulsePlotter

class FunctionalTest(TestCase):

    def test_read_pulse(self):
        link = TcpIpLink(TcpIpAddress('rp-f0060c.local', 5000), timeout=1)
        connection = ScpiConnection(link)
        scope = Oscilloscope(connection)
        commander = Commander(connection, scope)
        with RedPitayaOscilloscopeChannel(1, commander) as scope_channel:
            pulse = scope_channel.read()
        self.assertEqual(16384, len(pulse))

        
