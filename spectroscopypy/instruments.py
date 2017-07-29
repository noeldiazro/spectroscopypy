from abc import ABCMeta, abstractmethod
import scpipy
from spectroscopypy import *

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


class RedPitayaGenerator(Generator):

    def __init__(self, commander):
        self._commander = commander

    def open(self):
        self._commander.open()

    def write(self, pulse, channel):
        self._commander.write(pulse, channel)

    def close(self):
        self._commander.close()

    
class GeneratorCommander(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def write(self, pulse, chanel):
        pass


class ScpiGeneratorCommander(GeneratorCommander):
    def __init__(self, host, connection=None):
        self._connection = connection or scpipy.get_tcpip_scpi_connection(host)
        self._generator = scpipy.Generator(self._connection)

    def open(self):
        self._connection.open()

    def write(self, pulse, channel):
        pass

    def close(self):
        pass
