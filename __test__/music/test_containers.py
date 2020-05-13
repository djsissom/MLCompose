#!/usr/bin/env python

import unittest
from mlcompose import music as mus



class TestMeasure(unittest.TestCase):
	def test_something(self):
		song = mus.Song()
		track = song.add_track()
		measure = track.append_measure()
		beat = measure.append_beat()
		note = beat.add_note(mus.Note('C_6'))
		song.end_song()
		#self.assertTrue(a is b)
		# TODO:  write Measure tests
		return



if __name__ == "__main__":
	unittest.main()

