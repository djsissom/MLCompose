#!/usr/bin/env python

import unittest
import midi
import textwrap
from mlcompose import music as mus



class TestMidi(unittest.TestCase):
	def test_simple_saving_song_as_midi_file(self):
		song = mus.Song()
		track = song.add_track()

		measure = track.append_measure()
		beat = measure.beats[0]
		note = beat.add_note(mus.Note('C_6', duration='quarter'))

		measure = track.append_measure()
		beat = measure.beats[0]
		note = beat.add_note(mus.Note('C_6', duration='quarter'))
		song.end_song()

		song.to_midi('miditest_out_simple.mid')
		pattern = midi.read_midifile('miditest_out_simple.mid')

		test_string = textwrap.dedent('''\
			midi.Pattern(format=1, resolution=120, tracks=\\
			[midi.Track(\\
			  [midi.NoteOnEvent(tick=0, channel=0, data=[72, 127]),
			   midi.NoteOffEvent(tick=120, channel=0, data=[72, 0]),
			   midi.NoteOnEvent(tick=360, channel=0, data=[72, 127]),
			   midi.NoteOffEvent(tick=120, channel=0, data=[72, 0]),
			   midi.EndOfTrackEvent(tick=1, data=[])])])'''
		)
		self.maxDiff = None
		self.assertMultiLineEqual(repr(pattern), test_string)
		return


	def test_saving_song_as_midi_file(self):
		song = mus.Song()
		track = song.add_track()

		measure = track.append_measure()
		beat = measure.beats[0]
		note = beat.add_note(mus.Note('C_6', duration='quarter'))
		beat = measure.append_beat()
		rest = beat.add_note(mus.Rest(duration='dotted quarter'))
		beat = measure.append_beat()
		note = beat.add_note(mus.Note('C_7', duration='eighth'))
		beat = measure.append_beat()
		rest = beat.add_note(mus.Rest(duration='sixteenth'))
		beat = measure.append_beat()
		rest = beat.add_note(mus.Rest(duration='sixteenth'))
		beat = measure.append_beat()
		rest = beat.add_note(mus.Rest(duration='eighth'))

		measure = track.append_measure()
		beat = measure.beats[0]
		note = beat.add_note(mus.Note('C_6', duration='quarter'))
		measure.pad_rests()
		song.end_song()

		song.to_midi('miditest_out.mid')
		pattern = midi.read_midifile('miditest_out.mid')

		test_string = textwrap.dedent('''\
			midi.Pattern(format=1, resolution=120, tracks=\\
			[midi.Track(\\
			  [midi.NoteOnEvent(tick=0, channel=0, data=[72, 127]),
			   midi.NoteOffEvent(tick=120, channel=0, data=[72, 0]),
			   midi.NoteOnEvent(tick=180, channel=0, data=[84, 127]),
			   midi.NoteOffEvent(tick=60, channel=0, data=[84, 0]),
			   midi.NoteOnEvent(tick=120, channel=0, data=[72, 127]),
			   midi.NoteOffEvent(tick=120, channel=0, data=[72, 0]),
			   midi.EndOfTrackEvent(tick=1, data=[])])])'''
			)
		self.maxDiff = None
		self.assertMultiLineEqual(repr(pattern), test_string)
		return



if __name__ == "__main__":
	unittest.main()

