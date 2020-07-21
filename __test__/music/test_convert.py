#!/usr/bin/env python

import unittest
from mlcompose import music as mus



class TestMidi(unittest.TestCase):
	def test_saving_song_as_midi_file(self):
		song = mus.Song()
		track = song.add_track()
		measure = track.append_measure()
		beat = measure.beats[0]
		note = beat.add_note(mus.Note('C_6', duration='quarter'))
		beat = measure.append_beat()
		note = beat.add_note(mus.Note('C_7', duration='eighth'))
		song.end_song()

		song.to_midi('midiout_test.mid')
		# TODO:  check created file against known good file
		return



if __name__ == "__main__":
	unittest.main()

