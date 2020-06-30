#!/usr/bin/env python

import unittest
from mlcompose import music as mus



class TestMeasure(unittest.TestCase):
	def test_get_remaining_duration_simple(self):
		measure = mus.Measure()
		beat = measure.beats[0]
		note = beat.add_note(mus.Note('C_6', duration='quarter'))
		self.assertEqual(measure.remining_duration, 0.75)
		return


	def test_get_remaining_duration_complex(self):
		measure = mus.Measure(time_signature='5/8')
		beat = measure.beats[0]
		note = beat.add_note(mus.Note('C_6', duration='quarter'))

		beat = measure.append_beat()
		note1 = beat.add_note(mus.Note('C_6', duration='eighth'))
		note2 = beat.add_note(mus.Note('C_7', duration='dotted eighth'))
		note3 = beat.add_note(mus.Note('C_8', duration='dotted quarter'))

		self.assertEqual(measure.remining_duration, 1/4)
		self.assertEqual(measure.get_remaining_duration(method='min'), 0.25)
		self.assertEqual(measure.get_remaining_duration(method='max'), 0)
		self.assertEqual(measure.get_remaining_duration(note=note2), 3/16)
		return


	def test_pad_rests_simple(self):
		measure = mus.Measure()
		beat = measure.beats[0]
		note = beat.add_note(mus.Note('C_6', duration='quarter'))
		measure.pad_rests()
		self.assertEqual(measure.beats[-1].notes[0].duration.length, 0.75)
		return


	def test_pad_rests_complex(self):
		measure = mus.Measure(time_signature='5/8')
		beat = measure.beats[0]
		note = beat.add_note(mus.Note('C_6', duration='quarter'))

		beat = measure.append_beat()
		note1 = beat.add_note(mus.Note('C_6', duration='eighth'))
		note2 = beat.add_note(mus.Note('C_7', duration='dotted eighth'))
		note3 = beat.add_note(mus.Note('C_8', duration='dotted quarter'))
		measure.pad_rests()

		rest1 = measure.beats[-2].notes[0]
		rest2 = measure.beats[-1].notes[0]

		self.assertIsInstance(rest1, mus.Rest)
		self.assertIsInstance(rest2, mus.Rest)

		self.assertEqual(len(measure.beats), 4)
		self.assertEqual(rest1.duration.length, 0.25)
		self.assertEqual(rest2.duration.length, 3/16)
		return



if __name__ == "__main__":
	unittest.main()

