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
	test_note = Note()
	test_chord = Chord()
	test_control = Control()

	return



class Song():
	def __init__(self, key='C_Maj', time_signature=None, settings=None):
		self.settings = settings
		self.key = key
		self.time_signature = time_signature


	def add_chord(self, chord):
		return


	def add_note(self, note):
		return



class Note():
	def __init__(self, value=None, octave=None, duration=None, intensity=None, tie=None):
		self.value = value
		self.octave = octave
		self.duration = duration
		self.intensity = intensity
		self.tie = tie



class Chord():
	def __init__(self, key='C_Maj', timediff=32):
		self.key = key
		self.nodes = np.zeros((2,200), dtype=np.bool)


	def to_notes(self):
		return



class Control():
	def __init__(self):
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


	def update(self):
		max_mode_index = self.mode_nodes.argmax()
		mode_functions = [
			self.end_song,
			self.make_note,
			self.set_control_signal
		]
		mode_function = mode_functions[max_mode_index]
		return mode_function()


	def update_altmethod(self):
		if (endsong_node > notemode_node) and (endsong_node > controlmode_node):
			return self.end_song()
		elif (notemode_node >= endsong_node) and (notemode_node >= controlmode_node):
			return self.make_note()
		elif (controlmode_node >= endsong_node) and (controlmode_node > notemode_node):
			return self.set_control_signal()
		else:
			print("Shouldn't get here...")
			sys.exit(1923485)
		return


	def end_song(self):
		return


	def make_note(self):
		note = Note()
		return note


	def set_control_signal(self):
		return



if __name__ == "__main__":
	main()

