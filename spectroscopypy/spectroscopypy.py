from abc import ABCMeta, abstractmethod, abstractproperty
from array import array
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np
from scpipy import Waveform


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

    @property
    def times(self):
        return tuple([time for time, _ in self._samples])

    @property
    def voltages(self):
        return tuple([voltage for _, voltage in self._samples])

    def smooth(self, window_size=1000, order=4):
        '''http://scipy.github.io/old-wiki/pages/Cookbook/SavitzkyGolay'''
        order_range = range(order + 1)
        half_window = (window_size - 1) // 2
        b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window + 1)])
        m = np.linalg.pinv(b).A[0]

        y = np.asarray(self.voltages)
        firstvals = y[0] - np.abs(y[1:half_window+1][::-1] - y[0])
        lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
        
        smoothed_y = np.convolve(m[::-1],
                                 np.concatenate((firstvals, y, lastvals)),
                                 mode='valid')

        return Pulse(tuple([Sample(time, voltage) for time, voltage in zip(self.times, smoothed_y)]))
        
    def normalize_times(self):
        min_time = min(self.times)
        return Pulse(tuple(
            Sample(time, voltage)
            for time, voltage
            in zip([time - min_time for time in self.times], self.voltages)))

    def normalize_voltages(self):
        max_voltage = max(self.voltages)
        return Pulse(tuple(
            Sample(time, voltage)
            for time, voltage
            in zip(self.times, [1.0*voltage/max_voltage for voltage in self.voltages])))
        

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
#        self._axes.set_yticks([i for i in range(0, 9)])
        self._axes.grid(True)
#        self._axes.axis([-3, 13, -1, 9])

    def show(self):
        plt.show()

    def close(self):
        self._closed = True

    @property
    def closed(self):
        return self._closed


class RedPitaya(object):

    def __init__(self, host, port=5000):
        self._host = host
        self._port = port

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    def get_scope_channel(self, channel_id):
        return RedPitayaOscilloscopeChannel(channel_id)


class RedPitayaOscilloscopeChannel(PulseReader):

    def __init__(self, channel_id, commander):
        self._channel_id = channel_id
        self._commander = commander
    
    @property
    def channel_id(self):
        return self._channel_id

    def open(self):
        self._commander.open()

    def close(self):
        self._commander.close()

    def read(self):
        return self._commander.read(self._channel_id)

    @property
    def closed(self):
        return self._commander.closed


class RedPitayaGeneratorChannel(PulseWriter):
    
    def __init__(self, channel_id, connection, generator):
        self._channel_id = channel_id
        self._connection = connection
        self._generator = generator
        
    def open(self):
        self._connection.open()

    def close(self):
        self._connection.close()

    def write(self, pulse):
        self._generator.reset()

        self._generator.set_waveform(self.channel_id, Waveform.ARBITRARY)
        self._generator.set_arbitrary_waveform_data(self.channel_id, pulse.voltages)
        pulse_sampling_period = pulse.times[1] - pulse.times[0]
        self._generator.set_frequency(self.channel_id, int(1/(pulse_sampling_period*16384)))
        self._generator.set_amplitude(self.channel_id, 1)

        self._generator.set_burst_count(self.channel_id, 1)
        self._generator.set_burst_repetitions(self.channel_id, 1)
        self._generator.set_burst_period(self.channel_id, 2000)

        self._generator.enable_output(self.channel_id)
        self._generator.enable_burst(self.channel_id)
        self._generator.trigger_immediately(self.channel_id)

    @property
    def closed(self):
        return self._connection.closed

    @property
    def channel_id(self):
        return self._channel_id


class Commander(object):

    def __init__(self, connection, scope):
        self._connection = connection
        self._scope = scope

    @property
    def closed(self):
        return self._connection.closed

    def open(self):
        self._connection.open()

    def close(self):
        self._connection.close()

    def read(self, channel_id):
        self._scope.reset()
        self._scope.set_decimation_factor(64)
        self._scope.start()
        self._scope.trigger_immediately()
        times, voltages = self._scope.get_acquisition(channel_id)
        return Pulse(tuple([Sample(time, voltage) for time, voltage in zip(times, voltages)]))
