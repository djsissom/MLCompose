#!/usr/bin/env python

import midi
import numpy as np
from ipdb import set_trace

from .. import util
from .. import music



def main():
	'''
	convert.py

	Conversion functions between internal music format and midi or engraved
	score
	'''

	return


# TODO:  song_to_midi_file function

def song_to_midi(song, midi_file='song.mid'):
	pattern = midi.Pattern()
	for song_track in song.tracks:
		pattern = track_to_midi(song_track, pattern=pattern)

	# Save the pattern to disk
	midi.write_midifile(midi_file, pattern)
	return pattern



def track_to_midi(song_track, pattern=None):
	if pattern is None:
		pattern = midi.Pattern()
	midi_track = midi.Track()
	pattern.append(midi_track)

	# deactivation_queue is an array with a value for each midi note pitch
	# negative numbers indicate the pitch is not active
	# positive numbers are the remaining ticks until cutoff
	deactivation_queue = np.zeros(128, dtype=np.int) - 1

	for measure in song_track.measures:
		for beat in measure.beats:
			ticks_to_beat = midi_length(beat.offset)

			mask = (deactivation_queue >= 0)
			if mask.any():
				ticks_to_off_event = deactivation_queue[mask].min()
			else:
				ticks_to_off_event = 999999999

			# add note off events until time for the next beat
			while ticks_to_off_event <= ticks_to_beat:
				pitches_to_deactivate = np.where(deactivation_queue == ticks_to_off_event)
				deactivation_queue[mask] -= ticks_to_off_event
				deactivation_queue[pitches_to_deactivate] -= 1
				ticks_to_beat -= ticks_to_off_event
				for pitch in pitches_to_deactivate:
					off_event = midi.NoteOffEvent(tick=ticks_to_off_event, pitch=pitch)
					midi_track.append(off_event)
					ticks_to_off_event = 0
				mask = (deactivation_queue >= 0)
				if mask.any():
					ticks_to_off_event = deactivation_queue[mask].min()
				else:
					ticks_to_off_event = 999999999

			for note in beat.notes:
				midi_velocity = int(note.intensity * 127)
				midi_pitch = note.value
				note_on_event = midi.NoteOnEvent(tick=ticks_to_beat, velocity=midi_velocity, pitch=midi_pitch)
				midi_track.append(note_on_event)
				deactivation_queue[midi_pitch] = midi_length(note.duration) # note: doesn't handle ties yet
				ticks_to_beat = 0

			for event in beat.events:
				if event.name == 'end_track':
					midi_event = midi.EndOfTrackEvent(tick=1)
				else:
					midi_event = midi.ControlChangeEvent(tick=ticks_to_beat)
				# TODO:  look into event specification
				midi_track.append(midi_event)
				ticks_to_beat = 0

	# End the track
	if not isinstance(midi_track[-1], midi.EndOfTrackEvent):
		eot = midi.EndOfTrackEvent(tick=1)
		midi_track.append(eot)
	return pattern



def midi_length(duration, tpq=32):
	if duration == 0 or duration.base == 0:
		length = 0
	else:
		length = tpq * 4. / duration.base
		if duration.dot:
			length = length * 1.5
	return int(length)



def midi_to_song(midi_file):
	pattern = midi.read_midifile(midi_file)
	song = music.Song()
	for midi_track in pattern:
		track = midi_to_track(midi_track)
		song.add_track(track)
	return song


def midi_to_track(midi_track):
	return track



if __name__ == "__main__":
	main()

