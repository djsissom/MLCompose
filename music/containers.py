#!/usr/bin/env python

import numpy as np
import pandas as pd
from ipdb import set_trace



def main():
	'''
	containers.py

	Formatting and storage for music data.
	'''

	test_song = Song()
	test_track = Track()
	test_measure = Measure()
	test_beat = Beat()
	test_note = Note()
	test_rest = Rest()
	test_event = Event()
	test_control = Control()

	test_song.add_track(test_track)
	test_track.append_measure(test_measure)

	return



class Song():
	def __init__(self, key='C_Maj', time_signature=None, settings=None):
		self.settings = settings
		self.key = key
		self.time_signature = time_signature
		self.tracks = []


	def add_track(self, track):
		self.tracks.append(track)
		return self.tracks


	def end_song(self):
		for track in self.tracks:
			track.end_track()
		return



class Track():
	def __init__(self, desc=None):
		self.description = desc
		self.measures = []


	def set_description(self, desc):
		self.description = desc
		return


	def get_description(self):
		return self.description


	def append_measure(self, measure):
		self.measures.append(measure)
		return self.measures


	def end_track(self):
		end_signal = Event('end_track')
		self.measures[-1].add_event(end_signal)
		return



class Measure():
	def __init__(self, key=None, time_signature=None):
		self.key = key
		self.time_signature = time_signature
		self.beats = []


	def set_key(self, key):
		self.key = key
		return


	def set_timesig(self, time_signature):
		self.time_signature = time_signature
		return


	def append_beat(self, beat):
		self.beats.append(beat)
		return self.beats


	def add_event(self, event):
		return



class Beat():
	def __init__(self, offset=0.):
		self.offset = offset
		self.notes = []


	def append_note(self, note):
		self.notes.append(note)
		return self.notes



class Note():
	def __init__(self, value=None, octave=None, duration=None, intensity=None, tie=None):
		self.value = value
		self.octave = octave
		self.duration = duration
		self.intensity = intensity
		self.tie = tie



class Rest():
	def __init__(self, duration=None):
		self.duration = duration



class Event():
	def __init__(self, event_type=None, descr=None):
		self.event_type = event_type
		self.description = descr



class Control():
	def __init__(self, song=None):
		# set default song to work on
		self.song = song

		# tensor of nodes from neural net output
		self.nodes = np.zeros((6,8), dtype=np.float)

		# Array slices are used to make view instead of copy.  Descriptive
		# names can then be used to reference node values without
		# reinitialization steps.

		# first row used for mode control toggles
		self.modecontrol_nodes    = self.nodes[0,:]
		self.mode_nodes           = self.nodes[0,0:3]
		self.controloption_nodes  = self.nodes[0,3:8]

		self.endsong_node         = self.nodes[0,0:1]
		self.notemode_node        = self.nodes[0,1:2]
		self.controlmode_node     = self.nodes[0,2:3]
		self.change_keysig_node   = self.nodes[0,3:4]
		self.change_timesig_node  = self.nodes[0,4:5]
		self.change_tempo_node    = self.nodes[0,5:6]
		self.change_dynamic_node  = self.nodes[0,6:7]
		self.pedal_toggle_node    = self.nodes[0,7:8]

		# note mode needs note value, octave, and length
		self.rest_node            = self.nodes[1,0:1]
		self.note_nodes           = self.nodes[1,:]      # cyclical
		self.octave_nodes         = self.nodes[2,:]      # linear
		self.duration_nodes       = self.nodes[3,0:6]    # linear
		self.tie_nodes            = self.nodes[3,6:8]    # on/off

		# last two rows used for other per note settings
		self.note_settings_nodes  = self.nodes[4:6,:]

		self.accidental_nodes     = self.nodes[4,0:3]    # flat, natural (no change), sharp
		self.accent_nodes         = self.nodes[4,3:5]    # on/off
		self.arpeggio_nodes       = self.nodes[4,5:8]    # off/up/down
		self.velocity_nodes       = self.nodes[5,0:6]    # linear
		self.hand_nodes           = self.nodes[5,6:8]    # left/right

		# settings for control modes
		self.keysig_nodes         = self.nodes[1,:]
		self.keysig_sf_nodes      = self.nodes[4,0:3]
		self.timesig_numer_nodes  = self.nodes[2:4,:]
		self.timesig_denom_nodes  = self.nodes[5,:]
		self.tempo_nodes          = self.nodes[4:6,:]
		self.dynamic_nodes        = self.nodes[5,0:6]
		### ### ### ###


	def set_song(self, song):
		self._song = song
		return


	def get_song(self, song=None):
		if song == None:
			song = self._song
		return song


	song = property(get_song, set_song)


	def update(self, song=None):
		song = self.get_song(song)

		max_mode_index = self.mode_nodes.argmax()
		mode_functions = [
			self.end_song,
			self.make_note,
			self.set_control_signal
		]
		mode_function = mode_functions[max_mode_index]
		return mode_function(song)


	def update_altmethod(self, song=None):
		song = self.get_song(song)

		if (endsong_node > notemode_node) and \
		   (endsong_node > controlmode_node):
			return self.end_song(song)
		elif (notemode_node >= endsong_node) and \
		     (notemode_node >= controlmode_node):
			return self.make_note(song)
		elif (controlmode_node >= endsong_node) and \
		     (controlmode_node > notemode_node):
			return self.set_control_signal(song)
		else:
			print("Shouldn't get here...")
			sys.exit(1923485)
		return


	def end_song(self, song=None):
		song = self.get_song(song)
		return


	def make_note(self, song=None, key='C_Maj'):
		song = self.get_song(song)
		if song == None:
			song = self.song

		note_index = self.note_nodes.argmax()
		if note_index == 0:
			self.set_rest()
		else:
			scale_degree = note_index

		note = Note(degree=scale_degree, octave=octave, \
		            duration=duration, intensity=intensity, \
					tie=tie)
		return note


	def set_rest(self, song=None):
		song = self.get_song(song)
		return


	def set_control_signal(self, song=None):
		song = self.get_song(song)
		return



if __name__ == "__main__":
	main()

