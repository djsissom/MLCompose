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



class TestDurationTuplets(unittest.TestCase):
	def test_duplets(self):
		d = mus.Duration('eighth', tuplet=2)
		self.assertAlmostEqual(d.length, (1/8)*(3/2))
		return


	def test_triplets(self):
		d = mus.Duration('eighth', tuplet=3)
		self.assertAlmostEqual(d.length, (1/8)*(2/3))
		return


	def test_quadruplets(self):
		d = mus.Duration('eighth', tuplet=4)
		self.assertAlmostEqual(d.length, (1/8)*(3/4))
		return


	def test_quintuplets(self):
		d = mus.Duration('eighth', tuplet=5)
		self.assertAlmostEqual(d.length, (1/8)*(4/5))
		return

	#-------------------------------------------------------

	def test_duplet_names(self):
		d = mus.Duration('eighth', tuplet=2)
		self.assertEqual(d.name, 'duplet eighth')
		return


	def test_triplet_names(self):
		d = mus.Duration('eighth', tuplet=3)
		self.assertEqual(d.name, 'triplet eighth')
		return


	def test_quadruplet_names(self):
		d = mus.Duration('eighth', tuplet=4)
		self.assertEqual(d.name, 'quadruplet eighth')
		return


	def test_quintuplet_names(self):
		d = mus.Duration('eighth', tuplet=5)
		self.assertEqual(d.name, 'quintuplet eighth')
		return

	#-------------------------------------------------------

	def test_duplet_setting_by_names(self):
		d = mus.Duration('eighth', tuplet='duplet')
		self.assertAlmostEqual(d.length, (1/8)*(3/2))

		d = mus.Duration('duplet eighth')
		self.assertAlmostEqual(d.length, (1/8)*(3/2))
		return


	def test_triplet_setting_by_names(self):
		d = mus.Duration('eighth', tuplet='triplet')
		self.assertAlmostEqual(d.length, (1/8)*(2/3))

		d = mus.Duration('triplet eighth')
		self.assertAlmostEqual(d.length, (1/8)*(2/3))
		return


	def test_quadruplet_setting_by_names(self):
		d = mus.Duration('eighth', tuplet='quadruplet')
		self.assertAlmostEqual(d.length, (1/8)*(3/4))

		d = mus.Duration('quadruplet eighth')
		self.assertAlmostEqual(d.length, (1/8)*(3/4))
		return


	def test_quintuplet_setting_by_names(self):
		d = mus.Duration('eighth', tuplet='quintuplet')
		self.assertAlmostEqual(d.length, (1/8)*(4/5))

		d = mus.Duration('quintuplet eighth')
		self.assertAlmostEqual(d.length, (1/8)*(4/5))
		return

	#-------------------------------------------------------

	def test_duplet_setting_by_length(self):
		d = mus.Duration('eighth', tuplet=2)
		testlength = d.length
		d = mus.Duration(length=testlength)
		self.assertAlmostEqual(d.length, testlength)
		return


	def test_triplet_setting_by_length(self):
		d = mus.Duration('eighth', tuplet=3)
		testlength = d.length
		d = mus.Duration(length=testlength)
		self.assertAlmostEqual(d.length, testlength)
		return


	def test_quadruplet_setting_by_length(self):
		d = mus.Duration('eighth', tuplet=4)
		testlength = d.length
		d = mus.Duration(length=testlength)
		self.assertAlmostEqual(d.length, testlength)
		return


	def test_quintuplet_setting_by_length(self):
		d = mus.Duration('eighth', tuplet=5)
		testlength = d.length
		d = mus.Duration(length=testlength)
		self.assertAlmostEqual(d.length, testlength)
		return

	#-------------------------------------------------------

	def test_duplet_setting_by_auto_length(self):
		d = mus.Duration('eighth', tuplet=2)
		testlength = d.length
		d = mus.Duration(testlength)
		self.assertAlmostEqual(d.length, testlength)
		return


	def test_triplet_setting_by_auto_length(self):
		d = mus.Duration('eighth', tuplet=3)
		testlength = d.length
		d = mus.Duration(testlength)
		self.assertAlmostEqual(d.length, testlength)
		return


	def test_quadruplet_setting_by_auto_length(self):
		d = mus.Duration('eighth', tuplet=4)
		testlength = d.length
		d = mus.Duration(testlength)
		self.assertAlmostEqual(d.length, testlength)
		return


	def test_quintuplet_setting_by_auto_length(self):
		d = mus.Duration('eighth', tuplet=5)
		testlength = d.length
		d = mus.Duration(testlength)
		self.assertAlmostEqual(d.length, testlength)
		return

	#-------------------------------------------------------

	def test_duplet_setting_by_length_retain_tuplet(self):
		d = mus.Duration('eighth', tuplet=2)
		testlength = d.length
		d = mus.Duration(length=testlength, tuplet=2)
		self.assertAlmostEqual(d.length, testlength)
		self.assertEqual(d.tuplet, 2)
		return


	def test_triplet_setting_by_length_retain_tuplet(self):
		d = mus.Duration('eighth', tuplet=3)
		testlength = d.length
		d = mus.Duration(length=testlength, tuplet=3)
		self.assertAlmostEqual(d.length, testlength)
		self.assertEqual(d.tuplet, 3)
		return


	def test_quadruplet_setting_by_length_retain_tuplet(self):
		d = mus.Duration('eighth', tuplet=4)
		testlength = d.length
		d = mus.Duration(length=testlength, tuplet=4)
		self.assertAlmostEqual(d.length, testlength)
		self.assertEqual(d.tuplet, 4)
		return


	def test_quintuplet_setting_by_length_retain_tuplet(self):
		d = mus.Duration('eighth', tuplet=5)
		testlength = d.length
		d = mus.Duration(length=testlength, tuplet=5)
		self.assertAlmostEqual(d.length, testlength)
		self.assertEqual(d.tuplet, 5)
		return

	#-------------------------------------------------------

	def test_duplet_setting_by_auto_length_retain_tuplet(self):
		d = mus.Duration('eighth', tuplet=2)
		testlength = d.length
		d = mus.Duration(testlength, tuplet=2)
		self.assertAlmostEqual(d.length, testlength)
		self.assertEqual(d.tuplet, 2)
		return


	def test_triplet_setting_by_auto_length_retain_tuplet(self):
		d = mus.Duration('eighth', tuplet=3)
		testlength = d.length
		d = mus.Duration(testlength, tuplet=3)
		self.assertAlmostEqual(d.length, testlength)
		self.assertEqual(d.tuplet, 3)
		return


	def test_quadruplet_setting_by_auto_length_retain_tuplet(self):
		d = mus.Duration('eighth', tuplet=4)
		testlength = d.length
		d = mus.Duration(testlength, tuplet=4)
		self.assertAlmostEqual(d.length, testlength)
		self.assertEqual(d.tuplet, 4)
		return


	def test_quintuplet_setting_by_auto_length_retain_tuplet(self):
		d = mus.Duration('eighth', tuplet=5)
		testlength = d.length
		d = mus.Duration(testlength, tuplet=5)
		self.assertAlmostEqual(d.length, testlength)
		self.assertEqual(d.tuplet, 5)
		return



if __name__ == "__main__":
	unittest.main()

