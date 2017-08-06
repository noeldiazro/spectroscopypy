from spectroscopypy import PulseDataFileReader, PulsePlotter
import sys

def main(file_path, samples_per_pulse, number_of_pulses):
    with PulsePlotter() as plotter:
        with PulseDataFileReader(file_path, samples_per_pulse) as reader:
            for _ in range(number_of_pulses):
                plotter.write(reader.read())
            plotter.show()


if __name__ == '__main__':
    main(file_path=sys.argv[1],
         samples_per_pulse=int(sys.argv[2]),
         number_of_pulses=int(sys.argv[3]))
    
