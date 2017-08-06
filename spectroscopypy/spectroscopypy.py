from abc import ABCMeta, abstractmethod, abstractproperty
from array import array
from collections import namedtuple
import matplotlib.pyplot as plt


Sample = namedtuple('Sample', ['time', 'voltage'])


class Pulse(object):

    def __init__(self, samples=tuple()):
        self._samples = samples

    def __len__(self):
        return len(self._samples)

    def __getitem__(self, position):
        if isinstance(position, slice):
            return Pulse(self._samples[position])
        else:
            return self._samples[position]

    def __contains__(self, item):
        return item in self._samples

    def __iter__(self):
        return self._samples.__iter__()

    def __eq__(self, other):
        return all([sample1 == sample2 for sample1, sample2 in zip(self, other)])

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def get_maximum_voltage(self):
        return max([sample.voltage for sample in self._samples])

def plot_pulse(reader, writer):
    reader.open()
    writer.open()
    pulse = reader.read()
    writer.write(pulse)
    reader.close()
    writer.close()

class PulseIO(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractproperty
    def closed():
        pass

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class PulseReader(PulseIO):
    __metaclass__ = ABCMeta

    @abstractmethod
    def read(self):
        pass


class PulseWriter(PulseIO):
    __metaclass__ = ABCMeta

    @abstractmethod
    def write(self, pulse):
        pass


class PulseDataFileReader(PulseReader):

    def __init__(self, path, samples_per_pulse):
        self._path = path
        self._file = None
        self._samples_per_pulse = samples_per_pulse

    def open(self):
        self._file = open(self._path, 'r')

    def read(self):
        times = array('d')
        times.read(self._file, self._samples_per_pulse)

        voltages = array('d')
        voltages.read(self._file, self._samples_per_pulse)
        
        return Pulse(tuple([Sample(time, voltage) for time, voltage in zip(times, voltages)]))

    def close(self):
        self._file.close()

    @property
    def closed(self):
        return True if self._file is None else self._file.closed


class PulsePlotter(PulseWriter):
    def __init__(self):
        self._closed = True

    def open(self):
        self._closed = False
        self._figure = plt.figure()
        self._axes = self._figure.add_subplot(111)

    def write(self, pulse):
        times = [sample.time * 1000000 for sample in pulse]
        voltages = [sample.voltage for sample in pulse]

        self._axes.plot(times, voltages, 'b-')
        self._axes.set_xlabel('Time (us)')
        self._axes.set_ylabel('Voltage (V)')
        self._axes.set_yticks([i for i in range(0, 9)])
        self._axes.grid(True)
        self._axes.axis([-3, 13, -1, 9])

    def show(self):
        plt.show()

    def close(self):
        self._closed = True

    @property
    def closed(self):
        return self._closed


class PulseAcquisitor(object):

    def __init__(self, oscilloscope):
        self._oscilloscope = oscilloscope

    def acquire(self):
        return self._oscilloscope.acquire()


class Oscilloscope(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def acquire(self):
        pass

def generate_pulse(pulse, channel, generator):
    generator.open()
    generator.write(pulse, channel)
    generator.close()


class Generator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def write(self, pulse, channel):
        pass

    @abstractmethod
    def close(self):
        pass
