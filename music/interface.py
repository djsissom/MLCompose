#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd
from ipdb import set_trace

from .. import util



def main():
	'''
	interface.py

	ML node output music control interface.
	'''

	test_control = Control()

	return



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
		self.note_nodes           = self.nodes[1,1:]     # cyclical
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
		if song is None:
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
		end_node = self.endsong_node
		note_node = self.notemode_node
		control_node = self.controlmode_node

		if (end_node > self.notemode_node) and \
		   (end_node > control_node):
			mode_function = self.end_song
		elif (note_node >= end_node) and \
		     (note_node >= control_node):
			mode_function = self.make_note
		elif (control_node >= end_node) and \
		     (control_node > note_node):
			mode_function = self.set_control_signal
		else:
			print("Shouldn't get here...")
			sys.exit(1923485)
		return mode_function(song)


	def end_song(self, song=None):
		song = self.get_song(song)
		song.end_song()
		return


	def make_note(self, song=None, key='C_Maj'):
		song = self.get_song(song)

		if self.rest_node >= self.note_nodes.max():
			self.set_rest()
			return
		else:
			scale_degree = self.note_nodes.argmax() + 1
			# TODO: set other note properties

		note = Note(value=scale_degree, octave=octave, \
		            duration=duration, intensity=intensity, \
		            tie=tie)
		return


	def set_rest(self, song=None):
		song = self.get_song(song)
		return


	def set_control_signal(self, song=None):
		song = self.get_song(song)
		return



if __name__ == "__main__":
	main()

