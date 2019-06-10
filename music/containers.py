#!/usr/bin/env python

import numpy as np
import pandas as pd
from ipdb import set_trace



def main():
	'''
	containers.py

	Formatting and storage for music data.
	'''

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

		# first row used for mode control toggles
		self.modecontrol_nodes    = self.nodes[0,:]

		# array slices are used to make view instead of copy
		self.endsong_node         = self.nodes[0,0:1]
		self.notemode_node        = self.nodes[0,1:2]
		self.controlmode_node     = self.nodes[0,2:3]
		self.change_timesig_node  = self.nodes[0,3:4]
		self.change_keysig_node   = self.nodes[0,4:5]
		self.change_tempo_node    = self.nodes[0,5:6]
		self.pedal_toggle_node    = self.nodes[0,6:7]
		self.hand_toggle_node     = self.nodes[0,7:8]

		# second and third rows used for per note settings
		self.note_settings_nodes  = self.nodes[1:3,:]

		self.arpeggio_nodes       = self.nodes[1,0:3]
		self.tie_nodes            = self.nodes[1,3:5]
		self.shift_nodes          = self.nodes[1,5:8]

		self.accent_nodes         = self.nodes[2,0:2]
		self.dynamic_nodes        = self.nodes[2,2:8]

		# note mode needs note value, octave, and length
		self.rest_node            = self.nodes[3,0:1]
		self.note_nodes           = self.nodes[3,:]
		self.octave_nodes         = self.nodes[4,:]
		self.length_nodes         = self.nodes[5,:]
		self.length_dot_nodes     = self.nodes[5,6:8]

		# settings for control modes
		self.timesig_numer_nodes  = self.nodes[3:5,:]
		self.timesig_denom_nodes  = self.nodes[5,:]
		self.keysig_sf_nodes      = self.nodes[1,5:8]
		self.keysig_nodes         = self.nodes[3,:]
		self.tempo_nodes          = self.nodes[4:6,:]


	def make_note(self):
		note = Note()
		return note



if __name__ == "__main__":
	main()

