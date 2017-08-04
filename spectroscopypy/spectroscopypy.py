from abc import ABCMeta, abstractmethod, abstractproperty
from array import array
from collections import namedtuple

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

def plot_pulse(reader):
    reader.open()
    pulse = reader.read()
    reader.close()


class PulseReader(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def read(self):
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
