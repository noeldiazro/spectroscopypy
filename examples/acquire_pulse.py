from scpipy import get_tcpip_scpi_connection, Oscilloscope
from spectroscopypy import PulsePlotter, RedPitayaOscilloscopeChannel
import sys

def get_channel(host, channel_id):
    connection = get_tcpip_scpi_connection(host, timeout=1)
    oscilloscope = Oscilloscope(connection)
    return RedPitayaOscilloscopeChannel(channel_id, connection, oscilloscope)

def main(host, channel_id):
    with get_channel(host, channel_id) as channel:
        pulse = channel.read()
    with PulsePlotter() as plotter:
        plotter.write(pulse)
        plotter.show()

if __name__ == '__main__':
    main(host=sys.argv[1], channel_id=int(sys.argv[2]))
