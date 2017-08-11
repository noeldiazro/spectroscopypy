from scpipy import get_tcpip_scpi_connection, Generator
from spectroscopypy import PulseDataFileReader, RedPitayaGeneratorChannel
import sys


def read_pulse(path, samples_per_pulse):
    with PulseDataFileReader(path, samples_per_pulse) as reader:
        return reader.read()
    
def get_channel(host, channel_id):
    connection = get_tcpip_scpi_connection(host, timeout=1)
    generator = Generator(connection)
    return RedPitayaGeneratorChannel(channel_id, connection, generator)


def main(host, channel_id, path, samples_per_pulse):
    pulse = read_pulse(path, samples_per_pulse)
    with get_channel(host, channel_id) as channel:
        channel.write(pulse.smooth())


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
    
