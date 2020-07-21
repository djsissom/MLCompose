#!/usr/bin/env python

import midi
import numpy as np

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

def song_to_midi(song, midi_file='song.mid', resolution=120):
	pattern = midi.Pattern(resolution=resolution)
	for track in song.tracks:
		midi_track = track_to_midi(track, resolution=resolution)
		pattern.append(midi_track)

	# Save the pattern to disk
	midi.write_midifile(midi_file, pattern)
	return pattern



def track_to_midi(track, resolution=120):
	midi_track = midi.Track()

	# deactivation_queue is an array with a value for each midi note pitch
	# negative numbers indicate the pitch is not active
	# positive numbers are the remaining ticks until cutoff
	deactivation_queue = np.zeros(128, dtype=np.int) - 1

	for measure in track.measures:
		# TODO:  Handle key and time signature to create midi events
		for beat in measure.beats:
			ticks_to_beat = midi_length(beat.offset, resolution=resolution)

			mask = (deactivation_queue >= 0)
			if mask.any():
				ticks_to_off_event = deactivation_queue[mask].min()
			else:
				ticks_to_off_event = 999999999

			# add note off events until time for the next beat
			while ticks_to_off_event <= ticks_to_beat:
				pitches_to_deactivate = np.where(deactivation_queue == ticks_to_off_event)[0]
				deactivation_queue[mask] -= ticks_to_off_event
				deactivation_queue[pitches_to_deactivate] -= 1
				ticks_to_beat -= ticks_to_off_event
				for pitch in pitches_to_deactivate:
					off_event = midi.NoteOffEvent(tick=int(ticks_to_off_event), pitch=int(pitch))
					midi_track.append(off_event)
					ticks_to_off_event = 0
				mask = (deactivation_queue >= 0)
				if mask.any():
					ticks_to_off_event = deactivation_queue[mask].min()
				else:
					ticks_to_off_event = 999999999

			for note in beat.notes:
				if isinstance(note, music.Rest):
					# TODO:  Handle ending rests that are getting skipped.
					continue
				midi_velocity = round(note.intensity * 127)
				midi_pitch = note.value
				note_on_event = midi.NoteOnEvent(tick=int(ticks_to_beat), velocity=midi_velocity, pitch=midi_pitch)
				midi_track.append(note_on_event)
				deactivation_queue[midi_pitch] = midi_length(note.duration, resolution=resolution) # note: doesn't handle ties yet
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
	return midi_track



def midi_length(duration, resolution=120):
	if isinstance(duration, music.Duration):
		duration = duration.length
	length = round(resolution * 4 * duration)
	return length



def midi_to_song(midi_file):
	pattern = midi.read_midifile(midi_file)
	song = music.Song()
	for midi_track in pattern:
		track = midi_to_track(midi_track)
		song.add_track(track)
	return song


def midi_to_track(midi_track):
	track = music.Track()
	case = {
		'midi.TrackNameEvent':      handle_track_name_event,
		'midi.ControlChangeEvent':  handle_control_change_event,
		'midi.ProgramChangeEvent':  handle_program_change_event,
		'midi.TimeSignatureEvent':  handle_time_signature_event,
		'midi.KeySignatureEvent':   handle_key_signature_event,
		'midi.SetTempoEvent':       handle_set_tempo_event,
		'midi.NoteOnEvent':         handle_note_on_event,
		'midi.NoteOffEvent':        handle_note_off_event,
		'midi.EndOfTrackEvent':     handle_end_of_track_event
	}
	for event in midi_track:
		event_type_string = str(event).split('(')[0]
		parse_function = case.get(event_type_string, handle_unknown_event)
		track = parse_function(event, track)
	return track


def handle_unknown_event(event, track):
	print('Skipping unknown midi event  -> ', event)
	return track


def handle_track_name_event(event, track):
	try:
		track.description = event.text
	except AttributeError:
		print("Warning:  Track name event has no text attribute...skipping.")
	return track


def handle_control_change_event(event, track):
	# TODO:  add functionality to handler function
	print('Skipping control change event  -> ', event)
	return track


def handle_program_change_event(event, track):
	# TODO:  add functionality to handler function
	print('Skipping program change event  -> ', event)
	return track


def handle_time_signature_event(event, track):
	# TODO:  add functionality to handler function
	print('Skipping time signature event  -> ', event)
	return track


def handle_key_signature_event(event, track):
	# TODO:  add functionality to handler function
	print('Skipping key signature event  -> ', event)
	return track


def handle_set_tempo_event(event, track):
	# TODO:  add functionality to handler function
	print('Skipping set tempo event  -> ', event)
	return track


def handle_note_on_event(event, track):
	# TODO:  add functionality to handler function
	print('Skipping note on event  -> ', event)
	return track


def handle_note_off_event(event, track):
	# TODO:  add functionality to handler function
	print('Skipping note off event  -> ', event)
	return track


def handle_end_of_track_event(event, track):
	# TODO:  add functionality to handler function
	print('Skipping end of track event  -> ', event)
	return track



if __name__ == "__main__":
	main()

