from mock import Mock
from unittest import TestCase, skip
from spectroscopypy import *


class SampleTest(TestCase):

    def test_sample_can_be_created(self):
        sample = Sample(time=0.2, voltage=1.5)
        self.assertAlmostEqual(0.2, sample.time, delta=0.0001)
        self.assertAlmostEqual(1.5, sample.voltage, delta=0.0001)

    def test_samples_are_immutable(self):
        sample = Sample(time=0.2, voltage=1.5)
        with self.assertRaises(AttributeError):
            sample.voltage = 0.3


class PulseTest(TestCase):

    def get_test_samples(self):
        return (
            Sample(time=0.0, voltage=0.0),
            Sample(time=0.1, voltage=0.2),
            Sample(time=0.2, voltage=0.4),)
    
    def test_empty_pulse_has_zero_length(self):
        pulse = Pulse()
        self.assertEqual(0, len(pulse))
            
    def test_non_empty_pulse_has_correct_length(self):
        pulse = Pulse(self.get_test_samples())
        self.assertEqual(3, len(pulse))

    def test_get_sample_by_index(self):
        samples = self.get_test_samples()
        pulse = Pulse(samples)
        self.assertEqual(samples[1], pulse[1])

    def test_get_subpulse_by_slicing(self):
        samples = self.get_test_samples()
        pulse = Pulse(samples)
        self.assertEqual(2, len(pulse[:-1]))

    def test_pulse_sample_cannot_be_set(self):
        samples = self.get_test_samples()
        pulse = Pulse(samples)
        with self.assertRaises(TypeError):
            pulse[1] = Sample(0.1, 0.3)

    def test_pulse_contains_sample(self):
        samples = self.get_test_samples()
        pulse = Pulse(samples)
        self.assertIn(Sample(samples[1].time, samples[1].voltage), pulse)

    def test_pulse_can_be_iterated(self):
        samples = self.get_test_samples()
        pulse = Pulse(samples)
        number_of_samples = 0
        for sample in pulse:
            number_of_samples += 1
        self.assertEqual(len(samples), number_of_samples)

    def test_pulses_with_same_samples_in_same_order_are_equal(self):
        pulse1 = Pulse(self.get_test_samples())
        pulse2 = Pulse(self.get_test_samples())
        self.assertTrue(pulse1 == pulse2)

    def test_pulses_with_same_samples_in_different_order_are_not_equal(self):
        pulse1 = Pulse((Sample(0.0, 0.1), Sample(0.1, 0.4)))
        pulse2 = Pulse((Sample(0.1, 0.4), Sample(0.0, 0.1)))
        self.assertTrue(pulse1 != pulse2)

    def test_get_times(self):
        pulse = Pulse((Sample(0.0, 0.0), Sample(0.1, 0.2), Sample(0.2, 0.4), Sample(0.3, 0.25)))
        self.assertEqual((0.0, 0.1, 0.2, 0.3), pulse.times)

    def test_get_voltages(self):
        pulse = Pulse((Sample(0.0, 0.0), Sample(0.1, 0.2), Sample(0.2, 0.4), Sample(0.3, 0.25)))
        self.assertEqual((0.0, 0.2, 0.4, 0.25), pulse.voltages)
        
    def test_get_maximum_voltage(self):
        pulse = Pulse((Sample(0.0, 0.0), Sample(0.1, 0.2), Sample(0.2, 0.4), Sample(0.3, 0.25)))
        self.assertAlmostEqual(0.4, pulse.get_maximum_voltage())

    @skip('wip')
    def test_normalize_times(self):
        pulse = Pulse((Sample(-0.2, 0.4),
                       Sample(-0.1, 0.6),
                       Sample(0, 0.8),
                       Sample(0.1, 1.2),
                       Sample(0.2, 0.9),))

        normalized_pulse = pulse.normalize_times()

        expected_pulse = Pulse((Sample(0.0, 0.4),
                                Sample(0.1, 0.6),
                                Sample(0.2, 0.8),
                                Sample(0.3, 1.2),
                                Sample(0.4, 0.9),))
        self.assertEqual(expected_pulse.times, normalized_pulse.times)

    def test_normalize_voltages(self):
        pulse = Pulse((Sample(0.0, 0.0),
                       Sample(0.1, 1.0),
                       Sample(0.2, 2.0),
                       Sample(0.3, 3.0),
                       Sample(0.4, 4.0),))

        normalized_pulse = pulse.normalize_voltages()

        expected_pulse = Pulse((Sample(0.0, 0.0),
                       Sample(0.1, 0.25),
                       Sample(0.2, 0.5),
                       Sample(0.3, 0.75),
                       Sample(0.4, 1.0),))
        self.assertEqual(expected_pulse.voltages, normalized_pulse.voltages)
        

class PulseDataFileReaderTest(TestCase):

    def setUp(self):
        self.samples_per_pulse=8000
        self.reader = PulseDataFileReader(path='bi_207_amp.dat', samples_per_pulse=self.samples_per_pulse)

    def test_data_file_reader_is_closed_on_creation(self):
        self.assertTrue(self.reader.closed)

    def test_data_file_reader_is_not_closed_after_open(self):
        self.reader.open()
        self.assertFalse(self.reader.closed)

    def test_data_file_reader_is_closed_after_close(self):
        self.reader.open()
        self.reader.close()
        self.assertTrue(self.reader.closed)

    def test_pulse_has_correct_number_of_samples(self):
        with self.reader as r:
            pulse = self.reader.read()

        self.assertEqual(self.samples_per_pulse, len(pulse))


