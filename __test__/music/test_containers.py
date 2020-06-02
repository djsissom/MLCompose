#!/usr/bin/env python

import unittest
from mlcompose import music as mus



class TestMeasure(unittest.TestCase):
	# TODO:  Write Measure tests.
	def test_get_remaining_duration(self):
		measure = mus.Measure()
		#beat = measure.append_beat()
		beat = measure.beats[0]
		note = beat.add_note(mus.Note('C_6'))
		measure.pad_rests()
		for beat in measure.beats:
			print(beat)
		return



if __name__ == "__main__":
	unittest.main()

