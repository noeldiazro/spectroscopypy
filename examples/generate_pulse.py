from spectroscopypy import PulseDataFileReader, RedPitaya
import sys


def read_pulse(path, samples_per_pulse):
    with PulseDataFileReader(path, samples_per_pulse) as reader:
        return reader.read()
    
def main(host, channel_id, path, samples_per_pulse):
    pulse = read_pulse(path, samples_per_pulse)
    red_pitaya = RedPitaya(host)
    with red_pitaya.get_generator_channel(channel_id) as channel:
        channel.write(pulse.smooth())

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