class PulsePlotterTest(TestCase):

    def setUp(self):
        self.plotter = PulsePlotter()
        
    def test_plotter_is_closed_on_creation(self):
        self.assertTrue(self.plotter.closed)

    def test_plotter_is_not_closed_after_open(self):
        self.plotter.open()
        self.assertFalse(self.plotter.closed)

    def test_plotter_is_closed_after_close(self):
        self.plotter.open()
        self.plotter.close()
        self.assertTrue(self.plotter.closed)

    def test_write(self):
        with self.plotter as plotter:
            self.plotter.write(pulse=Pulse((Sample(0, 0), Sample(1, 2), Sample(2, 4), Sample(3, -1))))


class RedPitayaOscilloscopeChannelTest(TestCase):

    def test_channel_is_closed_on_creation(self):
        channel = RedPitayaOscilloscopeChannel(1, FakeCommander())
        self.assertTrue(channel.closed)

    def test_channel_is_not_closed_after_open(self):
        channel = RedPitayaOscilloscopeChannel(1, FakeCommander())
        channel.open()
        self.assertFalse(channel.closed)

    def test_channel_is_closed_after_closing(self):
        channel = RedPitayaOscilloscopeChannel(1, FakeCommander())
        channel.open()
        channel.close()
        self.assertTrue(channel.closed)

    def test_read_pulse_with_correct_length(self):
        with RedPitayaOscilloscopeChannel(1, FakeCommander()) as channel:
            pulse = channel.read()
        self.assertEqual(5, len(pulse))


class RedPitayaGeneratorChannelTest(TestCase):

    def setUp(self):
        self.CHANNEL_ID = 1
        self.channel = TestableRedPitayaGeneratorChannel(self.CHANNEL_ID, FakeConnection(), Mock(Generator))

    def test_correct_channel_id(self):
        self.assertTrue(self.CHANNEL_ID, self.channel.channel_id)
        
    def test_channel_is_closed_after_creation(self):
        self.assertTrue(self.channel.closed)

    def test_channel_is_not_closed_after_open(self):
        self.channel.open()
        self.assertFalse(self.channel.closed)

    def test_channel_is_closed_after_closing(self):
        self.channel.open()
        self.channel.close()
        self.assertTrue(self.channel.closed)

    def test_write(self):
        self.channel.write(Pulse((Sample(0, 0), Sample(1e-6, 2), Sample(2e-6, 4), Sample(3e-6, -1))))
        self.assertTrue(self.channel.generator.reset.called)
        self.assertTrue(self.channel.generator.set_waveform.called)
        self.channel.generator.set_arbitrary_waveform_data.assert_called_once_with(self.CHANNEL_ID, (0, 2, 4, -1))
        self.channel.generator.set_frequency.assert_called_once_with(self.CHANNEL_ID, 61)
        self.channel.generator.set_amplitude.assert_called_once_with(self.CHANNEL_ID, 1)

        self.channel.generator.set_burst_count.assert_called_once_with(self.CHANNEL_ID, 1)
        self.channel.generator.set_burst_repetitions.assert_called_once_with(self.CHANNEL_ID, 1)
        self.channel.generator.set_burst_period.assert_called_once_with(self.CHANNEL_ID, 2000)
        self.channel.generator.enable_output.assert_called_once_with(self.CHANNEL_ID)
        


class TestableRedPitayaGeneratorChannel(RedPitayaGeneratorChannel):

    def __init__(self, channel_id, connection, generator):
        RedPitayaGeneratorChannel.__init__(self, channel_id, connection, generator)
        self.generator = generator
        


class CommanderTest(TestCase):
    
    def test_can_create_commander(self):
        connection = FakeConnection()
        scope = FakeScope()
        commander = Commander(connection, scope)

    def test_commander_is_closed_on_creation(self):
        commander = Commander(FakeConnection(), FakeScope())
        self.assertTrue(commander.closed)

    def test_commander_is_not_closed_after_open(self):
        commander = Commander(FakeConnection(), FakeScope())
        commander.open()
        self.assertFalse(commander.closed)

    def test_commander_is_closed_after_close(self):
        commander = Commander(FakeConnection(), FakeScope())
        commander.open()
        commander.close()
        self.assertTrue(commander.closed)

    
    #def test_read_pulse_with_correct_length(self):
    #    commander = Commander(FakeConnection(), FakeScope())
    #    commander.open()
    #    pulse = commander.read(channel_id=1)
    #    commander.close()
    #    self.assertEqual(5, len(pulse))


class FakeCommander(object):

    def __init__(self):
        self._closed = True

    def open(self):
        self._closed = False

    def close(self):
        self._closed = True

    def read(self, channel_id):
        return Pulse((Sample(0.0, 0.0),
                     Sample(0.1, 0.2),
                     Sample(0.2, 0.6),
                     Sample(0.3, 0.7),
                     Sample(0.4, 0.9),))
    
    @property
    def closed(self):
        return self._closed


class FakeConnection(object):

    def __init__(self):
        self._closed = True

    def open(self):
        self._closed = False

    def close(self):
        self._closed = True

    @property
    def closed(self):
        return self._closed


class FakeScope(object):

    def get_acquisition(self, channel_id):
        return ([0.0, 0.1, 0.2, 0.3, 0.4],
                [0.0, 0.2, 0.6, 0.7, 0.9],)


class Generator(object):

    def reset(self):
        pass

    def set_waveform(self, channel_id, waveform):
        pass

    def set_arbitrary_waveform_data(self, channel_id, data):
        pass

    def set_frequency(self, channel_id, frequency):
        pass

    def set_amplitude(self, channel_id, amplitude):
        pass

    def set_burst_count(self, channel_id, count):
        pass

    def set_burst_repetitions(self, channel_id, count):
        pass

    def set_burst_period(self, channel_id, period):
        pass

    def enable_output(self, channel_id):
        pass

    def enable_burst(self, channel_id):
        pass

    def trigger_immediately(self, channel_id):
        pass
