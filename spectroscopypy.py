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

    def get_maximum_voltage(self):
        return max([sample.voltage for sample in self._samples])
