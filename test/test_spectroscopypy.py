from mock import Mock
from unittest import TestCase
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
        
    def test_get_maximum_voltage(self):
        pulse = Pulse((Sample(0.0, 0.0), Sample(0.1, 0.2), Sample(0.2, 0.4), Sample(0.3, 0.25)))
        self.assertAlmostEqual(0.4, pulse.get_maximum_voltage())


class PulseAcquisitorTest(TestCase):

    def test_can_create_pulse_acquisitor(self):
        oscilloscope_stub = Mock(Oscilloscope)
        pulse_acquisitor = PulseAcquisitor(oscilloscope_stub)

    def test_acquire_pulse(self):
        oscilloscope_stub = Mock(Oscilloscope)
        oscilloscope_stub.acquire = Mock(return_value=Pulse((Sample(0, 0),
                                                             Sample(1, 2),
                                                             Sample(2, 4))))
        acquisitor = PulseAcquisitor(oscilloscope_stub)
        pulse = acquisitor.acquire()
        expected_pulse = Pulse((Sample(0, 0),
                                Sample(1, 2),
                                Sample(2, 4)))
        self.assertEqual(expected_pulse, pulse)


class PlotPulseTest(TestCase):

    def get_sample_pulse(self):
        return Pulse((Sample(0, 0), Sample(0.1, 0.3), Sample(0.2, 0.8)))
    
    def test_plot_pulse_from_datafile(self):
        reader = Mock(PulseReader)
        reader.open = Mock(return_value=None)
        reader.read = Mock(return_value=self.get_sample_pulse())
        reader.close = Mock()
        
        writer = Mock(PulseWriter)
        writer.open = Mock()
        writer.write = Mock()
        writer.close = Mock()
        
        plot_pulse(reader, writer)

        reader.open.assert_called_once_with()
        reader.read.assert_called_once_with()
        reader.close.assert_called_once_with()


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
