#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd
from ipdb import set_trace

from . import containers
from .. import util



def main():
	'''
	interface.py

	ML node output music control interface.
	'''

	test_composer = Composer()

	return



class Composer():
	def __init__(self, song=None):
		# set default song to work on
		self.song = song

		# tensor of nodes from neural net output
		self.nodes = np.zeros((6,8), dtype=np.float)

		# node layout:
		# -----------------
		#  0 0 0 0 0 0 0 0  <-  mode control nodes
		#  0 0 0 0 0 0 0 0  <-  rest/note nodes -or- keysig nodes
		#  0 0 0 0 0 0 0 0  <-  octave nodes -or- timesig numerator nodes
		#  0 0 0 0 0 0 0 0  <-  duration and tie nodes -or- timesig numerator nodes
		#  0 0 0 0 0 0 0 0  <-  accidental, accent, and arpeggio nodes -or- tempo nodes
		#  0 0 0 0 0 0 0 0  <-  velocity and played hand nodes -or- timesig denominator nodes -or- tempo nodes -or- dynamic nodes
		# -----------------
		#
		# note mode node layout:
		# -----------------
		#  0 1 0 0 0 0 0 0  <-  mode control nodes
		#  0 0 0 0 0 0 0 0  <-  rest/note nodes (rest + scale degree 1-7)
		#  0 0 0 0 0 0 0 0  <-  octave nodes
		#  0 0 0 0 0 0 0 0  <-  duration and tie nodes
		#  0 0 0 0 0 0 0 0  <-  accidental, accent, and arpeggio nodes
		#  0 0 0 0 0 0 0 0  <-  velocity and played hand nodes
		# -----------------
		#
		# change keysig control mode node layout:
		# -----------------
		#  0 0 1 1 0 0 0 0  <-  mode control nodes
		#  0 0 0 0 0 0 0 0  <-  keysig nodes
		#  0 0 0 0 0 0 0 0  <-  (unused)
		#  0 0 0 0 0 0 0 0  <-  (unused)
		#  0 0 0 0 0 0 0 0  <-  keysig sharp/natural/flat nodes
		#  0 0 0 0 0 0 0 0  <-  (unused)
		# -----------------
		#
		# change timesig control mode node layout:
		# -----------------
		#  0 0 1 0 1 0 0 0  <-  mode control nodes
		#  0 0 0 0 0 0 0 0  <-  (unused)
		#  0 0 0 0 0 0 0 0  <-  timesig numerator nodes
		#  0 0 0 0 0 0 0 0  <-  timesig numerator nodes
		#  0 0 0 0 0 0 0 0  <-  (unused)
		#  0 0 0 0 0 0 0 0  <-  timesig denominator nodes
		# -----------------
		#
		# change tempo control mode node layout:
		# -----------------
		#  0 0 1 0 0 1 0 0  <-  mode control nodes
		#  0 0 0 0 0 0 0 0  <-  (unused)
		#  0 0 0 0 0 0 0 0  <-  (unused)
		#  0 0 0 0 0 0 0 0  <-  (unused)
		#  0 0 0 0 0 0 0 0  <-  tempo nodes
		#  0 0 0 0 0 0 0 0  <-  tempo nodes
		# -----------------
		#
		# change dynamic control mode node layout:
		# -----------------
		#  0 0 1 0 0 0 1 0  <-  mode control nodes
		#  0 0 0 0 0 0 0 0  <-  (unused)
		#  0 0 0 0 0 0 0 0  <-  (unused)
		#  0 0 0 0 0 0 0 0  <-  (unused)
		#  0 0 0 0 0 0 0 0  <-  (unused)
		#  0 0 0 0 0 0 0 0  <-  dynamic nodes
		# -----------------

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
		self.tie_nodes            = self.nodes[3,6:8]    # off/on

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
		'''
		Update the song using the currently set control nodes.

		This driver method should be called after updating the nodes attribute
		of the Composer.  The update method reads the currently activated
		control nodes and adds to/modifies the song accordingly.
		'''
		song = self.get_song(song)
		current_measures, current_beats = update_position(song)

		mode_list = np.array([
			self.endsong_node,
			self.notemode_node,
			self.controlmode_node
		])
		max_mode_index = mode_list.argmax()

		mode_functions = [
			self.end_song,
			self.make_note,
			self.set_control_signal
		]
		mode_function = mode_functions[max_mode_index]
		return mode_function(song)


	def update_position(self, song=None):
		'''Find the latest unfinished measures and beats.'''
		song = self.get_song(song)
		current_measures = []
		current_beats = []

		for track in song.tracks:
			last_measure = track.measures[-1]
			if check_measure_complete(last_measure):
				last_measure = track.append_measure()
			current_measures.append(last_measure)

			last_beat = last_measure.beats[-1]
			if last_beat.complete:
				last_beat = last_measure.append_beat()
			current_beats.append(last_beat)

		return current_measures, current_beats


	def check_measure_complete(self, measure):
		# TODO:  test for complete measure
		# Potentially add this to measure class instead...
		return True


	def end_song(self, song=None):
		song = self.get_song(song)
		song.end_song()
		return


	def make_note(self, song=None, key=None):
		song = self.get_song(song)

		# TODO:  This should depend on whether it's a real rest or ending a chord.
		if self.rest_node >= self.note_nodes.max():
			self.set_rest()
			return

		if key is None:
			key = song.key

		scale_degree = self.note_nodes.argmax() # note this is zero-based here
		note_name = key.notes[scale_degree]
		note_octave = self.octave_nodes.argmax()
		note_duration_power = self.duration_nodes.argmax()
		note_duration = containers.Duration(note_duration_power, mode='inverse_power')
		note_intensity = float(self.velocity_nodes.argmax() + 1) / float(len(self.velocity_nodes))
		note_tie = bool(self.tie_nodes.argmax())

		note = containers.Note(
				name=note_name,
				octave=note_octave,
				duration=note_duration,
				intensity=note_intensity,
				tie=note_tie
			)

		max_accidental_node = self.accidental_nodes.argmax()
		if max_accidental_node == 0:
			note.lower_note()
		elif max_accidental_node == 2:
			note.raise_note()

		return


	def set_rest(self, song=None):
		song = self.get_song(song)
		# TODO:  actually do something here
		return


	def set_control_signal(self, song=None):
		song = self.get_song(song)
		# TODO:  actually do something here
		return



if __name__ == "__main__":
	main()

