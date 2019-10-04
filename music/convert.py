#!/usr/bin/env python

import midi
from ipdb import set_trace

from .. import util



def main():
	'''
	convert.py

	Conversion functions between internal music format and midi or engraved
	score
	'''

	return



def song_to_midi(song, midi_file='song.mid'):
	pattern = midi.Pattern()
	for song_track in song.tracks:
		midi_track = midi.Track()
		pattern.append(midi_track)

		for measure in song_track.measures:
			for beat in measure.beats:
				offset = beat.offset

				for note in beat.notes:
					# TODO:  correct offset after first append
					# TODO:  convert note spec to midi event
					note_on = midi.NoteOnEvent(tick=0, velocity=20, pitch=midi.G_3)
					midi_track.append(note_on)
					# TODO:  will have to create a note_off queue to keep track
					# of when to turn each pitch off

					# Instantiate a MIDI note off event, append it to the track
					#off = midi.NoteOffEvent(tick=100, pitch=midi.G_3)
					#midi_track.append(off)

				for event in beat.events:
					midi_event = midi.ControlChangeEvent()
					# TODO:  look into event specification
					midi_track.append(midi_event)

		# End the track
		eot = midi.EndOfTrackEvent(tick=1)
		midi_track.append(eot)

	# Save the pattern to disk
	midi.write_midifile(midi_file, pattern)
	return



def midi_to_song(midi_file):
	return song



if __name__ == "__main__":
	main()

