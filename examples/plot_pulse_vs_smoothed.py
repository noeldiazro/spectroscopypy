from spectroscopypy import PulseDataFileReader, PulsePlotter

def get_pulse():
    with PulseDataFileReader('bi_207_amp.dat', 8000) as reader:
        return reader.read()

def plot_pulse(pulse):
    with PulsePlotter() as plotter:
        plotter.write(pulse)
        plotter.show()

pulse = get_pulse()
plot_pulse(pulse)
plot_pulse(pulse.smooth())

