from abc import ABCMeta, abstractmethod
import scpipy
from spectroscopypy import Oscilloscope, Pulse, Sample

class RedPitayaOscilloscope(Oscilloscope):
    def __init__(self, driver):
        self._driver = driver

    def acquire(self, channel):
        times, voltages = self._driver.acquire(channel)
        samples = tuple( [Sample(time, voltage) for time, voltage in zip(times, voltages)] )
        return Pulse(samples)


class OscilloscopeDriver(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def acquire(self, channel):
        pass


class ScpiOscilloscopeDriver(OscilloscopeDriver):

    def __init__(self, address):
        self._address = address
        self._connection = None
        self._commander = None
        
    def open(self):
        self._connection = scpipy.get_tcpip_scpi_connection(self._address)
        self._connection.open()
        self._commander = scpipy.Oscilloscope(self._connection)

    def close(self):
        self._connection.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    def acquire(self, channel):
        return self._commander.get_acquisition(channel)
        
