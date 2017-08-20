from spectroscopypy import PulsePlotter, RedPitaya
import sys


def main(host, channel_id):
    red_pitaya = RedPitaya(host)
    with red_pitaya.get_oscilloscope_channel(channel_id) as channel:
        pulse = channel.read()
    with PulsePlotter() as plotter:
        plotter.write(pulse)
        plotter.show()

if __name__ == '__main__':
    main(host=sys.argv[1], channel_id=int(sys.argv[2]))
